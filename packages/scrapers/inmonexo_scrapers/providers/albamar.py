import re

from bs4 import BeautifulSoup

from inmonexo_core.district import normalize_district
from inmonexo_scrapers.base import BaseProvider
from inmonexo_scrapers.html_utils import canonical_url, clean_text, slug_to_title
from inmonexo_scrapers.types import ProjectDraft

BASE = "https://albamar.com.pe"
LISTING_URL = "https://albamar.com.pe/departamentos/"


def canonicalize_albamar_url(href: str) -> str:
    return canonical_url(BASE, href)


def _district_from_address(text: str) -> str | None:
    match = re.search(r"<strong>([^<]+)</strong>", text)
    if match:
        return normalize_district(clean_text(match.group(1)))
    for part in reversed(re.split(r"[,\|]", text)):
        district = normalize_district(clean_text(part))
        if district:
            return district
    return None


def parse_albamar_listing(listing_html: str) -> list[ProjectDraft]:
    soup = BeautifulSoup(listing_html, "html.parser")
    drafts: list[ProjectDraft] = []
    seen: set[str] = set()

    for card in soup.select("a.card1"):
        href = card.get("href", "")
        if not href or "/departamentos/" not in href:
            continue

        source_url = canonicalize_albamar_url(href)
        if source_url in seen or source_url.rstrip("/").endswith("/departamentos"):
            continue
        seen.add(source_url)

        slug = source_url.rstrip("/").split("/")[-1]
        status_el = card.select_one(".card1_stage")
        price_el = card.select_one(".card1_price_textdown")
        address_el = card.select_one(".card_direccion")

        address_html = str(address_el) if address_el else ""
        address_text = clean_text(address_el.get_text()) if address_el else None
        price_text = clean_text(price_el.get_text()) if price_el else None

        drafts.append(
            ProjectDraft(
                project_name=slug_to_title(slug),
                source_url=source_url,
                project_url=source_url,
                district=_district_from_address(address_html or (address_text or "")),
                address=address_text,
                status_label=clean_text(status_el.get_text()) if status_el else None,
                price_text=price_text,
            )
        )

    return drafts


class AlbamarProvider(BaseProvider):
    company_slug = "albamar"
    company_name = "Albamar"
    website = "https://albamar.com.pe/"
    listing_url = LISTING_URL

    def discover_projects(self, listing_html: str) -> list[ProjectDraft]:
        return parse_albamar_listing(listing_html)

    def extract_project(self, html: str, url: str) -> ProjectDraft | None:
        projects = parse_albamar_listing(html)
        return projects[0] if projects else None
