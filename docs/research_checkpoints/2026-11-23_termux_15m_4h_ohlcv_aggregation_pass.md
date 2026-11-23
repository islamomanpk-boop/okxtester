# Termux 15M/4H OHLCV Aggregation Equivalence — 2026-11-23

**Project:** OKX Price Action V1  
**Branch:** `price-action-v1`  
**Status:** PASS for exact OHLCV aggregation equivalence against the available original 1M CSVs.  
**Scope:** Read-only comparison. No source or derived CSVs were modified.

## Method

For each of BTC, ETH, SOL, DOGE, and AVAX:

1. Loaded the original `~/okx_scalping_data/{ASSET}_USDT_USDT_1m.csv`.
2. Independently resampled 1M OHLCV to 15M and 4H using `closed="left"`, testing both `label="left"` and `label="right"`.
3. Retained only complete intervals containing exactly 15 or 240 one-minute observations, respectively.
4. Compared generated and existing timestamps, then compared all five OHLCV fields (open, high, low, close, volume) at common timestamps with `numpy.isclose(rtol=1e-9, atol=1e-9)`.

## Results

For every asset:

| Timeframe | Existing candles | Left-labelled common timestamps | Exact OHLCV matches | Maximum absolute difference |
|---|---:|---:|---:|---:|
| 15M | 37,941 | 37,941 | 37,941 | 0.0 |
| 4H | 2,370 | 2,370 | 2,370 | 0.0 |

The result is identical for BTC, ETH, SOL, DOGE, and AVAX. All five OHLCV fields match exactly for every compared candle.

The right-labelled alternative produced 37,940 common timestamps for 15M and 2,369 for 4H per asset, with zero matching rows under the timestamp intersection. Its large OHLCV differences confirm it is not the timestamp-label convention used by the existing files.

## Conclusion

The existing 15M and 4H files are exact OHLCV aggregations of the available original 1M source under left-closed, left-labelled resampling, over the complete intervals represented in the files.

Together with the previously recorded timestamp cadence audit, this verifies:
- no duplicate or missing interval steps within the observed 15M/4H ranges;
- exact common timestamps across the five assets within each timeframe;
- exact OHLCV equivalence to independently aggregated 1M source data;
- timestamp convention: `closed="left", label="left"`.

This does **not** by itself verify the original OKX instrument identity, raw-source provenance, volume-unit interpretation, funding lineage, breakout event-mask reproduction, or matched-control calculations.

## Next research gate

Use the verified left-labelled 15M/4H data and the original 1M data to reconstruct the accepted breakout event study. Before any matched-control candidate or outcome calculations, reproduce all 20 accepted asset/definition/direction event counts exactly. If any count differs, stop and investigate; do not proceed to matching or outcomes.
