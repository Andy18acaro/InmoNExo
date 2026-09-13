# 02: Price history chart per project

**What to build:** When viewing a project (row expand or detail panel), show price over time from `PriceSnapshot` history — table or simple line chart.

**Blocked by:** —

**Status:** done

- [x] API: endpoint or extend `GET /projects/{id}` with snapshot series (if not already exposed)
- [x] Web: project detail UI with history (dates + amount + currency)
- [x] Handle missing history / single point gracefully
- [x] Tests: fixture with two snapshots → series returned

## Notes

- ADR-0002: append-only snapshots; never overwrite latest only
- May need new read method in `read_service` / analytics package

## Comments

- 2026-09-08: GitHub issue [#2](https://github.com/Andy18acaro/InmoNExo/issues/2)