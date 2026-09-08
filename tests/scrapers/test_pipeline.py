from pathlib import Path

from sqlalchemy import func

from inmonexo_core.enums import MarketEventType
from inmonexo_db.models import MarketEvent, PriceSnapshot, Project, ScrapeRun
from inmonexo_scrapers.fetch import FetchResult, StaticFetcher
from inmonexo_scrapers.pipeline import run_provider_scrape
from inmonexo_scrapers.providers.hldi import HlProvider, LISTING_URL

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "hldi" / "listing.html"


def test_run_provider_scrape_idempotent(db_session) -> None:
    html = FIXTURE.read_text(encoding="utf-8")
    fetcher = StaticFetcher({LISTING_URL: html})
    provider = HlProvider()

    run1 = run_provider_scrape(db_session, provider, fetcher)
    count1 = db_session.query(func.count(Project.id)).scalar()
    events1 = db_session.query(func.count(MarketEvent.id)).scalar()

    run2 = run_provider_scrape(db_session, provider, fetcher)
    count2 = db_session.query(func.count(Project.id)).scalar()
    events2 = db_session.query(func.count(MarketEvent.id)).scalar()

    assert run1.status == "succeeded"
    assert run2.status == "succeeded"
    assert run1.projects_seen > 0
    assert count1 == count2
    assert events2 == events1
    assert db_session.query(ScrapeRun).count() == 2


def test_run_provider_scrape_price_change(db_session) -> None:
    html = FIXTURE.read_text(encoding="utf-8")
    fetcher = StaticFetcher({LISTING_URL: html})
    provider = HlProvider()

    run_provider_scrape(db_session, provider, fetcher)

    sq2_url = "https://hldi.pe/proyectos/sq-2-work-living/"
    project = db_session.query(Project).filter_by(source_url=sq2_url).one()
    assert project.price_min == 292769

    modified = html.replace("S/ 292,769*", "S/ 310,000*")
    fetcher2 = StaticFetcher({LISTING_URL: modified})
    run_provider_scrape(db_session, provider, fetcher2)

    db_session.refresh(project)
    assert project.price_min == 310000

    price_events = (
        db_session.query(MarketEvent)
        .filter_by(entity_id=project.id, event_type=MarketEventType.PRICE_CHANGE.value)
        .all()
    )
    assert len(price_events) == 1
    assert price_events[0].previous_value["price_min"] == 292769
    assert price_events[0].new_value["price_min"] == 310000

    snapshots = (
        db_session.query(PriceSnapshot)
        .filter_by(project_id=project.id)
        .order_by(PriceSnapshot.recorded_at)
        .all()
    )
    assert len(snapshots) == 2
    assert snapshots[-1].price == 310000


def test_fetch_result_stores_apify_metadata() -> None:
    result = FetchResult(
        url=LISTING_URL,
        html="<html></html>",
        apify_run_id="run-123",
        apify_dataset_id="dataset-456",
    )
    assert result.apify_run_id == "run-123"
    assert result.apify_dataset_id == "dataset-456"
