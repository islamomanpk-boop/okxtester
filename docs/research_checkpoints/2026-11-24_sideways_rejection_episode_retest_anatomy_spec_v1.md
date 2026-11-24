# Sideways Rejection Episode and Retest Anatomy V1 — Research Specification

**Date:** 2026-11-24  
**Repository:** `islamomanpk-boop/okxtester`  
**Branch:** `price-action-v1`  
**Status:** SPECIFICATION FROZEN BEFORE IMPLEMENTATION. No new measurements or outcomes are authorized by this document alone.

## 1. Purpose and research boundary

Describe what happens after a historically reconstructed sideways-channel boundary test records its first strong rejection:

- the anatomy of the 15-minute rejection candle;
- the subsequent 1-minute path relative to the frozen channel boundary;
- whether and when price revisits the boundary zone;
- whether and when price reaches a defined inward-separation level;
- the subsequent path relative to the rejection candle's own OHLC levels;
- differences by asset, boundary direction, strict/broad cohort, test rank, and chronological period.

This is a descriptive event/path study. It is not a strategy, signal-quality ranking, fill simulation, profitability test, or evidence of predictive power.

This study does not replace or redefine the accepted detector, boundary-test reconstruction, boundary interaction taxonomy, or rejection forward-outcome study. It does not attempt to complete the full range lifecycle taxonomy.

## 2. Accepted source population

Primary source event ledger:

`reports/sideways_boundary_events_historical_v1/boundary_tests_historical_v1.csv`

Use rows with non-null `first_strong_rejection_ts_ms` only.

Expected counts, which must be revalidated from the committed ledger before implementation:

- broad cohort: 1,154 rejection events;
- strict cohort: 838 rejection events;
- strict is a fully contained subset of broad; it is a separately reported subgroup, never an additive population.

Use the existing frozen detector feature files:

`reports/sideways_detector_original_v1/{ASSET}_features_original_v1.csv`

Join each event to its feature row by `asset` and zero-based `snapshot_index`. Recover `upper` and `lower` from that exact row. Do not recalculate channel bounds. Verify the event's snapshot availability and next-availability interval against the feature file and reconstruction protocol.

Use the five committed 1-minute source files:

`data/market_1m/{ASSET}_USDT_USDT_1m.csv`

Do not use the previous unreconciled 2,095-event cohort or its results.

## 3. Event identity, confirmation, and time zero

Preserve the event identity fields from the accepted ledger. The identity key is:

`asset, definition, direction, snapshot_index, segment_id, test_rank, test_start_ts_ms`

The ledger's `first_strong_rejection_ts_ms` is the OPEN timestamp of the 15-minute rejection candle. The candle becomes knowable only at its close.

Define:

`rejection_confirmed_at_ts_ms = first_strong_rejection_ts_ms + 900000`

This is time zero for all post-rejection measurements. The first eligible 1-minute bar must have timestamp exactly equal to this confirmation timestamp. Include that 1-minute bar and subsequent bars in forward windows. Never include any portion of the 15-minute rejection candle as post-confirmation data.

The 1-minute open at time zero is retained as a reference price only. It is not a verified executable entry or fill.

## 4. Frozen channel geometry and directional conventions

For each event, let:

- (U) = frozen upper channel boundary from its exact feature snapshot;
- (L) = frozen lower channel boundary;
- (W = U-L), required finite and strictly positive;
- (d = 0.10W), the existing boundary-touch band;
- (s = 0.20W), the existing inward-separation distance.

Do not modify these existing V1 geometric definitions.

Upper-bound rejection:
- expected inward direction is downward;
- boundary zone is price at or above (U-d);
- inward-separation line is (U-s).

Lower-bound rejection:
- expected inward direction is upward;
- boundary zone is price at or below (L+d);
- inward-separation line is (L+s).

The boundary zone is a geometric measurement, not an order price or executable limit.

## 5. Rejection-candle anatomy

Retain the original 15-minute rejection candle OHLC from the event ledger and calculate:

- absolute range: high minus low;
- body size: absolute close minus open;
- upper wick: high minus max(open, close);
- lower wick: min(open, close) minus low;
- body/range ratio;
- upper-wick/range ratio;
- lower-wick/range ratio;
- close location within candle range, scaled from 0 at low to 1 at high;
- range as a fraction of frozen channel width;
- body, upper wick, and lower wick as fractions of frozen channel width;
- signed close displacement from the relevant boundary, normalized by (W).

