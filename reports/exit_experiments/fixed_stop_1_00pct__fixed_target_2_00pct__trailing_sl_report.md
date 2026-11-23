# Exit experiment: fixed_stop_1_00pct__fixed_target_2_00pct__trailing_sl

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
- Accepted entries: 2,906
- Rejected entries: 15,037
- Closed trades: 2,906
- Final equity: $398.88
- Net PnL: $-601.12
- Return: -60.11%
- Maximum drawdown: 66.57%
- Gross PnL: $106.95
- Fees: $709.10
- Funding PnL: $1.03

## Important
This is a historical simulation, not a live-trading result. Fees, slippage and funding are modeled assumptions. No parameter has been selected as optimal from this single run.
