# Sideways Boundary Post-Rejection Outcome Run — Provisional Audit

**Date:** 2026-11-22  
**Branch:** `price-action-v1`  
**Status:** DESCRIPTIVE RUN COMPLETE; OUTCOME-CALCULATION AUDIT PENDING  
**Purpose:** Preserve the new repeated-boundary rejection follow-up run and its current audit state. This is a provisional checkpoint, not an accepted trading-edge finding.

## Scope and run summary

- Assets: BTC, ETH, SOL, DOGE, AVAX.
- Expected event cohorts: 20 (5 assets × broad/strict × upper/lower).
- Reconstructed rejection events: 2,095 cohort events.
- 15M-to-1M mapping failures: 0.
- Event cohort reproduction: PASS.
- Timing validation: PASS.
- Outcome rows: 10,465 across 15M, 1H, 4H, 12H, 24H.
- No source script or raw data was supplied in this checkpoint; the detailed outcome-generation code remains to be inspected.

The 2,095 count is a count across overlapping asset/definition/side cohorts, not necessarily 2,095 unique independent market episodes. Broad/strict overlap and repeated tests must not be added as unique observations.

## Outcome-row reconciliation

Expected rows before incomplete-window exclusion: 2,095 events × 5 horizons = 10,475. Observed rows: 10,465.

- 15M: 2,095 rows.
- 1H: 2,095 rows.
- 4H: 2,095 rows.
- 12H: 2,095 rows.
- 24H: 2,085 rows.

All ten excluded rows are in the 24H horizon:
- AVAX broad lower: 120 complete / 123 events (3 excluded).
- AVAX strict lower: 93 / 96 (3 excluded).
- BTC broad lower: 95 / 96 (1 excluded).
- DOGE broad lower: 121 / 123 (2 excluded).
- ETH broad lower: 102 / 103 (1 excluded).

All other cohorts have complete 24H rows. This reconciles the total to 10,465 under the stated complete-window exclusion rule. The exact code-level completeness predicate still requires inspection.

## Descriptive observations from the supplied output

- Upper rejection candles generally close lower within their candle range and show larger upper wicks; lower rejection candles generally close higher and show larger lower wicks. This describes candle anatomy, not forward predictive edge.
- Boundary retests are frequent in many longer-horizon cohorts, often around 85–96%; a retest alone does not establish a useful entry or invalidation level.
- Midpoint-reaching and directional net results vary by asset and side; no uniform cross-asset rejection response is evident.
- At 12H, first-test versus second-or-later comparisons are mixed. Later-test samples shown are small (commonly single digits to low twenties), so large median differences are unstable and hypothesis-generating only.
- The 0.25% continuation-first / pullback-first summary is horizon-dependent. `NEITHER` is substantial in many 15M cohorts and declines at longer horizons.
- `BOTH_SAME_MINUTE` appears in DOGE upper cohorts, with one event repeated across horizon summaries; it may represent the same underlying event rather than separate events. Verify against event-level records.

## First-test versus later-test comparison

The supplied comparison table reports 1H and 12H outcomes split into `FIRST` and `SECOND_PLUS`. The group counts reconcile with the displayed cohort sizes. Later-test groups are small, so the table does not support a general claim that repeated tests improve or weaken rejection outcomes.

Illustrative mixed 12H observations from the supplied table:
- AVAX strict upper: `SECOND_PLUS` median directional net +2.980% (n=8), versus +0.465% for `FIRST` (n=83).
- BTC strict upper: +0.111% (n=18), versus -0.149% (n=89).
- DOGE broad lower: -1.328% (n=14), versus +0.070% (n=109).
- ETH strict lower: -0.842% (n=7), versus +0.121% (n=68).
- SOL strict upper: -0.483% (n=7), versus +0.066% (n=81).

These are descriptive, dependent observations, not statistically established effects.

## Current validation status

### Passed / reconciled from supplied outputs
1. Event cohort reproduction reported PASS.
2. Timing validation reported PASS.
3. 15M-to-1M mapping failures: zero.
4. Outcome-row total reconciles exactly after excluding ten incomplete 24H windows.
5. First-test plus second-or-later counts reconcile with displayed cohort counts.
6. Continuation-first, pullback-first, `NEITHER`, and `BOTH_SAME_MINUTE` categories generally reconcile with horizon cohort totals.

### Still pending — outcome calculation audit
The outcome-construction code has not yet been supplied/reviewed. Inspect:
- Post-rejection candle selection and whether the entry candle is excluded from the forward path.
- Reference entry at next 1M candle open.
- Directional sign convention (upper rejection interpreted as short/down; lower as long/up).
- `net_directional`, MFE and MAE formulas and denominators.
- Threshold hit definitions and `time_*` timestamps.
- Continuation/pullback first-move classification and same-minute ambiguity handling.
- Complete-window predicate and exact reason for each excluded 24H event.
- Whether wick failure, boundary retest and midpoint measures use frozen event-time reference levels.

## Interpretation limits

1. These are descriptive historical price movements, not strategy profits.
2. The reference entry is the next 1M candle OPEN, not a verified fill.
3. Fees, spread, slippage, funding and execution are not modelled.
4. OHLC cannot reveal the exact order of high and low inside a 1M candle.
5. Same-minute continuation and pullback threshold hits are ambiguous.
6. Strict and broad groups overlap.
7. Repeated tests and overlapping horizons are not independent samples.
8. Incomplete horizon windows are excluded, not forward-filled.
9. Full-sample P25/P40 channel-width thresholds are retrospective and unsuitable as live thresholds without a causal recalibration.
10. No profitability or strategy-edge conclusion is supported at this stage.

## Next research steps

1. Complete the line-by-line audit of the outcome-generation block.
2. If formulas pass, preserve a validated outcome checkpoint and exact script/version provenance.
3. Then conduct a matched comparison of rejection events against non-rejection boundary touches, controlling for asset, side, volatility and sideways-channel context, using identical entry and horizon conventions.
4. Keep the older first-rejection-per-episode control study separate; its event definitions and matching procedure differ from this repeated-test run.

**Repository note:** This checkpoint records the output and audit status only. It does not claim that the local script or raw market data have been committed.