A zero-range candle must not produce division-by-zero values; ratios are null and the condition is counted in the audit. Preserve raw price fields and unrounded calculated values. Any display rounding belongs only in summaries.

Do not label a candle "strong", "weak", "good", or "profitable" beyond the source event's already-frozen strong-rejection definition.

## 6. Post-confirmation boundary path and first retest

Process exact 1-minute OHLC bars from confirmation time onward, with no gap bridging.

For each event, measure:

1. **First post-confirmation boundary-zone revisit.**
   - Upper event: first 1-minute bar whose high is at least (U-0.10W).
   - Lower event: first 1-minute bar whose low is at most (L+0.10W).
   - Record timestamp, elapsed minutes from confirmation, OHLC, and whether the same bar also closes back inward.
2. **First inward-separation close.**
   - Upper event: first 1-minute close at or below (U-0.20W).
   - Lower event: first 1-minute close at or above (L+0.20W).
   - Record timestamp, elapsed minutes, OHLC, and whether this occurred before or after the first boundary-zone revisit.
3. **First post-confirmation boundary penetration.**
   - Upper event: first high strictly above (U).
   - Lower event: first low strictly below (L).
   - Record timestamp, elapsed minutes, and penetration depth normalized by (W).
4. **Path extremes and location.**
   - maximum high and minimum low;
   - maximum inward excursion from the boundary;
   - maximum outward penetration beyond the boundary;
   - close-to-boundary distance at fixed horizons;
   - all distances normalized by (W), while retaining raw prices.

The first retest is a first-passage measurement. V1 does not count every repeated 1-minute touch as a separate independent retest episode. Consecutive bars at or inside the boundary zone must not be presented as multiple independent tests.

A bar may satisfy multiple OHLC conditions. Record all applicable conditions; do not infer intrabar ordering from OHLC. If a single bar both revisits the boundary zone and reaches the inward-separation line, classify the ordering as **same-bar ambiguous**, not retest-first or separation-first.

## 7. Rejection-candle price-level revisits

Measure first post-confirmation revisits to the rejection candle's own price levels, separately from channel-boundary retests:

- rejection candle high;
- rejection candle low;
- rejection candle open;
- rejection candle close.

A level is revisited when a subsequent 1-minute bar's range contains that price (low <= level <= high). For each level, record first timestamp, elapsed minutes, and the bar OHLC. Exact OHLC containment is a path-touch convention only; it does not establish a traded fill.

Do not merge these four level revisits into the channel-boundary retest metric. Do not infer the order of multiple level touches within the same 1-minute bar.

## 8. Fixed forward windows and censoring

Use fixed elapsed-time windows from confirmation:

- 15 minutes;
- 1 hour;
- 4 hours;
- 24 hours.

For each event and horizon, require every expected 1-minute timestamp exactly once, beginning at confirmation and ending at confirmation + horizon - 1 minute. The horizon endpoint price is the close of the final required bar.

If any required timestamp is missing, duplicated, irregular, or unavailable, mark that event/horizon incomplete with a specific censor reason. Do not interpolate, forward-fill, bridge gaps, or calculate partial-horizon metrics as if complete.

For each horizon, report:
- expected and observed bar counts;
- complete/incomplete status and censor reason;
- first retest and separation status/timing if observed within the complete window;
- path extremes and normalized excursions;
- end close and normalized location relative to (U), (L), and channel midpoint.

A first-passage event not observed in a complete window is reported as "not observed within horizon", not as proof that it can never occur.

## 9. Cohort and subgroup reporting

Report broad overall as the primary population. Report strict as a separately labelled nested subgroup.

Break down, where sample size permits:
- asset;
- upper versus lower boundary;
- first, second, third, and fourth-or-later test rank;
- chronological subperiod;
- strict versus broad (paired/nested comparison, not independent samples).

For every proportion, show numerator and denominator. For every time-to-event statistic, show the number of observed events and the number right-censored/incomplete. Provide medians and distribution quantiles, not means alone.

Events may overlap in time, strict is nested within broad, and upper/lower event paths can overlap. Do not use naive independent-event confidence intervals or treat rows as independent observations. If uncertainty intervals are later added, they require a separately reviewed dependence-aware method and explicit specification.

