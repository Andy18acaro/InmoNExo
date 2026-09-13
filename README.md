# InmoNExo

Real estate **market intelligence** for Lima: scrape public Developer sites → normalize → history + MarketEvents → API + dashboard.

Not a marketplace.

## Features

- Dashboard con métricas, distritos y explorer de proyectos filtrable/ordenable.
- **Feed de eventos de mercado** (proyectos nuevos, cambios de precio/estado) con filtros por tipo y distrito — `GET /events?event_type=&district=`.
- **Histórico de precios por proyecto** (gráfico + tabla desde snapshots append-only) en la fila expandible del explorer — `GET /projects/{id}/price-history`.

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

## Deploy (Vercel + Neon — gratis)

Stack sin costo inicial: **Vercel Hobby** (web + API) y **Neon** (Postgres free tier).

### 1. Base de datos (Neon)

1. Crea cuenta en [neon.tech](https://neon.tech) (plan Free).
2. Crea un proyecto y copia la connection string (`postgresql://...`).
3. En el dashboard de Vercel → **Settings → Environment Variables**, añade:
   - `DATABASE_URL` = tu connection string de Neon
   - `FASTAPI_ROOT_PATH` = `/svc`

### 2. Seed (una vez)

Con la `DATABASE_URL` de Neon en tu terminal local:

```powershell
cd E:\DEV\projects\InmoNExo
$env:DATABASE_URL="postgresql://USER:PASS@HOST/neondb?sslmode=require"
python infrastructure/scripts/seed_demo.py
```

### 3. Vercel

1. Importa el repo [Andy18acaro/InmoNExo](https://github.com/Andy18acaro/InmoNExo) en [vercel.com/new](https://vercel.com/new).
2. Vercel detecta `vercel.json` con dos servicios: **Next.js** (`apps/web`) y **FastAPI** (`backend/main.py`).
3. Deploy. URLs:
   - Dashboard: `https://tu-proyecto.vercel.app`
   - API / OpenAPI: `https://tu-proyecto.vercel.app/svc/docs`

CLI (opcional):

```powershell
npx vercel login
npx vercel --prod
```

La web usa el binding interno `INMONEXO_API_URL`; el navegador ve la API en `/svc`.

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
