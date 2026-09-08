# Provider adapter seam for scraping

Each Developer website is heterogeneous. We extract through a single Provider interface (`discover_projects`, `extract_project`, `extract_units`) with one adapter package per Developer. Shared normalization and persistence stay outside the adapters so adding a Developer means one new Provider, not a new pipeline.
