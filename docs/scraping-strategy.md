# Scraping strategy

## Principles

1. Public pages only
2. Respect robots.txt
3. Reasonable rate limits / concurrency (site-specific; e.g. Grupo MG crawl-delay 10)
4. No auth bypass, no CAPTCHA circumvention
5. Always store `source_url` (and Apify `runId` on ScrapeRun when used)
6. Log extraction failures on ScrapeRun
7. **Fetch via Apify** (user credits) for live runs; **parse/normalize in-repo Providers**
8. CI/tests use recorded fixtures — do not burn Apify credits in unit tests

## Fetch vs Provider

| Layer | Responsibility |
|-------|----------------|
| Apify Actors | Retrieve HTML/JSON (Cheerio or Playwright Actor as needed) |
| Provider adapter | Discover URLs, extract fields from payloads, map to drafts |
| `packages/core` | Money, District, ProjectStatus deterministic parsers |

```text
discover_projects() → Project seeds (url + name)
extract_project(url) → NormalizedRecord (project)
extract_units(project) → UnitType drafts (optional / sparse OK)
```

Providers must accept either fixture HTML or Apify dataset items so TDD stays offline.

## Apify config

- Secret: `APIFY_TOKEN` in `.env` (see `.env.example`)
- Optional: Cursor Apify MCP for agent-driven runs (authenticate when implementing ticket 02+)
- Persist on ScrapeRun: `apify_run_id`, `apify_dataset_id` when applicable

## Seed Developers

UNIO (`unio.pe`), Grupo MG (`grupomg.pe`), Albamar (`albamar.com.pe`), HL (`hldi.pe`), Morada (`morada.pe`).

First vertical slice Provider: **HL.DI**. Next: Grupo MG, Albamar. Morada/UNIO expect null Money where gated.

Detailed site notes: `docs/scraping-audit.md`.
