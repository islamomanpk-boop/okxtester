# Performance report: signal_extreme_atr_buffer_0_10__fixed_target_1_00pct

## Run metadata
- Experiment Id: signal_extreme_atr_buffer_0_10__fixed_target_1_00pct
- Stop Model: signal_extreme_atr_buffer_0_10
- Target Model: fixed_target_1_00pct
- Target Value: 0.010000
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
- Final Equity: 36.504042
- Net Pnl: -963.495958
- Total Return Pct: -96.349596
- Max Drawdown Amount: 985.574522
- Max Drawdown Pct: 96.471108
- Recovery Factor: -0.977598
- Sharpe Ratio: -8.328916
- Sortino Ratio: -8.197173
- Cagr Pct: -95.297958
- Calmar Ratio: -0.987839
- Worst Daily Loss: -62.396003
- Worst Daily Loss Pct: -8.140868
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 40.609740
- Max Capital Utilization Pct: 102.390546
- Max Gross Exposure: 1,017.515040
- Max Gross Exposure Equity Multiple: 1.023905

## Trade performance

- Trade Count: 4904
- Net Pnl: -963.495958
- Gross Pnl: -154.250130
- Total Fees: 810.224577
- Funding Pnl: 0.978748
- Winning Trades: 1620
- Losing Trades: 3284
- Breakeven Trades: 0
- Win Rate Pct: 33.034258
- Profit Factor: 0.691463
- Expectancy: -0.196471
- Average Win: 1.332895
- Average Loss: 0.950909
- Payoff Ratio: 1.401706
- Max Consecutive Losses: 34
- Average Duration Minutes: 88.223695
- Median Duration Minutes: 36.000000
- Max Duration Minutes: 3,470.000000
- Recovery Factor: -0.977598

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 961 | -123.720348 | -24.615348 | 99.071385 | -0.033615 | 32.986472 | 0.676502 | -0.128741 | 0.816167 | 0.593859 | 1.374344 |
| BTC | 851 | -182.357479 | -17.829918 | 164.657007 | 0.129446 | 28.437133 | 0.679946 | -0.214286 | 1.600884 | 0.935585 | 1.711104 |
| DOGE | 1136 | -198.409886 | -6.153033 | 192.692626 | 0.435773 | 34.419014 | 0.734485 | -0.174657 | 1.403721 | 1.003040 | 1.399467 |
| ETH | 824 | -254.312102 | -94.638405 | 159.699925 | 0.026228 | 33.131068 | 0.612851 | -0.308631 | 1.474623 | 1.192167 | 1.236926 |
| SOL | 1132 | -204.696143 | -11.013426 | 194.103635 | 0.420917 | 35.070671 | 0.732919 | -0.180827 | 1.414923 | 1.042749 | 1.356916 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1613 | -349.595417 | -53.779645 | 295.112342 | -0.703431 | 31.060136 | 0.680093 | -0.216736 | 1.483452 | 0.982738 | 1.509509 |
| SHORT | 3291 | -613.900541 | -100.470485 | 515.112236 | 1.682179 | 34.001823 | 0.697583 | -0.186539 | 1.265488 | 0.934614 | 1.354022 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 275 | -51.913640 | -21.325262 | 30.534530 | -0.053848 | 29.818182 | 0.567982 | -0.188777 | 0.832339 | 0.622619 | 1.336836 |
| AVAX | SHORT | 686 | -71.806708 | -3.290086 | 68.536855 | 0.020233 | 34.256560 | 0.726221 | -0.104675 | 0.810524 | 0.581552 | 1.393726 |
| BTC | LONG | 304 | -51.706098 | 10.134467 | 61.575130 | -0.265435 | 26.973684 | 0.731910 | -0.170086 | 1.721495 | 0.868778 | 1.981513 |
| BTC | SHORT | 547 | -130.651381 | -27.964385 | 103.081877 | 0.394881 | 29.250457 | 0.653355 | -0.238851 | 1.539070 | 0.973909 | 1.580303 |
| DOGE | LONG | 261 | -48.253977 | -10.705754 | 37.234834 | -0.313389 | 31.034483 | 0.665453 | -0.184881 | 1.184971 | 0.801314 | 1.478784 |
| DOGE | SHORT | 875 | -150.155909 | 4.552721 | 155.457792 | 0.749162 | 35.428571 | 0.750997 | -0.171607 | 1.460878 | 1.067306 | 1.368752 |
| ETH | LONG | 332 | -95.913757 | -33.057240 | 62.605632 | -0.250885 | 31.325301 | 0.610395 | -0.288897 | 1.444887 | 1.079746 | 1.338173 |
| ETH | SHORT | 492 | -158.398345 | -61.581165 | 97.094292 | 0.277113 | 34.349593 | 0.614323 | -0.321948 | 1.492922 | 1.271524 | 1.174121 |
| SOL | LONG | 441 | -101.807945 | 1.174144 | 103.162215 | 0.180126 | 34.467120 | 0.738519 | -0.230857 | 1.891736 | 1.347238 | 1.404159 |
| SOL | SHORT | 691 | -102.888199 | -12.187570 | 90.941419 | 0.240791 | 35.455861 | 0.727137 | -0.148898 | 1.119104 | 0.845446 | 1.323686 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | 0.002133 | 0.036539 | 0.000000 | -0.034406 |
| stop | 3274 | -2,555.933908 | 564.880174 | 0.453657 | -3,120.360425 |
| stop_gap | 9 | -1.961875 | 0.427082 | -0.002384 | -2.391341 |
| target | 1617 | 2,402.752679 | 244.790343 | 0.527476 | 2,158.489811 |
| target_gap | 3 | 0.890840 | 0.090438 | 0.000000 | 0.800402 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 827.565207 | -172.434793 | -17.243479 | False |
| 2025-12 | 827.565207 | 637.770191 | -189.795016 | -22.934146 | False |
| 2026-01 | 637.770191 | 570.867049 | -66.903142 | -10.490164 | False |
| 2026-02 | 570.867049 | 447.448849 | -123.418200 | -21.619430 | False |
| 2026-03 | 447.448849 | 287.950990 | -159.497859 | -35.646054 | False |
| 2026-04 | 287.950990 | 221.100415 | -66.850574 | -23.215956 | False |
| 2026-05 | 221.100415 | 161.636820 | -59.463595 | -26.894384 | False |
| 2026-06 | 161.636820 | 133.526332 | -28.110489 | -17.391142 | False |
| 2026-07 | 133.526332 | 97.837525 | -35.688807 | -26.727917 | False |
| 2026-08 | 97.837525 | 87.996051 | -9.841474 | -10.058997 | False |
| 2026-09 | 87.996051 | 54.049286 | -33.946766 | -38.577601 | False |
| 2026-10 | 54.049286 | 41.245463 | -12.803823 | -23.689162 | False |
| 2026-11 | 41.245463 | 36.504042 | -4.741421 | -11.495619 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
