from pathlib import Path

import pytest

from inmonexo_core.enums import ProjectStatus
from inmonexo_core.status import map_project_status
from inmonexo_scrapers.providers.hldi import canonicalize_hldi_url, parse_hldi_listing

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "hldi" / "listing.html"


@pytest.fixture
def listing_html() -> str:
    return FIXTURE.read_text(encoding="utf-8")


@pytest.mark.parametrize(
    ("href", "expected"),
    [
        (
            "https://hldi.pe/sq2-work-and-living/",
            "https://hldi.pe/proyectos/sq-2-work-living/",
        ),
        (
            "/proyectos/sq-2-work-living/",
            "https://hldi.pe/proyectos/sq-2-work-living/",
        ),
        (
            "/llums-family-style/",
            "https://hldi.pe/proyectos/llums-family-style/",
        ),
    ],
)
def test_canonicalize_hldi_url(href: str, expected: str) -> None:
    assert canonicalize_hldi_url(href) == expected


def test_parse_hldi_listing_discovers_projects(listing_html: str) -> None:
    drafts = parse_hldi_listing(listing_html)

    assert len(drafts) >= 8
    urls = {d.source_url for d in drafts}
    assert len(urls) == len(drafts)
    assert "https://hldi.pe/proyectos/sq-2-work-living/" in urls

    sq2 = next(d for d in drafts if "sq-2-work-living" in d.source_url)
    assert sq2.project_name == "SQ 2 Work & Living"
    assert sq2.district == "Surquillo"
    assert sq2.address is not None and "Surquillo" in sq2.address
    assert sq2.price_text is not None and "292" in sq2.price_text
    assert map_project_status(sq2.status_label) == ProjectStatus.PRE_SALE

    llums = next(d for d in drafts if "llums-family-style" in d.source_url)
    assert llums.project_name == "LLUMS Family Style"
    assert llums.district == "Jesús María"
    assert map_project_status(llums.status_label) == ProjectStatus.PRE_SALE
