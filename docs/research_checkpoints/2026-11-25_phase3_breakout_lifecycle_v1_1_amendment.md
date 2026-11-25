# Phase 3 Breakout Lifecycle V1.1 — Retest Geometry and Timing Amendment

**Date:** 2026-11-25  
**Parent protocol:** `docs/research_checkpoints/2026-11-25_phase3_boundary_lifecycle_closure_protocol_v1.md`  
**Applies to:** Module B — Breakout / failed-breakout lifecycle only.  
**Status:** Frozen before Module B implementation and historical outcome calculation.

## 1. Why this amendment is required

The independent source review found that two distinct “10%” values must not be confused:

1. The prior-test classification's primary `zone_pct_of_channel = 10.0` means 10% of frozen channel width. It is used to classify pre-breakout touch-test history.
2. The recovered original breakout script uses `RETEST_BAND_PCT = 0.10`, which means **0.10% of the frozen boundary price**, not 10% of channel width. It defines the post-breakout retest band.

The parent protocol's Module B retest formulas using 0.10 × channel width are therefore superseded by this amendment. No Module B implementation or new Module B outcomes have been run yet.

## 2. Immutable source and accepted primary population

Keep the original recovered source unchanged:
- `research/archive/final_timing_corrected_breakout_and_retest_recovered_original_2026-11-22.py`
- Git blob SHA: `95d2975947c449f3813d80ee7b12008db14f071f`
- Original source constant: `RETEST_BAND_PCT = 0.10`.

Use the prior-test classifications filtered to `zone_pct_of_channel = 10.0`:
- `reports/breakout_prior_test_count_v1/breakout_prior_test_classifications_v1.csv`
- `reports/breakout_prior_test_count_v1/breakout_prior_test_links_v1.csv`
- `reports/breakout_prior_test_count_v1/run_metadata.json`
- `reports/breakout_forward_outcome_v1/run_metadata.json` and accepted forward outcome CSV.

The primary population is **1,592 unique breakout events**:
- BROAD_P40: 932
- STRICT_P25: 660
- UPPER: 823
- LOWER: 769
- BTC 349, ETH 266, SOL 361, DOGE 276, AVAX 340.

Strict is nested within broad; these are not independent populations. The primary 10% prior-test classification keys are unique. The prior-test links are one-to-many, not one-to-one: 1,537 link rows represent 1,537 prior touch tests across 1,432 event keys; 160 events have zero prior touch tests. For every primary classification, the number of joined prior-test link rows must exactly equal `prior_touch_test_count` (sum 1,537); fail closed on any mismatch. Do not treat absent link rows as a missing event when the classification declares zero prior tests.

The existing forward-outcome archive contains 19,104 rows across three zone definitions and four horizons. Its primary 10% zone therefore has 1,592 × 4 = 6,368 event/horizon rows. This archive is context and a reproducibility check, not a substitute for the new lifecycle output.

## 3. Exact signal and 1-minute timing

The recovered original source explicitly:
- uses completed 15-minute candles labelled by their closing timestamps;
- finds the final 1-minute candle in the signal interval at `signal_time - 1 minute`;
- sets `start = signal_pos + 1`;
- therefore uses the first post-signal 1-minute candle opening exactly at `signal_time`.

Module B must preserve this convention. Verify every primary event has an exact 1-minute bar at `signal_time`; do not shift to a nearby timestamp. The first 1-minute bar's OPEN is the post-signal reference price for descriptive path calculations, but it is not a simulated fill.

Build subsequent 15-minute bars from exactly 15 consecutive 1-minute candles aligned to UTC quarter-hour boundaries:
- bar open timestamp (t);
- 1-minute opens at (t, t+1m, ldots, t+14m);
- 15-minute close/availability timestamp (t+15m);
- OHLC = first open, maximum high, minimum low, final close.
A 15-minute bar is valid only if all 15 component minutes exist and pass OHLC checks. The first post-signal 15-minute bar opens at `signal_time` and closes at `signal_time + 15 minutes`.

## 4. Post-breakout retest band — frozen formula

Let (B) be the frozen broken boundary price and (q = 0.10/100 = 0.001).

- `band_high = B * (1 + q)`
- `band_low = B * (1 - q)`

This is a ±0.10% band around boundary price. Do not substitute 0.10 × channel width, the prior-test 10%-of-channel zone, or any optimized distance.

### 4.1 Outside retest after breakout

For UPPER:
- Previous known completed close (initially the final 1-minute close of the signal candle, then the prior 1-minute close) must be strictly greater than `band_high`.
- Current 1-minute low must be less than or equal to `band_high`.
- `boundary_crossed` is true if current low is less than or equal to (B).

For LOWER:
- Previous known completed close must be strictly less than `band_low`.
- Current 1-minute high must be greater than or equal to `band_low`.
- `boundary_crossed` is true if current high is greater than or equal to (B).

If the first post-signal bar opens/prints back inside the band and there was no previous completed close beyond the outer band, record an immediate adverse/inside-band condition; do not mislabel it as an outside approach retest.

