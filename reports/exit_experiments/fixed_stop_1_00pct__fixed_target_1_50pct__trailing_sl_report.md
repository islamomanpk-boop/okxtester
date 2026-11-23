# Exit experiment: fixed_stop_1_00pct__fixed_target_1_50pct__trailing_sl

## Configuration
- Assets: BTC, ETH, SOL, DOGE, AVAX
- Execution: synchronized 1-minute candles
- Starting equity: $1,000
- Risk budget: 0.5% of current equity per trade
- Maximum gross exposure: 1.0x equity
- Taker fee: 0.05% per side
- Slippage: 2 bps per side
- Funding: historical asset-specific funding events
- Equity curve storage: summary-only mode

## Results
- Execution window: 2025-10-20T08:50:00+00:00 to 2026-11-19T14:14:00+00:00
- Candidates: 17,943
- Accepted entries: 3,120
- Rejected entries: 14,823
- Closed trades: 3,120
- Final equity: $338.15
- Net PnL: $-661.85
- Return: -66.18%
- Maximum drawdown: 71.75%
- Gross PnL: $52.22
- Fees: $715.42
- Funding PnL: $1.34

## Important
This is a historical simulation, not a live-trading result. Fees, slippage and funding are modeled assumptions. No parameter has been selected as optimal from this single run.
