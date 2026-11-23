# Performance report: fixed_stop_1_00pct__fixed_target_0_75pct__trailing_sl

## Run metadata
- Experiment Id: fixed_stop_1_00pct__fixed_target_0_75pct__trailing_sl
- Stop Model: fixed_stop_1_00pct
- Target Model: fixed_target_0_75pct
- Target Value: 0.007500
- Trailing Mode: trailing_stop_loss
- Assets: BTC,ETH,SOL,DOGE,AVAX
- Execution Timeframe: 1m
- Execution Window Start Utc: 2025-10-20T08:50:00+00:00
- Execution Window End Utc: 2026-11-19T14:14:00+00:00
- Taker Fee Rate Per Side: 0.000500
- Slippage Bps Per Side: 2.000000
- Funding Data: Historical asset-specific realized funding rates
- Funding Treatment: Applied at funding timestamps; mark price when supplied, otherwise candle close proxy
- Equity Curve Storage: summary-only
- Risk Fraction: 0.005000
- Max Gross Leverage: 1.000000
- End Of Data Policy: Open positions forcibly closed at final available candle

## Portfolio risk and return

- Initial Equity: 1,000.000000
- Final Equity: 181.497033
- Net Pnl: -818.502967
- Total Return Pct: -81.850297
- Max Drawdown Amount: 868.720333
- Max Drawdown Pct: 83.421146
- Recovery Factor: -0.942194
- Sharpe Ratio: -5.321968
- Sortino Ratio: -5.836250
- Cagr Pct: -79.320130
- Calmar Ratio: -0.950840
- Worst Daily Loss: -69.626757
- Worst Daily Loss Pct: -7.476494
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 35.690257
- Max Capital Utilization Pct: 102.230332
- Max Gross Exposure: 1,039.132660
- Max Gross Exposure Equity Multiple: 1.022303

## Trade performance

