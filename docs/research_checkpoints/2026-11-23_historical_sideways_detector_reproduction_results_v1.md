# Historical Sideways Detector V1 — Reproduction Results

**Date:** 2026-11-23  
**Branch:** `price-action-v1`  
**Status:** Formula-level reconstruction successfully matches all documented five-asset reference thresholds and candidate counts.

## Execution and tests

- Implementation: `research/sideways_detector_original_v1.py`
- Unit tests: `tests/test_sideways_detector_original_v1.py`
- Unit-test result: **16/16 passed**.
- Source data: 2,370 4H candles per asset.
- Feature alignment: 2,358 rows per asset (12-bar channel; 13 closes for 12 close-to-close changes).
- Assets: BTC, ETH, SOL, DOGE, AVAX.
- The run reported that no source market-data files were modified.
- Output directory: `reports/sideways_detector_original_v1/`

## Historical reference comparison

| Asset | P25 width reference (%) | Reproduced (%) | P40 width reference (%) | Reproduced (%) | Strict reference | Reproduced | Broad reference | Reproduced |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | 3.242 | 3.242203 | 3.948 | 3.947937 | 401 | 401 | 601 | 601 |
| ETH | 4.245 | 4.245214 | 5.475 | 5.474563 | 415 | 415 | 620 | 620 |
| SOL | 5.067 | 5.067174 | 6.115 | 6.114542 | 409 | 409 | 607 | 607 |
| DOGE | 5.166 | 5.165724 | 6.264 | 6.264058 | 407 | 407 | 606 | 606 |
| AVAX | 5.705 | 5.704868 | 6.916 | 6.916216 | 430 | 430 | 624 | 624 |

All ten P25/P40 width values agree with the original references to the three decimal places documented. All five strict and all five broad candidate counts match exactly.

## Reconstructed methodology

- 12-candle channel width: `(rolling_max_high / rolling_min_low - 1) * 100`.
- Directional efficiency: absolute net close change over the sum of 12 absolute close-to-close changes, requiring 13 closes.
- Adjacent candle overlap: intersection divided by the smaller candle range, clipped to [0, 1].
- Zero smaller-range pairs are missing and excluded from the mean; if all pairs are missing, the mean is missing.
- Historical thresholds use full-sample width quantiles; these are retrospective/exploratory and are not live-safe thresholds.
- Strict and broad candidate counts use the documented P25/P40 width thresholds and ER/overlap criteria.

## Interpretation and limitations

This is a successful **formula-level reconstruction** from the surviving research documentation. It is not proof that the exact original Python source has been recovered. The original quantile interpolation convention was not explicitly documented; the implementation uses linear interpolation, which matches the recorded rounded thresholds and candidate counts. The zero-path directional-efficiency convention is a defensive implementation choice where the historical documentation was silent.

Do not treat retrospective full-sample quantiles as deployable real-time thresholds. Any future live detector must use causal/rolling threshold estimation and separate validation.

## Next steps

1. Inspect the generated per-asset feature files, candidate grids, and summary outputs for consistency.
2. Preserve this historical reconstruction separately from the previously reconstructed detector V1, which uses different formulas.
3. Do not merge the two detector definitions or label the earlier reconstructed detector as the historical method.
4. Continue research only after reviewing the generated outputs and documenting any unresolved conventions.
