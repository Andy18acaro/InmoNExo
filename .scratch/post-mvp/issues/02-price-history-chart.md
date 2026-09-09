# 02: Price history chart per project

**What to build:** When viewing a project (row expand or detail panel), show price over time from `PriceSnapshot` history — table or simple line chart.

**Blocked by:** —

**Status:** open

- [ ] API: endpoint or extend `GET /projects/{id}` with snapshot series (if not already exposed)
- [ ] Web: project detail UI with history (dates + amount + currency)
- [ ] Handle missing history / single point gracefully
- [ ] Tests: fixture with two snapshots → series returned

## Notes

- ADR-0002: append-only snapshots; never overwrite latest only
- May need new read method in `read_service` / analytics package

## Comments
