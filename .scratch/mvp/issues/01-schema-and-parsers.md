# 01: Schema + Money parsers + empty ScrapeRun

**What to build:** A runnable database with companies/projects/units/price_history/events/scrape_runs (and district aliases), plus deterministic Money and ProjectStatus parsers that turn Peruvian marketing strings into normalized fields. Verifiable via migrations + unit tests without hitting the network.

**Blocked by:** None (can start immediately)

**Status:** done

- [x] Alembic migrations create the core tables
- [x] Money parser covers `S/`, `PEN`, `USD`, `K`/`mil` fixtures
- [x] ProjectStatus mapper covers seed marketing labels → controlled enum
- [x] District alias map includes common Lima variants
- [x] Tests pass using SQLite-in-tests or Postgres per ADR-0003
