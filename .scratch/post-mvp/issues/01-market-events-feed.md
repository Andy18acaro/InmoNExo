# 01: MarketEvents feed on dashboard

**What to build:** A dashboard section that lists recent `MarketEvent` records from `GET /events` — new projects, price changes, status changes, removals — with filters by type and district.

**Blocked by:** —

**Status:** open

- [ ] `fetchEvents()` in `apps/web/src/lib/api.ts` calling `/events`
- [ ] UI component: timeline or table (type, project, developer, district, detected_at, source_url link)
- [ ] Filter by event type and optional district (query params already on API if supported; extend API if not)
- [ ] Overview links to feed or shows “last 5 events” teaser
- [ ] Empty state when no events

## Notes

- API router: `packages/api/inmonexo_api/routers/events.py`
- Demo data already emits events on seed (`seed_demo.py`)
- This is the #1 recommended post-MVP feature

## Comments
