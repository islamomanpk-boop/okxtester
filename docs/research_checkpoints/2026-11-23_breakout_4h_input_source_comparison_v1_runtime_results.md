# Breakout 4H input source comparison V1 — runtime results

**Date:** 2026-11-23  
**Branch:** `price-action-v1`  
**Script:** `research/validation/breakout_4h_input_source_comparison_v1.py`  
**Status:** Source-provenance comparison passed for all five assets; event reproduction remains on HOLD.

## Run

The user ran:

```bash
cd ~/okxtester || exit 1
git pull --ff-only origin price-action-v1
python research/validation/breakout_4h_input_source_comparison_v1.py
```

The pull fast-forwarded from `b65e277` to `fc58ac9`. The script completed normally and wrote no files.

## Method actually executed

Compared:
- Standalone 4H files: `~/okx_adaptive_bot/data/{ASSET}_USDT_4h.csv`
- 4H bars resampled from 1M files: `~/okx_scalping_data/{ASSET}_USDT_USDT_1m.csv`

The 1M resampling used the archived breakout script convention: 4h, epoch origin, left label, left closed, retaining bins with exactly 240 1M close observations.

Compared timestamps and OHLC values on the timestamp intersection. Exact equality and tolerance equality (`rtol=1e-10, atol=1e-10`) were both reported.

## Results

| Asset | 1M source rows | Complete resampled 4H | Standalone 4H | Common 4H timestamps | Exact OHLC matches | Differences |
|---|---:|---:|---:|---:|---:|---:|
| BTC | 569,125 | 2,370 | 2,370 | 2,370 | 2,370/2,370 | 0 |
| ETH | 569,125 | 2,370 | 2,370 | 2,370 | 2,370/2,370 | 0 |
| SOL | 569,126 | 2,370 | 2,370 | 2,370 | 2,370/2,370 | 0 |
| DOGE | 569,126 | 2,370 | 2,370 | 2,370 | 2,370/2,370 | 0 |
| AVAX | 569,127 | 2,370 | 2,370 | 2,370 | 2,370/2,370 | 0 |

For each asset:
- Standalone-only 4H timestamps: 0.
- Resampled-only 4H timestamps: 0.
- Resampling bins not containing exactly 240 1M rows: 2.
- OPEN, HIGH, LOW, CLOSE maximum absolute difference: 0.
- OPEN, HIGH, LOW, CLOSE mean absolute difference: 0.
- Every common row was both exactly equal and equal within the specified tolerance.

The 1M source row counts differ slightly by asset (BTC/ETH 569,125; SOL/DOGE 569,126; AVAX 569,127). This comparison did not assert that the raw 1M indexes are identical across assets. Its finding is specifically that each asset's standalone 4H OHLC rows match its own 1M-resampled 4H rows at every 4H timestamp.

## Interpretation

**Confirmed:** For the five asset datasets tested, different standalone-versus-resampled 4H OHLC source values do not explain the historical breakout event-count discrepancy. The compared 4H timestamp grids also match exactly within each asset.

This eliminates one source-provenance hypothesis only. It does not establish the exact historical event engine or resolve:
- 4H feature-to-15M timestamp mapping and availability convention;
- quantile population and valid-row filtering;
- 12-bar channel and feature-row alignment details in the event producer;
- exact event mask, including prior-sideways selection;
- any differences in the contemporaneous run code or source snapshots.

The historical 20/20 count table remains not independently reproduced. Threshold agreement alone is not sufficient.

## Gate decision

**HOLD — do not construct matched controls or calculate forward outcomes.**

The comparison was source-only. It ran no sideways classifications, event masks, controls, matching, forward outcomes, inference, or profitability calculations. No files were written or modified.

## Next investigation

Continue with the exact feature-row and 4H-to-15M availability/alignment path. In particular, inspect the historical detector's 2,358 feature-row construction and compare it row-by-row with the event reconstruction's feature snapshots and 15M as-of mapping. Then test source-grounded alternatives one at a time, without tuning to the accepted target counts.

Preserve each diagnostic and all count tables. Do not proceed to matched controls until all 20 event counts are reproduced by a source-justified implementation or a new implementation is explicitly accepted with the historical discrepancy documented.
