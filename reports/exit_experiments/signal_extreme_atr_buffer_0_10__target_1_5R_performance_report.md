# Performance report: signal_extreme_atr_buffer_0_10__target_1_5R

## Run metadata
- Experiment Id: signal_extreme_atr_buffer_0_10__target_1_5R
- Stop Model: signal_extreme_atr_buffer_0_10
- Target Model: target_1_5R
- Target Value: 1.500000
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
- Final Equity: 17.661676
- Net Pnl: -982.338324
- Total Return Pct: -98.233832
- Max Drawdown Amount: 1,005.715349
- Max Drawdown Pct: 98.274177
- Recovery Factor: -0.976756
- Sharpe Ratio: -9.635312
- Sortino Ratio: -9.244242
- Cagr Pct: -97.595134
- Calmar Ratio: -0.993090
- Worst Daily Loss: -58.597751
- Worst Daily Loss Pct: -7.872325
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 37.077393
- Max Capital Utilization Pct: 102.508170
- Max Gross Exposure: 1,012.568772
- Max Gross Exposure Equity Multiple: 1.025082

## Trade performance

- Trade Count: 5406
- Net Pnl: -982.338324
- Gross Pnl: -159.834260
- Total Fees: 823.182569
- Funding Pnl: 0.678505
- Winning Trades: 2098
- Losing Trades: 3308
- Breakeven Trades: 0
- Win Rate Pct: 38.808731
- Profit Factor: 0.654820
- Expectancy: -0.181713
- Average Win: 0.888243
- Average Loss: 0.860300
- Payoff Ratio: 1.032481
- Max Consecutive Losses: 22
- Average Duration Minutes: 78.546800
- Median Duration Minutes: 31.000000
- Max Duration Minutes: 4,051.000000
- Recovery Factor: -0.976756

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 971 | -131.956551 | -29.431441 | 102.463665 | -0.061444 | 37.590113 | 0.624803 | -0.135898 | 0.602034 | 0.580361 | 1.037343 |
| BTC | 1039 | -216.679309 | -40.365513 | 176.452852 | 0.139055 | 38.498556 | 0.592334 | -0.208546 | 0.787081 | 0.831787 | 0.946254 |
| DOGE | 1239 | -169.702227 | 20.495916 | 190.486987 | 0.288844 | 40.516546 | 0.738635 | -0.136967 | 0.955359 | 0.880994 | 1.084411 |
| ETH | 966 | -225.896809 | -63.402498 | 162.512875 | 0.018565 | 38.095238 | 0.632675 | -0.233848 | 1.057286 | 1.028391 | 1.028097 |
| SOL | 1191 | -238.103429 | -47.130724 | 191.266189 | 0.293485 | 38.874895 | 0.659069 | -0.199919 | 0.994142 | 0.959328 | 1.036289 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1901 | -382.022148 | -62.950813 | 318.522416 | -0.548918 | 37.716991 | 0.619284 | -0.200959 | 0.866678 | 0.847492 | 1.022639 |
| SHORT | 3505 | -600.316177 | -96.883448 | 504.660152 | 1.227423 | 39.400856 | 0.674174 | -0.171274 | 0.899440 | 0.867440 | 1.036890 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 284 | -57.666525 | -26.232746 | 31.366079 | -0.067699 | 33.098592 | 0.468058 | -0.203051 | 0.539799 | 0.570566 | 0.946076 |
| AVAX | SHORT | 687 | -74.290026 | -3.198695 | 71.097586 | 0.006255 | 39.446870 | 0.694646 | -0.108137 | 0.623621 | 0.584835 | 1.066320 |
| BTC | LONG | 396 | -72.705334 | -3.859990 | 68.671290 | -0.174053 | 39.141414 | 0.595755 | -0.183599 | 0.691285 | 0.746284 | 0.926302 |
| BTC | SHORT | 643 | -143.973976 | -36.505523 | 107.781561 | 0.313109 | 38.102644 | 0.590585 | -0.223910 | 0.847688 | 0.883561 | 0.959399 |
| DOGE | LONG | 300 | -39.925878 | -3.820215 | 35.872582 | -0.233081 | 39.666667 | 0.651065 | -0.133086 | 0.626017 | 0.632165 | 0.990275 |
| DOGE | SHORT | 939 | -129.776349 | 24.316131 | 154.614405 | 0.521925 | 40.788072 | 0.757369 | -0.138207 | 1.057687 | 0.961997 | 1.099470 |
| ETH | LONG | 430 | -82.855712 | -10.648947 | 72.008678 | -0.198087 | 37.441860 | 0.643017 | -0.192688 | 0.926981 | 0.862824 | 1.074357 |
| ETH | SHORT | 536 | -143.041096 | -52.753551 | 90.504198 | 0.216652 | 38.619403 | 0.626406 | -0.266868 | 1.158634 | 1.163764 | 0.995592 |
| SOL | LONG | 491 | -128.868699 | -18.388915 | 110.603787 | 0.124002 | 38.289206 | 0.650427 | -0.262462 | 1.275413 | 1.216655 | 1.048295 |
| SOL | SHORT | 700 | -109.234730 | -28.741810 | 80.662402 | 0.169482 | 39.285714 | 0.668729 | -0.156050 | 0.801854 | 0.775870 | 1.033491 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| stop | 3288 | -2,336.340738 | 507.317609 | 0.169952 | -2,843.488396 |
| stop_gap | 11 | -1.505417 | 0.483513 | -0.004933 | -1.993863 |
| target | 2103 | 2,176.936106 | 315.105844 | 0.513486 | 1,862.343748 |
| target_gap | 4 | 1.075789 | 0.275603 | 0.000000 | 0.800187 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 790.173647 | -209.826353 | -20.982635 | False |
| 2025-12 | 790.173647 | 588.635892 | -201.537755 | -25.505502 | False |
| 2026-01 | 588.635892 | 499.210155 | -89.425737 | -15.192029 | False |
| 2026-02 | 499.210155 | 397.781472 | -101.428683 | -20.317833 | False |
| 2026-03 | 397.781472 | 241.828701 | -155.952771 | -39.205640 | False |
| 2026-04 | 241.828701 | 168.685679 | -73.143022 | -30.245799 | False |
| 2026-05 | 168.685679 | 112.596125 | -56.089554 | -33.250928 | False |
| 2026-06 | 112.596125 | 88.298469 | -24.297656 | -21.579478 | False |
| 2026-07 | 88.298469 | 59.228108 | -29.070361 | -32.922837 | False |
| 2026-08 | 59.228108 | 52.739849 | -6.488259 | -10.954695 | False |
| 2026-09 | 52.739849 | 32.930159 | -19.809691 | -37.561144 | False |
| 2026-10 | 32.930159 | 21.693269 | -11.236890 | -34.123401 | False |
| 2026-11 | 21.693269 | 17.661676 | -4.031593 | -18.584534 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
