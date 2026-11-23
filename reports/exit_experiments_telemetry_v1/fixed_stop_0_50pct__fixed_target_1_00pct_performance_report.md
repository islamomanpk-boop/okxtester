# Performance report: fixed_stop_0_50pct__fixed_target_1_00pct

## Run metadata
- Experiment Id: fixed_stop_0_50pct__fixed_target_1_00pct
- Stop Model: fixed_stop_0_50pct
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
- Trade Telemetry Version: trailing_exit_telemetry_v1
- Risk Fraction: 0.005000
- Max Gross Leverage: 1.000000
- End Of Data Policy: Open positions forcibly closed at final available candle

## Portfolio risk and return

- Initial Equity: 1,000.000000
- Final Equity: 40.850131
- Net Pnl: -959.149869
- Total Return Pct: -95.914987
- Max Drawdown Amount: 992.002381
- Max Drawdown Pct: 96.048264
- Recovery Factor: -0.966883
- Sharpe Ratio: -7.379208
- Sortino Ratio: -7.395423
- Cagr Pct: -94.783214
- Calmar Ratio: -0.986829
- Worst Daily Loss: -71.058649
- Worst Daily Loss Pct: -8.157192
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 42.299850
- Max Capital Utilization Pct: 101.868819
- Max Gross Exposure: 1,034.030447
- Max Gross Exposure Equity Multiple: 1.018688

## Trade performance

- Trade Count: 5026
- Net Pnl: -959.149869
- Gross Pnl: -74.127200
- Total Fees: 886.391482
- Funding Pnl: 1.368814
- Winning Trades: 1717
- Losing Trades: 3309
- Breakeven Trades: 0
- Win Rate Pct: 34.162356
- Profit Factor: 0.735113
- Expectancy: -0.190838
- Average Win: 1.550282
- Average Loss: 1.094284
- Payoff Ratio: 1.416710
- Max Consecutive Losses: 33
- Average Duration Minutes: 92.472742
- Median Duration Minutes: 36.000000
- Max Duration Minutes: 3,366.000000
- Recovery Factor: -0.966883

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1000 | -128.612756 | -14.439374 | 114.165719 | -0.007662 | 32.600000 | 0.725545 | -0.128613 | 1.042939 | 0.695269 | 1.500053 |
| BTC | 734 | -108.816324 | 18.635134 | 127.764867 | 0.313409 | 35.422343 | 0.786412 | -0.148251 | 1.540966 | 1.074826 | 1.433689 |
| DOGE | 1161 | -233.160324 | -5.820225 | 227.949360 | 0.609261 | 35.228252 | 0.748215 | -0.200827 | 1.694056 | 1.231422 | 1.375691 |
| ETH | 877 | -218.685056 | -34.853150 | 183.777584 | -0.054322 | 33.409350 | 0.711861 | -0.249356 | 1.843931 | 1.299584 | 1.418863 |
| SOL | 1254 | -269.875409 | -37.649585 | 232.733952 | 0.508128 | 34.210526 | 0.718269 | -0.215212 | 1.603832 | 1.161114 | 1.381287 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1730 | -371.719900 | -61.895262 | 309.148220 | -0.676418 | 32.890173 | 0.709044 | -0.214867 | 1.592022 | 1.100414 | 1.446748 |
| SHORT | 3296 | -587.429969 | -12.231939 | 577.243262 | 2.045232 | 34.830097 | 0.749326 | -0.178225 | 1.529594 | 1.090970 | 1.402049 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 309 | -60.268067 | -25.392845 | 34.734420 | -0.140802 | 28.802589 | 0.601629 | -0.195042 | 1.022679 | 0.687666 | 1.487174 |
| AVAX | SHORT | 691 | -68.344689 | 10.953471 | 79.431300 | 0.133140 | 34.298119 | 0.784622 | -0.098907 | 1.050548 | 0.698953 | 1.503031 |
| BTC | LONG | 272 | -25.504336 | 24.328884 | 49.622913 | -0.210308 | 36.029412 | 0.866356 | -0.093766 | 1.687083 | 1.096773 | 1.538225 |
| BTC | SHORT | 462 | -83.311988 | -5.693750 | 78.141954 | 0.523717 | 35.064935 | 0.738530 | -0.180329 | 1.452574 | 1.062097 | 1.367648 |
| DOGE | LONG | 262 | -47.064707 | -7.299624 | 39.502905 | -0.262178 | 32.061069 | 0.711503 | -0.179636 | 1.381821 | 0.916504 | 1.507709 |
| DOGE | SHORT | 899 | -186.095617 | 1.479399 | 188.446455 | 0.871439 | 36.151279 | 0.756065 | -0.207003 | 1.774757 | 1.329080 | 1.335328 |
| ETH | LONG | 371 | -95.589907 | -27.294671 | 68.018492 | -0.276744 | 33.153639 | 0.666745 | -0.257655 | 1.554856 | 1.156601 | 1.344331 |
| ETH | SHORT | 506 | -123.095149 | -7.558479 | 115.759093 | 0.222422 | 33.596838 | 0.739271 | -0.243271 | 2.053086 | 1.405118 | 1.461148 |
| SOL | LONG | 516 | -143.292883 | -26.237006 | 117.269491 | 0.213614 | 33.914729 | 0.704843 | -0.277699 | 1.955359 | 1.423697 | 1.373437 |
| SOL | SHORT | 738 | -126.582526 | -11.412579 | 115.464461 | 0.294514 | 34.417344 | 0.732066 | -0.171521 | 1.361639 | 0.976113 | 1.394960 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | 0.001928 | 0.033029 | 0.000000 | -0.031101 |
| stop | 3299 | -3,034.194519 | 583.912957 | 0.763536 | -3,617.343940 |
| stop_gap | 9 | -3.045655 | 0.578670 | 0.015099 | -3.609225 |
| target | 1715 | 2,962.002029 | 301.754240 | 0.590178 | 2,660.837968 |
| target_gap | 2 | 1.109016 | 0.112587 | 0.000000 | 0.996429 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 933.516373 | -66.483627 | -6.648363 | False |
| 2025-12 | 933.516373 | 721.910406 | -211.605967 | -22.667622 | False |
| 2026-01 | 721.910406 | 613.903374 | -108.007032 | -14.961279 | False |
| 2026-02 | 613.903374 | 439.590148 | -174.313226 | -28.394245 | False |
| 2026-03 | 439.590148 | 301.338344 | -138.251804 | -31.450160 | False |
| 2026-04 | 301.338344 | 236.840501 | -64.497844 | -21.403796 | False |
| 2026-05 | 236.840501 | 183.907972 | -52.932528 | -22.349441 | False |
| 2026-06 | 183.907972 | 160.942936 | -22.965036 | -12.487244 | False |
| 2026-07 | 160.942936 | 123.008693 | -37.934243 | -23.569995 | False |
| 2026-08 | 123.008693 | 106.712237 | -16.296457 | -13.248215 | False |
| 2026-09 | 106.712237 | 59.621520 | -47.090717 | -44.128694 | False |
| 2026-10 | 59.621520 | 48.090819 | -11.530702 | -19.339831 | False |
| 2026-11 | 48.090819 | 40.850131 | -7.240688 | -15.056279 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
