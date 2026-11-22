# Likely Candle Downloader Located — 2026-11-22

## Discovery
A read-only search of `~/okx_scalp` and `~/okx_adaptive_bot` found:
- `~/okx_scalp/1_fetch.py`
- The file references the OKX endpoint `/api/v5/market/history-candles`.
- It constructs instrument identifiers using `{asset}-USDT-SWAP`.

No Git repository was present in either inspected project directory. No matching downloader was found in the inspected `~/okx_adaptive_bot` search.

## Significance
This is strong evidence that `1_fetch.py` was written to retrieve OKX historical candles for USDT perpetual swap instruments. It is not yet proof that this script generated the five CSV files under `~/okx_scalping_data`.

## Questions still to verify
1. Which assets does the script fetch?
2. What exact output directory and filenames does it write?
3. Does its CSV schema match `ts,open,high,low,close,vol`?
4. Does it explicitly identify the candle volume unit or document OKX's volume semantics?
5. Is there evidence the script was run to create the current files (logs, timestamps, matching ranges, shell history, or other metadata)?

## Next step
Inspect `~/okx_scalp/1_fetch.py` as text only. Do not execute it. Avoid sharing any credentials or secrets if present.

## Safety state
No script was executed; no network request, download, data transformation, or file modification occurred. Backtests remain paused.
