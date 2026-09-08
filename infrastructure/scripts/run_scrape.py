#!/usr/bin/env python3
"""Run one or all Provider scrapes (Apify fetch by default)."""

import argparse
import sys
import time

from inmonexo_db.session import get_session_factory
from inmonexo_scrapers.apify_client import ApifyFetcher
from inmonexo_scrapers.pipeline import run_all_provider_scrapes, run_provider_scrape
from inmonexo_scrapers.registry import PROVIDERS


def main() -> int:
    parser = argparse.ArgumentParser(description="Run InmoNExo provider scrape")
    parser.add_argument(
        "--provider",
        default="all",
        choices=[*PROVIDERS.keys(), "all"],
    )
    args = parser.parse_args()

    session_factory = get_session_factory()
    with session_factory() as session:
        if args.provider == "all":
            fetcher = ApifyFetcher()

            def fetcher_for(_provider):
                return fetcher

            runs = run_all_provider_scrapes(session, list(PROVIDERS.values()), fetcher_for)
            for index, run in enumerate(runs):
                print(
                    f"ScrapeRun {run.provider_slug} status={run.status} "
                    f"projects_seen={run.projects_seen}"
                )
                if run.error_log:
                    print(run.error_log, file=sys.stderr)
                provider = list(PROVIDERS.values())[index]
                delay = getattr(provider, "crawl_delay_seconds", 0)
                if delay and index < len(runs) - 1:
                    time.sleep(delay)
            failed = [run for run in runs if run.status != "succeeded"]
            return 1 if failed else 0

        provider = PROVIDERS[args.provider]
        run = run_provider_scrape(session, provider, ApifyFetcher())
        print(f"ScrapeRun {run.id} status={run.status} projects_seen={run.projects_seen}")
        if run.error_log:
            print(run.error_log, file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
