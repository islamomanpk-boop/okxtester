# Sideways Rejection Early-Path Sequence and Conditional Follow-Through V1 — Frozen Specification

**Date:** 2026-11-24  
**Repository:** `islamomanpk-boop/okxtester`  
**Branch:** `price-action-v1`  
**Status:** DESIGN FROZEN BEFORE IMPLEMENTATION. No new historical outcomes are authorized until implementation and synthetic tests are reviewed.

## 1. Purpose

Test whether the *sequence observed during the first 15 minutes after rejection confirmation* is descriptively associated with the subsequent path, using a strict temporal split between classification and outcomes.

The study follows the completed:
- Sideways boundary interaction taxonomy V1;
- Sideways rejection forward-outcome V1;
- Sideways rejection episode/retest anatomy V1.

It does not replace or modify any of them. It is not a matched-control design, strategy test, profitability analysis, or causal study.

## 2. Frozen source population and inputs

Use only:
- accepted source ledger: `reports/sideways_boundary_events_historical_v1/boundary_tests_historical_v1.csv`;
- frozen feature snapshots: `reports/sideways_detector_original_v1/{ASSET}_features_original_v1.csv`;
- original 1-minute candles: `data/market_1m/{ASSET}_USDT_USDT_1m.csv`.

Assets: BTC, ETH, SOL, DOGE, AVAX.

Eligible events must have non-null `first_strong_rejection_ts_ms`. Expected counts:
- broad: 1,154;
- strict: 838.

Strict is a nested subset of broad. Report it separately and never add it to broad.

Use exact feature snapshot joins by asset and zero-based `snapshot_index`. Verify frozen upper/lower bounds and feature availability intervals. Do not recalculate boundaries, change event labels, or use the prior unreconciled 2,095-event cohort.

## 3. Confirmation and temporal split

The source rejection timestamp is the OPEN timestamp of the 15-minute rejection candle.

Define:
`confirmation_ts_ms = first_strong_rejection_ts_ms + 900000`.

Require the exact 1-minute candle at confirmation.

### Classification window

Use exactly 15 consecutive 1-minute candles with opening timestamps:
`confirmation_ts_ms + k * 60000`, for k = 0 through 14.

The classification window ends at the close of the candle timestamped confirmation + 14 minutes, i.e. at confirmation + 15 minutes.

The confirmation-minute candle is included, consistent with the completed anatomy V1. A first touch stamped at elapsed 0 is a touch observed somewhere within that minute's OHLC bar, not proof of a touch at the exact confirmation instant.

If any of the 15 required bars is missing, duplicated, or irregular, classification is incomplete and the event is excluded from sequence-conditioned primary outcomes with an explicit reason. Never gap-bridge or partially classify.

### Outcome window

The first eligible outcome candle opens at:
`landmark_ts_ms = confirmation_ts_ms + 15 * 60000`.

No candle used for sequence classification may be reused in a forward outcome. Every future metric must use bars timestamped at or after this landmark.

Fixed future horizons, measured from the landmark:
- 1 hour: 60 consecutive 1-minute bars, from landmark through landmark + 59 minutes;
- 4 hours: 240 bars, from landmark through landmark + 239 minutes;
- 24 hours: 1,440 bars, from landmark through landmark + 1,439 minutes.

The horizon close is the close of the final required bar. If any required timestamp is absent, the relevant horizon is censored; do not interpolate, forward-fill, bridge gaps, or treat partial windows as complete.

## 4. Frozen sequence classification

Reuse the exact V1 geometry:
- channel width W = upper - lower, finite and strictly positive;
- boundary-touch band = 10% of W;
- inward-separation distance = 20% of W.

Within the 15-bar classification window:

Upper-bound event:
- boundary-zone touch if any 1-minute high >= upper - 0.10W;
- inward separation if any 1-minute close <= upper - 0.20W.

Lower-bound event:
- boundary-zone touch if any 1-minute low <= lower + 0.10W;
- inward separation if any 1-minute close >= lower + 0.20W.

Find the first bar index satisfying each condition. Assign exactly one sequence class:
1. `RETEST_FIRST`: first retest exists and precedes first inward-separation close, or retest exists and separation is not observed within the window;
2. `SEPARATION_FIRST`: first inward-separation close precedes first retest, or separation exists and retest is not observed within the window;
3. `SAME_BAR_AMBIGUOUS`: both conditions first occur in the same 1-minute bar;
4. `NEITHER_WITHIN_15M`: neither condition occurs.

Do not infer intrabar order from OHLC. Same-bar cases remain ambiguous and are never arbitrarily assigned to either ordered class.

For every event retain:
- first retest and separation indices, timestamps, elapsed minutes and OHLC;
- sequence class;
- whether the first retest candle closes inward of the exact channel boundary;
- whether each condition was observed;
- classification bar count and completeness.

The retest-close-inward flag is a geometric close-location descriptor only. It is not a success label.

## 5. Future outcomes

For each complete post-landmark horizon calculate:

### Direction-relative channel path

