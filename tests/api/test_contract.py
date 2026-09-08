from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from inmonexo_api.app import create_app
from inmonexo_api.deps import get_db
from inmonexo_db.session import get_session_factory
from inmonexo_scrapers.fetch import StaticFetcher
from inmonexo_scrapers.pipeline import run_all_provider_scrapes
from inmonexo_scrapers.registry import PROVIDERS

FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures"


@pytest.fixture
def populated_db(db_session):
    def fetcher_for(provider):
        html = (FIXTURE_ROOT / provider.company_slug / "listing.html").read_text(encoding="utf-8")
        return StaticFetcher({provider.listing_url: html})

    run_all_provider_scrapes(db_session, list(PROVIDERS.values()), fetcher_for)
    db_session.commit()
    return db_session


@pytest.fixture
def api_client(populated_db, sqlite_engine):
    app = create_app()
    session_factory = get_session_factory()

    def override_get_db():
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client


def test_get_companies(api_client: TestClient) -> None:
    response = api_client.get("/companies")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert all(item["project_count"] > 0 for item in data)


def test_get_projects_and_district_filter(api_client: TestClient) -> None:
    all_projects = api_client.get("/projects")
    assert all_projects.status_code == 200
    assert len(all_projects.json()) >= 20

    surquillo = api_client.get("/projects", params={"district": "surquillo"})
    assert surquillo.status_code == 200
    rows = surquillo.json()
    assert rows
    assert all(row["district"] == "Surquillo" for row in rows)


def test_get_project_by_id(api_client: TestClient) -> None:
    projects = api_client.get("/projects").json()
    project_id = projects[0]["id"]
    response = api_client.get(f"/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()["id"] == project_id


def test_get_project_not_found(api_client: TestClient) -> None:
    response = api_client.get("/projects/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_get_events(api_client: TestClient) -> None:
    response = api_client.get("/events")
    assert response.status_code == 200
    events = response.json()
    assert events
    assert events[0]["event_type"] == "NEW_PROJECT"


def test_analytics_overview(api_client: TestClient) -> None:
    response = api_client.get("/analytics/overview")
    assert response.status_code == 200
    data = response.json()
    assert data["company_count"] == 5
    assert data["project_count"] >= 20
    assert data["district_count"] >= 5
    assert data["last_scrape_status"] == "succeeded"


def test_analytics_districts(api_client: TestClient) -> None:
    response = api_client.get("/analytics/districts")
    assert response.status_code == 200
    rows = response.json()
    assert rows
    assert rows[0]["project_count"] >= rows[-1]["project_count"]
    assert any(row["district"] == "Surquillo" for row in rows)


def test_openapi_available(api_client: TestClient) -> None:
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "/projects" in schema["paths"]
    assert "/analytics/overview" in schema["paths"]
