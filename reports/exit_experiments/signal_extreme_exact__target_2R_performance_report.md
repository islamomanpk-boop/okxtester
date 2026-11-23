# Performance report: signal_extreme_exact__target_2R

## Run metadata
- Experiment Id: signal_extreme_exact__target_2R
- Stop Model: signal_extreme_exact
- Target Model: target_2R
- Target Value: 2.000000
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
- Final Equity: 31.221561
- Net Pnl: -968.778439
- Total Return Pct: -96.877844
- Max Drawdown Amount: 1,001.835650
- Max Drawdown Pct: 97.030022
- Recovery Factor: -0.967003
- Sharpe Ratio: -8.598495
- Sortino Ratio: -8.487762
- Cagr Pct: -95.930024
- Calmar Ratio: -0.988663
- Worst Daily Loss: -56.911759
- Worst Daily Loss Pct: -7.347600
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 38.361763
- Max Capital Utilization Pct: 102.520907
- Max Gross Exposure: 1,025.312877
- Max Gross Exposure Equity Multiple: 1.025209

## Trade performance

- Trade Count: 5053
- Net Pnl: -968.778439
- Gross Pnl: -36.049231
- Total Fees: 933.664188
- Funding Pnl: 0.934979
- Winning Trades: 1644
- Losing Trades: 3409
- Breakeven Trades: 0
- Win Rate Pct: 32.535128
- Profit Factor: 0.693477
- Expectancy: -0.191723
- Average Win: 1.333188
- Average Loss: 0.927116
- Payoff Ratio: 1.437994
- Max Consecutive Losses: 32
- Average Duration Minutes: 89.556105
- Median Duration Minutes: 28.000000
- Max Duration Minutes: 8,591.000000
- Recovery Factor: -0.967003

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 965 | -141.849159 | -17.990385 | 123.863216 | 0.004442 | 31.813472 | 0.663022 | -0.146994 | 0.909107 | 0.639734 | 1.421070 |
| BTC | 933 | -209.027965 | -14.576423 | 194.525811 | 0.074270 | 32.475884 | 0.634970 | -0.224039 | 1.200016 | 0.908941 | 1.320235 |
| DOGE | 1175 | -221.496260 | -1.630465 | 220.330378 | 0.464583 | 33.702128 | 0.710722 | -0.188507 | 1.374217 | 0.982909 | 1.398112 |
| ETH | 885 | -190.492542 | -7.179684 | 183.268533 | -0.044325 | 31.638418 | 0.711422 | -0.215246 | 1.677195 | 1.091086 | 1.537179 |
| SOL | 1095 | -205.912514 | 5.327726 | 211.676250 | 0.436009 | 32.694064 | 0.722178 | -0.188048 | 1.495128 | 1.005656 | 1.486719 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1711 | -386.633897 | -26.879774 | 359.165867 | -0.588256 | 31.677382 | 0.658003 | -0.225970 | 1.372482 | 0.967082 | 1.419199 |
| SHORT | 3342 | -582.144542 | -9.169456 | 574.498321 | 1.523235 | 32.974267 | 0.713232 | -0.174190 | 1.313861 | 0.906259 | 1.449764 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 269 | -46.303239 | -5.558772 | 40.664593 | -0.079874 | 30.483271 | 0.634706 | -0.172131 | 0.981134 | 0.677841 | 1.447440 |
| AVAX | SHORT | 696 | -95.545920 | -12.431613 | 83.198623 | 0.084316 | 32.327586 | 0.675222 | -0.137279 | 0.882857 | 0.624605 | 1.413466 |
| BTC | LONG | 369 | -84.930089 | -4.371811 | 80.364988 | -0.193291 | 31.707317 | 0.613888 | -0.230163 | 1.154122 | 0.872866 | 1.322220 |
| BTC | SHORT | 564 | -124.097875 | -10.204612 | 114.160824 | 0.267561 | 32.978723 | 0.648119 | -0.220032 | 1.228885 | 0.932991 | 1.317146 |
| DOGE | LONG | 269 | -54.094957 | -8.435657 | 45.313420 | -0.345881 | 31.970260 | 0.642710 | -0.201096 | 1.131496 | 0.827342 | 1.367628 |
| DOGE | SHORT | 906 | -167.401303 | 6.805192 | 175.016959 | 0.810464 | 34.216336 | 0.727485 | -0.184770 | 1.441552 | 1.030675 | 1.398648 |
| ETH | LONG | 380 | -96.031303 | -20.471065 | 75.252416 | -0.307822 | 30.789474 | 0.614920 | -0.252714 | 1.310675 | 0.948214 | 1.382256 |
| ETH | SHORT | 505 | -94.461238 | 13.291381 | 108.016117 | 0.263497 | 32.277228 | 0.770014 | -0.187052 | 1.940280 | 1.200956 | 1.615613 |
| SOL | LONG | 424 | -105.274309 | 11.957530 | 117.570451 | 0.338612 | 33.018868 | 0.725144 | -0.248288 | 1.983876 | 1.348651 | 1.471007 |
| SOL | SHORT | 671 | -100.638205 | -6.629804 | 94.105798 | 0.097397 | 32.488823 | 0.719006 | -0.149982 | 1.181253 | 0.790621 | 1.494082 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | -0.116616 | 0.011644 | 0.000556 | -0.127705 |
| stop | 3375 | -2,514.201699 | 629.211888 | 0.002269 | -3,143.411318 |
| stop_gap | 20 | -11.591149 | 4.443648 | 0.025065 | -16.009732 |
| target | 1653 | 2,489.370307 | 299.898229 | 0.907089 | 2,190.379168 |
| target_gap | 4 | 0.489926 | 0.098779 | 0.000000 | 0.391147 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 817.775060 | -182.224940 | -18.222494 | False |
| 2025-12 | 817.775060 | 648.104685 | -169.670375 | -20.747805 | False |
| 2026-01 | 648.104685 | 564.565857 | -83.538828 | -12.889712 | False |
| 2026-02 | 564.565857 | 508.843783 | -55.722074 | -9.869898 | False |
| 2026-03 | 508.843783 | 337.241599 | -171.602184 | -33.723942 | False |
| 2026-04 | 337.241599 | 251.925705 | -85.315895 | -25.298153 | False |
| 2026-05 | 251.925705 | 162.372199 | -89.553506 | -35.547586 | False |
| 2026-06 | 162.372199 | 133.338565 | -29.033634 | -17.880915 | False |
| 2026-07 | 133.338565 | 86.231568 | -47.106997 | -35.328861 | False |
| 2026-08 | 86.231568 | 78.031874 | -8.199694 | -9.508924 | False |
| 2026-09 | 78.031874 | 51.296635 | -26.735238 | -34.261946 | False |
| 2026-10 | 51.296635 | 36.401872 | -14.894764 | -29.036532 | False |
| 2026-11 | 36.401872 | 31.221561 | -5.180311 | -14.230892 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
