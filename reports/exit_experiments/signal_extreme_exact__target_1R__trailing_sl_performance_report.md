# Performance report: signal_extreme_exact__target_1R__trailing_sl

## Run metadata
- Experiment Id: signal_extreme_exact__target_1R__trailing_sl
- Stop Model: signal_extreme_exact
- Target Model: target_1R
- Target Value: 1.000000
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
- Final Equity: 1.087679
- Net Pnl: -998.912321
- Total Return Pct: -99.891232
- Max Drawdown Amount: 1,013.870751
- Max Drawdown Pct: 99.892835
- Recovery Factor: -0.985246
- Sharpe Ratio: -14.664257
- Sortino Ratio: -11.807212
- Cagr Pct: -99.816711
- Calmar Ratio: -0.999238
- Worst Daily Loss: -68.036489
- Worst Daily Loss Pct: -7.307998
- Worst Daily Loss Date Utc: 2025-11-18
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 31.117208
- Max Capital Utilization Pct: 102.362562
- Max Gross Exposure: 1,009.573898
- Max Gross Exposure Equity Multiple: 1.023626

## Trade performance

- Trade Count: 7549
- Net Pnl: -998.912321
- Gross Pnl: -232.865600
- Total Fees: 766.727819
- Funding Pnl: 0.681098
- Winning Trades: 3354
- Losing Trades: 4195
- Breakeven Trades: 0
- Win Rate Pct: 44.429726
- Profit Factor: 0.503614
- Expectancy: -0.132324
- Average Win: 0.302164
- Average Loss: 0.479707
- Payoff Ratio: 0.629893
- Max Consecutive Losses: 20
- Average Duration Minutes: 42.584051
- Median Duration Minutes: 15.000000
- Max Duration Minutes: 4,012.000000
- Recovery Factor: -0.985246

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1385 | -138.792229 | -42.206520 | 96.521015 | -0.064694 | 46.064982 | 0.442221 | -0.100211 | 0.172473 | 0.333106 | 0.517773 |
| BTC | 1415 | -210.199423 | -54.896418 | 155.409207 | 0.106201 | 40.706714 | 0.424326 | -0.148551 | 0.268987 | 0.435204 | 0.618072 |
| DOGE | 1781 | -203.183818 | -33.254772 | 170.221800 | 0.292754 | 45.423919 | 0.548178 | -0.114084 | 0.304716 | 0.462653 | 0.658627 |
| ETH | 1275 | -213.855870 | -61.052655 | 152.766982 | -0.036232 | 43.686275 | 0.505436 | -0.167730 | 0.392383 | 0.602247 | 0.651532 |
| SOL | 1693 | -232.880982 | -41.455235 | 191.808815 | 0.383068 | 45.717661 | 0.548936 | -0.137555 | 0.366165 | 0.561799 | 0.651773 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2720 | -279.881657 | -40.730442 | 239.034080 | -0.117136 | 43.676471 | 0.506973 | -0.102898 | 0.242255 | 0.370549 | 0.653774 |
| SHORT | 4829 | -719.030664 | -192.135158 | 527.693739 | 0.798233 | 44.854007 | 0.502294 | -0.148898 | 0.335023 | 0.542505 | 0.617549 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 402 | -33.287083 | -14.865597 | 18.400814 | -0.020671 | 44.029851 | 0.330871 | -0.082804 | 0.092993 | 0.221097 | 0.420598 |
| AVAX | SHORT | 983 | -105.505146 | -27.340923 | 78.120200 | -0.044023 | 46.897253 | 0.470045 | -0.107330 | 0.202989 | 0.381385 | 0.532242 |
| BTC | LONG | 553 | -47.170604 | 1.074313 | 48.209386 | -0.035531 | 40.144665 | 0.501846 | -0.085299 | 0.214055 | 0.286075 | 0.748248 |
| BTC | SHORT | 862 | -163.028820 | -55.970731 | 107.199821 | 0.141732 | 41.067285 | 0.397184 | -0.189129 | 0.303436 | 0.532373 | 0.569970 |
| DOGE | LONG | 432 | -25.703555 | -5.377532 | 20.232199 | -0.093825 | 46.064815 | 0.468732 | -0.059499 | 0.113960 | 0.207646 | 0.548817 |
| DOGE | SHORT | 1349 | -177.480263 | -27.877240 | 149.989602 | 0.386579 | 45.218681 | 0.557756 | -0.131564 | 0.366946 | 0.543055 | 0.675707 |
| ETH | LONG | 610 | -47.054936 | 6.541159 | 53.537148 | -0.058947 | 43.770492 | 0.615262 | -0.077139 | 0.281831 | 0.356571 | 0.790393 |
| ETH | SHORT | 665 | -166.800933 | -67.593814 | 99.229834 | 0.022715 | 43.609023 | 0.462122 | -0.250828 | 0.494167 | 0.826958 | 0.597572 |
| SOL | LONG | 723 | -126.665479 | -28.102785 | 98.654533 | 0.091838 | 44.674965 | 0.498469 | -0.175194 | 0.389758 | 0.631394 | 0.617299 |
| SOL | SHORT | 970 | -106.215503 | -13.352450 | 93.154283 | 0.291230 | 46.494845 | 0.597265 | -0.109501 | 0.349269 | 0.508161 | 0.687319 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| stop | 3937 | -1,581.766047 | 410.896914 | 0.235618 | -1,992.427343 |
| stop_gap | 27 | -8.957885 | 3.152929 | 0.005596 | -12.105218 |
| target | 3573 | 1,354.564249 | 351.606250 | 0.439884 | 1,003.397883 |
| target_gap | 12 | 3.294083 | 1.071726 | 0.000000 | 2.222357 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 630.626345 | -369.373655 | -36.937365 | False |
| 2025-12 | 630.626345 | 405.236451 | -225.389894 | -35.740640 | False |
| 2026-01 | 405.236451 | 270.251360 | -134.985091 | -33.310205 | False |
| 2026-02 | 270.251360 | 198.236207 | -72.015153 | -26.647471 | False |
| 2026-03 | 198.236207 | 100.769235 | -97.466972 | -49.167089 | False |
| 2026-04 | 100.769235 | 57.004740 | -43.764495 | -43.430413 | False |
| 2026-05 | 57.004740 | 31.657399 | -25.347341 | -44.465322 | False |
| 2026-06 | 31.657399 | 19.320819 | -12.336580 | -38.969026 | False |
| 2026-07 | 19.320819 | 10.106296 | -9.214523 | -47.692199 | False |
| 2026-08 | 10.106296 | 7.567043 | -2.539253 | -25.125455 | False |
| 2026-09 | 7.567043 | 3.953232 | -3.613811 | -47.757243 | False |
| 2026-10 | 3.953232 | 1.940440 | -2.012792 | -50.915108 | False |
| 2026-11 | 1.940440 | 1.087679 | -0.852761 | -43.946778 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
