# Exit experiment: fixed_stop_0_75pct__fixed_target_1_50pct__trailing_sl

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
- Accepted entries: 3,968
- Rejected entries: 13,975
- Closed trades: 3,968
- Final equity: $140.25
- Net PnL: $-859.75
- Return: -85.97%
- Maximum drawdown: 87.15%
- Gross PnL: $43.46
- Fees: $904.51
- Funding PnL: $1.31

## Important
This is a historical simulation, not a live-trading result. Fees, slippage and funding are modeled assumptions. No parameter has been selected as optimal from this single run.
