from pathlib import Path

import pytest

from inmonexo_scrapers.providers.morada import parse_morada_listing

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "morada" / "listing.html"


@pytest.fixture
def listing_html() -> str:
    return FIXTURE.read_text(encoding="utf-8")


def test_parse_morada_listing(listing_html: str) -> None:
    drafts = parse_morada_listing(listing_html)

    assert len(drafts) == 5
    javier = next(d for d in drafts if "javier-prado-oeste-2168" in d.source_url)
    assert javier.project_name == "Javier Prado Oeste 2168"
    assert javier.district == "San Isidro"
    assert javier.status_label == "Lanzamiento"
    assert javier.price_text is None

    assert all(d.price_text is None for d in drafts)
