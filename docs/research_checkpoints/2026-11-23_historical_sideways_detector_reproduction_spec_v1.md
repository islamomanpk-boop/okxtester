# Historical Sideways Detector — Reproduction Specification V1

Date: 2026-11-23
Branch: `price-action-v1`
Status: **Recovered from historical research documents; implementation pending local data run and numerical reconciliation.**
Purpose: Reproduce the historical 48H feature calculations as documented, separately from `research/sideways_detector_v1.py`.

## 1. Source documents and evidence

This specification is based on:
- `docs/research/sideways_market_identification_methodology_v1.md`
- `docs/research/sideways_feature_distributions_48h_v1.md`
- `docs/research/sideways_candidate_joint_frequencies_v1.md`
- `docs/research/sideways_24h_48h_72h_horizon_comparison_v1.md`
- `docs/research/sideways_48h_rolling_label_persistence_v1.md`

The historical Python implementation was not found in the repository's `research/` directory. This is a formula-level reproduction from saved methodology and empirical result documents, not recovery of the original source code.

## 2. Window alignment recovered from documented counts

Each asset has 2,370 complete 4H candles and the historical 48H study reports 2,358 valid feature rows.

The documented feature definitions imply this alignment:
- Channel high/low and overlap: latest 12 completed 4H candles.
- Directional efficiency: latest 12 close-to-close changes, which requires 13 closes.
- For a feature row ending at 4H candle index `i` (zero-based), channel/overlap use candles `i-11 ... i`, while directional efficiency uses closes `i-12 ... i`.
- First valid row is therefore `i=12`; row count is `2370 - 12 = 2358`.
- New row advances by one 4H candle.
- Feature values become available only at the close of candle `i`.

This alignment reconciles the historical count of 2,358. It is intentionally different from reconstructed V1's 12 closes / 11 changes and 2,359 rows.

## 3. Historical feature formulas

### 3.1 Channel width

Over the 12-candle channel window:
- `upper = max(high)`
- `lower = min(low)`
- `channel_width_pct = (upper / lower - 1) * 100`

This formula is explicitly stated in the historical methodology and feature-distribution documents.

### 3.2 Directional efficiency

Over 12 consecutive close-to-close changes:
- `net = abs(close[i] - close[i-12])`
- `path = sum(abs(close[j] - close[j-1]))` for `j=i-11 ... i`
- `directional_efficiency = net / path`

The 12 increments use 13 closes. The historical documents do not explicitly specify the zero-path case; implementation should set ER to 0 when path is zero and document this defensive convention.

### 3.3 Adjacent-candle range overlap

For each of the 11 adjacent pairs inside the 12-candle channel window:
- `intersection = max(0, min(high_a, high_b) - max(low_a, low_b))`
- `denominator = min(high_a - low_a, high_b - low_b)`
- `pair_overlap = clip(intersection / denominator, 0, 1)`

If the smaller candle range is zero, that pair is treated as missing, as stated in the historical feature-distribution document. The rolling mean is taken over non-missing pair values. If all 11 pairs are missing, mean overlap is undefined (NaN) and cannot satisfy the overlap threshold.

This is not intersection-over-union. Reconstructed V1's IoU formula must remain unchanged and separate.

## 4. Historical thresholds and candidate definitions

For each asset separately, calculate full-sample channel-width quantiles over the 2,358 valid feature rows. These thresholds are retrospective/exploratory and not live-safe.

Historical reports give these 48H thresholds:

| Asset | P25 width % | P40 width % | P50 width % |
|---|---:|---:|---:|
| BTC | 3.242 | 3.948 | 4.423 |
| ETH | 4.245 | 5.475 | 6.219 |
| SOL | 5.067 | 6.115 | 6.856 |
| DOGE | 5.166 | 6.264 | 7.134 |
| AVAX | 5.705 | 6.916 | 7.758 |

The exact quantile interpolation method used in the original run is not preserved in the documents. Start with linear interpolation as a clearly marked reproduction assumption, then compare recomputed thresholds against the rounded reference values above. Do not claim exact historical reproduction unless all five asset thresholds round to the documented values (and other summary counts also reconcile).

The saved joint-frequency study evaluates width percentiles P25/P40/P50, ER ceilings 0.20/0.30/0.40, and overlap floors 0.50/0.60/0.70. The primary retained candidates are:
- STRICT_P25: width <= asset P25, ER <= 0.30, mean overlap >= 0.70.
- BROAD_P40: width <= asset P40, ER <= 0.30, mean overlap >= 0.70.

## 5. Historical numerical reference checks

For 48H:
- 2,370 complete 4H candles per asset.
- 2,358 valid rolling feature rows per asset.
- Reference P25/P40/P50 thresholds are listed in Section 4.
- Historical strict qualifying counts:
  - BTC 401; ETH 415; SOL 409; DOGE 407; AVAX 430.
- Historical broad qualifying counts:
  - BTC 601; ETH 620; SOL 607; DOGE 606; AVAX 624.
- Strict qualifying shares: 17.01%, 17.60%, 17.35%, 17.26%, 18.24%.
- Broad qualifying shares: 25.49%, 26.29%, 25.74%, 25.70%, 26.46%.

The joint-frequency document contains all 27 candidate combinations per asset and is the stronger comparison target than only the selected counts.

## 6. Implementation and audit requirements

Create a new, separate implementation, tests, and output directory:
- `research/sideways_detector_original_v1.py`
- `tests/test_sideways_detector_original_v1.py`
- `reports/sideways_detector_original_v1/`

Do not modify or overwrite reconstructed V1 files or reports.

Tests must cover:
- 12-bar channel extrema and exact width formula.
- 12-change ER requiring 13 closes.
- Zero path handling.
- Smaller-range overlap normalization.
- Disjoint, partial, nested, equal, and zero-width range pairs.
- Missing-pair mean behavior, including all-pairs-missing.
- 2,370 input candles produce 2,358 rows.
- First row's channel and ER use the documented distinct index ranges.
- Full-sample quantiles and all 27 candidate combinations.

Run both independent formula tests and data-level comparisons. Reconcile thresholds, feature distributions, joint counts, persistence counts, and episode metrics. Any mismatch must be reported and investigated, not tuned away.

## 7. Causality and research safeguards

- A 4H feature row is available only after its ending 4H candle closes.
- For downstream 15M analysis, apply the state only after that availability time; retain the predeclared exclusion of the first 15M candle at/immediately after the snapshot availability time.
- Full-sample P25/P40 labels are retrospective research labels, not live-safe classifications.
- Keep historical reproduction separate from reconstructed V1.
- Do not interpret detector labels or post-rejection MFE/MAE as strategy profitability.
- Do not proceed to new strategy testing or matched-control analysis on the basis of detector counts alone.
