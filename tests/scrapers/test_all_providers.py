from pathlib import Path

from sqlalchemy import func

from inmonexo_db.models import Company, Project
from inmonexo_scrapers.fetch import StaticFetcher
from inmonexo_scrapers.pipeline import run_all_provider_scrapes
from inmonexo_scrapers.registry import PROVIDERS

FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures"


def _fixture_fetcher(provider):
    html = (FIXTURE_ROOT / provider.company_slug / "listing.html").read_text(encoding="utf-8")
    return StaticFetcher({provider.listing_url: html})


def test_run_all_provider_scrapes(db_session) -> None:
    runs = run_all_provider_scrapes(
        db_session,
        list(PROVIDERS.values()),
        _fixture_fetcher,
    )

    assert len(runs) == 5
    assert all(run.status == "succeeded" for run in runs)
    assert db_session.query(func.count(Company.id)).scalar() == 5
    assert db_session.query(func.count(Project.id)).scalar() >= 20

    morada_projects = (
        db_session.query(Project)
        .join(Company)
        .filter(Company.company_name == "Morada")
        .all()
    )
    assert morada_projects
    assert all(project.price_min is None for project in morada_projects)

    unio_projects = (
        db_session.query(Project)
        .join(Company)
        .filter(Company.company_name == "UNIO Grupo Inmobiliario")
        .all()
    )
    assert len(unio_projects) == 1
    assert unio_projects[0].price_min is None
