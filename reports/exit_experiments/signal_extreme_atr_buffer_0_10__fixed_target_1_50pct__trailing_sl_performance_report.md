# Performance report: signal_extreme_atr_buffer_0_10__fixed_target_1_50pct__trailing_sl

## Run metadata
- Experiment Id: signal_extreme_atr_buffer_0_10__fixed_target_1_50pct__trailing_sl
- Stop Model: signal_extreme_atr_buffer_0_10
- Target Model: fixed_target_1_50pct
- Target Value: 0.015000
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
- Final Equity: 8.412746
- Net Pnl: -991.587254
- Total Return Pct: -99.158725
- Max Drawdown Amount: 1,010.143646
- Max Drawdown Pct: 99.174052
- Recovery Factor: -0.981630
- Sharpe Ratio: -10.861637
- Sortino Ratio: -9.913697
- Cagr Pct: -98.787647
- Calmar Ratio: -0.996104
- Worst Daily Loss: -60.763960
- Worst Daily Loss Pct: -8.071738
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 34.102737
- Max Capital Utilization Pct: 102.390539
- Max Gross Exposure: 1,013.385326
- Max Gross Exposure Equity Multiple: 1.023905

## Trade performance

- Trade Count: 6324
- Net Pnl: -991.587254
- Gross Pnl: -112.157435
- Total Fees: 880.165029
- Funding Pnl: 0.735210
- Winning Trades: 2201
- Losing Trades: 4123
- Breakeven Trades: 0
- Win Rate Pct: 34.803922
- Profit Factor: 0.611506
- Expectancy: -0.156797
- Average Win: 0.709133
- Average Loss: 0.619061
- Payoff Ratio: 1.145498
- Max Consecutive Losses: 24
- Average Duration Minutes: 57.058982
- Median Duration Minutes: 26.000000
- Max Duration Minutes: 2,718.000000
- Recovery Factor: -0.981630

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1133 | -113.731978 | -9.014637 | 104.829426 | 0.112084 | 35.127979 | 0.624415 | -0.100381 | 0.475078 | 0.411990 | 1.153128 |
| BTC | 1177 | -207.606496 | -34.299725 | 173.325945 | 0.019175 | 32.455395 | 0.534598 | -0.176386 | 0.624275 | 0.561107 | 1.112579 |
| DOGE | 1499 | -188.825011 | 17.471124 | 206.647056 | 0.350920 | 35.223482 | 0.680784 | -0.125967 | 0.762693 | 0.609194 | 1.251972 |
| ETH | 1077 | -198.166543 | -27.121469 | 170.928980 | -0.116094 | 35.654596 | 0.621308 | -0.183999 | 0.846682 | 0.755112 | 1.121267 |
| SOL | 1438 | -283.257225 | -59.192729 | 224.433622 | 0.369126 | 35.396384 | 0.588694 | -0.196980 | 0.796503 | 0.741310 | 1.074453 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2217 | -371.851062 | -48.047131 | 323.387887 | -0.416043 | 32.611637 | 0.562104 | -0.167727 | 0.660202 | 0.568391 | 1.161526 |
| SHORT | 4107 | -619.736192 | -64.110303 | 556.777142 | 1.151254 | 35.987339 | 0.636137 | -0.150898 | 0.733069 | 0.647856 | 1.131532 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 326 | -49.960730 | -21.789532 | 28.134792 | -0.036406 | 29.754601 | 0.375257 | -0.153254 | 0.309374 | 0.349214 | 0.885915 |
| AVAX | SHORT | 807 | -63.771248 | 12.774896 | 76.694634 | 0.148490 | 37.298637 | 0.713829 | -0.079023 | 0.528477 | 0.440401 | 1.199991 |
| BTC | LONG | 461 | -74.582092 | -8.100422 | 66.343297 | -0.138373 | 31.670282 | 0.497877 | -0.161783 | 0.506516 | 0.471535 | 1.074186 |
| BTC | SHORT | 716 | -133.024403 | -26.199303 | 106.982648 | 0.157548 | 32.960894 | 0.552929 | -0.185788 | 0.697126 | 0.619888 | 1.124600 |
| DOGE | LONG | 339 | -37.586925 | -5.210609 | 32.223284 | -0.153032 | 33.628319 | 0.566868 | -0.110876 | 0.431512 | 0.385686 | 1.118817 |
| DOGE | SHORT | 1160 | -151.238086 | 22.681733 | 174.423771 | 0.503952 | 35.689655 | 0.700369 | -0.130378 | 0.853888 | 0.676605 | 1.262017 |
| ETH | LONG | 498 | -59.555521 | 16.072595 | 75.402816 | -0.225301 | 33.534137 | 0.692723 | -0.119589 | 0.803960 | 0.585549 | 1.373001 |
| ETH | SHORT | 579 | -138.611022 | -43.194064 | 95.526164 | 0.109206 | 37.478411 | 0.579298 | -0.239397 | 0.879560 | 0.910153 | 0.966386 |
| SOL | LONG | 593 | -150.165793 | -29.019164 | 121.283697 | 0.137068 | 33.558179 | 0.558436 | -0.253231 | 0.954329 | 0.863140 | 1.105648 |
| SOL | SHORT | 845 | -133.091432 | -30.173565 | 103.149925 | 0.232058 | 36.686391 | 0.618212 | -0.157505 | 0.695189 | 0.651589 | 1.066914 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| stop | 5673 | -1,167.761201 | 800.096734 | 0.606667 | -1,967.251268 |
| stop_gap | 83 | 13.022257 | 9.873359 | -0.002942 | 3.145956 |
| target | 568 | 1,042.581509 | 70.194936 | 0.131486 | 972.518059 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 808.162255 | -191.837745 | -19.183774 | False |
| 2025-12 | 808.162255 | 585.392070 | -222.770185 | -27.565032 | False |
| 2026-01 | 585.392070 | 456.529974 | -128.862096 | -22.012955 | False |
| 2026-02 | 456.529974 | 342.396687 | -114.133287 | -25.000174 | False |
| 2026-03 | 342.396687 | 185.456794 | -156.939893 | -45.835693 | False |
| 2026-04 | 185.456794 | 122.440648 | -63.016146 | -33.978882 | False |
| 2026-05 | 122.440648 | 82.593726 | -39.846922 | -32.543867 | False |
| 2026-06 | 82.593726 | 56.544664 | -26.049063 | -31.538791 | False |
| 2026-07 | 56.544664 | 38.159685 | -18.384979 | -32.514083 | False |
| 2026-08 | 38.159685 | 32.234408 | -5.925277 | -15.527585 | False |
| 2026-09 | 32.234408 | 19.013944 | -13.220463 | -41.013514 | False |
| 2026-10 | 19.013944 | 11.425635 | -7.588309 | -39.909181 | False |
| 2026-11 | 11.425635 | 8.412746 | -3.012889 | -26.369551 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
