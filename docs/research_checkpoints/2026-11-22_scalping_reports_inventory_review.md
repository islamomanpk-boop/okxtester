# 2026-11-22 Scalping Reports Directory Provenance Search

## Status
Read-only inventory and text search completed for `~/okx_scalping_reports`. This directory contains outputs from an earlier 1-minute strategy-testing pilot, but the inventory/search does not identify the original candle downloader or prove the source of the five 1-minute CSV files.

## Inventory findings
The directory contains:
- `RUN_CONFIG.json` (1,903 bytes)
- `DATA_COVERAGE.csv` (278 bytes)
- `FINAL_COMPARISON.csv` and `OOS_RANKING.csv`
- Full and out-of-sample equity curves for multiple strategies
- Full and out-of-sample trade files
- Monthly summaries

All listed files were modified on 2026-11-19, roughly 18:32–18:49 local file time.

## Search findings
A recursive search across Python, shell, Markdown, JSON, and text files searched for the five dataset directory/filenames, OKX candle endpoint patterns, and `1m`.

Only matches were in `RUN_CONFIG.json`:
- It contains the timeframe value `1m`.
- It states: "Only 1m candles are tested in this pilot."

No exact source CSV filename, `okx_scalping_data` path, or OKX candle endpoint was found in this directory.

## Interpretation
This is evidence that an earlier pilot tested 1-minute candles and generated strategy reports. It is not evidence of which downloader produced those candles, which exchange/instrument the inputs represented, or whether the pilot used the same five files now under `~/okx_scalping_data/`.

## Controls
No reports, source data, or scripts were modified. No scripts or backtests were executed. The research pause remains active.

## Next read-only step
Inspect the complete `RUN_CONFIG.json` and `DATA_COVERAGE.csv` contents to identify recorded assets, date range, data paths, or other provenance clues. Do not execute any scripts.
