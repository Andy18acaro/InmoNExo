# 12: Inventory & absorption per unit type

**What to build:** Track available vs sold units per `UnitType` in each project over time (style: Zonda's lot-level community tracking) and compute absorption velocity (units sold / week). Nobody publishes this in Peru; it is the most differentiating feature in the roadmap. Requires live scrapes feeding snapshots of unit availability.

**Blocked by:** 03

**Status:** open

- [ ] Model/ADR: append-only availability snapshot per project (units available per UnitType, captured at scrape time)
- [ ] Scraper pipeline: capture unit availability during each Fetch into the snapshot
- [ ] Analytics: absorption velocity per project and per district (units/week, rolling window)
- [ ] API: expose inventory + absorption in project detail and district analytics
- [ ] Web: inventory panel in project row expand + district absorption column
- [ ] Tests: two scrape runs with different availability → absorption computed

## Notes

- From competitive research (`docs/research/urbania-competitive-analysis.md`): "how much supply is entering and how fast is it absorbed" is the unanswerable question in Peru today (Yardi Matrix does it for US multifamily).
- Depends on 03 (live scrape) because meaningful absorption needs recurring observations; demo fixtures only have one scrape pass.
- Follow ADR-0002 (append-only) for the availability snapshots.

## Comments

- 2026-09-13: Created from Urbania competitive research (feature #2 of the new batch).
