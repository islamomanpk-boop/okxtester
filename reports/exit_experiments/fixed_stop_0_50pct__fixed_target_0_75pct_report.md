# Exit experiment: fixed_stop_0_50pct__fixed_target_0_75pct

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
- Accepted entries: 5,976
- Rejected entries: 11,967
- Closed trades: 5,976
- Final equity: $24.24
- Net PnL: $-975.76
- Return: -97.58%
- Maximum drawdown: 97.63%
- Gross PnL: $-21.00
- Fees: $955.90
- Funding PnL: $1.14

## Important
This is a historical simulation, not a live-trading result. Fees, slippage and funding are modeled assumptions. No parameter has been selected as optimal from this single run.
