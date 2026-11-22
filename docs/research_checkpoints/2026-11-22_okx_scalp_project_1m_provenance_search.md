# 1-Minute Candle Provenance Search: OKX_Scalp Project

Date: 2026-11-22
Project branch: `price-action-v1`

## Scope

Read-only inspection of Python files and directory structure under `~/okx_scalp`, following discovery of `1_fetch.py`.

## Findings

- Python files found: `1_fetch.py`, `2_indicadors.py`, `2_indicators.py`, `backtest.py`, `3_backtest.py`, and `4_report.py`.
- The earlier inspected `1_fetch.py` explicitly requests OKX `/api/v5/market/history-candles` for instruments named `{coin}-USDT-SWAP`, but requests 15-minute bars, three months, and saves gzip CSV files under `~/okx_scalp/data`.
- The current search across Python files in `~/okx_scalp` found no references to `1m`, `okx_scalping_data`, or `USDT_USDT_1m`.
- The only observed OKX candle endpoint reference in this project remains in `1_fetch.py`.
- The two indicator scripts contain `to_csv` calls, but this search alone does not establish that they generate the five 1-minute source CSVs.
- Directory listing showed only `~/okx_scalp/data` as a subdirectory. No provenance link from that directory to `~/okx_scalping_data` was established.
- `~/okx_scalp` has no Git repository, so local Git history is unavailable for this project.

## Conclusion

The inspected `okx_scalp` project does not currently provide evidence that it created the five 1-minute files in `~/okx_scalping_data`. It contains a separate, identifiable OKX USDT-swap 15-minute downloader, but the timeframe, output directory, requested history, and file format differ.

This is not proof that the five 1-minute files are not from OKX. Their provenance remains **unverified**.

## Safety and scope

- Inspection only; no scripts were executed.
- No CSV files or existing reports were modified.
- Backtests and experiments remain paused.

## Next investigation

Read the source of `2_indicators.py`, `2_indicadors.py`, and relevant data-loading sections of the backtest scripts to understand their inputs and output paths. Separately, inspect the files in `~/okx_scalping_data` for evidence of a distinct 1-minute downloader or transformation workflow. Do not execute any script or overwrite outputs without explicit approval.
