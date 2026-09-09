# Post-MVP: Intelligence features

**Status:** ready-for-agent  
**Feature slug:** `post-mvp`  
**Depends on:** MVP complete (`.scratch/mvp/`)

## Problem Statement

The MVP proves ingest, normalization, API, and a basic dashboard. The **differentiating value** — temporal market monitoring, price history, and fresh data — is mostly in the backend but under-exposed in the UI and pipeline.

## Solution

Incrementally ship intelligence-facing features that use existing domain objects (`MarketEvent`, `PriceSnapshot`, `UnitType`, analytics) without becoming a marketplace.

## Feature backlog (prioritized)

### Tier 1 — High impact, low effort

| ID | Feature | Rationale | Existing seams |
|----|---------|-----------|----------------|
| F1 | **MarketEvents feed** | Core “monitor the market over time” story | `GET /events`, `MarketEvent` enum in DB |
| F2 | **Price history per project** | Justifies append-only `PriceSnapshot` | Price snapshots on upsert; project detail API |
| F3 | **Alerts digest (email/Slack)** | Analysts want push, not only pull | Events + scrape run timestamps |

### Tier 2 — Medium effort, high value

| ID | Feature | Rationale | Notes |
|----|---------|-----------|-------|
| F4 | **Live scrape (Apify)** | Demo → credible freshness | ADR-0006; `APIFY_TOKEN`; Providers unchanged |
| F5 | **Developer / district compare** | Competitive intelligence | Analytics aggregations exist |
| F6 | **Export CSV/Excel** | Analyst workflow | Read API + table data |
| F7 | **District heatmap** | Spatial view of supply/prices | Was out of MVP scope; keep simple |

### Tier 3 — Phase 2

| ID | Feature | Rationale |
|----|---------|-----------|
| F8 | **UnitTypes in explorer** | Typology-level comparison |
| F9 | **Market activity score** | Single index per district (events + new supply) |
| F10 | **More Providers** | Coverage expansion; ADR-0001 adapter seam |
| F11 | **Auth + workspaces (B2B)** | Premium access; still not marketplace |

## Recommended implementation order

1. F1 — MarketEvents feed (ticket `01`)
2. F2 — Price history chart (ticket `02`)
3. F4 — Live Apify scrape (ticket `03`)
4. F5 or F6 — compare or export (tickets `04`–`05`)
5. Neon Postgres in prod (ops; replace bundled SQLite when data must persist across redeploys)

## Testing decisions

- Behavior tests at API + UI seams: event list filters, chart data given fixture snapshots, export column correctness.
- Do not add Apify calls in CI; keep fixtures for Provider tests.

## Out of scope (still)

Nationwide developers, financial predictions, LLM-default extraction, marketplace/lead gen, real-time WebSocket scraping.

## References

- Handoff: `.scratch/post-mvp/handoff.md`
- MVP spec: `.scratch/mvp/spec.md`
- Domain: `CONTEXT.md`
- ADRs: `docs/adr/`
