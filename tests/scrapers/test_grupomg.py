from pathlib import Path

import pytest

from inmonexo_scrapers.providers.grupomg import parse_grupomg_listing

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "grupomg" / "listing.html"


@pytest.fixture
def listing_html() -> str:
    return FIXTURE.read_text(encoding="utf-8")


def test_parse_grupomg_listing(listing_html: str) -> None:
    drafts = parse_grupomg_listing(listing_html)

    assert len(drafts) == 10
    allure = next(d for d in drafts if d.project_name == "ALLURE")
    assert allure.district == "Jesús María"
    assert allure.address is not None
    assert allure.status_label == "EN CONSTRUCCIÓN"
    assert allure.price_text is not None and "268000" in allure.price_text.replace(",", "")

    urls = {d.source_url for d in drafts}
    assert len(urls) == len(drafts)
    assert all(url.startswith("https://grupomg.pe/departamentos/") for url in urls)
