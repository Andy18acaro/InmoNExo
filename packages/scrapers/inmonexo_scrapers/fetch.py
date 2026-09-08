from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class FetchResult:
    url: str
    html: str
    apify_run_id: str | None = None
    apify_dataset_id: str | None = None


class PageFetcher(Protocol):
    def fetch(self, url: str) -> FetchResult: ...


class StaticFetcher:
    """Offline fetcher for tests — url → html map."""

    def __init__(self, pages: dict[str, str]) -> None:
        self._pages = pages

    def fetch(self, url: str) -> FetchResult:
        if url not in self._pages:
            raise KeyError(f"No fixture for URL: {url}")
        return FetchResult(url=url, html=self._pages[url])
