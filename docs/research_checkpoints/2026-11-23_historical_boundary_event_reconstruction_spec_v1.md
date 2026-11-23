# Historical detector to 15M boundary-event reconstruction — implementation specification V1

**Date:** 2026-11-23  
**Status:** SPECIFICATION FROZEN FOR FIRST IMPLEMENTATION; event results NOT RUN.  
**Repository:** `islamomanpk-boop/okxtester`, branch `price-action-v1`

## Evidence inspected

The existing local `reports/sideways_detector_original_v1/` feature CSVs were inspected read-only for BTC, ETH, SOL, DOGE, and AVAX. Each contains 2,358 rows and the required fields:
- `channel_end_candle_ts_ms`, `available_at_ts_ms`
- `upper`, `lower`, `channel_width_pct`
- `directional_efficiency`, `mean_overlap`
- `width_p25_pct`, `width_p40_pct`

The 15M and 4H source CSV schemas for all five assets are `ts,open,high,low,close,vol`; `ts` is Unix milliseconds. 15M timestamps are on 900,000 ms intervals; 4H timestamps are on 14,400,000 ms intervals. Existing 1M-to-15M/4H aggregation audit passed previously; it is not repeated here.

## Cohorts

For each asset and each independent definition:
- strict: `channel_width_pct <= width_p25_pct`, `directional_efficiency <= 0.30`, `mean_overlap >= 0.70`
- broad: `channel_width_pct <= width_p40_pct`, `directional_efficiency <= 0.30`, `mean_overlap >= 0.70`

Strict and broad cohorts overlap and are not independent. Upper and lower direction cohorts can also overlap.

## Causal snapshot mapping

A feature row's 4H channel is not available at the 4H candle's opening timestamp. Its availability is `available_at_ts_ms`, equal to the final 4H candle start plus 4 hours. Freeze that row's upper/lower bounds only for 15M candles whose opening timestamps are at or after this availability and before the next feature snapshot's availability.

The first 15M candle at or after each new snapshot availability is suppressed. The first subsequent 15M candle is the first eligible candle. Never use a feature row before its availability. Do not forward-fill a missing 15M candle or bridge a timestamp gap.

## Boundary tests

Let `W = upper - lower`; require finite positive W.

- Upper touch: `high >= upper - 0.10 * W`.
- Lower touch: `low <= lower + 0.10 * W`.
- A test starts at the first eligible touch for that direction in the current snapshot/continuity segment.
- Further touches before separation remain in the same test.
- First strong upper rejection in a test: upper touch AND `close < upper - 0.10*W` AND `close > lower`.
- First strong lower rejection in a test: lower touch AND `close > lower + 0.10*W` AND `close < upper`.
- At most one first strong rejection is recorded per test.
- After an upper test, separation is confirmed only by a completed **non-touch** 15M candle with `close <= upper - 0.20*W`.
- After a lower test, separation is confirmed only by a completed **non-touch** 15M candle with `close >= lower + 0.20*W`.
- The separation candle arms the next test; it cannot also start that next test. A subsequent touch starts it.

Process upper and lower independently. Test ranks begin at one within each 4H snapshot/direction. A 15M timestamp gap ends the active test/segment and resets rank; never bridge it. A new 4H snapshot always resets test state and numbering.

## Required outputs and audit

Write only to a new directory, `reports/sideways_boundary_events_historical_v1/`; do not overwrite detector outputs or earlier event/outcome reports.

Produce:
- event/test-level CSV with asset, definition, direction, snapshot availability, segment, rank, test start/end, closure reason, first strong rejection timestamp and OHLC;
- summary CSV with counts by asset/definition/direction/rank (1, 2, 3, 4+), rejection numerator/denominator/rate, and snapshot test-count distribution;
- audit CSV or Markdown with source row counts, snapshot counts, suppressed first bars, eligible bars, 15M gaps, reset counts, and invariant results.

Acceptance checks must establish:
1. Feature availability and 4H snapshot timestamps are strictly ordered and 4H-spaced; 15M timestamps are strictly ordered.
2. Each 15M candle is assigned to at most one snapshot for a given asset.
3. No bar before feature availability is processed; first post-snapshot bar is suppressed.
4. No state is carried across snapshot changes or 15M gaps.
5. Every event starts on a qualifying touch; each rejection is on a qualifying touch and satisfies its direction's close condition.
6. At most one rejection per test; rank sequence has no duplicates within a segment.
7. Separation is confirmed by a completed non-touch candle meeting the 20% close distance; that candle does not start the next test.
8. All generated files are new and kept separate from prior reports.

## Limitations

Full-sample P25/P40 thresholds are retrospective/exploratory, not live-safe. This is descriptive event reconstruction only; no forward outcomes, fills, costs, funding, profitability, or predictive claims. Earlier 2,095 event cohort and provisional outcome run remain unreconciled and must not be reused as accepted results.