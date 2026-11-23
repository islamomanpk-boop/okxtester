# Historical Sideways Detector Reproduction — Build Checkpoint

Date: 2026-11-23
Branch: `price-action-v1`
Status: **Specification and separate implementation committed; local execution and historical numerical reconciliation pending.**

## Recovery findings

The historical research documents were recovered and inspected:
- `docs/research/sideways_market_identification_methodology_v1.md`
- `docs/research/sideways_feature_distributions_48h_v1.md`
- `docs/research/sideways_candidate_joint_frequencies_v1.md`
- `docs/research/sideways_24h_48h_72h_horizon_comparison_v1.md`
- `docs/research/sideways_48h_rolling_label_persistence_v1.md`

The repository's `research/` directory contained the reconstructed V1 script but no historical feature-generation script. Therefore, this is a separate formula-level reproduction from documented methods and result tables, not recovery of the original Python source.

## Recovered 48H historical definitions

- Channel envelope: 12 completed 4H candles.
- Width: `(rolling_max_high / rolling_min_low - 1) * 100`.
- Directional efficiency: 12 close-to-close changes, requiring 13 closes.
- Adjacent overlap: intersection divided by the smaller candle range; clip to [0,1].
- Zero smaller-range pairs: missing, excluded from the mean.
- 11 adjacent pairs in the 12-candle channel window.
- Full-sample per-asset width quantiles; P25 strict and P40 broad retained candidates.
- ER ceiling 0.30 and mean overlap floor 0.70 for the retained strict/broad candidates.

The historical 2,358-row count from 2,370 source candles reconciles with the 13-close ER requirement: the channel/overlap window uses candles i-11 through i, while ER uses closes i-12 through i.

## New separate files committed

1. Specification:
   `docs/research_checkpoints/2026-11-23_historical_sideways_detector_reproduction_spec_v1.md`
   Commit: `1df0cae`

2. Implementation:
   `research/sideways_detector_original_v1.py`
   Commit: `81a230b`

3. Tests:
   `tests/test_sideways_detector_original_v1.py`
   Initial commit: `4df820d`
   Missing-overlap edge-case strengthening: `a81e8bb`

The reconstructed implementation `research/sideways_detector_v1.py`, its tests, specification, and existing reports were not modified.

## Historical numerical targets

For 2,358 feature rows per asset, compare the reproduced run against the saved historical reports:

| Asset | P25 width % | P40 width % | P50 width % | Strict count | Broad count |
|---|---:|---:|---:|---:|---:|
| BTC | 3.242 | 3.948 | 4.423 | 401 | 601 |
| ETH | 4.245 | 5.475 | 6.219 | 415 | 620 |
| SOL | 5.067 | 6.115 | 6.856 | 409 | 607 |
| DOGE | 5.166 | 6.264 | 7.134 | 407 | 606 |
| AVAX | 5.705 | 6.916 | 7.758 | 430 | 624 |

These are acceptance targets, not results of the new reproduction run.

## Explicit unresolved points

- Original quantile interpolation method was not preserved. The new script uses linear interpolation as a stated reproduction assumption and prints comparisons against the rounded historical reference thresholds.
- The historical documents do not define zero-path ER; the script uses ER=0 as a defensive convention.
- If all 11 overlap pairs are missing, the script returns NaN and that row cannot pass the overlap threshold.
- Exact original script and original external research bibliography have not been recovered.

## Next action

User should pull the new commits on Termux, run the unit tests, then run the historical detector against existing validated 4H files. Review all threshold/count comparisons and feature distributions. Do not accept the reproduction or continue downstream event analysis until discrepancies are understood.

Suggested local commands are provided in the next assistant message. No local CSV outputs have yet been created by this new historical reproduction.
