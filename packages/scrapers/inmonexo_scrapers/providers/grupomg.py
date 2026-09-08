import re

from bs4 import BeautifulSoup

from inmonexo_core.district import normalize_district
from inmonexo_scrapers.base import BaseProvider
from inmonexo_scrapers.html_utils import canonical_url, clean_text, slug_to_title
from inmonexo_scrapers.types import ProjectDraft

BASE = "https://grupomg.pe"
LISTING_URL = "https://grupomg.pe/departamentos-en-venta/en-venta/"


def canonicalize_grupomg_url(href: str) -> str:
    return canonical_url(BASE, href)


def parse_grupomg_listing(listing_html: str) -> list[ProjectDraft]:
    soup = BeautifulSoup(listing_html, "html.parser")
    drafts: list[ProjectDraft] = []
    seen: set[str] = set()

    for item in soup.select(".b1project_item a.gcard"):
        href = item.get("href", "")
        if not href or "/departamentos/" not in href:
            continue

        source_url = canonicalize_grupomg_url(href)
        if source_url in seen:
            continue
        seen.add(source_url)

        status_el = item.select_one(".gcard_status")
        district_el = item.select_one(".gcard_district")
        address_el = item.select_one(".gcard_address")
        name_el = item.select_one(".gcard_project")
        price_el = item.select_one(".gcard_price")

        price_text = clean_text(price_el.get_text()) if price_el else None
        if price_text and not re.search(r"s/", price_text, re.I):
            price_text = None

        drafts.append(
            ProjectDraft(
                project_name=clean_text(name_el.get_text()) if name_el else slug_to_title(source_url.rstrip("/").split("/")[-1]),
                source_url=source_url,
                project_url=source_url,
                district=normalize_district(clean_text(district_el.get_text())) if district_el else None,
                address=clean_text(address_el.get_text()) if address_el else None,
                status_label=clean_text(status_el.get_text()) if status_el else None,
                price_text=price_text,
            )
        )

    return drafts


class GrupoMgProvider(BaseProvider):
    company_slug = "grupomg"
    company_name = "Grupo MG"
    website = "https://grupomg.pe/"
    listing_url = LISTING_URL
    crawl_delay_seconds = 10

    def discover_projects(self, listing_html: str) -> list[ProjectDraft]:
        return parse_grupomg_listing(listing_html)

    def extract_project(self, html: str, url: str) -> ProjectDraft | None:
        projects = parse_grupomg_listing(html)
        return projects[0] if projects else None
