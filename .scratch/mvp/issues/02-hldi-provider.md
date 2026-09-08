# 02: HL.DI Provider → DB + MarketEvents (Apify fetch)

**What to build:** End-to-end: fetch HL.DI public pages via **Apify** (user credits), parse with the HL Provider, normalize, upsert, append PriceSnapshots, emit MarketEvents. Offline path: same Provider against fixtures so TDD does not burn credits. Verifiable by one live ScrapeRun (Apify) plus fixture tests.

**Blocked by:** 01

**Status:** done

- [x] Thin Apify fetch client (`APIFY_TOKEN`) returns HTML/dataset items; ScrapeRun stores `apify_run_id` / `apify_dataset_id`
- [x] HL.DI Provider implements discover + extract behind the shared interface (works on fixtures OR Apify payloads)
- [x] Canonicalize dual URL patterns (marketing root vs `/proyectos/{slug}/`)
- [x] At least several Projects land with District, ProjectStatus, and Money when public
- [x] Re-running the ScrapeRun is idempotent (no duplicate Projects)
- [x] A second run with a fixture price change emits `PRICE_CHANGE`
- [x] Failures are logged on the ScrapeRun; `source_url` stored
- [x] No CAPTCHA/auth bypass; polite concurrency
