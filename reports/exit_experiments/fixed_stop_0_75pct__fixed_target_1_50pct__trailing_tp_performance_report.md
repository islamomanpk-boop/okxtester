# Performance report: fixed_stop_0_75pct__fixed_target_1_50pct__trailing_tp

## Run metadata
- Experiment Id: fixed_stop_0_75pct__fixed_target_1_50pct__trailing_tp
- Stop Model: fixed_stop_0_75pct
- Target Model: fixed_target_1_50pct
- Target Value: 0.015000
- Trailing Mode: trailing_take_profit
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
- Final Equity: 285.691505
- Net Pnl: -714.308495
- Total Return Pct: -71.430850
- Max Drawdown Amount: 795.930283
- Max Drawdown Pct: 76.037761
- Recovery Factor: -0.897451
- Sharpe Ratio: -3.162341
- Sortino Ratio: -3.812686
- Cagr Pct: -68.558170
- Calmar Ratio: -0.901633
- Worst Daily Loss: -69.123815
- Worst Daily Loss Pct: -7.395085
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 42.966618
- Max Capital Utilization Pct: 102.827592
- Max Gross Exposure: 1,051.832827
- Max Gross Exposure Equity Multiple: 1.028276

## Trade performance

- Trade Count: 2932
- Net Pnl: -714.308495
- Gross Pnl: 44.942430
- Total Fees: 760.903631
- Funding Pnl: 1.652706
- Winning Trades: 1028
- Losing Trades: 1904
- Breakeven Trades: 0
- Win Rate Pct: 35.061392
- Profit Factor: 0.836310
- Expectancy: -0.243625
- Average Win: 3.550089
- Average Loss: 2.291912
- Payoff Ratio: 1.548964
- Max Consecutive Losses: 38
- Average Duration Minutes: 192.527626
- Median Duration Minutes: 81.500000
- Max Duration Minutes: 3,777.000000
- Recovery Factor: -0.897451

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 614 | -129.528255 | 1.173756 | 130.841775 | 0.139764 | 33.550489 | 0.830653 | -0.210958 | 3.084180 | 1.874680 | 1.645177 |
| BTC | 428 | -98.227712 | 9.454140 | 107.989881 | 0.308028 | 35.514019 | 0.843318 | -0.229504 | 3.478277 | 2.271470 | 1.531289 |
| DOGE | 654 | -136.449731 | 41.660458 | 178.913216 | 0.803027 | 36.544343 | 0.865351 | -0.208639 | 3.669149 | 2.441871 | 1.502598 |
| ETH | 546 | -220.267790 | -66.577579 | 153.847088 | 0.156878 | 33.882784 | 0.752964 | -0.403421 | 3.629049 | 2.469922 | 1.469297 |
| SOL | 690 | -129.835007 | 59.231655 | 189.311671 | 0.245010 | 35.652174 | 0.878316 | -0.188167 | 3.809560 | 2.403123 | 1.585254 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 930 | -305.046295 | -34.651219 | 268.551960 | -1.843115 | 32.580645 | 0.806167 | -0.328007 | 4.187165 | 2.509980 | 1.668207 |
| SHORT | 2002 | -409.262201 | 79.593649 | 492.351671 | 3.495821 | 36.213786 | 0.853313 | -0.204427 | 3.283835 | 2.184842 | 1.503008 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 186 | -80.378040 | -36.903205 | 43.309456 | -0.165380 | 27.956989 | 0.700743 | -0.432140 | 3.619491 | 2.004415 | 1.805760 |
| AVAX | SHORT | 428 | -49.150216 | 38.076961 | 87.532320 | 0.305143 | 35.981308 | 0.900962 | -0.114837 | 2.903426 | 1.811233 | 1.603011 |
| BTC | LONG | 144 | -60.953016 | -18.970742 | 41.296037 | -0.686236 | 31.944444 | 0.761046 | -0.423285 | 4.220200 | 2.602880 | 1.621358 |
| BTC | SHORT | 284 | -37.274697 | 28.424882 | 66.693843 | 0.994264 | 37.323944 | 0.899757 | -0.131249 | 3.156310 | 2.089009 | 1.510913 |
| DOGE | LONG | 139 | -41.894124 | -1.604229 | 39.658942 | -0.630953 | 33.812950 | 0.818614 | -0.301397 | 4.022816 | 2.510505 | 1.602393 |
| DOGE | SHORT | 515 | -94.555607 | 43.264687 | 139.254274 | 1.433980 | 37.281553 | 0.879148 | -0.183603 | 3.582574 | 2.422321 | 1.478984 |
| ETH | LONG | 206 | -35.588924 | 24.298972 | 59.387766 | -0.500130 | 35.922330 | 0.890715 | -0.172762 | 3.919774 | 2.467062 | 1.588843 |
| ETH | SHORT | 340 | -184.678865 | -90.876551 | 94.459322 | 0.657008 | 32.647059 | 0.673706 | -0.543173 | 3.435233 | 2.471571 | 1.389899 |
| SOL | LONG | 255 | -86.232191 | -1.472016 | 84.899759 | 0.139584 | 32.941176 | 0.825252 | -0.338165 | 4.848007 | 2.885759 | 1.679976 |
| SOL | SHORT | 435 | -43.602816 | 60.703671 | 104.411913 | 0.105426 | 37.241379 | 0.923974 | -0.100236 | 3.271106 | 2.100813 | 1.557067 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | -0.864253 | 0.166460 | -0.000920 | -1.031633 |
| stop | 1900 | -3,860.445188 | 501.868196 | 1.093131 | -4,361.220253 |
| stop_gap | 3 | -1.370942 | 0.177237 | 0.000000 | -1.548179 |
| trailing_take_profit | 885 | 3,344.178892 | 223.796591 | 0.259650 | 3,120.641951 |
| trailing_take_profit_gap | 143 | 563.443920 | 34.895146 | 0.300845 | 528.849619 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 987.423296 | -12.576704 | -1.257670 | False |
| 2025-12 | 987.423296 | 828.813512 | -158.609784 | -16.062998 | False |
| 2026-01 | 828.813512 | 821.243028 | -7.570484 | -0.913412 | False |
| 2026-02 | 821.243028 | 743.731587 | -77.511440 | -9.438307 | False |
| 2026-03 | 743.731587 | 593.259472 | -150.472115 | -20.232046 | False |
| 2026-04 | 593.259472 | 583.348501 | -9.910972 | -1.670596 | False |
| 2026-05 | 583.348501 | 480.441158 | -102.907343 | -17.640800 | False |
| 2026-06 | 480.441158 | 473.009863 | -7.431295 | -1.546765 | False |
| 2026-07 | 473.009863 | 402.574641 | -70.435222 | -14.890857 | False |
| 2026-08 | 402.574641 | 435.401684 | 32.827043 | 8.154275 | False |
| 2026-09 | 435.401684 | 306.787948 | -128.613736 | -29.539099 | False |
| 2026-10 | 306.787948 | 273.263155 | -33.524793 | -10.927676 | False |
| 2026-11 | 273.263155 | 285.691505 | 12.428350 | 4.548125 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
