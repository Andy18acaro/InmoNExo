from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from inmonexo_db.models import Company, MarketEvent, Project, ScrapeRun


@dataclass(frozen=True, slots=True)
class OverviewMetrics:
    company_count: int
    project_count: int
    projects_with_price: int
    district_count: int
    event_count: int
    recent_event_count: int
    last_scrape_at: datetime | None
    last_scrape_status: str | None


@dataclass(frozen=True, slots=True)
class DistrictMetrics:
    district: str
    project_count: int
    company_count: int
    priced_project_count: int
    min_price: int | None
    max_price: int | None
    avg_price: float | None


def overview_metrics(session: Session) -> OverviewMetrics:
    company_count = session.scalar(select(func.count(Company.id))) or 0
    project_count = session.scalar(select(func.count(Project.id))) or 0
    projects_with_price = (
        session.scalar(select(func.count(Project.id)).where(Project.price_min.is_not(None))) or 0
    )
    district_count = (
        session.scalar(
            select(func.count(func.distinct(Project.district))).where(Project.district.is_not(None))
        )
        or 0
    )
    event_count = session.scalar(select(func.count(MarketEvent.id))) or 0

    cutoff = datetime.now(UTC) - timedelta(days=7)
    recent_event_count = (
        session.scalar(
            select(func.count(MarketEvent.id)).where(MarketEvent.detected_at >= cutoff)
        )
        or 0
    )

    last_run = session.scalar(
        select(ScrapeRun)
        .where(ScrapeRun.finished_at.is_not(None))
        .order_by(ScrapeRun.finished_at.desc())
        .limit(1)
    )

    return OverviewMetrics(
        company_count=company_count,
        project_count=project_count,
        projects_with_price=projects_with_price,
        district_count=district_count,
        event_count=event_count,
        recent_event_count=recent_event_count,
        last_scrape_at=last_run.finished_at if last_run else None,
        last_scrape_status=last_run.status if last_run else None,
    )


def district_breakdown(session: Session) -> list[DistrictMetrics]:
    rows = session.execute(
        select(
            Project.district,
            func.count(Project.id),
            func.count(func.distinct(Project.company_id)),
            func.count(Project.id).filter(Project.price_min.is_not(None)),
            func.min(Project.price_min),
            func.max(Project.price_min),
            func.avg(Project.price_min),
        )
        .where(Project.district.is_not(None))
        .group_by(Project.district)
        .order_by(func.count(Project.id).desc(), Project.district)
    ).all()

    return [
        DistrictMetrics(
            district=row[0],
            project_count=row[1],
            company_count=row[2],
            priced_project_count=row[3],
            min_price=row[4],
            max_price=row[5],
            avg_price=float(row[6]) if row[6] is not None else None,
        )
        for row in rows
    ]
