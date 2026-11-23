# Performance report: signal_extreme_atr_buffer_0_10__fixed_target_2_00pct

## Run metadata
- Experiment Id: signal_extreme_atr_buffer_0_10__fixed_target_2_00pct
- Stop Model: signal_extreme_atr_buffer_0_10
- Target Model: fixed_target_2_00pct
- Target Value: 0.020000
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
- Final Equity: 218.516165
- Net Pnl: -781.483835
- Total Return Pct: -78.148384
- Max Drawdown Amount: 813.965761
- Max Drawdown Pct: 80.566499
- Recovery Factor: -0.960094
- Sharpe Ratio: -3.553987
- Sortino Ratio: -4.327844
- Cagr Pct: -75.453089
- Calmar Ratio: -0.936532
- Worst Daily Loss: -66.877065
- Worst Daily Loss Pct: -7.741015
- Worst Daily Loss Date Utc: 2026-02-06
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 46.179628
- Max Capital Utilization Pct: 103.047293
- Max Gross Exposure: 1,008.594240
- Max Gross Exposure Equity Multiple: 1.030473

## Trade performance

- Trade Count: 3177
- Net Pnl: -781.483835
- Gross Pnl: 15.881446
- Total Fees: 799.334526
- Funding Pnl: 1.969244
- Winning Trades: 719
- Losing Trades: 2458
- Breakeven Trades: 0
- Win Rate Pct: 22.631413
- Profit Factor: 0.790305
- Expectancy: -0.245982
- Average Win: 4.096348
- Average Loss: 1.516175
- Payoff Ratio: 2.701765
- Max Consecutive Losses: 54
- Average Duration Minutes: 171.116462
- Median Duration Minutes: 55.000000
- Max Duration Minutes: 4,395.000000
- Recovery Factor: -0.960094

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 618 | -177.226458 | -50.346014 | 126.982992 | 0.102548 | 21.197411 | 0.701509 | -0.286774 | 3.179508 | 1.219183 | 2.607901 |
| BTC | 540 | -138.927545 | 6.100175 | 145.121849 | 0.094129 | 19.444444 | 0.768981 | -0.257273 | 4.404199 | 1.382456 | 3.185778 |
| DOGE | 744 | -146.183523 | 56.720202 | 204.163941 | 1.260216 | 24.462366 | 0.845543 | -0.196483 | 4.396992 | 1.684050 | 2.610963 |
| ETH | 557 | -193.764617 | -54.888685 | 138.894537 | 0.018605 | 21.903052 | 0.722739 | -0.347872 | 4.140067 | 1.606558 | 2.576979 |
| SOL | 718 | -125.381692 | 58.295769 | 184.171207 | 0.493746 | 24.930362 | 0.858543 | -0.174626 | 4.251270 | 1.644451 | 2.585222 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 992 | -291.830374 | 17.930587 | 307.929955 | -1.831005 | 21.169355 | 0.785893 | -0.294184 | 5.100864 | 1.742982 | 2.926516 |
| SHORT | 2185 | -489.653462 | -2.049140 | 491.404570 | 3.800249 | 23.295195 | 0.792849 | -0.224098 | 3.681912 | 1.410350 | 2.610637 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 172 | -84.621167 | -43.763014 | 40.703491 | -0.154662 | 18.604651 | 0.559160 | -0.491984 | 3.354165 | 1.371103 | 2.446326 |
| AVAX | SHORT | 446 | -92.605291 | -6.583000 | 86.279501 | 0.257211 | 22.197309 | 0.769517 | -0.207635 | 3.123053 | 1.157889 | 2.697195 |
| BTC | LONG | 173 | -30.187358 | 31.861450 | 61.364614 | -0.684194 | 19.075145 | 0.869770 | -0.174493 | 6.109477 | 1.655715 | 3.689933 |
| BTC | SHORT | 367 | -108.740187 | -25.761275 | 83.757236 | 0.778323 | 19.618529 | 0.705764 | -0.296295 | 3.622613 | 1.252774 | 2.891673 |
| DOGE | LONG | 170 | -34.334414 | 16.441855 | 50.186857 | -0.589411 | 22.352941 | 0.848794 | -0.201967 | 5.071988 | 1.720227 | 2.948441 |
| DOGE | SHORT | 574 | -111.849109 | 40.278347 | 153.977083 | 1.849627 | 25.087108 | 0.844517 | -0.194859 | 4.218868 | 1.672945 | 2.521822 |
| ETH | LONG | 214 | -73.465632 | -11.847036 | 61.012484 | -0.606112 | 20.560748 | 0.738992 | -0.343297 | 4.727355 | 1.655701 | 2.855198 |
| ETH | SHORT | 343 | -120.298985 | -43.041650 | 77.882053 | 0.624717 | 22.740525 | 0.711778 | -0.350726 | 3.808777 | 1.575032 | 2.418221 |
| SOL | LONG | 263 | -69.221803 | 25.237331 | 94.662510 | 0.203375 | 23.954373 | 0.839287 | -0.263201 | 5.738037 | 2.153591 | 2.664405 |
| SOL | SHORT | 455 | -56.159889 | 33.058438 | 89.508697 | 0.290371 | 25.494505 | 0.876745 | -0.123428 | 3.443801 | 1.344073 | 2.562212 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | 0.012770 | 0.218727 | 0.000000 | -0.205957 |
| stop | 2449 | -3,083.359089 | 642.613031 | 1.354212 | -3,724.617908 |
| stop_gap | 8 | -1.597738 | 0.325052 | -0.011711 | -1.934501 |
| target | 719 | 3,100.825502 | 156.177715 | 0.626743 | 2,945.274531 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 880.198686 | -119.801314 | -11.980131 | False |
| 2025-12 | 880.198686 | 797.880015 | -82.318670 | -9.352283 | False |
| 2026-01 | 797.880015 | 758.737686 | -39.142329 | -4.905791 | False |
| 2026-02 | 758.737686 | 694.185445 | -64.552241 | -8.507847 | False |
| 2026-03 | 694.185445 | 552.421268 | -141.764177 | -20.421658 | False |
| 2026-04 | 552.421268 | 486.034455 | -66.386812 | -12.017425 | False |
| 2026-05 | 486.034455 | 400.399253 | -85.635203 | -17.619163 | False |
| 2026-06 | 400.399253 | 392.224095 | -8.175158 | -2.041752 | False |
| 2026-07 | 392.224095 | 319.768974 | -72.455120 | -18.472889 | False |
| 2026-08 | 319.768974 | 318.815180 | -0.953794 | -0.298276 | False |
| 2026-09 | 318.815180 | 236.160615 | -82.654566 | -25.925543 | False |
| 2026-10 | 236.160615 | 206.917037 | -29.243578 | -12.382919 | False |
| 2026-11 | 206.917037 | 218.516165 | 11.599128 | 5.605690 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
