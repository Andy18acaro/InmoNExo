# 03: Remaining four Providers (Grupo MG, Albamar, UNIO, Morada)

**What to build:** Providers for the other four seed Developers using the same Apify-fetch + in-repo-parse pipeline proven on HL.DI. Verifiable when all five Developers have Projects (or explicit empty/failure notes) after a combined ScrapeRun.

**Blocked by:** 02

**Status:** done

- [x] Grupo MG Provider via Apify (honor crawl-delay / low concurrency)
- [x] Albamar Provider via Apify (Cloudflare-aware Actor if needed; no CAPTCHA bypass)
- [x] UNIO Provider (expect sparse prices)
- [x] Morada Provider (expect null Money)
- [x] Sparse/missing prices stay null; no invented values
- [x] Fixture coverage per Provider so CI stays credit-free