For upper-bound events (expected inward direction down):
- maximum inward excursion = max(0, (upper - minimum future low) / W);
- maximum outward penetration = max(0, (maximum future high - upper) / W);
- terminal close inward distance = (upper - final close) / W;
- terminal close relative to midpoint, direction-adjusted = (midpoint - final close) / W.

For lower-bound events (expected inward direction up):
- maximum inward excursion = max(0, (maximum future high - lower) / W);
- maximum outward penetration = max(0, (lower - minimum future low) / W);
- terminal close inward distance = (final close - lower) / W;
- terminal close relative to midpoint, direction-adjusted = (final close - midpoint) / W.

Also preserve raw future max high, min low, final close, expected/observed bar counts, and horizon status.

### Future first passages

Within each post-landmark horizon separately record:
- first subsequent boundary-zone revisit using the same 10% band;
- first strict boundary penetration (high > upper for upper events; low < lower for lower events);
- elapsed minutes from the landmark and corresponding OHLC.

A first passage not observed in a complete horizon is "not observed within horizon", not proof it never occurs.

No P&L, win rate, executable fill, stop/target sequencing, fees, slippage, spread, funding, or liquidation metrics are authorized.

## 6. Required reporting

Primary population: broad cohort.

Sensitivity subgroup: strict cohort, separately labelled.

Report:
- sequence class counts and proportions, with numerators and denominators;
- classification completeness/exclusion reasons;
- class distributions by asset, boundary direction, test rank (1, 2, 3, 4+), and UTC confirmation month;
- for each class and future horizon: event count, complete/censored count, median and quartiles of inward excursion, outward penetration, terminal close inward distance, and direction-adjusted midpoint close;
- future retest and penetration first-passage frequencies with numerator/denominator and time-to-event quantiles;
- broad and strict results separately; no pooled broad+strict counts.

Small subgroup counts must be displayed and not hidden by aggregate averages. No independent-event confidence intervals or significance tests are permitted in V1 because events overlap and cohorts are nested.

## 7. Dependence and interpretation limits

- Events may overlap in time and repeated tests may share market paths.
- Strict is nested within broad.
- The same asset/date market shocks affect multiple events and assets.
- Sequence class is a post-confirmation observed state, not a randomized treatment.
- Class comparisons are descriptive conditional associations; they do not establish causal effects or predictive probabilities.
- The 15-minute classification split prevents reuse of the classification bars as forward outcomes, but does not eliminate event selection, overlapping-event dependence, or market-regime confounding.
- Minute OHLC cannot establish intrabar order, actual touch timing within a bar, or executable fills.
- The study cannot authorize a trading rule or strategy selection.

## 8. Required outputs

Create a new directory only:
`reports/sideways_rejection_early_path_sequence_followthrough_v1/`

Required files:
1. `event_sequence_v1.csv` — one row per eligible source event with event identity, frozen bounds, classification-window metrics and sequence class;
2. `event_followthrough_v1.csv` — one row per event/horizon with post-landmark path outcomes and censor fields;
3. `group_summary_v1.csv` — class/horizon aggregate metrics and subgroup counts;
4. `data_validation_v1.csv` — per-asset data, snapshot, event, classification, and horizon audits;
5. `run_metadata_v1.json` — source counts, definitions, timestamps, thresholds, horizons, implementation hash, and limitations;
6. a Markdown results checkpoint after independent audit.

Never overwrite a non-empty output directory or alter prior source files, studies, logs, or checkpoints.

## 9. Synthetic tests and acceptance gates

Before the historical run, test:
- upper/lower sequence symmetry;
- each of the four sequence classes;
- first-passage ordering and same-bar ambiguity;
- retest-only and separation-only cases;
- confirmation-minute inclusion and exact 15-minute classification boundary;
- no pre-confirmation candle use;
- no classification-window candle use in future outcomes;
- exact 1h/4h/24h outcome window boundaries from the landmark;
- missing classification bar exclusion;
- missing future minute horizon censoring;
- strict cohort nesting and event-key uniqueness;
- exact feature snapshot join and availability interval;
- raw and normalized outcome formulas;
- no zero/negative channel width and valid OHLC.

Acceptance must independently reconcile:
- eligible source events to 1,154 broad and 838 strict;
- event-sequence rows to complete plus excluded classifications;
- event-horizon rows to event count × 3 horizons;
- group numerators/denominators to event-level records;
- every outcome bar timestamp >= landmark;
- no horizon marked complete unless all required timestamps are present exactly once.

## 10. Implementation sequence

1. Implement calculations and synthetic tests only.
2. Run compilation and unit tests.
3. Review the code against this specification and the V1 results checkpoint.
4. Only after review passes, run the five-asset study to a fresh output directory.
5. Independently audit temporal separation, event counts, censoring, and summary reconciliation.
6. Commit outputs and results checkpoint only after all acceptance gates pass.

**Research rule:** The sequence classes are descriptive labels of the first 15 minutes after a selected rejection. Any later difference in path is conditional association only and must never be described as a causal or profitable edge.
