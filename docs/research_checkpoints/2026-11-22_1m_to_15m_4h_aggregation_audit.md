# 2026-11-22 Independent 1M-to-15M/4H OHLCV Aggregation Audit

Status: **PASS — all 10 asset/timeframe comparisons passed.**

## Method
For BTC, ETH, SOL, DOGE, and AVAX, the 1M source files were independently resampled into 15M and 4H buckets:
- Epoch origin
- Left-labeled
- Left-closed
- OHLCV aggregation: first open, maximum high, minimum low, last close, summed volume
- Only buckets with exactly 15 or 240 constituent 1M candles were retained as complete.

The rebuilt candles were compared against the supplied 15M and 4H files by timestamp and by each OHLCV field.

## Results

Each asset had:
- 37,941 rebuilt complete 15M buckets and 37,941 supplied 15M candles.
- 2,370 rebuilt complete 4H buckets and 2,370 supplied 4H candles.
- Zero missing timestamps and zero extra timestamps for both timeframes.
- Zero mismatches in open, high, low, close, or volume for both timeframes.

| Asset | 15M | 4H |
|---|---|---|
| BTC | PASS | PASS |
| ETH | PASS | PASS |
| SOL | PASS | PASS |
| DOGE | PASS | PASS |
| AVAX | PASS | PASS |

Total comparisons: 10. Passed: 10. Investigations required: 0.

## Interpretation
The supplied 15M and 4H OHLCV histories are exactly reproducible from the corresponding 1M source histories using the tested epoch-anchored, left-labeled, left-closed aggregation convention, over every complete bucket represented in the supplied higher-timeframe files.

This establishes cross-timeframe candle consistency for these files. It does not independently establish cross-asset timestamp alignment, detector correctness, event reconstruction correctness, outcome formula correctness, or strategy profitability.

## Next research stage
Proceed to an independently implemented and auditable reconstruction of the sideways boundary snapshots, 15M test numbering, strong rejection events, and post-rejection outcomes. Preserve the provisional November 22 report; do not overwrite it. Audit formulas and intermediate event-level records before interpreting findings.