- Trade Count: 4300
- Net Pnl: -818.502967
- Gross Pnl: -43.382806
- Total Fees: 776.149180
- Funding Pnl: 1.029019
- Winning Trades: 2496
- Losing Trades: 1804
- Breakeven Trades: 0
- Win Rate Pct: 58.046512
- Profit Factor: 0.776000
- Expectancy: -0.190350
- Average Win: 1.136028
- Average Loss: 2.025516
- Payoff Ratio: 0.560859
- Max Consecutive Losses: 19
- Average Duration Minutes: 125.933256
- Median Duration Minutes: 55.000000
- Max Duration Minutes: 3,804.000000
- Recovery Factor: -0.942194

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 891 | -114.232366 | 5.785589 | 119.891973 | -0.125982 | 58.361392 | 0.794667 | -0.128207 | 0.850184 | 1.499537 | 0.566965 |
| BTC | 612 | -92.990317 | 18.552491 | 111.683176 | 0.140369 | 59.640523 | 0.817586 | -0.151945 | 1.141879 | 2.063871 | 0.553271 |
| DOGE | 956 | -230.646288 | -45.965719 | 185.140066 | 0.459496 | 57.740586 | 0.742198 | -0.241262 | 1.202934 | 2.214519 | 0.543203 |
| ETH | 746 | -196.260699 | -40.298649 | 156.046398 | 0.084348 | 56.702413 | 0.739992 | -0.263084 | 1.320484 | 2.336920 | 0.565053 |
| SOL | 1095 | -184.373297 | 18.543482 | 203.387567 | 0.470788 | 58.082192 | 0.803531 | -0.168377 | 1.185631 | 2.044520 | 0.579907 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1455 | -294.548565 | -29.503168 | 263.917057 | -1.128339 | 56.975945 | 0.764696 | -0.202439 | 1.154684 | 1.999651 | 0.577443 |
| SHORT | 2845 | -523.954402 | -13.879638 | 512.232123 | 2.157359 | 58.594025 | 0.781890 | -0.184167 | 1.126751 | 2.039260 | 0.552529 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 272 | -49.714312 | -12.466432 | 37.039484 | -0.208397 | 54.411765 | 0.725374 | -0.182773 | 0.887237 | 1.459882 | 0.607746 |
| AVAX | SHORT | 619 | -64.518054 | 18.252020 | 82.852489 | 0.082415 | 60.096931 | 0.828091 | -0.104229 | 0.835443 | 1.519445 | 0.549834 |
| BTC | LONG | 226 | -31.620694 | 10.638305 | 41.815993 | -0.443006 | 60.176991 | 0.832389 | -0.139915 | 1.154668 | 2.096172 | 0.550846 |
| BTC | SHORT | 386 | -61.369623 | 7.914185 | 69.867183 | 0.583375 | 59.326425 | 0.808889 | -0.158989 | 1.134284 | 2.045354 | 0.554566 |
| DOGE | LONG | 226 | -43.007456 | -5.913066 | 36.666921 | -0.427469 | 59.734513 | 0.754588 | -0.190298 | 0.979544 | 1.925779 | 0.508648 |
| DOGE | SHORT | 730 | -187.638833 | -40.052654 | 148.473145 | 0.886966 | 57.123288 | 0.739180 | -0.257039 | 1.275254 | 2.298466 | 0.554828 |
| ETH | LONG | 297 | -59.337145 | 0.905517 | 59.926949 | -0.315713 | 56.228956 | 0.787609 | -0.199788 | 1.317600 | 2.149049 | 0.613108 |
| ETH | SHORT | 449 | -136.923553 | -41.204165 | 96.119449 | 0.400061 | 57.015590 | 0.712012 | -0.304952 | 1.322365 | 2.463466 | 0.536790 |
| SOL | LONG | 434 | -110.868958 | -22.667493 | 88.467710 | 0.266245 | 55.990783 | 0.740644 | -0.255458 | 1.302919 | 2.238106 | 0.582152 |
| SOL | SHORT | 661 | -73.504339 | 41.210975 | 114.919857 | 0.204543 | 59.455371 | 0.856144 | -0.111202 | 1.113110 | 1.906554 | 0.583833 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 2 | -0.643323 | 0.163256 | 0.000000 | -0.806579 |
| stop | 1799 | -3,324.152237 | 326.399803 | 0.318995 | -3,650.233045 |
| stop_gap | 3 | -2.724534 | 0.265819 | 0.000000 | -2.990353 |
| target | 2494 | 3,283.317124 | 449.207662 | 0.712156 | 2,834.821617 |
| target_gap | 2 | 0.820164 | 0.112640 | -0.002131 | 0.705392 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 964.017798 | -35.982202 | -3.598220 | False |
| 2025-12 | 964.017798 | 807.221927 | -156.795871 | -16.264832 | False |
| 2026-01 | 807.221927 | 748.463848 | -58.758078 | -7.279049 | False |
| 2026-02 | 748.463848 | 605.009252 | -143.454596 | -19.166536 | False |
| 2026-03 | 605.009252 | 457.638264 | -147.370988 | -24.358469 | False |
| 2026-04 | 457.638264 | 403.810221 | -53.828043 | -11.762138 | False |
| 2026-05 | 403.810221 | 359.135818 | -44.674403 | -11.063218 | False |
| 2026-06 | 359.135818 | 322.738430 | -36.397388 | -10.134714 | False |
| 2026-07 | 322.738430 | 275.175337 | -47.563092 | -14.737350 | False |
| 2026-08 | 275.175337 | 268.811384 | -6.363954 | -2.312690 | False |
| 2026-09 | 268.811384 | 212.145660 | -56.665724 | -21.080106 | False |
| 2026-10 | 212.145660 | 188.405271 | -23.740388 | -11.190608 | False |
| 2026-11 | 188.405271 | 181.497033 | -6.908238 | -3.666690 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
