# 03: Live scrape via Apify

**What to build:** Wire live fetch through Apify (ADR-0006) for scheduled or manual scrape runs in non-CI environments; keep fixtures for tests.

**Blocked by:** —

**Status:** open

- [ ] Document `APIFY_TOKEN` setup in README
- [ ] CLI or script: `infrastructure/scripts/run_scrape.py` runs live against configured Providers
- [ ] Optional: Vercel cron or external scheduler (document limits — serverless timeout)
- [ ] ScrapeRun logging visible via API or admin view
- [ ] CI must not call Apify

## Notes

- User Apify credits; Providers parse payloads, Actors do not embed business rules
- Production today uses static `backend/inmonexo.db`; live scrape needs Postgres (Neon) for persistence

## Comments

- 2026-09-08: GitHub issue [#3](https://github.com/Andy18acaro/InmoNExo/issues/3)