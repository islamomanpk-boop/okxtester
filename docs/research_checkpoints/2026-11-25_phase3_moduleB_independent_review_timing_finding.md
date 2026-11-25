# Phase 3 Module B — Independent Review Timing Finding

**Date:** 2026-11-25  
**Project:** OKX Price Action V1 — Phase 3 Sideways / Range  
**Module:** Breakout / failed-breakout lifecycle V1.1  
**Status:** Review in progress; not a Module B acceptance or closure.

## Verified archive review

The historical workflow completed successfully and archived seven report files on `price-action-v1`. The run metadata and group summary show:

- 1,592 unique primary breakout events (932 BROAD_P40; 660 nested STRICT_P25).
- 6,368 event/horizon rows across 15M, 1H, 4H and 12H.
- 6,368/6,368 archived comparisons passed, checking 18 fields per row.
- The four horizons each cover all 1,592 events; 1,592 complete and zero censored at each horizon.
- 244 group-summary rows (61 groups per horizon).
- 454 overlap clusters.
- Five lifecycle retest fields remain unavailable in the frozen historical forward-outcome archive and are descriptive only, without an independent archived cross-check.

The archived run is descriptive research only. It does not test orders, fills, fees, funding, PnL or profitability.

## Timing issue found during independent code review

The frozen V1.1 amendment requires the first completed 15-minute close **strictly after** the retest candle. The helper `_first_15m_close_after` previously selected a close timestamp greater than or equal to the 1-minute candle's close timestamp. If both timestamps were equal (for example, a retest in the final minute of a 15-minute bar), it could treat a simultaneous close as a post-retest hold.

The implementation is corrected to require a strictly later 15-minute close, and a regression test covers the equality boundary. This aligns implementation with the already-frozen amendment; it does not change the research definition or retest distance.

## Remaining review gates

- Re-run the complete synthetic suite and historical workflow after the correction.
- Review event-level output contract, row counts, timing fields, ambiguity handling and summary consistency.
- Retain the explicit limitation that the five retest fields lack an independent archived historical benchmark.
- Do not close Module B or Gate 1 until independent review is complete and the project register is reconciled.
