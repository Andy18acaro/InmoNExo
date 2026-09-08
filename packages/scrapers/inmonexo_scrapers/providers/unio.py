import re

from bs4 import BeautifulSoup

from inmonexo_core.district import normalize_district
from inmonexo_scrapers.base import BaseProvider
from inmonexo_scrapers.html_utils import canonical_url, clean_text, slug_to_title
from inmonexo_scrapers.types import ProjectDraft

BASE = "https://unio.pe"
LISTING_URL = "https://unio.pe/proyectos-venta/"
PROJECT_PATH = re.compile(r"^/proyectos/([a-z0-9-]+)/?$", re.I)


def canonicalize_unio_url(href: str) -> str:
    return canonical_url(BASE, href)


def _name_and_district_from_slug(slug: str) -> tuple[str, str | None]:
    parts = slug.split("-")
    for size in range(len(parts), 0, -1):
        district_candidate = " ".join(parts[-size:])
        district = normalize_district(district_candidate)
        if district:
            name_parts = parts[:-size] or [slug]
            name = " ".join(name_parts).replace("-", " ").title()
            return name, district
    return slug_to_title(slug), None


def parse_unio_listing(listing_html: str) -> list[ProjectDraft]:
    soup = BeautifulSoup(listing_html, "html.parser")
    drafts: list[ProjectDraft] = []
    seen: set[str] = set()

    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith("/"):
            match = PROJECT_PATH.match(href)
        else:
            full = canonicalize_unio_url(href)
            match = PROJECT_PATH.match(full.replace(BASE, ""))
        if not match:
            continue

        slug = match.group(1)
        source_url = f"{BASE}/proyectos/{slug}/"
        if source_url in seen:
            continue
        seen.add(source_url)

        project_name, district = _name_and_district_from_slug(slug)
        for paragraph in soup.find_all("p"):
            text = clean_text(paragraph.get_text())
            if slug.replace("-", " ") not in text.lower() and project_name.lower() not in text.lower():
                continue
            if "–" in text or "-" in text:
                left, _, right = text.partition("–") if "–" in text else text.partition("-")
                if left.strip():
                    project_name = clean_text(left)
                maybe_district = normalize_district(clean_text(right))
                if maybe_district:
                    district = maybe_district
            break

        drafts.append(
            ProjectDraft(
                project_name=project_name,
                source_url=source_url,
                project_url=source_url,
                district=district,
                address=None,
                status_label=None,
                price_text=None,
            )
        )

    return drafts


class UnioProvider(BaseProvider):
    company_slug = "unio"
    company_name = "UNIO Grupo Inmobiliario"
    website = "https://unio.pe/"
    listing_url = LISTING_URL

    def discover_projects(self, listing_html: str) -> list[ProjectDraft]:
        return parse_unio_listing(listing_html)

    def extract_project(self, html: str, url: str) -> ProjectDraft | None:
        projects = parse_unio_listing(html)
        if projects:
            return projects[0]
        match = PROJECT_PATH.search(url.replace(BASE, ""))
        if not match:
            return None
        slug = match.group(1)
        name, district = _name_and_district_from_slug(slug)
        source_url = canonicalize_unio_url(url)
        return ProjectDraft(
            project_name=name,
            source_url=source_url,
            project_url=source_url,
            district=district,
        )
