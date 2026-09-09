# Handoff — Post-MVP features

**Date:** 2026-09-08  
**Status:** ready-to-continue  
**Feature slug:** `post-mvp`

## Where we left off

### MVP shipped

- Monorepo with 5 Lima Developers, normalized data, read API, Next.js dashboard.
- **50 tests** passing locally.
- **Deployed on Vercel (free):**
  - Dashboard: https://inmonexo-xi.vercel.app
  - API / OpenAPI: https://inmonexo-xi.vercel.app/svc/docs
  - Vercel project: https://vercel.com/andy-acaro/inmonexo
- Production uses **bundled demo SQLite** (`backend/inmonexo.db`) seeded from fixtures — no Neon yet.
- GitHub: https://github.com/Andy18acaro/InmoNExo (`master` at `020b151` or later).

### Deploy stack (for context)

- `vercel.json` — two services: Next.js (`apps/web`) + FastAPI (`backend.main:app`).
- Public API under `/svc/*`; internal binding `INMONEXO_API_URL` for SSR fetches.
- Env on Vercel: `FASTAPI_ROOT_PATH=/svc` (optional; middleware strips `/svc` when `VERCEL=1`).

### Product objective (reminder)

**Market intelligence** for Lima residential developers — scrape/normalize/history/events → API + dashboard. **Not a marketplace.**

See root `CONTEXT.md` and `.scratch/mvp/spec.md` for domain language and MVP scope.

---

## Conversation to resume

User asked: *"¿qué feature adicional podemos darle?"*

We prioritized three features (see `spec.md` and `issues/`). Recommended order:

1. **MarketEvents feed** — API exists (`GET /events`); dashboard does not consume it yet.
2. **Price history chart** — `PriceSnapshot` is append-only (ADR-0002); no UI yet.
3. **Live scrape via Apify** — ADR-0006; MVP uses fixtures / `seed_demo.py`.

---

## How to pick up in a new session

Tell the agent:

> Continúa desde `.scratch/post-mvp/handoff.md`. Implementa el ticket `01-market-events-feed` (o el que indique).

Or:

> Lee el handoff post-MVP y ayúdame a elegir/implementar la siguiente feature.

Useful commands:

```powershell
cd E:\DEV\projects\InmoNExo
python -m pytest
# local demo
python infrastructure/scripts/seed_demo.py
python infrastructure/scripts/run_api.py
# web: apps/web → npm run dev
```

---

## Full backlog

Documented in `.scratch/post-mvp/spec.md`.

Ticket stubs (not started):

| # | File | Feature |
|---|------|---------|
| 01 | `issues/01-market-events-feed.md` | Feed de MarketEvents en dashboard |
| 02 | `issues/02-price-history-chart.md` | Histórico de precios por proyecto |
| 03 | `issues/03-live-scrape-apify.md` | Scrape live con Apify |
| 04 | `issues/04-district-developer-compare.md` | Comparador developers / distritos |
| 05 | `issues/05-export-csv.md` | Export CSV/Excel |
| 06 | `issues/06-district-heatmap.md` | Mapa de calor por distrito |
| 07 | `issues/07-unit-types-explorer.md` | UnitTypes en explorer |
| 08 | `issues/08-market-activity-score.md` | Score de movimiento de mercado |
| 09 | `issues/09-more-providers.md` | Más developers + onboarding Provider |
| 10 | `issues/10-auth-workspaces.md` | Auth + workspaces B2B |

---

## Out of scope (unchanged from MVP)

Maps (except simple heatmap exploration), auth/payments in MVP sense, nationwide coverage, real-time scraping as default, LLM-default extraction, financial predictions, marketplace lead gen — see `.scratch/mvp/spec.md`.

---

## Comments

- 2026-09-08: Handoff created after Vercel deploy + feature roadmap discussion.
