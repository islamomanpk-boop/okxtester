# Exit experiment: fixed_stop_1_00pct__fixed_target_0_75pct__trailing_tp

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
- Accepted entries: 3,802
- Rejected entries: 14,141
- Closed trades: 3,802
- Final equity: $204.62
- Net PnL: $-795.38
- Return: -79.54%
- Maximum drawdown: 81.67%
- Gross PnL: $-22.98
- Fees: $773.83
- Funding PnL: $1.43

## Important
This is a historical simulation, not a live-trading result. Fees, slippage and funding are modeled assumptions. No parameter has been selected as optimal from this single run.
