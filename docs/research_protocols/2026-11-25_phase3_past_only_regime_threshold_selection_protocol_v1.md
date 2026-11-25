# Phase 3 Past-Only Regime Threshold Selection Protocol V1

**Date:** 2026-11-25  
**Project:** OKX Price Action V1 — Phase 3 Sideways / Range  
**Status:** PRE-REGISTERED EXPLORATORY PROTOCOL — threshold selection is not yet authorized; no candidate generation or PnL simulation.  
**Governance:** `docs/RESEARCH_GOVERNANCE_RULES_V1.md`  
**Prior diagnostic:** `docs/research_checkpoints/2026-11-25_phase3_past_only_regime_threshold_diagnostic_v1.md`

## 1. Research question

Which past-only channel-width threshold policy can define a live-knowable range-width filter for Phase 3 without using future observations, while retaining a clearly documented warm-up, update schedule and asset-specific calibration?

This protocol compares calibration mechanics only. It does not test whether any regime label predicts price movement or produces a tradable edge.

## 2. Hypotheses and competing explanations

- **H1 — Fixed calibration:** a threshold estimated from an initial completed calibration window is easiest to audit and operationally stable, but may become stale as volatility changes.
- **H2 — Expanding prior history:** thresholds use all prior completed snapshots and should be relatively stable, but may adapt slowly to structural changes.
- **H3 — Rolling prior history:** thresholds use a fixed recent history and should adapt faster, but may fluctuate more and cause regime-label turnover.

No hypothesis is presumed superior. The preliminary 180-snapshot comparison is exploratory and cannot itself select a policy.

## 3. Population and source data

Use the five existing asset-specific 4H feature ledgers, without modifying them:

- `reports/sideways_detector_original_v1/BTC_features_original_v1.csv`
- `reports/sideways_detector_original_v1/ETH_features_original_v1.csv`
- `reports/sideways_detector_original_v1/SOL_features_original_v1.csv`
- `reports/sideways_detector_original_v1/DOGE_features_original_v1.csv`
- `reports/sideways_detector_original_v1/AVAX_features_original_v1.csv`

Required fields include asset, snapshot availability timestamp, channel width, directional efficiency, mean overlap, and frozen channel bounds. Preserve the original per-asset calibration convention. Do not pool assets or change the historical feature definitions in this study.

The study must verify unique and strictly increasing availability timestamps per asset, finite feature values, and the expected four-hour snapshot cadence. It must stop on missing/duplicate timestamps rather than silently bridge gaps. Each threshold at time t may use only rows whose availability timestamp is strictly earlier than t.

## 4. Candidate policies to compare

All policies are asset-specific and use linear-interpolated quantiles, consistent with the historical archive. Use a common initial warm-up of 180 completed 4H snapshots (30 days) for the first mechanical comparison. The warm-up is a comparison setting, not a selected production parameter.

1. **Fixed-180 calibration:** calculate P25 and P40 once from the first 180 completed snapshots; freeze those values for all later snapshots.
2. **Expanding-prior:** after the first 180 snapshots, calculate P25 and P40 from every prior completed snapshot, excluding the current row.
3. **Rolling-180:** after the first 180 snapshots, calculate P25 and P40 from only the immediately preceding 180 completed snapshots, excluding the current row.

Retain the existing full-sample P25/P40 values only as a clearly labelled retrospective leakage reference. They must never be treated as a live policy or used to generate candidates.

The descriptive regime filters remain unchanged for this mechanical comparison: strict width P25 or broad width P40, plus directional efficiency <= 0.30 and mean overlap >= 0.70. Strict and broad remain nested labels, not independent cohorts.

## 5. Measurements

For each asset and policy, report:

- first eligible timestamp and warm-up rows excluded;
- P25/P40 threshold time series: median, interquartile range, minimum and maximum;
- absolute and relative threshold changes per 4H update;
- robust dispersion (median absolute deviation) and normalized dispersion;
- width-only regime label transition counts/rates and median/maximum episode duration;
- strict/broad combined label transition counts/rates and eligible-row counts;
- the number and percentage of rows where the causal policy differs from the retrospective full-sample label, solely as a leakage-impact diagnostic;
- all missing, invalid, duplicate, cadence or non-finite rows and the exact stop reason.

Do not interpret higher or lower eligible-row counts as better. Do not rank policies using forward returns, MFE/MAE, breakout outcomes, rejection outcomes, trade PnL, win rate or any strategy-performance measure.

## 6. Event-eligibility mapping — separate descriptive reconciliation

Only after the feature-only diagnostic passes, map the time-varying threshold outputs to the existing source event records by exact asset and frozen snapshot identity:

- Rejection source: `reports/phase3_rejection_lifecycle_v1_1/rejection_lifecycle_events_v1.csv` and the accepted event-anatomy source.
- Breakout source: `reports/phase3_breakout_lifecycle_v1_1/breakout_lifecycle_events_v1_1.csv` and its prior-link provenance.

For each event, use the threshold value available at the source snapshot's own availability time, and separately verify that the boundary snapshot was available no later than the event confirmation/availability time and was still valid then. Preserve all original event IDs, family, side, boundary type, overlap-cluster identity, censoring and ambiguity flags.

Report family, asset, side and strict/broad event eligibility separately. Do not pool rejection, breakout continuation and failed-breakout reversal. Do not create or simulate candidate orders in this protocol. If the event ledgers cannot be mapped unambiguously to exact feature snapshot identities, stop and record the missing join evidence rather than infer a match.

## 7. Decision rules

A policy is ineligible if it violates the strict past-only timestamp rule, uses incomplete/unavailable snapshots, cannot be reproduced from immutable inputs, or silently bridges missing 4H observations.

