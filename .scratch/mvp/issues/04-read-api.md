# 04: Read API + analytics overview

**What to build:** FastAPI read endpoints for companies, projects (filter by District), events, and analytics overview/districts so a client can consume NormalizedRecords and MarketEvents without SQL. Verifiable via OpenAPI and contract tests.

**Blocked by:** 02 (can start after MG data exists; enrich after 03)

**Status:** done

- [x] `GET /companies`, `GET /projects`, `GET /projects/{id}`, `GET /events`
- [x] `GET /projects?district=` filters by canonical District
- [x] `GET /analytics/overview` and `GET /analytics/districts` return demo metrics
- [x] OpenAPI generated and runnable locally
- [x] No business logic buried only in route handlers (use packages)
