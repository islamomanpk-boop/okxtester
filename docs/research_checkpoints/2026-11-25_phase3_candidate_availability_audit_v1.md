# Phase 3 Candidate Availability and Source-Timing Audit V1

**Date:** 2026-11-25  
**Project:** OKX Price Action V1 — Phase 3 Sideways / Range  
**Purpose:** Read-only source and timestamp audit for Gate 0 G0-04 / G0-05  
**Status:** Findings recorded; candidate generation NOT authorized; no strategy or PnL simulation performed.

## 1. Decision summary

The accepted descriptive lifecycle studies contain useful source identities, frozen boundaries and event timestamps. The original breakout construction also contains a causally ordered 15-minute/4-hour join and a corrected 15-minute close-time convention.

However, the historical STRICT_P25 / BROAD_P40 regime labels use **full-sample channel-width quantiles** calculated over the complete feature sample. Those percentile thresholds are retrospective. They are not live-knowable thresholds at each historical event time. Therefore, the accepted descriptive event ledgers must not be passed directly into an executable Phase 3 candidate generator as though their regime labels were causal.

G0-04 and G0-05 remain **OPEN / CRITICAL**. The next requirement is a separately specified, past-only regime-threshold policy and a causal candidate contract covering all three Phase 3 families. No candidate generator or strategy backtest is authorized by this audit.

## 2. Support/resistance rejection source chain

### 2.1 Accepted historical source records

The rejection lifecycle uses:
- `reports/sideways_boundary_events_historical_v1/boundary_tests_historical_v1.csv`
- `reports/sideways_phase3_research_archive_v1/episode_retest_anatomy_v1/event_anatomy_v1.csv`
- `reports/sideways_detector_original_v1/{ASSET}_features_original_v1.csv`
- `data/market_1m/{ASSET}_USDT_USDT_1m.csv`

The boundary ledger retains asset, definition, upper/lower direction, snapshot index, snapshot availability and next-availability timestamps, segment/test identity, test start/end, first strong rejection timestamp and rejection OHLC where present. The anatomy ledger retains a stable event identity, frozen upper/lower boundaries, the rejection-candle fields and confirmation timestamp.

The accepted V1.1 specification states that `first_strong_rejection_ts_ms` is the **open timestamp** of the 15-minute rejection candle. That candle is not knowable at its open. Its close/availability time is:

`rejection_confirmed_at_ts_ms = first_strong_rejection_ts_ms + 900000`

This is the accepted descriptive lifecycle's time zero. The first eligible 1-minute bar begins at that confirmation timestamp. This prevents using any portion of the rejection candle as post-confirmation information.

### 2.2 Frozen boundary availability

The original detector feature builder forms each channel from 12 completed 4-hour candles. The feature row records:
- `channel_start_ts_ms`
- `channel_end_candle_ts_ms`
- `available_at_ts_ms = channel_end_candle_ts_ms + 4 hours`
- frozen `upper` and `lower`

The rejection lifecycle joins an event to the exact feature row by asset and snapshot index and checks the event's snapshot availability and next-availability values against that row. This is useful provenance for the historical boundary, but the candidate pipeline must still assert, per event, that the selected feature snapshot was available no later than the proposed signal availability and that the event lies within its declared snapshot-validity interval.

### 2.3 Critical retrospective threshold finding

In `research/sideways_detector_original_v1.py`, `classify_asset()` computes P25/P40/P50 thresholds using `np.quantile` over the complete `channel_width_pct` feature array for that asset. It then applies those thresholds to every historical feature row. The accepted strict and broad classifications inherit this full-sample percentile approach.

This is a look-ahead issue for live candidate generation: the threshold used at an early historical timestamp depends on later observations in the full sample. The accepted descriptive cohorts remain valid as historical descriptive cohorts under their frozen protocol, but they are not a causal regime signal. Before generating rejection candidates, the project must freeze a past-only threshold policy (for example, a separately calibrated fixed threshold or a predeclared expanding/rolling percentile based only on prior completed snapshots). No choice among these alternatives is made by this audit.

## 3. Breakout continuation source chain

The recovered original script `research/archive/final_timing_corrected_breakout_and_retest_recovered_original_2026-11-22.py` shows:

