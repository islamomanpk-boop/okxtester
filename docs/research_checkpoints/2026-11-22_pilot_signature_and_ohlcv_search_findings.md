# 2026-11-22 Pilot Signature and OHLCV Source Search Findings

## Status
Read-only recursive searches completed across `~/okx_adaptive_bot`, `~/okxtester`, and `~/okx_scalp`. No scripts were executed.

## Pilot signature search
Searched for distinctive strings from `~/okx_scalping_reports/RUN_CONFIG.json`, including:
- `start_balance_per_strategy_portfolio`
- `ORDER_BLOCK_LIQUIDITY_SWEEP`
- `BB_SQUEEZE_BREAKOUT`
- `Existing cache is preserved`
- `Only 1m candles are tested in this pilot`

No matches were returned. The pilot runner was not located in these three trees by these signatures.

## OHLCV/cache search
Searched source/configuration/documentation files for:
- `fetch_ohlcv`
- `load_markets`
- `ohlcv`
- `cache`
- `since`
- `timeframe`

Relevant matches:
- `~/okx_adaptive_bot/config.json` records `source_timeframe: 1m` and timeframes `1d`, `4h`, `15m`.
- `~/okx_adaptive_bot/src/prepare_data.py` contains `make_timeframe(df, rule)` and comments about retaining only fully closed higher-timeframe candles.
- `~/okx_adaptive_bot/src/calculate_indicators.py` reads per-symbol 1d/4h/15m files and writes indicator-enriched outputs.
- The corresponding `prepare_data.py` and `calculate_indicators.py` files also exist under `~/okxtester/src`.
- `~/okxtester/src/run_exit_experiments.py` records 1m as its execution timeframe, but this is a consumer of execution data, not a downloader.

No match in this search established a candle downloader writing the five 1m CSV files in `~/okx_scalping_data/`.

## Interpretation
`okx_adaptive_bot` is a plausible separate workflow that expects 1m source data and derives higher timeframes. This is a lead for further inspection, not proof that it created or consumed the five files under `~/okx_scalping_data/`.

The earlier seven-day pilot's source code was not found by its distinctive strings in the three searched trees. It may be elsewhere, may use different names, or may no longer be present.

## Controls
- No scripts or experiments were executed.
- No data or reports were changed.
- The pause remains in effect.
- No provenance claim is upgraded based on these search results.

## Next read-only step
Inspect the relevant configuration and source code in `~/okx_adaptive_bot`, especially `config.json` and `src/prepare_data.py`, plus a shallow file inventory. Determine the exact input path and whether the code reads 1m source files or downloads them. Do not execute any code.
