# Apify as the live fetch layer

Live page retrieval uses the user's Apify account (API token / MCP) so crawls get managed concurrency, optional browser rendering, and run provenance. Site-specific extraction and normalization stay in in-repo Providers so the adapter seam remains testable with fixtures and does not lock business logic inside Actors. CI must not call Apify.
