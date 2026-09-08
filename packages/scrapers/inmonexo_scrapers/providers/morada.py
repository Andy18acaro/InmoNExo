import re

from bs4 import BeautifulSoup

from inmonexo_core.district import normalize_district
from inmonexo_scrapers.base import BaseProvider
from inmonexo_scrapers.html_utils import canonical_url, clean_text
from inmonexo_scrapers.types import ProjectDraft

BASE = "https://morada.pe"
LISTING_URL = "https://morada.pe/proyectos/"


def canonicalize_morada_url(href: str) -> str:
    return canonical_url(BASE, href)


def _parse_meta_line(text: str) -> tuple[str | None, str | None]:
    parts = [clean_text(part) for part in text.split("|") if clean_text(part)]
    district: str | None = None
    status: str | None = None
    for part in parts:
        normalized = normalize_district(part)
        if normalized and not district:
            district = normalized
            continue
        lowered = part.lower()
        if any(k in lowered for k in ("lanzamiento", "construc", "entrega", "venta")):
            status = status or part
    return district, status


def parse_morada_listing(listing_html: str) -> list[ProjectDraft]:
    soup = BeautifulSoup(listing_html, "html.parser")
    drafts: list[ProjectDraft] = []
    seen: set[str] = set()

    for card in soup.select(".project-card"):
        link = card.select_one('a[href*="/proyectos/"]')
        if not link:
            continue

        source_url = canonicalize_morada_url(link.get("href", ""))
        if source_url in seen:
            continue
        seen.add(source_url)

        title_el = card.select_one("h3")
        meta_el = card.select_one(".brxe-text-basic")
        project_name = clean_text(title_el.get_text()) if title_el else source_url.rstrip("/").split("/")[-1]
        district, status = _parse_meta_line(meta_el.get_text()) if meta_el else (None, None)

        drafts.append(
            ProjectDraft(
                project_name=project_name,
                source_url=source_url,
                project_url=source_url,
                district=district,
                address=project_name,
                status_label=status,
                price_text=None,
            )
        )

    return drafts


class MoradaProvider(BaseProvider):
    company_slug = "morada"
    company_name = "Morada"
    website = "https://morada.pe/"
    listing_url = LISTING_URL

    def discover_projects(self, listing_html: str) -> list[ProjectDraft]:
        return parse_morada_listing(listing_html)

    def extract_project(self, html: str, url: str) -> ProjectDraft | None:
        projects = parse_morada_listing(html)
        return projects[0] if projects else None
