from abc import ABC, abstractmethod

from inmonexo_scrapers.types import ProjectDraft


class BaseProvider(ABC):
    company_slug: str
    company_name: str
    website: str
    listing_url: str

    @abstractmethod
    def discover_projects(self, listing_html: str) -> list[ProjectDraft]:
        """Parse a listing page and return project seeds with public fields."""

    @abstractmethod
    def extract_project(self, html: str, url: str) -> ProjectDraft | None:
        """Parse a single project page (optional enrichment)."""
