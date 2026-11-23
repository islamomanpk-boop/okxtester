# Rejection Forward-Outcome Block Bootstrap Plan V1

Date: 2026-11-23
Branch: `price-action-v1`
Status: **Analysis plan frozen before bootstrap calculation. No bootstrap results calculated yet.**

## Purpose

Estimate uncertainty in upper-versus-lower direction-adjusted forward outcomes while respecting temporal clustering, overlapping events, and cross-asset market co-movement. This is an uncertainty analysis of the existing descriptive event study, not a trading backtest.

## Frozen population and data

- Input: local `reports/sideways_rejection_forward_outcomes_v1/event_level_outcomes.csv`.
- Primary cohort: `definition == broad` (1,154 events).
- Sensitivity cohort: `definition == strict` (838 events), analysed separately. Strict is nested in broad and is not an independent replication.
- No changes to event definitions, event timestamps, entry convention, horizon definitions, or outcome metrics.
- For each horizon, use only rows with status `complete` and a finite direction-adjusted return. Censored rows are excluded from that horizon's statistic.
- Time key: UTC calendar day derived from `rejection_confirmed_at_ts_ms`.

## Primary estimand

The predeclared primary comparison is the **24-hour difference in arithmetic mean direction-adjusted return**:

`mean(upper) - mean(lower)`

within the broad cohort, in percentage points when displayed. Positive values favour the expected direction after upper rejections relative to lower rejections.

The mean difference is primary because it is an additive, directly interpretable contrast and can be recomputed under each resampled calendar-block population. Median differences are secondary descriptive statistics, not substituted for the primary estimand after seeing results.

## Secondary analyses

- Repeat the upper-minus-lower mean contrast for 15m, 1h, and 4h.
- Repeat by asset for all four horizons, with broad as the principal per-asset analysis.
- Report strict-cohort results separately as sensitivity only.
- Report sample counts and censored counts alongside every contrast.
- Asset-level and non-primary-horizon intervals are exploratory; no claim of family-wise significance will be made.

## Resampling method

Use a **synchronous moving calendar-block bootstrap**:
1. Construct the complete UTC calendar-day index from the earliest to latest event confirmation day, including days with no events.
2. Keep all assets and both directions attached to their original calendar days.
3. For each replicate, sample contiguous calendar blocks with replacement. Use one shared set of sampled date blocks for all assets, preserving contemporaneous cross-asset dependence within each block.
4. Concatenate sampled blocks and truncate to the original number of calendar days. Include all eligible event rows on each selected day; repeated sampled days repeat their event clusters.
5. Calculate the upper-minus-lower arithmetic mean contrast on the resampled event rows for each cohort/horizon/asset group.
6. Use 10,000 replicates and a fixed, documented random seed for reproducibility.
7. Report percentile 95% intervals (2.5th and 97.5th percentiles), point estimates from the original sample, and the number of valid replicates.

Primary block length: **7 calendar days**. Sensitivity block lengths: **3 and 14 calendar days**. Blocks are longer than the 24-hour maximum outcome horizon, reducing (but not eliminating) dependence across resampled block interiors. Differences across block lengths must be shown; conclusions that change materially are fragile.

## Interpretation and limitations

- This bootstrap is a practical dependence-aware approximation, not a guarantee that all serial dependence is captured.
- The finite historical sample may contain relatively few effectively independent time blocks; wide intervals are expected and informative.
- Events may cluster and overlap. Resampling event rows independently is prohibited.
- Broad and strict are not pooled. Strict results cannot be described as an independent replication.
- Per-asset and multi-horizon comparisons are exploratory and subject to multiple-comparison risk.
- Censoring at the dataset tail remains horizon-specific; no forward fill or imputation.
- No fees, spread, slippage, latency, funding, fills, stop/target sequencing, sizing, or portfolio P&L are introduced.
- A confidence interval excluding zero would still not establish a tradable edge or profitability.

## Implementation and validation requirements

- Create a separate script and output directory; do not overwrite existing study outputs.
- Validate required columns, allowed cohorts/directions/assets, timestamps, statuses, finite returns, and unique `(definition, event_id)` identities.
- Ensure the calendar-day grid includes empty days and block sampling is shared across assets.
- Record seed, replicate count, block lengths, horizon counts, point estimates, valid bootstrap counts, and percentile intervals.
- Add deterministic unit tests for block resampling, synchronized day selection, difference calculation, horizon censoring, and reproducibility.
- Compare original point estimates with independently recomputed raw-data contrasts before interpreting bootstrap intervals.
