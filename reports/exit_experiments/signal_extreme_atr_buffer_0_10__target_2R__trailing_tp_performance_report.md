# Performance report: signal_extreme_atr_buffer_0_10__target_2R__trailing_tp

## Run metadata
- Experiment Id: signal_extreme_atr_buffer_0_10__target_2R__trailing_tp
- Stop Model: signal_extreme_atr_buffer_0_10
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
- Final Equity: 40.260162
- Net Pnl: -959.739838
- Total Return Pct: -95.973984
- Max Drawdown Amount: 972.907260
- Max Drawdown Pct: 96.156149
- Recovery Factor: -0.986466
- Sharpe Ratio: -7.916584
- Sortino Ratio: -7.955282
- Cagr Pct: -94.852833
- Calmar Ratio: -0.986446
- Worst Daily Loss: -59.867762
- Worst Daily Loss Pct: -7.702321
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 39.067381
- Max Capital Utilization Pct: 102.376773
- Max Gross Exposure: 996.448075
- Max Gross Exposure Equity Multiple: 1.023768

## Trade performance

- Trade Count: 4529
- Net Pnl: -959.739838
- Gross Pnl: -175.221432
- Total Fees: 785.152323
- Funding Pnl: 0.633916
- Winning Trades: 1470
- Losing Trades: 3059
- Breakeven Trades: 0
- Win Rate Pct: 32.457496
- Profit Factor: 0.680588
- Expectancy: -0.211910
- Average Win: 1.391135
- Average Loss: 0.982252
- Payoff Ratio: 1.416271
- Max Consecutive Losses: 23
- Average Duration Minutes: 104.770369
- Median Duration Minutes: 37.000000
- Max Duration Minutes: 8,591.000000
- Recovery Factor: -0.986466

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 865 | -147.879057 | -43.396495 | 104.537013 | 0.054451 | 31.445087 | 0.640667 | -0.170958 | 0.969332 | 0.693992 | 1.396748 |
| BTC | 820 | -176.662742 | -20.352547 | 156.266580 | -0.043616 | 33.292683 | 0.652280 | -0.215442 | 1.213910 | 0.928812 | 1.306949 |
| DOGE | 1065 | -198.273619 | -8.492823 | 190.288910 | 0.508115 | 32.863850 | 0.732540 | -0.186172 | 1.551560 | 1.036811 | 1.496474 |
| ETH | 788 | -256.867319 | -111.554585 | 145.159115 | -0.153620 | 31.091371 | 0.588698 | -0.325974 | 1.500633 | 1.150133 | 1.304747 |
| SOL | 991 | -180.057101 | 8.575018 | 188.900706 | 0.268586 | 33.299697 | 0.749667 | -0.181692 | 1.633976 | 1.088153 | 1.501605 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1525 | -368.363415 | -64.550988 | 303.022472 | -0.789955 | 31.016393 | 0.654239 | -0.241550 | 1.473590 | 1.012711 | 1.455095 |
| SHORT | 3004 | -591.376423 | -110.670444 | 482.129851 | 1.423871 | 33.189081 | 0.695063 | -0.196863 | 1.352017 | 0.966287 | 1.399188 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 240 | -50.130020 | -18.716259 | 31.315872 | -0.097889 | 27.500000 | 0.578743 | -0.208875 | 1.043499 | 0.683913 | 1.525776 |
| AVAX | SHORT | 625 | -97.749037 | -24.680236 | 73.221141 | 0.152340 | 32.960000 | 0.665857 | -0.156398 | 0.945570 | 0.698178 | 1.354340 |
| BTC | LONG | 317 | -68.116309 | -4.125656 | 63.674251 | -0.316401 | 33.753943 | 0.639978 | -0.214878 | 1.131625 | 0.900953 | 1.256031 |
| BTC | SHORT | 503 | -108.546433 | -16.226890 | 92.592328 | 0.272785 | 33.001988 | 0.659579 | -0.215798 | 1.266948 | 0.946172 | 1.339026 |
| DOGE | LONG | 250 | -55.725611 | -18.912935 | 36.539539 | -0.273137 | 29.200000 | 0.608657 | -0.222902 | 1.187263 | 0.804496 | 1.475785 |
| DOGE | SHORT | 815 | -142.548008 | 10.420111 | 153.749371 | 0.781251 | 33.987730 | 0.761993 | -0.174906 | 1.647566 | 1.113241 | 1.479972 |
| ETH | LONG | 324 | -93.480243 | -31.387460 | 61.769528 | -0.323256 | 30.246914 | 0.596442 | -0.288519 | 1.409794 | 1.024956 | 1.375468 |
| ETH | SHORT | 464 | -163.387076 | -80.167126 | 83.389587 | 0.169636 | 31.681034 | 0.584132 | -0.352127 | 1.561192 | 1.239376 | 1.259659 |
| SOL | LONG | 394 | -100.911232 | 8.591322 | 109.723282 | 0.220728 | 32.741117 | 0.736617 | -0.256120 | 2.187777 | 1.445791 | 1.513205 |
| SOL | SHORT | 597 | -79.145868 | -0.016303 | 79.177423 | 0.047858 | 33.668342 | 0.764541 | -0.132573 | 1.278551 | 0.848825 | 1.506260 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | -0.147252 | 0.014703 | 0.000702 | -0.161254 |
| stop | 3042 | -2,461.805514 | 539.563681 | 0.133243 | -3,001.235951 |
| stop_gap | 10 | -2.255192 | 0.713796 | -0.006224 | -2.975213 |
| trailing_take_profit | 1200 | 1,921.663911 | 198.871297 | 0.412476 | 1,723.205091 |
| trailing_take_profit_gap | 276 | 367.322616 | 45.988845 | 0.093719 | 321.427490 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 828.910447 | -171.089553 | -17.108955 | False |
| 2025-12 | 828.910447 | 670.044982 | -158.865465 | -19.165576 | False |
| 2026-01 | 670.044982 | 585.412126 | -84.632856 | -12.630922 | False |
| 2026-02 | 585.412126 | 479.710012 | -105.702114 | -18.056017 | False |
| 2026-03 | 479.710012 | 298.069190 | -181.640822 | -37.864714 | False |
| 2026-04 | 298.069190 | 218.153411 | -79.915779 | -26.811150 | False |
| 2026-05 | 218.153411 | 146.308409 | -71.845003 | -32.933247 | False |
| 2026-06 | 146.308409 | 132.178422 | -14.129987 | -9.657672 | False |
| 2026-07 | 132.178422 | 94.255805 | -37.922616 | -28.690474 | False |
| 2026-08 | 94.255805 | 85.554679 | -8.701126 | -9.231396 | False |
| 2026-09 | 85.554679 | 59.275209 | -26.279470 | -30.716579 | False |
| 2026-10 | 59.275209 | 44.367853 | -14.907356 | -25.149395 | False |
| 2026-11 | 44.367853 | 40.260162 | -4.107691 | -9.258259 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
