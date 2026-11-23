# Performance report: signal_extreme_exact__target_2R__trailing_tp

## Run metadata
- Experiment Id: signal_extreme_exact__target_2R__trailing_tp
- Stop Model: signal_extreme_exact
- Target Model: target_2R
- Target Value: 2.000000
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
- Final Equity: 24.815562
- Net Pnl: -975.184438
- Total Return Pct: -97.518444
- Max Drawdown Amount: 997.821833
- Max Drawdown Pct: 97.625989
- Recovery Factor: -0.977313
- Sharpe Ratio: -8.973492
- Sortino Ratio: -8.715580
- Cagr Pct: -96.707784
- Calmar Ratio: -0.990595
- Worst Daily Loss: -56.266189
- Worst Daily Loss Pct: -7.468726
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 38.016773
- Max Capital Utilization Pct: 102.362167
- Max Gross Exposure: 1,014.224021
- Max Gross Exposure Equity Multiple: 1.023622

## Trade performance

- Trade Count: 5127
- Net Pnl: -975.184438
- Gross Pnl: -101.260186
- Total Fees: 874.668460
- Funding Pnl: 0.744207
- Winning Trades: 1641
- Losing Trades: 3486
- Breakeven Trades: 0
- Win Rate Pct: 32.007022
- Profit Factor: 0.670086
- Expectancy: -0.190206
- Average Win: 1.207004
- Average Loss: 0.847928
- Payoff Ratio: 1.423474
- Max Consecutive Losses: 31
- Average Duration Minutes: 86.833821
- Median Duration Minutes: 28.000000
- Max Duration Minutes: 8,591.000000
- Recovery Factor: -0.977313

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 988 | -132.936443 | -17.108543 | 115.789357 | -0.038543 | 31.477733 | 0.658108 | -0.134551 | 0.822795 | 0.574336 | 1.432601 |
| BTC | 927 | -218.446561 | -39.637225 | 178.795617 | -0.013719 | 31.930960 | 0.589736 | -0.235649 | 1.060836 | 0.843826 | 1.257174 |
| DOGE | 1198 | -196.959566 | 3.932808 | 201.336970 | 0.444595 | 33.472454 | 0.719807 | -0.164407 | 1.261805 | 0.881987 | 1.430639 |
| ETH | 909 | -204.109836 | -30.147578 | 173.883997 | -0.078261 | 30.363036 | 0.672310 | -0.224543 | 1.517264 | 0.984004 | 1.541928 |
| SOL | 1105 | -222.732032 | -18.299648 | 204.862519 | 0.430135 | 32.307692 | 0.685753 | -0.201567 | 1.361481 | 0.947568 | 1.436816 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1723 | -385.029594 | -51.890112 | 332.532290 | -0.607192 | 30.876378 | 0.631729 | -0.223465 | 1.241500 | 0.877840 | 1.414266 |
| SHORT | 3404 | -590.154844 | -49.370073 | 542.136170 | 1.351399 | 32.579318 | 0.691078 | -0.173371 | 1.190456 | 0.832406 | 1.430140 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 277 | -50.244033 | -13.632552 | 36.557891 | -0.053590 | 29.241877 | 0.561463 | -0.181386 | 0.794172 | 0.584551 | 1.358602 |
| AVAX | SHORT | 711 | -82.692410 | -3.475991 | 79.231466 | 0.015047 | 32.348805 | 0.698482 | -0.116304 | 0.832875 | 0.570174 | 1.460739 |
| BTC | LONG | 365 | -81.360258 | -10.805047 | 70.335326 | -0.219885 | 31.506849 | 0.578291 | -0.222905 | 0.970172 | 0.771720 | 1.257155 |
| BTC | SHORT | 562 | -137.086304 | -28.832179 | 108.460291 | 0.206166 | 32.206406 | 0.596240 | -0.243926 | 1.118439 | 0.891139 | 1.255068 |
| DOGE | LONG | 272 | -46.757745 | -7.207630 | 39.244393 | -0.305721 | 31.250000 | 0.637745 | -0.171903 | 0.968428 | 0.690236 | 1.403039 |
| DOGE | SHORT | 926 | -150.201822 | 11.140439 | 162.092577 | 0.750316 | 34.125270 | 0.738265 | -0.162205 | 1.340719 | 0.940769 | 1.425131 |
| ETH | LONG | 385 | -87.396905 | -17.064806 | 70.023642 | -0.308457 | 29.870130 | 0.622090 | -0.227005 | 1.251017 | 0.856533 | 1.460559 |
| ETH | SHORT | 524 | -116.712931 | -13.082771 | 103.860355 | 0.230195 | 30.725191 | 0.701967 | -0.222735 | 1.707440 | 1.078818 | 1.582696 |
| SOL | LONG | 424 | -119.270655 | -3.180077 | 116.371039 | 0.280461 | 32.075472 | 0.684191 | -0.281299 | 1.899976 | 1.311345 | 1.448876 |
| SOL | SHORT | 681 | -103.461378 | -15.119571 | 88.491480 | 0.149674 | 32.452276 | 0.687535 | -0.151926 | 1.030099 | 0.719811 | 1.431068 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | -0.092813 | 0.009268 | 0.000442 | -0.101638 |
| stop | 3447 | -2,343.078586 | 594.279908 | -0.103185 | -2,937.461679 |
| stop_gap | 23 | -11.490189 | 4.378457 | 0.021126 | -15.847520 |
| trailing_take_profit | 1318 | 1,846.266387 | 216.598421 | 0.718921 | 1,630.386887 |
| trailing_take_profit_gap | 338 | 407.135016 | 59.402406 | 0.106902 | 347.839513 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 805.570819 | -194.429181 | -19.442918 | False |
| 2025-12 | 805.570819 | 638.257677 | -167.313142 | -20.769514 | False |
| 2026-01 | 638.257677 | 535.166515 | -103.091162 | -16.151966 | False |
| 2026-02 | 535.166515 | 449.976319 | -85.190197 | -15.918447 | False |
| 2026-03 | 449.976319 | 286.802054 | -163.174265 | -36.262856 | False |
| 2026-04 | 286.802054 | 214.066395 | -72.735659 | -25.360927 | False |
| 2026-05 | 214.066395 | 136.890185 | -77.176210 | -36.052464 | False |
| 2026-06 | 136.890185 | 112.488827 | -24.401358 | -17.825498 | False |
| 2026-07 | 112.488827 | 74.476755 | -38.012072 | -33.791864 | False |
| 2026-08 | 74.476755 | 66.429387 | -8.047368 | -10.805208 | False |
| 2026-09 | 66.429387 | 42.750896 | -23.678491 | -35.644603 | False |
| 2026-10 | 42.750896 | 29.482632 | -13.268263 | -31.036223 | False |
| 2026-11 | 29.482632 | 24.815562 | -4.667070 | -15.829897 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
