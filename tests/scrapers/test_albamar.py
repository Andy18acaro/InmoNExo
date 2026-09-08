from pathlib import Path

import pytest

from inmonexo_scrapers.providers.albamar import parse_albamar_listing

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "albamar" / "listing.html"


@pytest.fixture
def listing_html() -> str:
    return FIXTURE.read_text(encoding="utf-8")


def test_parse_albamar_listing(listing_html: str) -> None:
    drafts = parse_albamar_listing(listing_html)

    assert len(drafts) == 12
    arenales = next(d for d in drafts if "arenales" in d.source_url)
    assert arenales.project_name == "Albamar Arenales"
    assert arenales.district == "Santa Beatriz"
    assert arenales.status_label == "Entrega inmediata"
    assert arenales.price_text is not None and "280" in arenales.price_text

    urls = {d.source_url for d in drafts}
    assert len(urls) == len(drafts)
