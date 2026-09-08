#!/usr/bin/env python3
"""Seed local SQLite with fixture scrapes for demo / development."""

import os
from pathlib import Path

from inmonexo_db.session import get_session_factory, init_db
from inmonexo_scrapers.fetch import StaticFetcher
from inmonexo_scrapers.pipeline import run_all_provider_scrapes
from inmonexo_scrapers.registry import PROVIDERS

ROOT = Path(__file__).resolve().parents[2]
FIXTURE_ROOT = ROOT / "tests" / "fixtures"
DB_PATH = ROOT / "inmonexo.db"


def main() -> None:
    os.environ["DATABASE_URL"] = f"sqlite:///{DB_PATH}"
    init_db()
    session_factory = get_session_factory()

    def fetcher_for(provider):
        html = (FIXTURE_ROOT / provider.company_slug / "listing.html").read_text(encoding="utf-8")
        return StaticFetcher({provider.listing_url: html})

    with session_factory() as session:
        runs = run_all_provider_scrapes(session, list(PROVIDERS.values()), fetcher_for)
        total = sum(run.projects_seen for run in runs)
        print(f"Seeded {DB_PATH} — {len(runs)} providers, {total} projects")


if __name__ == "__main__":
    main()
