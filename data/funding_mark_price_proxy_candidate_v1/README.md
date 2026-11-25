# Funding-time 4H mark-price candidate proxy V1

This immutable snapshot contains the 4H OKX mark-price candle at each of the 5,940 audited funding timestamps (1,188 per asset across BTC, ETH, SOL, DOGE, and AVAX USDT swaps).

- mark_open is the candidate public proxy price at the funding timestamp.
- mark_high, mark_low, and mark_close are diagnostic candle fields; do not substitute the 4H close as the funding price.
- All rows are confirmed 4H candles and have an exact funding-timestamp match.
- The CSV is byte-identical to an independent VPS-runner retrieval (recorded in manifest.json).

Important: this is a candle-derived proxy, not an independently verified exact OKX funding settlement mark. The engine has not adopted this mode and no strategy PnL backtest is authorized by this dataset. See docs/research/funding_price_fidelity_shared_v1.md and the full-window audit checkpoint for limits and policy status.
