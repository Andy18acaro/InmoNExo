# Architecture

InmoNExo ingests public Developer websites through Provider adapters, normalizes into a shared schema, stores history in Postgres, emits MarketEvents, and exposes read APIs plus a dashboard.

```text
Developer sites → Provider → normalize → database (+ PriceSnapshot / MarketEvent) → API → web
```

## Packages

| Package | Responsibility |
|---------|----------------|
| `packages/scrapers` | Provider interface + per-Developer adapters |
| `packages/core` | Money/district/status parsers, shared types |
| `packages/database` | SQLAlchemy models, Alembic, upsert/diff |
| `packages/analytics` | Overview aggregations for API/dashboard |
| `apps/api` | FastAPI read surface |
| `apps/web` | Next.js market dashboard |

See ADRs in `docs/adr/` and glossary in `CONTEXT.md`.