Retest depth must match the original source's percentage-of-boundary calculation:
- UPPER: `max(0, (B - current_low) / B * 100)`.
- LOWER: `max(0, (current_high - B) / B * 100)`.

Record first outside retest timestamp, elapsed minutes from signal, OHLC, depth, boundary-crossed flag, and whether the first completed 15-minute close after the retest remains beyond the boundary. The first completed 15-minute close after the retest must be strictly after the retest candle; do not use a partial bar or same-candle ordering.

### 4.2 One-minute return-inside

Keep the parent protocol definition:
- UPPER: first post-signal 1-minute close (le B).
- LOWER: first post-signal 1-minute close (ge B).

This is a descriptive first passage, not a completed-15-minute failed-breakout confirmation.

### 4.3 Completed 15-minute return-inside confirmation

Keep the parent protocol definition, using the exact 15-minute resampling rule in Section 3:
- UPPER: first completed post-signal 15-minute close (le B).
- LOWER: first completed post-signal 15-minute close (ge B).

The close timestamp is the failure-state availability timestamp. Do not use an intrabar wick or 1-minute close as a completed-15-minute confirmation.

### 4.4 Breakout-side reclaim

After the completed-15-minute return-inside confirmation:
- UPPER: first later completed 15-minute close (> B).
- LOWER: first later completed 15-minute close (< B).

Record reclaim timestamp and delay from failure confirmation. Do not infer reclaim from a wick.

### 4.5 Inside retest after failure

After the completed-15-minute return-inside confirmation, measure the first approach back toward the broken boundary from inside using the same ±0.10% boundary-price band.

For UPPER:
- Previous known completed close (initially the failure-confirmation 15-minute close, then the prior 1-minute close) must be strictly below `band_low`.
- Current 1-minute high must be greater than or equal to `band_low`.

For LOWER:
- Previous known completed close must be strictly above `band_high`.
- Current 1-minute low must be less than or equal to `band_high`.

If the failure-confirmation close is already within the ±0.10% band, record `ALREADY_IN_BAND_AT_FAILURE_CONFIRMATION`; do not call the first subsequent touch a retest from inside. Record retest depth relative to boundary price, whether the 1-minute candle crosses the boundary, and the next completed 15-minute close status.

## 5. Continuation and reversal path

Retain the parent protocol's 15m, 1h, 4h and 12h horizons, measured from the first post-signal 1-minute bar opening at `signal_time`. The full lifecycle observation limit is 12 hours.

For each horizon and event, record:
- complete/incomplete status and reason;
- breakout-direction maximum favourable excursion and maximum adverse excursion from the first post-signal 1-minute OPEN;
- maximum extension beyond the original boundary in raw price and as a percentage of channel width;
- first 1-minute return-inside and first completed-15-minute return-inside confirmation, if within the horizon;
- outside retest, depth, boundary-crossed flag and first completed-15-minute hold/failure status, if within the horizon;
- after failure confirmation, reversal-direction and breakout-direction excursions, times to extremes, inside retest and breakout-side reclaim.

For UPPER, reversal direction is downward; for LOWER, reversal direction is upward. Report directions separately. All values are descriptive path measurements, not trade returns or fills.

## 6. Overlap clustering and de-clustering

Assign deterministic interval-graph overlap clusters by asset across both definitions and both directions, using half-open observed windows:
- start = `signal_time`;
- end-exclusive = `signal_time + observed_bars_12h * 60000`, capped at 720 bars and stopped at first gap/source end.

Sort by signal time then immutable event ID. A new event joins the current cluster only if its start is strictly before the running cluster end; otherwise start a new cluster. Use stable per-asset cluster IDs, propagate them to event and horizon rows, and report cluster counts, largest cluster and size distribution. Do not discard or deduplicate source events. Strict remains nested within broad.

## 7. Additional acceptance checks

Before outcome calculations:
1. Reproduce all 20 original event counts and all 10 original P25/P40 thresholds from the immutable source; use the archived prior-test metadata/reproduction evidence.
2. Verify 1,592 unique primary classification keys.
3. Verify exact signal-time to first 1-minute bar mapping for every event.
4. Verify the one-to-many prior-test link count equals `prior_touch_test_count` for all 1,592 events (1,537 links total; 160 events with zero prior tests).
5. Verify frozen upper/lower/channel-width values are finite and consistent across classification, links, and original event reproduction.
6. Verify 1-minute source Git blob pins, 569,125 common timestamps, and zero gaps in all five assets.
7. Synthetic tests must cover UPPER/LOWER symmetry, exact band equality, outer-band approach from outside, immediate inside-band adverse entry, 1M return-inside, 15M confirmation timing, reclaim, inside retest, already-in-band status, incomplete 15M bars, same-bar ambiguity, horizon censoring, overlapping clusters, and no gap bridging.

Any failed source reproduction, link-count mismatch, timestamp mismatch, or data-hash mismatch is a hard stop. Preserve the existing forward-outcome archive unchanged.

## 8. Scope boundary

No entry/exit orders, fills, stops, targets, costs, funding, position sizing, PnL, profitability, causal, predictive or live-readiness claims are authorized. The output is descriptive lifecycle evidence for Gate 1 only.
