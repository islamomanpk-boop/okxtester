# Forward Rejection Outcome Study V1 — Initial Results Checkpoint

Date: 2026-11-23
Branch: `price-action-v1`
Status: **Full historical run completed; initial aggregate results reviewed. Descriptive only; no trading edge or profitability established.**

## Execution and integrity

The user ran:

```bash
python research/sideways_rejection_forward_outcomes_v1.py
```

The script completed successfully and wrote:
- `reports/sideways_rejection_forward_outcomes_v1/event_level_outcomes.csv`
- `reports/sideways_rejection_forward_outcomes_v1/aggregate_summary.csv`
- `reports/sideways_rejection_forward_outcomes_v1/data_validation.csv`

Reconciled population:
- Broad: 1,154 first-strong-rejection events.
- Strict: 838 events, a contained subgroup of broad.
- Output rows: 1,992 because the two labelled cohorts are both represented; do not add or pool broad and strict as independent events.

Source validation across BTC, ETH, SOL, DOGE, AVAX:
- 569,125–569,127 1M rows per asset.
- Zero non-60-second gaps.
- 1,992/1,992 event rows had the exact confirmation-minute candle.
- Zero missing confirmation-minute rows.

Horizon coverage:
- Broad: 15m 1,154/1,154; 1h 1,154/1,154; 4h 1,154/1,154; 24h 1,146/1,154 (8 censored).
- Strict: 15m 838/838; 1h 838/838; 4h 838/838; 24h 836/838 (2 censored).
- Incomplete 24h observations are excluded from that horizon's return denominator.

## Overall aggregate results

Positive direction-adjusted return frequency and median direction-adjusted return:

| Cohort | Horizon | Complete | Positive frequency | Median adjusted return |
|---|---:|---:|---:|---:|
| Broad | 15m | 1,154 | 52.253% | +0.0160% |
| Broad | 1h | 1,154 | 51.127% | +0.0152% |
| Broad | 4h | 1,154 | 52.166% | +0.0451% |
| Broad | 24h | 1,146 | 52.356% | +0.1447% |
| Strict | 15m | 838 | 51.671% | +0.0134% |
| Strict | 1h | 838 | 49.761% | 0.0000% |
| Strict | 4h | 838 | 52.029% | +0.0429% |
| Strict | 24h | 836 | 54.426% | +0.2129% |

## Directional asymmetry — broad cohort

Upper rejection (expected down):
- Positive adjusted frequency: 54.362% (15m), 52.685% (1h), 55.872% (4h), 57.383% (24h).
- Median adjusted return: +0.0260%, +0.0327%, +0.1022%, +0.2898% respectively.

Lower rejection (expected up):
- Positive adjusted frequency: 50.000% (15m), 49.462% (1h), 48.208% (4h), 46.909% (24h).
- Median adjusted return: +0.0005%, 0.0000%, -0.0213%, -0.1269% respectively.

## Directional asymmetry — strict subgroup

Upper rejection:
- Positive adjusted frequency: 53.846% (15m), 51.810% (1h), 55.430% (4h), 60.181% (24h).
- Median adjusted return: +0.0220%, +0.0242%, +0.0732%, +0.3674%.

Lower rejection:
- Positive adjusted frequency: 49.242% (15m), 47.475% (1h), 48.232% (4h), 47.970% (24h).
- Median adjusted return: 0.0000%, -0.0220%, -0.0116%, -0.0739%.

## Initial interpretation

The broad all-event aggregate is weak: positive direction-adjusted frequency is approximately 51–52% across horizons, with small median adjusted returns.

A directional asymmetry is visible in the supplied aggregate output:
- Upper-bound rejection outcomes are more directionally consistent than lower-bound rejection outcomes, particularly at 4h and 24h.
- Broad upper 24h: 57.383% positive frequency and +0.2898% median adjusted return.
- Broad lower 24h: 46.909% positive frequency and -0.1269% median adjusted return.
- The strict subgroup displays the same qualitative split.