1. 15-minute bars are constructed only when all 15 one-minute candles are present, with `resample(label="right", closed="left")`. Their index is the **15-minute candle close time**.
2. 4-hour bars are constructed only when all 240 one-minute candles are present.
3. The 4-hour context uses the previous 12 completed 4-hour candles. Its channel and context fields are shifted so the current 4-hour candle is not included.
4. A backward as-of join attaches the most recently available 4-hour context to each 15-minute close timestamp.
5. Breakout conditions use the previous and current completed 15-minute closes crossing the frozen upper/lower boundary while the same snapshot remains active.
6. The corrected timing code identifies the final 1-minute candle inside the 15-minute signal bar at `signal_time - 1 minute`; the first post-signal 1-minute candle opens at `signal_time`. Since `signal_time` is the completed 15-minute close label, this first following minute is eligible at the signal's availability time, not before it.

This supports a causal timestamp interpretation for the breakout candle **conditional on** the 4-hour context and regime threshold themselves being live-knowable.

The same full-sample P25/P40 channel-width thresholds are calculated across the complete joined 15-minute sample. Therefore the historical STRICT_P25 / BROAD_P40 breakout classifications remain retrospective and cannot directly be treated as live candidate signals. A past-only regime threshold policy must be specified and independently audited first.

## 4. Failed-breakout reversal source chain

The accepted Module B descriptive output records:
- first 1-minute return-inside bar open and availability timestamp;
- first completed 15-minute return-inside close timestamp;
- later breakout-side reclaim close timestamp;
- outside/inside retest states and same-bar ambiguity flags.

For a future failed-breakout reversal candidate, the earliest defensible confirmation timestamp would be the **completed 15-minute return-inside close availability time**, with direction opposite the original breakout (failed upside break → short; failed downside break → long). This is a candidate-definition proposal only, not an accepted signal rule. The source breakout must itself pass the past-only regime-threshold and provenance requirements. Any same-bar or incomplete-bar ambiguity must remain explicit; no intraminute ordering may be inferred.

## 5. Minimum candidate-record contract to freeze later

Before implementation, the candidate protocol should require, at minimum:

- immutable `candidate_id` and immutable `source_event_id`;
- `family`: `SUPPORT_REJECTION`, `RESISTANCE_REJECTION`, `BREAKOUT_CONTINUATION`, or `FAILED_BREAKOUT_REVERSAL`;
- instrument ID, asset, direction/side, boundary side and regime definition/version;
- source snapshot ID, snapshot availability time, snapshot-validity interval, frozen upper/lower boundary and source hashes;
- signal candle open timestamp, candle close/availability timestamp and explicit confirmation rule;
- `signal_available_at_ts_ms` and `first_eligible_execution_bar_open_ts_ms`;
- past-only threshold/calibration version and the exact prior data window used to set it;
- original event/cohort definition, strict/broad nesting label and overlap-cluster identity;
- event de-clustering/repeated-signal policy, invalidation reference and expiry/censoring reason;
- source file Git blob IDs and SHA-256 manifest references.

The generator must reject missing source rows, duplicate event identities, non-monotonic or incomplete bars, a snapshot not yet available at signal time, a signal availability timestamp earlier than confirmation, and any first execution bar beginning before signal availability. It must never synthesize a fill or treat an OHLC touch as a fill.

## 6. Required decisions before G0-04 / G0-05 implementation

1. Freeze a past-only range-regime threshold method. Preserve the existing full-sample P25/P40 outputs as descriptive history; do not overwrite them.
2. Decide whether the live regime context is refreshed only on completed 4-hour snapshots, and freeze the exact 4-hour availability and validity interval.
3. Reconcile the raw 15-minute source files and their hashes with the committed 1-minute canonical market files. The current 15-minute raw source is described as local in the provenance checkpoint; do not assume it is identical to a resample of the tracked 1-minute data without verifying.
4. Freeze rejection candidate confirmation, repeated-event/de-clustering and invalidation semantics using the accepted Module A source identities.
5. Freeze breakout continuation signal availability and separate it from any retest-entry hypothesis.
6. Freeze failed-breakout reversal confirmation at completed 15-minute return-inside close, or reject/replace that proposal with a separately justified protocol.
7. Freeze asset/side/family output reconciliation and source-hash checks before implementation.

## 7. Explicit exclusions and current disposition

- This audit does not produce candidates, orders, fills, stops, targets, PnL or profitability results.
- The accepted descriptive Module A and Module B closeouts are not invalidated; their historical descriptive scope remains accepted.
- The full-sample P25/P40 thresholds are explicitly retrospective and must not be presented as live-calibrated.
- The three Phase 3 families remain separate; no pooling that hides a losing side or family is permitted.
- Gate 0 remains CONDITIONAL HOLD. G0-04 / G0-05 remain OPEN / CRITICAL. Gate 2 remains closed until Gate 0 is formally passed.
