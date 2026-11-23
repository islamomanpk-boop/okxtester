# Termux 15M/4H File Inventory Check — 2026-11-23

**Project:** OKX Price Action V1  
**Branch:** `price-action-v1`  
**Status:** File inventory/count check passed; timestamp coverage alignment remains open.  
**Scope:** Read-only inspection of existing files under `~/okx_adaptive_bot/data/`. No data or source files changed.

## Observed results

For each of BTC, ETH, SOL, DOGE, and AVAX:

- 15M CSV: 37,942 lines including header = **37,941 data candles**.
- 4H CSV: 2,371 lines including header = **2,370 data candles**.
- Both file types have columns `ts,open,high,low,close,vol`.
- First observed 15M timestamp: `1760950800000`.
- First observed 4H timestamp: `1760961600000`.
- Last observed 15M timestamp: `1795096800000`.
- Last observed 4H timestamp: `1795075200000`.

The candle counts agree with the previously accepted study's reported complete-candle counts (37,941 15M and 2,370 4H per asset).

## Important limitation

The last 15M timestamp is six hours later than the last 4H timestamp. Matching counts do not establish timestamp alignment, identical coverage, or OHLCV aggregation equivalence to the synchronized 1M source. The first timestamps also differ as expected for different candle intervals, but their exact timestamp-label convention must be verified.

## Next validation gate

Before using these 15M/4H files in a reconstructed breakout or matched-control calculation:

1. Audit timestamp cadence and duplicates for each file.
2. Determine exact candle timestamp semantics (open-time vs close-time labels).
3. Compare 15M and 4H OHLCV against bars independently aggregated from the synchronized five-asset 1M data, using the accepted resampling/complete-bar conventions.
4. Establish the common complete time range and explain the six-hour end difference.

No event counts, matched controls, or outcomes are calculated by this inventory check. The accepted 20 breakout counts remain the required reproduction gate.
