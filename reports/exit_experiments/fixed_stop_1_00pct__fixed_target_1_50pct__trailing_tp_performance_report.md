# Performance report: fixed_stop_1_00pct__fixed_target_1_50pct__trailing_tp

## Run metadata
- Experiment Id: fixed_stop_1_00pct__fixed_target_1_50pct__trailing_tp
- Stop Model: fixed_stop_1_00pct
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
- Final Equity: 465.143126
- Net Pnl: -534.856874
- Total Return Pct: -53.485687
- Max Drawdown Amount: 640.979817
- Max Drawdown Pct: 60.230157
- Recovery Factor: -0.834436
- Sharpe Ratio: -2.146037
- Sortino Ratio: -2.727923
- Cagr Pct: -50.681704
- Calmar Ratio: -0.841467
- Worst Daily Loss: -62.918493
- Worst Daily Loss Pct: -6.409426
- Worst Daily Loss Date Utc: 2026-02-06
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 40.259727
- Max Capital Utilization Pct: 102.861776
- Max Gross Exposure: 1,060.357998
- Max Gross Exposure Equity Multiple: 1.028618

## Trade performance

- Trade Count: 2529
- Net Pnl: -534.856874
- Gross Pnl: 91.046120
- Total Fees: 627.320852
- Funding Pnl: 1.417859
- Winning Trades: 1052
- Losing Trades: 1477
- Breakeven Trades: 0
- Win Rate Pct: 41.597469
- Profit Factor: 0.870734
- Expectancy: -0.211489
- Average Win: 3.424716
- Average Loss: 2.801393
- Payoff Ratio: 1.222504
- Max Consecutive Losses: 25
- Average Duration Minutes: 256.082641
- Median Duration Minutes: 113.000000
- Max Duration Minutes: 5,126.000000
- Recovery Factor: -0.834436

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 521 | -113.970948 | -0.995144 | 112.851128 | -0.124676 | 40.882917 | 0.849413 | -0.218754 | 3.018185 | 2.457287 | 1.228259 |
| BTC | 349 | -7.525948 | 81.669730 | 89.192281 | -0.003396 | 42.693410 | 0.986652 | -0.021564 | 3.733590 | 2.819155 | 1.324365 |
| DOGE | 571 | -120.030583 | 22.416206 | 143.416422 | 0.969633 | 42.907180 | 0.874115 | -0.210211 | 3.401903 | 2.924837 | 1.163109 |
| ETH | 461 | -189.461555 | -67.537966 | 122.116529 | 0.192940 | 39.479393 | 0.770987 | -0.410980 | 3.504579 | 2.965215 | 1.181897 |
| SOL | 627 | -103.867841 | 55.493293 | 159.744492 | 0.383359 | 41.945774 | 0.899760 | -0.165658 | 3.544955 | 2.846679 | 1.245295 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 796 | -162.417265 | 45.547725 | 205.863363 | -2.101628 | 40.326633 | 0.881194 | -0.204042 | 3.752832 | 2.878055 | 1.303947 |
| SHORT | 1733 | -372.439609 | 45.498394 | 421.457490 | 3.519487 | 42.181189 | 0.865574 | -0.214910 | 3.280632 | 2.765052 | 1.186463 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 151 | -65.199158 | -29.107080 | 35.753454 | -0.338624 | 36.423841 | 0.743847 | -0.431783 | 3.442421 | 2.651378 | 1.298352 |
| AVAX | SHORT | 370 | -48.771790 | 28.111936 | 77.097674 | 0.213948 | 42.702703 | 0.902905 | -0.131816 | 2.870508 | 2.369396 | 1.211493 |
| BTC | LONG | 110 | 7.826465 | 41.508741 | 32.817593 | -0.864683 | 42.727273 | 1.037140 | 0.071150 | 4.650053 | 3.344857 | 1.390210 |
| BTC | SHORT | 239 | -15.352413 | 40.160989 | 56.374688 | 0.861287 | 42.677824 | 0.956522 | -0.064236 | 3.311299 | 2.577408 | 1.284740 |
| DOGE | LONG | 132 | 0.379658 | 30.668203 | 29.617436 | -0.671109 | 43.181818 | 1.002041 | 0.002876 | 3.270467 | 2.480493 | 1.318475 |
| DOGE | SHORT | 439 | -120.410241 | -8.251997 | 113.798986 | 1.640742 | 42.824601 | 0.843106 | -0.274283 | 3.441754 | 3.057609 | 1.125636 |
| ETH | LONG | 172 | -38.773859 | 7.541585 | 45.769228 | -0.546216 | 40.697674 | 0.868463 | -0.225429 | 3.657162 | 2.889953 | 1.265475 |
| ETH | SHORT | 289 | -150.687696 | -75.079551 | 76.347301 | 0.739156 | 38.754325 | 0.717029 | -0.521411 | 3.409215 | 3.008586 | 1.133162 |
| SOL | LONG | 231 | -66.650371 | -5.063724 | 61.905651 | 0.319004 | 39.826840 | 0.841688 | -0.288530 | 3.851690 | 3.028819 | 1.271680 |
| SOL | SHORT | 396 | -37.217470 | 60.557017 | 97.838841 | 0.064355 | 43.181818 | 0.939502 | -0.093984 | 3.379929 | 2.734157 | 1.236187 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 2 | -2.311622 | 0.419083 | -0.001163 | -2.731868 |
| stop | 1473 | -3,762.297788 | 369.465404 | 0.726928 | -4,131.036265 |
| stop_gap | 2 | -3.544646 | 0.345415 | 0.000000 | -3.890061 |
| trailing_take_profit | 960 | 3,490.969775 | 234.919110 | 0.290142 | 3,256.340806 |
| trailing_take_profit_gap | 92 | 368.230401 | 22.171840 | 0.401953 | 346.460514 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 1,026.447218 | 26.447218 | 2.644722 | False |
| 2025-12 | 1,026.447218 | 897.984536 | -128.462682 | -12.515274 | False |
| 2026-01 | 897.984536 | 889.042408 | -8.942128 | -0.995800 | False |
| 2026-02 | 889.042408 | 781.874357 | -107.168051 | -12.054324 | False |
| 2026-03 | 781.874357 | 647.315525 | -134.558832 | -17.209777 | False |
| 2026-04 | 647.315525 | 630.865425 | -16.450100 | -2.541280 | False |
| 2026-05 | 630.865425 | 565.703229 | -65.162196 | -10.329017 | False |
| 2026-06 | 565.703229 | 571.378462 | 5.675233 | 1.003217 | False |
| 2026-07 | 571.378462 | 503.211028 | -68.167435 | -11.930347 | False |
| 2026-08 | 503.211028 | 579.099769 | 75.888741 | 15.080898 | False |
| 2026-09 | 579.099769 | 479.932309 | -99.167460 | -17.124417 | False |
| 2026-10 | 479.932309 | 451.785900 | -28.146409 | -5.864662 | False |
| 2026-11 | 451.785900 | 465.143126 | 13.357226 | 2.956539 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
