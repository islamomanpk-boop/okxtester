# 2026-11-22 Earlier 1m Pilot Configuration and Coverage Review

## Status
Read-only inspection of `~/okx_scalping_reports/RUN_CONFIG.json` and `DATA_COVERAGE.csv` completed. No scripts or experiments were run.

## Run configuration facts
The earlier pilot configuration records:
- Version: V1.1
- Symbols: `BTC/USDT:USDT`, `ETH/USDT:USDT`, `SOL/USDT:USDT`, `DOGE/USDT:USDT`, `AVAX/USDT:USDT`, and `LINK/USDT:USDT`
- Requested duration: 7 days
- Starting balance per strategy portfolio: $1,000
- Risk per trade: 0.5%
- Maximum gross exposure: 1.0
- Fee per side: 0.0005
- Slippage per side: 0.00025
- OOS fraction: 20%
- Warm-up: 30 days
- Seven named strategies
- Only timeframe: 1m

The notes state that each strategy has an independent portfolio with capital shared across its symbols; existing cache is preserved and only the requested date range is used; OOS starts flat while indicators retain pre-split warm-up history; signals use completed candles and enter at the next available candle open; stop wins when stop and target touch in the same candle; stop gaps fill at the worse of stop and candle open; and funding is applied according to the listed settlement/mark-proxy rules. The notes also explicitly warn that seven-day results are preliminary and do not prove a durable edge.

## Data coverage facts
The coverage CSV records:
- BTC/USDT:USDT: 10,079 bars, 99.990079% coverage, 0 gaps, max gap 1 bar
- ETH/USDT:USDT: 10,079 bars, 99.990079% coverage, 0 gaps, max gap 1 bar
- SOL/USDT:USDT: 10,080 bars, 100% coverage, 0 gaps, max gap 1 bar
- DOGE/USDT:USDT: 10,080 bars, 100% coverage, 0 gaps, max gap 1 bar
- AVAX/USDT:USDT: 10,080 bars, 100% coverage, 0 gaps, max gap 1 bar
- LINK/USDT:USDT: 10,080 bars, 100% coverage, 0 gaps, max gap 1 bar

The expected count of 10,080 is consistent with seven complete days of 1-minute bars. BTC and ETH are each short by one bar according to the recorded count.

## Provenance interpretation and limitations
The `BASE/USDT:USDT` symbol notation is consistent with a USDT-settled swap/perpetual symbol convention used by trading libraries, but the configuration alone does not identify the exchange or prove the actual instrument metadata. The report files contain no source endpoint or downloader reference.

This establishes that an earlier pilot was configured for six swap-style symbols and 1m bars over seven days. It does **not** establish that the pilot read the current five long-history CSV files under `~/okx_scalping_data/`. The 7-day report may have used a separate cache or input path. The six-symbol pilot and five-file long-history dataset must remain separate evidence items until a script/config/cache link is found.

## Research controls
- No backtest, downloader, or audit script was executed.
- No local data or reports were changed.
- The pause on experiments remains active.
- Do not infer OKX provenance solely from symbol notation.

## Next read-only step
Search source files for distinctive configuration strings and strategy names, plus common OHLCV cache/download references, to locate the pilot runner and determine its input/cache path. Inspect source only; do not execute it.
