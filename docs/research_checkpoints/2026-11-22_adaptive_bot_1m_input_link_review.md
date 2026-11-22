# 2026-11-22 Adaptive Bot Source Input Link Review

## Status
Read-only inspection of `~/okx_adaptive_bot/config.json`, `src/prepare_data.py`, and a file inventory completed. No code was executed and no files were changed.

## Strong project-level evidence
The adaptive-bot configuration explicitly records:
- `exchange: OKX`
- `market: USDT_PERPETUAL`
- Symbols: BTC, ETH, SOL, DOGE, AVAX
- `source_timeframe: 1m`
- Derived timeframes: 1d, 4h, 15m
- Mode: BACKTEST_ONLY
- LINK excluded

The preparation script defines:
- `BASE = ~/okx_adaptive_bot`
- `DATA_DIR = ~/okx_adaptive_bot/data`
- Required columns: `ts,open,high,low,close,vol`
- Input path for each symbol: `DATA_DIR / f"{symbol}_USDT_USDT_1m.csv"`

This filename pattern is an exact match for the five files currently known under `~/okx_scalping_data/`, apart from the directory.

## Preparation-script behavior
The inspected `prepare_data.py`:
- Reads the five expected 1m CSV files from `~/okx_adaptive_bot/data/`.
- Parses millisecond timestamps as UTC.
- Checks required columns, numeric values, nulls, duplicate timestamps, one-minute timestamp continuity, OHLC consistency, and nonnegative volume.
- Aggregates source candles into 15m, 4h, and 1d OHLCV candles.
- Excludes incomplete higher-timeframe candles.
- Writes derived files back into `~/okx_adaptive_bot/data/`.
- Does not download data and does not write or modify the original 1m input files.

## Important discrepancy
The supplied adaptive-bot file inventory shows derived 15m, 4h, and 1d files in `~/okx_adaptive_bot/data/`, but does not show the five expected 1m input files there.

Therefore:
- The adaptive-bot project was configured for OKX USDT perpetuals and expects the same five-coin 1m filename pattern.
- The current five source files under `~/okx_scalping_data/` are a plausible match to the inputs used by that workflow.
- A direct copy/move relationship between the two directories is not yet proven.
- The original downloader and actual exchange API provenance remain unknown.

The config documents intended exchange/market settings; it does not by itself prove the historical files were actually downloaded from that exchange or instrument.

## Additional observation
The preparation script hardcodes the five symbols, source file path, and derived timeframes. The config's `source_timeframe` is not used in the displayed preparation code.

## Controls
- No downloader, preparation script, audit, or backtest was run.
- No data, source, or report files were modified.
- The research pause remains active.
- No OKX provenance claim is treated as fully verified.

## Next read-only step
Inspect the file listing inside `~/okx_adaptive_bot/okx_research_project.zip` without extracting or executing it, and inspect source-file references for copy operations or data-path changes. The archive may preserve an earlier downloader or project documentation.