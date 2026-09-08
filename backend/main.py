"""Vercel entrypoint — adds monorepo packages to PYTHONPATH."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for pkg in ("core", "database", "scrapers", "analytics", "api"):
    sys.path.insert(0, str(ROOT / "packages" / pkg))

from inmonexo_api.app import app  # noqa: E402
