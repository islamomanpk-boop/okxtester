# Historical sideways detector local output audit — 2026-11-23

**Repository:** islamomanpk-boop/okxtester  
**Branch:** `price-action-v1`  
**Status:** PASS for consistency of the generated historical detector outputs against the documented reference values.  
**Evidence source:** Read-only Termux inspection of the existing `reports/sideways_detector_original_v1/` CSV outputs. No detector rerun was performed for this audit.

## Files present

The output directory contains:
- Per-asset feature CSVs for BTC, ETH, SOL, DOGE, and AVAX.
- Per-asset candidate-grid CSVs for all five assets.
- `detector_summary_original_v1.csv`.
- `all_candidate_grid_original_v1.csv`.
- `feature_distributions_original_v1.csv`.

## Summary validation

Each asset has 2,358 valid feature windows and zero overlap-missing windows.

| Asset | P25 width % | P40 width % | P50 width % | Strict P25 count | Broad P40 count |
|---|---:|---:|---:|---:|---:|
| BTC | 3.242203 | 3.947937 | 4.423343 | 401 | 601 |
| ETH | 4.245214 | 5.474563 | 6.218933 | 415 | 620 |
| SOL | 5.067174 | 6.114542 | 6.856281 | 409 | 607 |
| DOGE | 5.165724 | 6.264058 | 7.134351 | 407 | 606 |
| AVAX | 5.704868 | 6.916216 | 7.757650 | 430 | 624 |

The strict/broad definitions checked in the combined candidate grid are:
- Strict: width percentile 25, directional-efficiency maximum 0.30, mean-overlap minimum 0.70.
- Broad: width percentile 40, directional-efficiency maximum 0.30, mean-overlap minimum 0.70.

The combined candidate grid reproduces all ten strict/broad qualifying counts and the corresponding width thresholds exactly as shown in the detector summary. This independently cross-checks the summary against the candidate-grid output.

## Feature distribution inspection

The feature-distribution CSV contains the 0.10, 0.25, 0.40, 0.50, 0.60, 0.75, and 0.90 quantiles for:
- channel width percentage;
- directional efficiency;
- mean overlap.

The reported P25 and P40 channel-width quantiles agree with the summary thresholds for all five assets. No overlap-missing windows are reported in the summary.

## Conclusion and limits

**PASS:** The existing generated outputs are present and internally consistent across the detector summary, combined candidate grid, and feature-distribution report. The historical P25/P40 thresholds and strict/broad qualifying counts match the documented reference values.

This audit does not independently recompute feature values from source candles, retest detector formulas, or validate downstream 15M boundary/rejection event populations. It does not establish predictive value, profitability, or live safety. The full-sample width quantiles remain retrospective/exploratory rather than live-safe thresholds.

## Next research gate

Build a separately versioned, auditable historical-detector-to-15M boundary-event reconstruction. Preserve the existing detector outputs and all earlier event/outcome reports unchanged. Before calculating forward outcomes, validate causal 4H label availability, frozen channel boundaries, exact 15M continuity, first post-snapshot 15M suppression, strict non-touch separation, and first-strong-rejection event timestamps/counts. Do not reuse the earlier 2,095 event population without reconciliation.