This is a hypothesis for further investigation, not evidence of statistical significance, predictive probability, or a robust trading edge. The events may overlap and are not independent. No naive independent-event confidence intervals should be used. The event study excludes fees, spread, slippage, latency, funding, fills, position sizing, stop/target sequencing, and portfolio P&L. Excursions are path statistics, not realized trade returns. Broad and strict must not be pooled.

## Next validation step

Inspect the asset-by-direction aggregate rows and run additional event-level consistency checks before treating this as a finalized empirical result. In particular:
- Check the upper/lower split within each asset (to determine whether the pooled asymmetry is broadly distributed or concentrated in a few assets).
- Verify status counts, unique event identities within each cohort, and finite metrics for complete horizons.
- Keep the analysis descriptive and avoid optimizing definitions/horizons on these same observations.

The full event-level CSVs are local generated outputs; this checkpoint records the user-reported run and aggregate tables, not a claim that the generated CSVs have been uploaded to GitHub.


## Asset × direction review and event-level integrity

The user inspected all asset × direction × horizon rows and ran event-level integrity checks.

Event ledger checks:
- 1,992 total rows: 1,154 broad and 838 strict.
- Unique event IDs: 1,154 broad and 838 strict.
- Duplicate `(definition, event_id)` pairs: zero.
- For each horizon (15m, 1h, 4h, 24h), every complete row had all three metrics present: direction-adjusted return, favorable excursion, adverse excursion.
- Every incomplete row had a null direction-adjusted return.
- Complete row counts: 1,992 for 15m, 1,992 for 1h, 1,992 for 4h, 1,982 for 24h. The 10 remaining 24h rows are censored (8 broad, 2 strict).
- These checks passed. This establishes output consistency, not market predictiveness.

Asset-level 24h directional results (positive adjusted-return frequency; median adjusted return):

| Asset | Broad upper | Broad lower | Strict upper | Strict lower |
|---|---:|---:|---:|---:|
| BTC | 55.65%; +0.2105% | 41.35%; -0.2991% | 57.78%; +0.2884% | 38.03%; -0.3496% |
| ETH | 63.72%; +0.8000% | 49.02%; -0.0730% | 66.67%; +0.8906% | 55.41%; +0.1880% |
| SOL | 54.62%; +0.2362% | 48.78%; -0.0574% | 59.09%; +0.4572% | 51.76%; +0.1240% |
| DOGE | 59.13%; +0.2396% | 41.41%; -0.2421% | 58.89%; +0.2087% | 39.71%; -0.3328% |
| AVAX | 54.48%; +0.2582% | 52.46%; +0.0833% | 59.14%; +0.4650% | 52.08%; +0.0696% |

Interpretation refinement:
- The 24h upper-direction results are positive across all five assets in both cohorts, although their magnitude varies.
- Lower-direction results are substantially weaker and negative for BTC and DOGE in both cohorts.
- ETH, SOL, and AVAX lower-direction results are mixed; strict ETH/SOL lower results are positive at 24h. Therefore the pooled upper/lower asymmetry is not universal.
- At shorter horizons the asset-level picture is mixed; for example, upper results are not uniformly positive for AVAX at 15m/1h, and lower ETH can be positive at 1h/4h.
- Strict remains a nested subgroup of broad, not an independent replication. The repeated directional pattern across cohorts is a consistency check only.
- Do not infer significance from these raw frequencies. Events may overlap and cluster in time; asset samples are modest, and many asset/direction/horizon comparisons create multiple-testing risk.

## Updated next research step

Before any strategy or parameter selection, quantify uncertainty while respecting event dependence and overlap. A suitable next descriptive validation is a time-block or cluster bootstrap (with blocks long enough to preserve serial dependence and overlapping forward windows), reporting confidence intervals for upper-minus-lower differences by horizon and asset, with a predeclared primary comparison. Do not use naive IID event-level confidence intervals. Keep broad as the primary cohort and strict as a nested sensitivity cohort. No trading-cost or execution claim is yet supported.
