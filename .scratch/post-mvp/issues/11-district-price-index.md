# 11: District price index (Índice InmoNExo)

**What to build:** Weekly price index per district computed from `PriceSnapshot` history — the InmoNExo answer to Urbania Índex (monthly, Lima-aggregated only). Public methodology, per-district and per-developer granularity: avg price per m², week-over-week delta, trend sparkline. Exposed via `GET /analytics/index` and a dashboard section.

**Blocked by:** 02

**Status:** open

- [ ] Analytics: index computation from PriceSnapshots (median price/m² per district per ISO week; handle sparse data)
- [ ] API: `GET /analytics/index?district=` returning series + WoW delta
- [ ] Web: index section with per-district trend (reuse SVG chart pattern from PriceChart)
- [ ] Public methodology doc (`docs/index-methodology.md`)
- [ ] Tests: two weeks of snapshots → index series with delta

## Notes

- From competitive research (`docs/research/urbania-competitive-analysis.md`): Urbania Índex is monthly and Lima-wide; weekly + per-district is the differentiator.
- Altos Research's Market Action Index is the UX reference (simple, branded, weekly).
- Density guard: districts with < N snapshots in a week need fallback (carry-forward or null, decide in implementation).

## Comments

- 2026-09-13: Created from Urbania competitive research (feature #1 of the new batch).
