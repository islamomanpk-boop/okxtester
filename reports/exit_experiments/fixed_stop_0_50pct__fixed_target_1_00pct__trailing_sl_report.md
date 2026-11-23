# Exit experiment: fixed_stop_0_50pct__fixed_target_1_00pct__trailing_sl

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
- Accepted entries: 6,360
- Rejected entries: 11,583
- Closed trades: 6,360
- Final equity: $15.75
- Net PnL: $-984.25
- Return: -98.42%
- Maximum drawdown: 98.44%
- Gross PnL: $-112.21
- Fees: $872.86
- Funding PnL: $0.82

## Important
This is a historical simulation, not a live-trading result. Fees, slippage and funding are modeled assumptions. No parameter has been selected as optimal from this single run.
