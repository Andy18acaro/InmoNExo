# Data model (draft)

Entities follow `CONTEXT.md`. Schema is implemented in a later ticket; this doc is the contract.

## Tables (proposed)

- **companies** — Developer identity (`website` natural key)
- **projects** — Project tied to company (`source_url` natural key); holds latest snapshot fields + `first_seen_at` / `last_seen_at`
- **units** — UnitType rows under a project (fingerprint: project + typology + bedrooms + area band)
- **price_history** — PriceSnapshot append-only
- **events** — MarketEvent append-only
- **scrape_runs** — ScrapeRun ops log
- **districts** + **district_aliases** — canonical District mapping

## ProjectStatus

`PRE_SALE` | `UNDER_CONSTRUCTION` | `READY_TO_MOVE` | `DELIVERED` | `UNKNOWN`

## Money

Store `price_min` / `price_max` as numeric + `currency` (`PEN` | `USD`). Parse marketing strings in `packages/core`.
