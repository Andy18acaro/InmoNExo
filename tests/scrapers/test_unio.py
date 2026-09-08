from pathlib import Path

import pytest

from inmonexo_scrapers.providers.unio import parse_unio_listing

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "unio" / "listing.html"


@pytest.fixture
def listing_html() -> str:
    return FIXTURE.read_text(encoding="utf-8")


def test_parse_unio_listing_sparse_catalog(listing_html: str) -> None:
    drafts = parse_unio_listing(listing_html)

    assert len(drafts) == 1
    varenna = drafts[0]
    assert varenna.source_url == "https://unio.pe/proyectos/varenna-san-isidro/"
    assert "VARENNA" in varenna.project_name.upper()
    assert varenna.district == "San Isidro"
    assert varenna.price_text is None
