# InmoNExo

Real estate **market intelligence** for Lima: scrape public Developer sites → normalize → history + MarketEvents → API + dashboard.

Not a marketplace.

## Correr (demo local)

Terminal 1 — API + datos de demo:

```powershell
cd E:\DEV\projects\InmoNExo
python -m pip install -e ".[dev]"
python infrastructure/scripts/seed_demo.py
$env:DATABASE_URL="sqlite:///E:/DEV/projects/InmoNExo/inmonexo.db"
python infrastructure/scripts/run_api.py
```

Terminal 2 — Dashboard Next.js:

```powershell
cd E:\DEV\projects\InmoNExo\apps\web
npm install
copy .env.example .env.local
npm run dev
```

- **Dashboard:** http://127.0.0.1:3100
- **API / OpenAPI:** http://127.0.0.1:8100/docs

## Tests

```powershell
cd E:\DEV\projects\InmoNExo
python -m pytest
```

Migraciones (Postgres):

```powershell
cd packages/database
python -m alembic -c alembic.ini upgrade head
```

## Layout

- `apps/api` — ASGI entrypoint
- `apps/web` — Next.js dashboard
- `packages/scrapers` — Providers
- `packages/core` — parsers / shared types
- `packages/database` — models / migrations
- `packages/analytics` — aggregations
- `packages/api` — FastAPI read surface
- `docs/` — architecture, ADRs, scraping audit
- `.scratch/mvp/` — specs and tickets

## Navegación

```powershell
proj inmonexo
cproj inmonexo
```
