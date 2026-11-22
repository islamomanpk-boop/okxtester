# Downloader Comparison: 15m Script vs Five 1m Files — 2026-11-22

## Source inspected
Read-only inspection of `~/okx_scalp/1_fetch.py`.

## What the script does
- Uses `https://www.okx.com`.
- Calls `/api/v5/public/instruments` with `instType=SWAP` and an instrument ID.
- Calls `/api/v5/market/history-candles`.
- Constructs IDs as `{asset}-USDT-SWAP`.
- Requests `BAR = "15m"`.
- Requests approximately three months of history.
- Writes gzip CSV files to `~/okx_scalp/data/{COIN}.csv.gz`.
- Retains `ts,open,high,low,close,vol` and discards `volCcy`, `volCcyQuote`, and `confirm`.
- The script file's observed modification time was 2026-11-11 16:45.

## Comparison with the five execution files
The five files under investigation are:
- `BTC_USDT_USDT_1m.csv`
- `ETH_USDT_USDT_1m.csv`
- `SOL_USDT_USDT_1m.csv`
- `DOGE_USDT_USDT_1m.csv`
- `AVAX_USDT_USDT_1m.csv`

Observed differences:
- Current files are 1-minute, while the located script requests 15-minute candles.
- Current files span from 2025-10-20 to 2026-11-19, while the located script requests only about three months.
- Located script writes compressed files under `~/okx_scalp/data/`; current files are uncompressed CSVs under `~/okx_scalping_data/`.
- Current files were modified on 2026-11-19, later than the located script's observed modification time.
- The located script's planned coin list includes BTC, ETH, SOL, DOGE, and AVAX, but shared asset names alone do not establish that it generated the current files.

## Interpretation
The script proves that an OKX USDT-swap 15-minute candle download workflow existed in `~/okx_scalp`. It does **not** establish the origin of the five current 1-minute CSVs. Their provenance remains **UNVERIFIED**.

The script retains the OKX candle response's raw `vol` field and discards `volCcy` and `volCcyQuote`. This describes the located 15-minute script only. Do not infer the unit of the separate 1-minute files from this script.

## Next safe investigation
Inspect all source files in `~/okx_scalp` and search for other 1-minute download implementations, output paths, or transformations that mention `okx_scalping_data` or the five filenames. Do not execute any scripts.

## Safety state
No scripts were run and no data or code was modified. Backtests remain paused.
