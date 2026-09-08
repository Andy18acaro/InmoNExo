# InmoNExo

Structured market intelligence from public Peruvian residential developer websites, starting in Lima. Not a property marketplace.

## Language

### Market entities

**Developer**:
A real estate company that builds and sells residential projects from its own official website.
_Avoid_: inmobiliaria (ambiguous), broker, agency, listing portal

**Project**:
A named residential development (edificio / multifamiliar) published by a Developer.
_Avoid_: listing, property, property ad

**UnitType**:
A publicly advertised apartment typology within a Project (e.g. 2 dorms / 65 m²), not necessarily a specific inventory unit number.
_Avoid_: unit inventory SKU, apartment listing

**District**:
Canonical Lima district name used for grouping and filters (e.g. San Isidro).
_Avoid_: barrio, zona, raw scraped locality string

**Money**:
A numeric amount with an ISO currency (`PEN` or `USD`) after deterministic parsing of Peruvian marketing strings.
_Avoid_: raw price text, "desde" string

### Pipeline

**Fetch**:
Cloud retrieval of public page payloads for a ScrapeRun, executed on Apify using the project token.
_Avoid_: ad-hoc local-only crawler as the sole live path; Actor that embeds all business rules

**Provider**:
A scraper adapter for one Developer's website that implements discovery and extraction behind a shared interface (consumes Apify payloads or fixtures).
_Avoid_: spider, crawler script, scraper monolith

**ScrapeRun**:
One execution of the ingest pipeline for one or more Providers, with logged successes and failures.
_Avoid_: job (ambiguous), sync

**NormalizedRecord**:
A Project or UnitType validated against the shared schema after parsing and district/status mapping.
_Avoid_: raw HTML row, scrape dict

**PriceSnapshot**:
An append-only historical observation of a price at a point in time; never an in-place overwrite of the latest value alone.
_Avoid_: current price column as sole store

**MarketEvent**:
A detected change vs prior state (`NEW_PROJECT`, `PRICE_CHANGE`, `PROJECT_STATUS_CHANGE`, `PROJECT_REMOVED`, `NEW_UNIT_TYPE`, `PRICE_REMOVED`).
_Avoid_: log line, notification (UI concern)

**ProjectStatus**:
Controlled enum: `PRE_SALE`, `UNDER_CONSTRUCTION`, `READY_TO_MOVE`, `DELIVERED`, `UNKNOWN`.
_Avoid_: free-text site labels as stored truth
