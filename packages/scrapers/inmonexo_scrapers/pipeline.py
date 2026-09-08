import uuid
from collections.abc import Callable
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from inmonexo_core.enums import MarketEventType
from inmonexo_core.money import parse_money
from inmonexo_core.status import map_project_status
from inmonexo_core.district import normalize_district
from inmonexo_db.models import Company, MarketEvent, PriceSnapshot, Project, ScrapeRun
from inmonexo_scrapers.base import BaseProvider
from inmonexo_scrapers.fetch import FetchResult, PageFetcher
from inmonexo_scrapers.types import ProjectDraft


def _utcnow() -> datetime:
    return datetime.now(UTC)


def ensure_company(session: Session, provider: BaseProvider) -> Company:
    company = session.query(Company).filter_by(website=provider.website).one_or_none()
    if company:
        return company
    company = Company(company_name=provider.company_name, website=provider.website)
    session.add(company)
    session.flush()
    return company


def draft_to_fields(draft: ProjectDraft) -> dict:
    money = parse_money(draft.price_text) if draft.price_text else None
    return {
        "project_name": draft.project_name,
        "project_url": draft.project_url,
        "district": normalize_district(draft.district),
        "address": draft.address,
        "project_status": map_project_status(draft.status_label).value,
        "price_min": money.amount if money else None,
        "currency": money.currency.value if money else None,
        "source_url": draft.source_url,
    }


def upsert_project(
    session: Session,
    company: Company,
    draft: ProjectDraft,
) -> tuple[Project, list[MarketEvent]]:
    fields = draft_to_fields(draft)
    events: list[MarketEvent] = []
    existing = session.query(Project).filter_by(source_url=fields["source_url"]).one_or_none()

    if existing is None:
        project = Project(company_id=company.id, **fields)
        session.add(project)
        session.flush()
        events.append(
            MarketEvent(
                event_type=MarketEventType.NEW_PROJECT.value,
                entity_type="project",
                entity_id=project.id,
                previous_value=None,
                new_value={"project_name": project.project_name, "source_url": project.source_url},
            )
        )
        if project.price_min is not None:
            session.add(
                PriceSnapshot(
                    project_id=project.id,
                    price=project.price_min,
                    currency=project.currency or "PEN",
                    source_url=project.source_url,
                )
            )
        session.add_all(events)
        return project, events

    project = existing
    if project.price_min != fields["price_min"]:
        prev = {"price_min": project.price_min, "currency": project.currency}
        new = {"price_min": fields["price_min"], "currency": fields["currency"]}
        if fields["price_min"] is None and project.price_min is not None:
            event_type = MarketEventType.PRICE_REMOVED.value
        else:
            event_type = MarketEventType.PRICE_CHANGE.value
        events.append(
            MarketEvent(
                event_type=event_type,
                entity_type="project",
                entity_id=project.id,
                previous_value=prev,
                new_value=new,
            )
        )
        if fields["price_min"] is not None:
            session.add(
                PriceSnapshot(
                    project_id=project.id,
                    price=fields["price_min"],
                    currency=fields["currency"] or "PEN",
                    source_url=project.source_url,
                )
            )

    if project.project_status != fields["project_status"]:
        events.append(
            MarketEvent(
                event_type=MarketEventType.PROJECT_STATUS_CHANGE.value,
                entity_type="project",
                entity_id=project.id,
                previous_value={"project_status": project.project_status},
                new_value={"project_status": fields["project_status"]},
            )
        )

    for key, value in fields.items():
        setattr(project, key, value)
    project.last_seen_at = _utcnow()
    session.add_all(events)
    return project, events


def run_provider_scrape(
    session: Session,
    provider: BaseProvider,
    fetcher: PageFetcher,
) -> ScrapeRun:
    run = ScrapeRun(provider_slug=provider.company_slug, status="running")
    session.add(run)
    session.flush()

    errors: list[str] = []
    seen = 0
    apify_run_id: str | None = None
    apify_dataset_id: str | None = None

    try:
        listing: FetchResult = fetcher.fetch(provider.listing_url)
        apify_run_id = listing.apify_run_id
        apify_dataset_id = listing.apify_dataset_id
        company = ensure_company(session, provider)
        drafts = provider.discover_projects(listing.html)
        for draft in drafts:
            upsert_project(session, company, draft)
            seen += 1
        company.last_checked_at = _utcnow()
        run.status = "succeeded"
    except Exception as exc:  # noqa: BLE001 — log scrape failure on run record
        errors.append(str(exc))
        run.status = "failed"

    run.projects_seen = seen
    run.projects_failed = len(errors)
    run.error_log = "\n".join(errors) if errors else None
    run.apify_run_id = apify_run_id
    run.apify_dataset_id = apify_dataset_id
    run.finished_at = _utcnow()
    session.commit()
    return run


def run_all_provider_scrapes(
    session: Session,
    providers: list[BaseProvider],
    fetcher_for: Callable[[BaseProvider], PageFetcher],
) -> list[ScrapeRun]:
    runs: list[ScrapeRun] = []
    for provider in providers:
        fetcher = fetcher_for(provider)
        runs.append(run_provider_scrape(session, provider, fetcher))
    return runs
