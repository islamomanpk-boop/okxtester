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


## Additional same-bar ambiguity finding

A second review check found that an inside retest can begin with a failure-confirmation close already inside the boundary band. If the next 1-minute candle both closes beyond the inner edge (moving away) and its range also reaches back into the band, OHLC cannot establish whether the move-away preceded the touch. The prior implementation skipped this candle and could miss the ambiguity.

The state machine now records `SAME_BAR_AMBIGUOUS` for this case on both UPPER and LOWER directions. It does not count the ambiguous candle as a definite inside retest and does not assign a subsequent 15-minute hold result to it. Event and horizon outputs expose an explicit ambiguity flag. Synthetic tests cover both directions and preserve the separate move-away-then-later-retest case.

## Remaining review gates

- Re-run the complete synthetic suite and historical workflow after the correction.
- Review event-level output contract, row counts, timing fields, ambiguity handling and summary consistency.
- Retain the explicit limitation that the five retest fields lack an independent archived historical benchmark.
- Do not close Module B or Gate 1 until independent review is complete and the project register is reconciled.


## 2026-11-25 — Historical rerun and independent report review

The reporting amendment at `939dad6783c37b0638c24ea7cf27e5713b68beff` completed successfully in GitHub Actions run [45639123024](https://github.com/islamomanpk-boop/okxtester/actions/runs/45639123024). The workflow ran all 19 synthetic tests successfully, completed the frozen historical run, passed the archive contract, uploaded the seven-file artifact, and committed the generated reports as `fe176e98a95470659a387d3547d4999e8c14cb48`.

Verified run totals:
- 1,592 primary events (932 BROAD_P40 and 660 nested STRICT_P25).
- 1,537 prior-test links; 160 events have zero prior touch tests.
- 6,368 event/horizon rows; all 6,368 matched the frozen forward archive across 18 archived fields per row.
- 454 overlap clusters.
- 569,125 common 1-minute timestamps across the five assets; zero common-timeline gaps.
- Five lifecycle retest fields remain absent from the frozen forward archive and are not independently benchmarked.

Independent output review:
- Event CSV contains 1,592 rows; group-summary CSV contains 244 rows (61 group combinations for each of four horizons).
- Event-level 12H totals independently agree with the group-summary 12H totals: 107 outside-retest same-bar-ordering ambiguities, 551 inside-retest same-bar-ordering ambiguities, and 630 inside retests confirmed after separation.
- The group summary now has separate outside- and inside-retest ambiguity columns. Counts are horizon-scoped rather than copied unchanged across horizons; for example, the 15M/1H/4H outside ambiguity totals are 61/82/99, and the 15M/1H/4H inside ambiguity totals are 0/248/455.
- The code keeps same-bar ambiguity distinct from a confirmed retest. The inside-retest ambiguous state does not receive a hold status; the confirmed-after-separation state remains separate.
- The strict-later 15M close rule and both-direction same-bar ambiguity regression tests are present and passed in the 19-test run.

This confirms the reporting amendment and the stated count propagation. It does **not** constitute final Module B acceptance. Remaining independent closeout checks include horizon-level lifecycle timestamp/censor propagation, a full event-to-horizon consistency review, and reconciliation of this evidence into the project research register/control center. Keep Module B and Gate 1 open until those checks and the formal closeout are complete. No strategy simulation, orders, fills, fees, funding, PnL, or profitability inference was performed.
