# Performance report: signal_extreme_atr_buffer_0_10__fixed_target_1_50pct

## Run metadata
- Experiment Id: signal_extreme_atr_buffer_0_10__fixed_target_1_50pct
- Stop Model: signal_extreme_atr_buffer_0_10
- Target Model: fixed_target_1_50pct
- Target Value: 0.015000
- Trailing Mode: none
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
- Final Equity: 107.928340
- Net Pnl: -892.071660
- Total Return Pct: -89.207166
- Max Drawdown Amount: 920.493981
- Max Drawdown Pct: 90.131207
- Recovery Factor: -0.969123
- Sharpe Ratio: -5.619811
- Sortino Ratio: -6.152933
- Cagr Pct: -87.203922
- Calmar Ratio: -0.967522
- Worst Daily Loss: -57.630038
- Worst Daily Loss Pct: -5.851767
- Worst Daily Loss Date Utc: 2025-11-18
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 42.724782
- Max Capital Utilization Pct: 102.639200
- Max Gross Exposure: 1,013.209353
- Max Gross Exposure Equity Multiple: 1.026392

## Trade performance

- Trade Count: 3806
- Net Pnl: -892.071660
- Gross Pnl: -74.210580
- Total Fees: 819.271474
- Funding Pnl: 1.410394
- Winning Trades: 998
- Losing Trades: 2808
- Breakeven Trades: 0
- Win Rate Pct: 26.221755
- Profit Factor: 0.747615
- Expectancy: -0.234386
- Average Win: 2.647792
- Average Loss: 1.258749
- Payoff Ratio: 2.103510
- Max Consecutive Losses: 48
- Average Duration Minutes: 128.058066
- Median Duration Minutes: 49.000000
- Max Duration Minutes: 3,470.000000
- Recovery Factor: -0.969123

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 746 | -136.951299 | -18.351351 | 118.700044 | 0.100095 | 26.005362 | 0.731711 | -0.183581 | 1.925309 | 0.924749 | 2.081981 |
| BTC | 682 | -166.688757 | -9.375243 | 157.586366 | 0.272852 | 22.140762 | 0.728444 | -0.244412 | 2.961183 | 1.155984 | 2.561613 |
| DOGE | 865 | -195.085551 | 4.946640 | 200.747947 | 0.715757 | 27.861272 | 0.777469 | -0.225532 | 2.828137 | 1.404914 | 2.013032 |
| ETH | 645 | -188.020710 | -38.951859 | 149.029194 | -0.039657 | 26.666667 | 0.722560 | -0.291505 | 2.846963 | 1.432766 | 1.987040 |
| SOL | 868 | -205.325343 | -12.478766 | 193.207923 | 0.361347 | 27.649770 | 0.760110 | -0.236550 | 2.710787 | 1.362921 | 1.988954 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1210 | -337.205710 | -22.834194 | 313.178521 | -1.192994 | 24.132231 | 0.738541 | -0.278682 | 3.261994 | 1.404911 | 2.321852 |
| SHORT | 2596 | -554.865950 | -51.376385 | 506.092953 | 2.603388 | 27.195686 | 0.752828 | -0.213739 | 2.393759 | 1.187757 | 2.015362 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 217 | -56.812591 | -15.854159 | 40.899309 | -0.059124 | 22.580645 | 0.676861 | -0.261809 | 2.428614 | 1.046516 | 2.320666 |
| AVAX | SHORT | 529 | -80.138708 | -2.497192 | 77.800735 | 0.159219 | 27.410208 | 0.760527 | -0.151491 | 1.755227 | 0.871476 | 2.014086 |
| BTC | LONG | 230 | -48.691628 | 12.912272 | 61.228711 | -0.375189 | 20.434783 | 0.777190 | -0.211703 | 3.613678 | 1.194178 | 3.026081 |
| BTC | SHORT | 452 | -117.997129 | -22.287515 | 96.357655 | 0.648042 | 23.008850 | 0.701494 | -0.261056 | 2.666306 | 1.135899 | 2.347308 |
| DOGE | LONG | 196 | -52.886383 | -6.857349 | 45.586056 | -0.442978 | 25.510204 | 0.736495 | -0.269828 | 2.956344 | 1.374682 | 2.150566 |
| DOGE | SHORT | 669 | -142.199168 | 11.803989 | 155.161891 | 1.158735 | 28.550075 | 0.789635 | -0.212555 | 2.794575 | 1.414149 | 1.976154 |
| ETH | LONG | 247 | -54.425988 | 6.891607 | 60.890189 | -0.427406 | 25.101215 | 0.787138 | -0.220348 | 3.246138 | 1.382089 | 2.348718 |
| ETH | SHORT | 398 | -133.594722 | -45.843466 | 88.139005 | 0.387749 | 27.638191 | 0.683434 | -0.335665 | 2.621974 | 1.465319 | 1.789354 |
| SOL | LONG | 320 | -124.389120 | -19.926566 | 104.574256 | 0.111702 | 26.250000 | 0.716633 | -0.388716 | 3.744994 | 1.860037 | 2.013398 |
| SOL | SHORT | 548 | -80.936223 | 7.447800 | 88.633667 | 0.249644 | 28.467153 | 0.805883 | -0.147694 | 2.153906 | 1.063637 | 2.025039 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | 0.006307 | 0.108032 | 0.000000 | -0.101725 |
| stop | 2801 | -2,906.996329 | 628.055600 | 0.957072 | -3,534.094857 |
| stop_gap | 6 | -0.281847 | 0.089452 | 0.000000 | -0.371299 |
| target | 998 | 2,833.061290 | 191.018390 | 0.453322 | 2,642.496222 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 859.114431 | -140.885569 | -14.088557 | False |
| 2025-12 | 859.114431 | 751.666844 | -107.447587 | -12.506784 | False |
| 2026-01 | 751.666844 | 706.520976 | -45.145868 | -6.006101 | False |
| 2026-02 | 706.520976 | 618.454691 | -88.066285 | -12.464780 | False |
| 2026-03 | 618.454691 | 447.506117 | -170.948573 | -27.641245 | False |
| 2026-04 | 447.506117 | 368.881073 | -78.625045 | -17.569602 | False |
| 2026-05 | 368.881073 | 267.011123 | -101.869950 | -27.615933 | False |
| 2026-06 | 267.011123 | 253.686979 | -13.324143 | -4.990108 | False |
| 2026-07 | 253.686979 | 186.811986 | -66.874993 | -26.361224 | False |
| 2026-08 | 186.811986 | 186.697734 | -0.114252 | -0.061159 | False |
| 2026-09 | 186.697734 | 137.388761 | -49.308973 | -26.411125 | False |
| 2026-10 | 137.388761 | 116.011312 | -21.377449 | -15.559824 | False |
| 2026-11 | 116.011312 | 107.928340 | -8.082972 | -6.967400 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
