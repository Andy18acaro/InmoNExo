#!/usr/bin/env python3
"""Run the InmoNExo Next.js dashboard (port 3100)."""

import os
import subprocess
import sys
from pathlib import Path

WEB_DIR = Path(__file__).resolve().parents[2] / "apps" / "web"


def main() -> int:
    env = os.environ.copy()
    env.setdefault("NEXT_PUBLIC_API_URL", "http://127.0.0.1:8100")
    if not (WEB_DIR / "node_modules").is_dir():
        subprocess.run(["npm", "install"], cwd=WEB_DIR, check=True, shell=True)
    return subprocess.call(["npm", "run", "dev"], cwd=WEB_DIR, env=env, shell=True)


if __name__ == "__main__":
    raise SystemExit(main())