Among policies that pass those controls:

- Do not choose a policy because its eligible-event count is larger or because its labels resemble the retrospective full-sample labels.
- Describe the operational trade-off: fixed = stable but non-adaptive; expanding = gradual adaptation; rolling = faster adaptation with potentially greater turnover.
- If the diagnostics do not establish a uniquely justified operational policy, retain the valid policies as named sensitivity variants and defer the production choice. Do not force a winner.
- Any later predictive or strategy evaluation requires its own frozen protocol and chronological development/validation/untouched-test design. The calibration policy must be fixed before the untouched test period is inspected.

## 8. Stopping rule and expected consequence

Stop after the feature-only diagnostics and event-eligibility reconciliation are reproducible and interpreted, or earlier if source identity/timestamp checks fail. Do not add more window lengths or percentile grids after seeing results. Any additional method requires a separate protocol amendment before execution.

The output should establish whether Phase 3 can define a causal regime threshold and quantify how that choice changes the eligible descriptive event population. It does not establish a trading edge.

## 9. Explicit exclusions

- No edits to original feature ledgers or retrospective outputs.
- No candidate generator, order simulation, fill assumptions, stop/target rules or PnL backtest.
- No threshold optimization against forward market outcomes.
- No parameter sweep beyond the three predeclared policies and the shared 180-snapshot warm-up.
- No change to Phase 3 family scope or the approved phase order.

**Current gate status:** G0-04 and G0-05 remain OPEN / CRITICAL. Gate 0 remains CONDITIONAL HOLD. Gate 2 and strategy backtesting remain closed.


## 10. Source-specific calibration amendment — mandatory

The detector feature ledgers and the recovered breakout pipeline are distinct source constructions. The three candidate policies in Sections 4–5 are first applied to the detector feature ledgers for the rejection source chain. Their numerical thresholds must not be copied into breakout events without an independent source reconstruction.

### Rejection pipeline
- Preserve the exact feature-ledger identity and the existing event-to-feature join by asset and `snapshot_index`.
- Verify `snapshot_available_at_ts_ms` and `snapshot_next_available_at_ts_ms` against the exact feature row and next feature row.
- Calculate the past-only threshold from the prior completed detector feature snapshots, strictly before the event's snapshot availability timestamp.

### Breakout pipeline
- Reconstruct complete 4H bars from the exact canonical common 1M source hashes recorded in the accepted breakout metadata.
- Reproduce the recovered source's lagged 12-completed-4H-candle context and its backward as-of join to complete, right-labelled 15M bars. Verify that the event's `snapshot` is the right-labelled context timestamp and is no later than the breakout signal close timestamp.
- The accepted historical P25/P40 values were calculated over the joined 15M channel-width series. That full-sample population is retrospective. The follow-up must separately compare two clearly specified past-only populations: (a) unique completed 4H context snapshots, and (b) the exact joined 15M rows. Do not assume they are interchangeable, even if complete 15M coverage often repeats each 4H context value uniformly.
- For any event, its threshold must use only observations available strictly before the signal's own context snapshot timestamp, or an explicitly justified same-snapshot availability convention frozen before running the diagnostic. Do not include later 15M rows from the same 4H context period.
- Compare the reconstructed breakout 4H context values/timestamps with the detector feature ledgers. Any offset, value difference or source mismatch must be reported; do not force an approximate join.

### Family scope
- Rejection and breakout calibration results remain separate.
- Failed-breakout reversal inherits the source breakout's regime context and therefore cannot be assigned a separate threshold until the breakout source context is causally verified.
- If the source-specific reconstruction or exact event-to-snapshot join fails, stop that family and record the blocker. Do not generate candidates.


### Expected timestamp relationship to the detector feature ledger

The recovered breakout implementation labels 4H bars on their right edge and applies a one-row shift to the rolling 12-candle channel. Consequently, its context row labelled at time **T** uses the prior 12 completed 4H candles and corresponds to the detector feature-ledger row whose `available_at_ts_ms` is **T − 4 hours**. The expected cross-pipeline mapping is therefore:

`breakout_context_snapshot_ts_ms = detector_feature_available_at_ts_ms + 14,400,000`

This is a source-code-derived expected offset, not permission to force a join. The follow-up must verify the exact asset, upper/lower values, width formula and timestamp relation against reconstructed 1M-derived bars. Any mismatch beyond documented numeric tolerance, missing snapshot, or source-hash discrepancy is a stop condition. Do not mistake this deliberate one-4H context lag for a data error, and do not remove it to make the pipelines appear aligned.


### Existing breakout-ledger coverage limitation and full-population requirement

The 1,592 accepted lifecycle rows were successfully matched to detector feature rows using the expected four-hour offset, with exact upper/lower boundary and width equality for every row. However, these rows contain only 932 unique signal keys because the 660 strict-labelled records are nested duplicates of signals also present in the 932 broad-labelled records.

Those 932 unique signals were originally selected using retrospective full-sample P25/P40 filters. Reclassifying them under past-only thresholds is a useful provenance/sensitivity check, but it cannot recover signals that the retrospective filter excluded. It is not a complete causal breakout cohort.

Before G0-04/G0-05 can close, rebuild the full completed-15M breakout signal population from the canonical common 1M source, apply the predeclared past-only regime threshold at each context snapshot, and preserve unique event identity independently of strict/broad labels. Reconcile the resulting full population against the 932 previously archived unique signals, reporting newly eligible, no-longer-eligible, unchanged and source-excluded signals separately. Never infer the complete new event universe from the selected historical ledger alone.
