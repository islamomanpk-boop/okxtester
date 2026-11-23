# Performance report: fixed_stop_0_50pct__fixed_target_2_00pct__trailing_sl

## Run metadata
- Experiment Id: fixed_stop_0_50pct__fixed_target_2_00pct__trailing_sl
- Stop Model: fixed_stop_0_50pct
- Target Model: fixed_target_2_00pct
- Target Value: 0.020000
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
- Final Equity: 18.905176
- Net Pnl: -981.094824
- Total Return Pct: -98.109482
- Max Drawdown Amount: 1,000.095677
- Max Drawdown Pct: 98.146338
- Recovery Factor: -0.981001
- Sharpe Ratio: -9.713514
- Sortino Ratio: -8.963501
- Cagr Pct: -97.439175
- Calmar Ratio: -0.992795
- Worst Daily Loss: -58.072292
- Worst Daily Loss Pct: -7.422297
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 38.155630
- Max Capital Utilization Pct: 101.313052
- Max Gross Exposure: 1,016.028271
- Max Gross Exposure Equity Multiple: 1.013131

## Trade performance

- Trade Count: 6016
- Net Pnl: -981.094824
- Gross Pnl: -114.768161
- Total Fees: 867.341936
- Funding Pnl: 1.015272
- Winning Trades: 2367
- Losing Trades: 3649
- Breakeven Trades: 0
- Win Rate Pct: 39.345080
- Profit Factor: 0.647556
- Expectancy: -0.163081
- Average Win: 0.761552
- Average Loss: 0.762863
- Payoff Ratio: 0.998281
- Max Consecutive Losses: 19
- Average Duration Minutes: 66.973238
- Median Duration Minutes: 33.000000
- Max Duration Minutes: 2,169.000000
- Recovery Factor: -0.981001

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1206 | -113.820574 | -4.007729 | 109.918512 | 0.105666 | 37.064677 | 0.685425 | -0.094379 | 0.554817 | 0.476711 | 1.163843 |
| BTC | 883 | -121.805308 | 1.643978 | 123.590223 | 0.140936 | 40.203851 | 0.685651 | -0.137945 | 0.748391 | 0.733871 | 1.019785 |
| DOGE | 1395 | -224.011833 | -0.872980 | 223.493965 | 0.355112 | 39.713262 | 0.686462 | -0.160582 | 0.885294 | 0.849542 | 1.042084 |
| ETH | 1069 | -268.914341 | -80.792005 | 188.058242 | -0.064094 | 39.663237 | 0.563062 | -0.251557 | 0.817307 | 0.954190 | 0.856545 |
| SOL | 1463 | -252.542768 | -30.739425 | 222.280995 | 0.477652 | 40.123035 | 0.641510 | -0.172620 | 0.769881 | 0.804182 | 0.957347 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2090 | -369.917091 | -84.558512 | 284.958874 | -0.399704 | 37.799043 | 0.596601 | -0.176994 | 0.692511 | 0.705385 | 0.981749 |
| SHORT | 3926 | -611.177733 | -30.209649 | 582.383061 | 1.414976 | 40.168110 | 0.672587 | -0.155674 | 0.796138 | 0.794673 | 1.001843 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 349 | -39.525716 | -11.518182 | 27.977152 | -0.030382 | 33.524355 | 0.585446 | -0.113254 | 0.477089 | 0.410970 | 1.160884 |
| AVAX | SHORT | 857 | -74.294859 | 7.510453 | 81.941360 | 0.136048 | 38.506418 | 0.721198 | -0.086692 | 0.582375 | 0.505652 | 1.151731 |
| BTC | LONG | 339 | -50.412277 | -2.314337 | 47.982850 | -0.115090 | 41.002950 | 0.665443 | -0.148709 | 0.721377 | 0.753419 | 0.957472 |
| BTC | SHORT | 544 | -71.393032 | 3.958315 | 75.607373 | 0.256026 | 39.705882 | 0.698510 | -0.131237 | 0.765775 | 0.721952 | 1.060700 |
| DOGE | LONG | 335 | -35.036163 | -2.483048 | 32.384774 | -0.168340 | 38.507463 | 0.667479 | -0.104586 | 0.545186 | 0.511481 | 1.065896 |
| DOGE | SHORT | 1060 | -188.975670 | 1.610068 | 191.109191 | 0.523452 | 40.094340 | 0.689746 | -0.178279 | 0.988527 | 0.959212 | 1.030561 |
| ETH | LONG | 459 | -87.260538 | -19.472243 | 67.525573 | -0.262722 | 39.651416 | 0.587569 | -0.190110 | 0.683052 | 0.763812 | 0.894267 |
| ETH | SHORT | 610 | -181.653803 | -61.319762 | 120.532669 | 0.198628 | 39.672131 | 0.550224 | -0.297793 | 0.918276 | 1.097491 | 0.836705 |
| SOL | LONG | 608 | -157.682398 | -48.770701 | 109.088526 | 0.176830 | 36.677632 | 0.554608 | -0.259346 | 0.880485 | 0.919560 | 0.957507 |
| SOL | SHORT | 855 | -94.860370 | 18.031276 | 113.192469 | 0.300823 | 42.573099 | 0.729305 | -0.110948 | 0.702121 | 0.713712 | 0.983760 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | -0.020917 | 0.015296 | 0.000000 | -0.036213 |
| stop | 5758 | -723.535482 | 826.189433 | 0.947381 | -1,548.777535 |
| stop_gap | 89 | 84.527662 | 14.786754 | 0.019021 | 69.759929 |
| target | 168 | 524.260576 | 26.350453 | 0.048871 | 497.958994 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 839.077141 | -160.922859 | -16.092286 | False |
| 2025-12 | 839.077141 | 615.526117 | -223.551024 | -26.642488 | False |
| 2026-01 | 615.526117 | 527.033910 | -88.492208 | -14.376678 | False |
| 2026-02 | 527.033910 | 376.853755 | -150.180154 | -28.495349 | False |
| 2026-03 | 376.853755 | 214.594604 | -162.259151 | -43.056265 | False |
| 2026-04 | 214.594604 | 153.712751 | -60.881853 | -28.370636 | False |
| 2026-05 | 153.712751 | 120.347943 | -33.364808 | -21.705947 | False |
| 2026-06 | 120.347943 | 92.800798 | -27.547145 | -22.889585 | False |
| 2026-07 | 92.800798 | 70.316421 | -22.484377 | -24.228646 | False |
| 2026-08 | 70.316421 | 57.458688 | -12.857733 | -18.285533 | False |
| 2026-09 | 57.458688 | 33.609741 | -23.848947 | -41.506251 | False |
| 2026-10 | 33.609741 | 24.708502 | -8.901240 | -26.484106 | False |
| 2026-11 | 24.708502 | 18.905176 | -5.803326 | -23.487162 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
