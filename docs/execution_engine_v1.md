# Price Action V1 — Execution Engine

## Scope

The initial execution engine simulates one market-entry trade using
one-minute OHLC candles. It supports long and short positions, risk-based
quantity sizing, stop-loss and take-profit exits, fees, slippage and
historical funding events.

## Entry timing

A signal becomes eligible only at its explicit `signal_available_at`
timestamp. The entry selector chooses the first one-minute candle whose
opening timestamp is at or after that availability timestamp.

## Position sizing

- Default risk budget: 0.5% of current equity.
- Default gross exposure cap: 1.0x equity.
- Quantity is the lower of stop-risk-based quantity and exposure-capped
  quantity.

## Execution assumptions

- Market entry uses the eligible candle open.
- Slippage is adverse to the trader.
- Fees are explicit configuration inputs; no exchange fee tier is assumed.
- Stop-loss has priority if stop and target are both touched in one candle.
- A stop gap is filled at the candle open, with adverse slippage.
- A target gap is conservatively filled at the target, with adverse slippage.
- If neither stop nor target is reached, the trade exits at the last
  available candle close.

## Funding

Funding uses the actual historical `funding_rate` and `funding_time`.
Positive funding means longs pay and shorts receive.

Funding notional is calculated using:
1. An explicitly supplied settlement `mark_price`, when available.
2. Otherwise, the close of the one-minute candle timestamped at the
   funding settlement time.

The one-minute close is a proxy, not the exact exchange settlement mark.
Exact funding-cost reconstruction requires historical mark-price data.
If neither a mark price nor a candle at the funding timestamp is available,
the engine fails instead of silently substituting entry price.

## Limitations

This is the single-trade execution foundation, not the complete portfolio
backtester. It does not yet implement maker limit orders, multiple
simultaneous positions, portfolio-wide capital allocation, or strategy
signal generation. These will be added and tested in later stages.
