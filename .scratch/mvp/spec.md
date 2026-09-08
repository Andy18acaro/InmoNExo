# MVP: Market intelligence ingest for 5 Lima Developers

**Status:** ready-for-agent  
**Feature slug:** `mvp`

## Problem Statement

Public Project data for Lima residential Developers is scattered across independent marketing sites. Analysts and competing Developers cannot reliably compare supply, pricing, and status without manual visits. InmoNExo needs a working prototype that monitors five named Developers, stores NormalizedRecords with PriceSnapshots, emits MarketEvents, and exposes the dataset via API and a simple dashboard.

## Solution

A modular ingest pipeline (Provider adapters → deterministic normalize → Postgres → MarketEvents) plus a read API and an intelligence-oriented dashboard. First vertical proof uses the **HL.DI** Provider end-to-end (per `docs/scraping-audit.md`); then the remaining four Providers; then API and web.

## User Stories

1. As a market analyst, I want all monitored Developers listed in one place, so that I know coverage of the dataset.
2. As a market analyst, I want Projects discovered automatically from official sites, so that I do not hunt listing pages manually.
3. As a market analyst, I want Project fields normalized (District, ProjectStatus, Money), so that I can filter and compare.
4. As a market analyst, I want UnitTypes when public, so that I can compare typologies—not only Project-level "desde" prices.
5. As a market analyst, I want PriceSnapshots over time, so that I can see price moves instead of lost history.
6. As a market analyst, I want MarketEvents (new Project, price/status change, removal), so that I can monitor the market temporally.
7. As a competing Developer, I want Projects grouped by District and by Developer, so that I can see local supply.
8. As an investor, I want overview metrics (counts, districts covered, last ScrapeRun time), so that I trust freshness.
9. As a consultant, I want to search/filter/sort Projects in a table, so that I can explore without SQL.
10. As an engineer, I want one Provider per Developer behind a shared interface, so that adding a sixth Developer is one adapter.
11. As an engineer, I want ScrapeRun failure logs, so that broken selectors are visible.
12. As an engineer, I want provenance `source_url` on records, so that every fact is auditable.
13. As a product lead, I want interview notes captured separately, so that discovery does not force premature pivots.
14. As a stakeholder, I want OpenAPI docs for the read API, so that I can explore data without a custom client.
15. As a future user, I want the schema flexible enough for new fields, so that interview insights can extend the model without a rewrite.

## Implementation Decisions

- Monorepo layout: `apps/api`, `apps/web`, `packages/{core,database,scrapers,analytics}`.
- Provider seam (ADR-0001): `discover_projects` / `extract_project` / `extract_units`.
- Append-only PriceSnapshot + MarketEvent (ADR-0002).
- Postgres runtime; SQLite only in tests (ADR-0003).
- Deterministic Money/District/ProjectStatus parsers before any optional LLM (ADR-0004).
- Not a marketplace (ADR-0005).
- Seed Developers: UNIO, Grupo MG, Albamar, HL, Morada.
- First Provider: HL.DI (Grupo MG second).
- Live fetch via **Apify** (user credits); Providers parse; fixtures for tests (ADR-0006).
- Stack: Python 3.12 + uv, FastAPI, SQLAlchemy 2 + Alembic, Requests+BS4 (Playwright only if audit requires), Next.js + TS + Tailwind.
- Local issue tracker under `.scratch/mvp/`.

## Testing Decisions

- Prefer behavior tests at the highest seam: normalize Money/District/status; upsert + MarketEvent emission given fixture HTML or fixture drafts; API contract tests once endpoints exist.
- Do not assert on brittle full-page HTML snapshots as the only test; use recorded fixtures per Provider.
- Good tests assert external behavior (parsed Money, emitted MarketEvent type), not private helper structure.

## Out of Scope

Maps, auth, payments, nationwide Developers, real-time scraping, LLM-default extraction, financial predictions, marketplace lead gen.

## Further Notes

Glossary: root `CONTEXT.md`. Site audit: `docs/scraping-audit.md`. Architecture notes: `docs/architecture.md`.