## 10. Required output artifacts

Write only to a new directory:

`reports/sideways_rejection_episode_retest_anatomy_v1/`

Required files:

1. `event_anatomy_v1.csv` — one row per source rejection event, source identity, frozen boundaries, rejection candle OHLC and anatomy metrics.
2. `event_path_outcomes_v1.csv` — one row per event/horizon, first-passage times/status, level revisits, path extremes, normalized metrics, censor fields.
3. `group_summary_v1.csv` — aggregate distributions and numerator/denominator counts by the declared cohort/group dimensions.
4. `data_validation_v1.csv` — per-asset input, timestamp, event join, horizon completeness, and invariant audit.
5. `run_metadata_v1.json` — source paths, source row counts, event counts, definitions, horizons, code version/hash if available, execution timestamp, and explicit limitations.
6. A Markdown results checkpoint under `docs/research_checkpoints/` after outputs pass audit.

Never overwrite an existing non-empty output directory. Never modify source candles, detector features, accepted event ledger, earlier outcome reports, or existing checkpoints.

## 11. Mandatory validation and acceptance gates

Before calculating metrics:

1. Confirm all five source 1-minute files and all five feature files exist and have the expected schemas.
2. Validate finite positive OHLC, valid high/low relationships, integer epoch timestamps, strict timestamp ordering, and uniqueness.
3. Reconcile broad and strict rejection event counts to 1,154 and 838 respectively; if counts differ, stop and investigate rather than silently adapting.
4. Validate unique event identity keys and allowed asset, definition, and direction values.
5. Validate every event joins to exactly one feature row using asset and snapshot_index.
6. Validate (U>L), finite positive (W), and the feature availability mapping against the source event snapshot.
7. Recompute confirmation timestamps and verify exact 1-minute confirmation bars exist where expected.
8. Verify no post-confirmation measurement uses a bar earlier than confirmation.
9. Test upper/lower direction symmetry, candle anatomy formulas, zero-range handling, boundary touch inequalities, strict penetration inequalities, first-passage timestamps, same-bar ambiguity, and price-level containment.
10. Test exact horizon boundaries, gap censoring, truncated-tail censoring, and no partial-horizon masquerading as complete.
11. Reconcile event counts through event-level outputs and aggregate numerators/denominators.
12. Ensure all outputs are newly created in the dedicated directory and prior files remain unchanged.

Any failed invariant blocks acceptance. Preserve failure logs and diagnose in a new version; do not silently patch prior outputs.

## 12. Unit tests required before full run

At minimum, include synthetic tests for:

- upper and lower rejection candle anatomy;
- normalized geometry and invalid/zero channel width;
- zero-range rejection candle;
- first boundary-zone revisit and no revisit;
- first inward-separation close;
- strict boundary penetration versus equality at the boundary;
- boundary retest and inward separation in the same 1-minute bar;
- rejection OHLC level containment;
- same-minute multiple level touches without inferred ordering;
- exact 15m, 1h, 4h, and 24h horizon boundaries;
- missing minute and truncated history censoring;
- no look-ahead before confirmation;
- overlapping event identities and nested cohort accounting;
- event-to-feature snapshot join integrity.

## 13. Explicit exclusions

V1 does not:
- alter or optimize detector thresholds, channel geometry, or source event definitions;
- create new rejection events or redefine strong rejection;
- infer intrabar tick sequence from OHLC;
- count each consecutive boundary-zone candle as an independent retest;
- infer order fills, spread, slippage, liquidity, fees, funding, or executable prices;
- calculate trade P&L, win rate, expectancy, or strategy profitability;
- claim predictive probabilities, causal effects, or a tradable edge;
- complete the broader range lifecycle, breakout-failure, or matched-control research gates.

## 14. Implementation sequence

1. Implement the frozen calculations and synthetic unit tests only.
2. Run tests and inspect code/output schema without running the historical study.
3. Review the implementation against this specification and the accepted source protocols.
4. Only after implementation review passes, run the five-asset historical study to a fresh output directory.
5. Independently audit event counts, joins, timestamps, censoring, and summary reconciliation.
6. Commit outputs and a results checkpoint only after all acceptance gates pass.

**Research interpretation rule:** A retest frequency or post-rejection path distribution is a historical description of this selected event population. It is not a probability of future market behaviour and must not be interpreted as a trading edge.
