# Exit experiment: fixed_stop_0_50pct__fixed_target_2_00pct

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
- Accepted entries: 3,332
- Rejected entries: 14,611
- Closed trades: 3,332
- Final equity: $205.45
- Net PnL: $-794.55
- Return: -79.45%
- Maximum drawdown: 81.71%
- Gross PnL: $169.06
- Fees: $966.10
- Funding PnL: $2.49

## Important
This is a historical simulation, not a live-trading result. Fees, slippage and funding are modeled assumptions. No parameter has been selected as optimal from this single run.
