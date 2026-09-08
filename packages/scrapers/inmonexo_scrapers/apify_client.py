import time
from dataclasses import dataclass

import httpx
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApifySettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    apify_token: str = ""
    apify_default_actor: str = "apify/cheerio-scraper"


@dataclass(frozen=True, slots=True)
class ApifyRunMeta:
    run_id: str
    dataset_id: str


class ApifyFetcher:
    """Thin Apify client: run cheerio-scraper for a single start URL."""

    def __init__(self, settings: ApifySettings | None = None) -> None:
        self._settings = settings or ApifySettings()
        if not self._settings.apify_token:
            raise ValueError("APIFY_TOKEN is required for ApifyFetcher")

    def fetch(self, url: str) -> "FetchResult":
        from inmonexo_scrapers.fetch import FetchResult

        actor_id = self._settings.apify_default_actor.replace("/", "~")
        headers = {"Authorization": f"Bearer {self._settings.apify_token}"}
        input_payload = {
            "startUrls": [{"url": url}],
            "pageFunction": """async function pageFunction(context) {
                const { request, $ } = context;
                return { url: request.url, html: $.html() };
            }""",
            "maxRequestsPerCrawl": 1,
        }

        with httpx.Client(timeout=120.0) as client:
            run_resp = client.post(
                f"https://api.apify.com/v2/acts/{actor_id}/runs",
                headers=headers,
                json=input_payload,
            )
            run_resp.raise_for_status()
            run_data = run_resp.json()["data"]
            run_id = run_data["id"]
            dataset_id = run_data["defaultDatasetId"]

            for _ in range(60):
                status_resp = client.get(
                    f"https://api.apify.com/v2/actor-runs/{run_id}",
                    headers=headers,
                )
                status_resp.raise_for_status()
                status = status_resp.json()["data"]["status"]
                if status in {"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"}:
                    break
                time.sleep(2)
            else:
                raise TimeoutError(f"Apify run {run_id} did not finish in time")

            if status != "SUCCEEDED":
                raise RuntimeError(f"Apify run {run_id} ended with status {status}")

            items_resp = client.get(
                f"https://api.apify.com/v2/datasets/{dataset_id}/items",
                headers=headers,
                params={"limit": 1},
            )
            items_resp.raise_for_status()
            items = items_resp.json()
            if not items:
                raise RuntimeError(f"Apify dataset {dataset_id} returned no items")

            html = items[0].get("html") or items[0].get("body") or ""
            return FetchResult(
                url=url,
                html=html,
                apify_run_id=run_id,
                apify_dataset_id=dataset_id,
            )
