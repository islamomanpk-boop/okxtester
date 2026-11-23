# Exit experiment: fixed_stop_0_50pct__fixed_target_2_00pct__trailing_tp

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
- Accepted entries: 3,307
- Rejected entries: 14,636
- Closed trades: 3,307
- Final equity: $184.97
- Net PnL: $-815.03
- Return: -81.50%
- Maximum drawdown: 83.63%
- Gross PnL: $92.22
- Fees: $909.50
- Funding PnL: $2.25

## Important
This is a historical simulation, not a live-trading result. Fees, slippage and funding are modeled assumptions. No parameter has been selected as optimal from this single run.
