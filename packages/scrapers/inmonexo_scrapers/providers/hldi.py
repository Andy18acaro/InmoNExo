import html as html_lib
import re
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from inmonexo_core.district import normalize_district
from inmonexo_scrapers.base import BaseProvider
from inmonexo_scrapers.types import ProjectDraft

BASE = "https://hldi.pe"

# Marketing root paths → canonical /proyectos/ URL (dual URL pattern)
_SLUG_ALIASES: dict[str, str] = {
    "sq2-work-and-living": "sq-2-work-living",
    "sq-work-and-living": "sq-work-living",
    "llums-family-style": "llums-family-style",
    "urban-mood-apartments": "urban-mood-apartments",
    "malena-family-apartments": "malena-family-apartments",
    "millennium-magdalena": "millennium-magdalena",
    "friendz-2": "friendz-2",
    "family-apartments": "family-apartments",
    "mf-work-living": "mf-work-living",
}


def canonicalize_hldi_url(href: str) -> str:
    full = urljoin(BASE, href.strip())
    parsed = urlparse(full)
    path = parsed.path.strip("/")
    if not path:
        return full.rstrip("/") + "/"

    segments = path.split("/")
    if segments[0] == "proyectos" and len(segments) >= 2:
        slug = segments[1]
    else:
        slug = segments[0]

    slug = _SLUG_ALIASES.get(slug, slug)
    return f"{BASE}/proyectos/{slug}/"


def _clean_text(value: str) -> str:
    return html_lib.unescape(" ".join(value.split()))


def _is_price(text: str) -> bool:
    return bool(re.search(r"(?i)s/\s*[\d.,]+|\$\s*[\d.,]+|usd\s*[\d.,]+", text))


def _is_status(text: str) -> bool:
    lowered = text.lower()
    keywords = (
        "venta",
        "construc",
        "entrega",
        "lanzamiento",
        "inmediata",
        "pronta",
    )
    return any(k in lowered for k in keywords) and not _is_price(text)


def _classify_card_texts(texts: list[str]) -> dict[str, str | None]:
    project_name: str | None = None
    status_label: str | None = None
    price_text: str | None = None
    address: str | None = None
    district: str | None = None

    for text in texts:
        if text == "Desde":
            continue
        if _is_price(text):
            price_text = price_text or text
            continue
        if _is_status(text):
            status_label = status_label or text
            continue
        if "N°" in text or "Nº" in text:
            address = address or text
            continue
        normalized = normalize_district(text)
        if normalized and normalized == text and not district:
            district = normalized
            continue
        if not project_name:
            project_name = text

    return {
        "project_name": project_name,
        "status_label": status_label,
        "price_text": price_text,
        "address": address,
        "district": district,
    }


def parse_hldi_listing(listing_html: str) -> list[ProjectDraft]:
    soup = BeautifulSoup(listing_html, "html.parser")
    drafts: list[ProjectDraft] = []
    seen: set[str] = set()

    for item in soup.select(".jet-listing-grid__item"):
        links = item.select("h2.elementor-heading-title a")
        if not links:
            continue

        hrefs = [a.get("href", "") for a in links if a.get("href")]
        if not hrefs:
            continue

        primary_href = hrefs[0]
        source_url = canonicalize_hldi_url(primary_href)
        if source_url in seen:
            continue
        seen.add(source_url)

        texts = [_clean_text(a.get_text()) for a in links]
        fields = _classify_card_texts(texts)
        name = fields["project_name"] or source_url.rstrip("/").split("/")[-1].replace("-", " ").title()
        drafts.append(
            ProjectDraft(
                project_name=name,
                source_url=source_url,
                project_url=source_url,
                district=fields["district"],
                address=fields["address"],
                status_label=fields["status_label"],
                price_text=fields["price_text"],
            )
        )

    return drafts


LISTING_URL = "https://hldi.pe/proyectos/"


class HlProvider(BaseProvider):
    company_slug = "hldi"
    company_name = "HL Desarrollos Inmobiliarios"
    website = "https://hldi.pe/"
    listing_url = LISTING_URL

    def discover_projects(self, listing_html: str) -> list[ProjectDraft]:
        return parse_hldi_listing(listing_html)

    def extract_project(self, html: str, url: str) -> ProjectDraft | None:
        projects = parse_hldi_listing(html)
        if projects:
            return projects[0]
        return None
