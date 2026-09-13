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

Ticket status:

| # | File | Feature | Status | GitHub |
|---|------|---------|--------|--------|
| 01 | `issues/01-market-events-feed.md` | Feed de MarketEvents en dashboard | **done** (2026-09-13) | [#1](https://github.com/Andy18acaro/InmoNExo/issues/1) |
| 02 | `issues/02-price-history-chart.md` | Histórico de precios por proyecto | **done** (2026-09-13) | [#2](https://github.com/Andy18acaro/InmoNExo/issues/2) |
| 03 | `issues/03-live-scrape-apify.md` | Scrape live con Apify | open | [#3](https://github.com/Andy18acaro/InmoNExo/issues/3) |
| 04 | `issues/04-district-developer-compare.md` | Comparador developers / distritos | open | [#4](https://github.com/Andy18acaro/InmoNExo/issues/4) |
| 05 | `issues/05-export-csv.md` | Export CSV/Excel | open | [#5](https://github.com/Andy18acaro/InmoNExo/issues/5) |
| 06 | `issues/06-district-heatmap.md` | Mapa de calor por distrito | open | [#6](https://github.com/Andy18acaro/InmoNExo/issues/6) |
| 07 | `issues/07-unit-types-explorer.md` | UnitTypes en explorer | open | [#7](https://github.com/Andy18acaro/InmoNExo/issues/7) |
| 08 | `issues/08-market-activity-score.md` | Score de movimiento de mercado | open | [#8](https://github.com/Andy18acaro/InmoNExo/issues/8) |
| 09 | `issues/09-more-providers.md` | Más developers + onboarding Provider | open | [#9](https://github.com/Andy18acaro/InmoNExo/issues/9) |
| 10 | `issues/10-auth-workspaces.md` | Auth + workspaces B2B | open | [#10](https://github.com/Andy18acaro/InmoNExo/issues/10) |
| 11 | `issues/11-district-price-index.md` | Índice InmoNExo por distrito | open (blocked by 02 ✅) | — |
| 12 | `issues/12-inventory-absorption.md` | Inventario y absorción por tipología | open (blocked by 03) | — |

---

## Out of scope (unchanged from MVP)

Maps (except simple heatmap exploration), auth/payments in MVP sense, nationwide coverage, real-time scraping as default, LLM-default extraction, financial predictions, marketplace lead gen — see `.scratch/mvp/spec.md`.

---

## Comments

- 2026-09-08: Handoff created after Vercel deploy + feature roadmap discussion.
- 2026-09-13: Tickets **01 y 02 implementados**: `GET /events` enriquecido (project/company/district/source_url) + filtro `district`; `GET /projects/{id}/price-history` nuevo; dashboard con `EventsFeed` (filtros por tipo/distrito) e histórico de precios con SVG chart en fila expandible del explorer. 56 tests passing, `npm run build` OK.
- 2026-09-13: Research competitivo Urbania + referentes US en `docs/research/urbania-competitive-analysis.md` → nuevos tickets **11** (índice por distrito, desbloqueado) y **12** (inventario/absorción, requiere 03). Siguiente feature recomendada: **11** o **03**.
