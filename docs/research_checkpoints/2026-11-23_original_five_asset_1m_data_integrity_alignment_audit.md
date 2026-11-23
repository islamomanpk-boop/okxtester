# Original five-asset 1-minute data integrity and alignment audit

**Date:** 2026-11-23  
**Repository:** islamomanpk-boop/okxtester  
**Branch:** price-action-v1  
**Status:** Individual-file integrity PASS; cross-asset timestamp alignment not perfect, with a two-minute tail difference.

## Source files

All five files were found under `~/okx_scalping_data/`:

- `BTC_USDT_USDT_1m.csv`
- `ETH_USDT_USDT_1m.csv`
- `SOL_USDT_USDT_1m.csv`
- `DOGE_USDT_USDT_1m.csv`
- `AVAX_USDT_USDT_1m.csv`

All use the same schema: `ts,open,high,low,close,vol`. Timestamps are Unix milliseconds.

## Individual-file audit

| Asset | Data rows | Unique timestamps | Duplicates | Missing 1m intervals | Unexpected intervals | Invalid OHLCV rows | First timestamp | Last timestamp |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | 569,125 | 569,125 | 0 | 0 | 0 | 0 | 1760950200000 | 1795097640000 |
| ETH | 569,125 | 569,125 | 0 | 0 | 0 | 0 | 1760950200000 | 1795097640000 |
| SOL | 569,126 | 569,126 | 0 | 0 | 0 | 0 | 1760950200000 | 1795097700000 |
| DOGE | 569,126 | 569,126 | 0 | 0 | 0 | 0 | 1760950200000 | 1795097700000 |
| AVAX | 569,127 | 569,127 | 0 | 0 | 0 | 0 | 1760950200000 | 1795097760000 |

All five files individually pass the checks performed:
- no duplicate timestamps;
- no missing one-minute intervals within each file;
- no unexpected timestamp intervals;
- no invalid OHLCV rows under the tested rules (high >= open/close/low, low <= open/close, and all OHLCV values nonnegative).

## Cross-asset alignment

- Common timestamps across all five assets: **569,125**
- Union of timestamps across all five assets: **569,127**
- Timestamps present in at least one asset but not all five: **2**
- Perfect timestamp alignment: **No**

The files share the same first timestamp. Their tails differ:
- BTC and ETH end at 1795097640000.
- SOL and DOGE end at 1795097700000.
- AVAX ends at 1795097760000.

The two union-only timestamps are at the very end of the observed period. This is a small tail mismatch, not an internal gap in any individual file.

## Decision

For any combined five-asset analysis, use the **intersection of timestamps common to all five assets**. Do not forward-fill, fabricate, or otherwise synthesize missing candles. Preserve the original source CSVs unchanged.

Before rebuilding the historical sideways-boundary/rejection event population, verify the exact resampling convention and confirm that the 4H/15M bars derived from these 1M files match the intended historical data and candle-close timestamps. Keep asset-specific analyses separate where appropriate.

## Scope and limitations

This audit verifies the five files' observed timestamp continuity, cross-asset timestamp intersection, basic OHLCV consistency, and common schema. It does not independently verify exchange provenance, completeness before the first timestamp, timezone interpretation, or whether the files are the exact source used in every earlier research run.

## Next step

Perform a read-only audit of the 1M-to-15M and 1M-to-4H resampling/alignment rules against the historical detector's expected candle timestamps before regenerating any research events.
