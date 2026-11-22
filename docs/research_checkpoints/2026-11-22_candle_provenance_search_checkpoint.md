# Candle Provenance Search — 2026-11-22

## Purpose
Record a read-only search for the origin of the five 1-minute candle CSVs. No scripts were executed and no files were modified.

## Search performed
Within `~/okxtester`:
- Searched filenames for download/fetch/candle/OHLCV/market-data/history/klines terms.
- Searched `src`, `scripts`, and `docs` for OKX candle endpoint strings, API host, `instId`, and `USDT-SWAP`.
- Searched all available Git history for download/candle/market-data/OKX-data commit messages.

## Findings
1. No candle downloader or candle-fetch implementation was found by the filename search. The only download-related source found was:
   - `src/download_funding_archives.py`
   - its funding-specific test and compiled cache files.
2. OKX instrument references found in the inspected source belong to funding workflows:
   - `src/download_funding_archives.py`
   - `src/merge_funding_history.py`
   - funding tests.
   These reference instruments such as `BTC-USDT-SWAP`, but do not establish the source or instrument identity of the five candle CSVs.
3. `src/backtest_input_preflight.py` contains expected instrument-name checks, but an expected value in a preflight script is not proof of the source identity of existing CSV data.
4. The download-related Git commit-message search returned no results.
5. The search was limited to the inspected repository paths and commit-message terms. It does not prove that a downloader never existed elsewhere, in another repository, on another branch not represented in the search, or outside the current workspace.

## Conclusion
Candle provenance remains **UNVERIFIED**. There is currently no evidence in the inspected project files that the five candle CSVs were downloaded from OKX or represent the intended USDT perpetual swap instruments.

## Next safe investigation
Search the relevant home-directory project folders and shell history for the original candle download command/script, without running it. Inspect any candidate source and metadata before drawing conclusions.

## Safety / execution state
- Backtests and batch experiments remain paused.
- No downloads, API calls, data transformations, or scripts were run.
- No files were changed or overwritten.
