# Performance report: signal_extreme_atr_buffer_0_10__fixed_target_1_00pct__trailing_sl

## Run metadata
- Experiment Id: signal_extreme_atr_buffer_0_10__fixed_target_1_00pct__trailing_sl
- Stop Model: signal_extreme_atr_buffer_0_10
- Target Model: fixed_target_1_00pct
- Target Value: 0.010000
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
- Final Equity: 5.865928
- Net Pnl: -994.134072
- Total Return Pct: -99.413407
- Max Drawdown Amount: 1,009.039908
- Max Drawdown Pct: 99.422022
- Recovery Factor: -0.985228
- Sharpe Ratio: -11.923183
- Sortino Ratio: -10.485608
- Cagr Pct: -99.131031
- Calmar Ratio: -0.997073
- Worst Daily Loss: -57.108598
- Worst Daily Loss Pct: -8.215929
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 33.793602
- Max Capital Utilization Pct: 102.390474
- Max Gross Exposure: 1,007.757316
- Max Gross Exposure Equity Multiple: 1.023905

## Trade performance

- Trade Count: 6667
- Net Pnl: -994.134072
- Gross Pnl: -181.036005
- Total Fees: 813.906473
- Funding Pnl: 0.808406
- Winning Trades: 2404
- Losing Trades: 4263
- Breakeven Trades: 0
- Win Rate Pct: 36.058197
- Profit Factor: 0.580925
- Expectancy: -0.149113
- Average Win: 0.573242
- Average Loss: 0.556465
- Payoff Ratio: 1.030151
- Max Consecutive Losses: 24
- Average Duration Minutes: 52.285886
- Median Duration Minutes: 24.000000
- Max Duration Minutes: 3,470.000000
- Recovery Factor: -0.985228

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1246 | -123.539906 | -27.481261 | 96.124955 | 0.066310 | 36.516854 | 0.554275 | -0.099149 | 0.337640 | 0.350400 | 0.963585 |
| BTC | 1203 | -197.853781 | -35.919290 | 162.026487 | 0.091996 | 33.250208 | 0.530100 | -0.164467 | 0.558004 | 0.524353 | 1.064177 |
| DOGE | 1555 | -173.028440 | 14.675210 | 188.006775 | 0.303125 | 36.463023 | 0.684109 | -0.111272 | 0.660879 | 0.554399 | 1.192062 |
| ETH | 1142 | -216.946500 | -53.061582 | 163.814851 | -0.070067 | 36.602452 | 0.571024 | -0.189971 | 0.690873 | 0.698524 | 0.989047 |
| SOL | 1521 | -282.765445 | -79.249082 | 203.933405 | 0.417042 | 37.080868 | 0.544301 | -0.185908 | 0.598837 | 0.648390 | 0.923575 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2311 | -344.905473 | -60.574954 | 283.972287 | -0.358231 | 34.097793 | 0.538849 | -0.149245 | 0.511443 | 0.491085 | 1.041455 |
| SHORT | 4356 | -649.228599 | -120.461051 | 529.934186 | 1.166637 | 37.098255 | 0.600299 | -0.149042 | 0.603377 | 0.592805 | 1.017834 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 350 | -38.173307 | -15.089161 | 23.052896 | -0.031249 | 33.714286 | 0.417917 | -0.109067 | 0.232264 | 0.282675 | 0.821667 |
| AVAX | SHORT | 896 | -85.366599 | -12.392100 | 73.072058 | 0.097559 | 37.611607 | 0.596539 | -0.095275 | 0.374537 | 0.378507 | 0.989511 |
| BTC | LONG | 474 | -63.588651 | -2.433819 | 61.028527 | -0.126304 | 32.700422 | 0.518189 | -0.134153 | 0.441225 | 0.413726 | 1.066467 |
| BTC | SHORT | 729 | -134.265130 | -33.485471 | 100.997959 | 0.218300 | 33.607682 | 0.535538 | -0.184177 | 0.631885 | 0.597266 | 1.057962 |
| DOGE | LONG | 347 | -31.220943 | -2.939732 | 28.148524 | -0.132687 | 34.293948 | 0.586366 | -0.089974 | 0.371921 | 0.331051 | 1.123457 |
| DOGE | SHORT | 1208 | -141.807497 | 17.614943 | 159.858251 | 0.435811 | 37.086093 | 0.699730 | -0.117390 | 0.737633 | 0.621404 | 1.187042 |
| ETH | LONG | 507 | -61.485073 | 3.080078 | 64.372769 | -0.192382 | 34.911243 | 0.636606 | -0.121272 | 0.608541 | 0.512718 | 1.186893 |
| ETH | SHORT | 635 | -155.461427 | -56.141660 | 99.442082 | 0.122315 | 37.952756 | 0.538052 | -0.244821 | 0.751341 | 0.854149 | 0.879637 |
| SOL | LONG | 633 | -150.437499 | -43.192319 | 107.369571 | 0.124391 | 34.597156 | 0.507871 | -0.237658 | 0.708902 | 0.738375 | 0.960085 |
| SOL | SHORT | 888 | -132.327946 | -36.056763 | 96.563835 | 0.292652 | 38.851351 | 0.579674 | -0.149018 | 0.528969 | 0.579783 | 0.912357 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| stop | 5430 | -1,409.267254 | 680.898341 | 0.731941 | -2,089.433654 |
| stop_gap | 82 | 9.775584 | 8.968298 | 0.000000 | 0.807286 |
| target | 1153 | 1,218.176704 | 124.011514 | 0.076465 | 1,094.241655 |
| target_gap | 2 | 0.278960 | 0.028320 | 0.000000 | 0.250640 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 758.658159 | -241.341841 | -24.134184 | False |
| 2025-12 | 758.658159 | 523.817281 | -234.840878 | -30.954769 | False |
| 2026-01 | 523.817281 | 402.117050 | -121.700232 | -23.233337 | False |
| 2026-02 | 402.117050 | 300.325392 | -101.791658 | -25.313937 | False |
| 2026-03 | 300.325392 | 161.892509 | -138.432883 | -46.094299 | False |
| 2026-04 | 161.892509 | 102.885508 | -59.007000 | -36.448259 | False |
| 2026-05 | 102.885508 | 66.460777 | -36.424731 | -35.403170 | False |
| 2026-06 | 66.460777 | 44.713764 | -21.747013 | -32.721575 | False |
| 2026-07 | 44.713764 | 29.482672 | -15.231092 | -34.063542 | False |
| 2026-08 | 29.482672 | 23.609587 | -5.873086 | -19.920466 | False |
| 2026-09 | 23.609587 | 13.551505 | -10.058081 | -42.601683 | False |
| 2026-10 | 13.551505 | 7.981239 | -5.570266 | -41.104410 | False |
| 2026-11 | 7.981239 | 5.865928 | -2.115311 | -26.503546 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
