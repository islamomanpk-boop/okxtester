# Sideways Detector Version Status and Research Usage

Date: 2026-11-23
Branch: `price-action-v1`

## Current reference for historical 48H reproduction

Use `research/sideways_detector_original_v1.py` when reproducing the historical 48H sideways study documented in the repository's original research notes.

Its implementation is a formula-level reproduction from the saved methodology and empirical reference documents. It is **not recovery of the missing original Python source**.

Validation recorded in `docs/research_checkpoints/2026-11-23_historical_sideways_detector_reproduction_results_v1.md`:
- 16/16 unit tests passed.
- Each of the five assets produced 2,358 feature rows from 2,370 4H candles.
- All five assets' P25 and P40 width thresholds matched the historical references to three decimal places.
- Strict and broad qualifying counts matched the historical reference counts for all five assets.

The historical implementation uses:
- Channel width: `(rolling_max_high / rolling_min_low - 1) * 100`.
- Directional efficiency: 12 close-to-close changes, requiring 13 closes.
- Adjacent-candle overlap: intersection divided by the smaller candle range.
- A 2,358-row alignment for 2,370 input candles.

Its full-sample percentile thresholds are retrospective/exploratory and are **not live-safe**.

## Reconstructed detector V1 — superseded for historical reproduction

`research/sideways_detector_v1.py` and its associated specification, tests, and saved outputs are retained as historical research artifacts.

**Status: SUPERSEDED for reproducing the documented historical 48H study. Do not use it as the current historical-reference detector.**

It is intentionally not deleted. Its 8/8 tests show that its own specified formulas were implemented consistently; they do not prove that those formulas match the historical study.

Key differences from the historical formula-level reproduction:
- Width is normalized by channel midpoint rather than lower boundary.
- Directional efficiency uses 11 changes from 12 closes rather than 12 changes from 13 closes.
- Overlap uses intersection-over-union rather than intersection divided by the smaller candle range.
- It produces 2,359 rolling rows from 2,370 input candles rather than 2,358.

## Downstream research safeguard

Previously generated boundary-test, rejection, and post-rejection outcome results must not be assumed to match the historical detector merely because this detector's feature-level reference checks pass.

Before using historical-detector labels for downstream conclusions, rebuild or independently reconcile the timestamped 15M boundary tests, rejection events, and outcome rows against this detector. Preserve earlier datasets and reports as historical evidence; do not overwrite or delete them.

Neither detector's classifications or post-rejection outcomes establish strategy profitability or authorize live trading.
