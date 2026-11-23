# Performance report: fixed_stop_1_00pct__fixed_target_2_00pct__trailing_sl

## Run metadata
- Experiment Id: fixed_stop_1_00pct__fixed_target_2_00pct__trailing_sl
- Stop Model: fixed_stop_1_00pct
- Target Model: fixed_target_2_00pct
- Target Value: 0.020000
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
- Final Equity: 398.880142
- Net Pnl: -601.119858
- Total Return Pct: -60.111986
- Max Drawdown Amount: 720.339166
- Max Drawdown Pct: 66.566298
- Recovery Factor: -0.834496
- Sharpe Ratio: -2.429221
- Sortino Ratio: -3.122717
- Cagr Pct: -57.207450
- Calmar Ratio: -0.859406
- Worst Daily Loss: -77.766352
- Worst Daily Loss Pct: -7.690636
- Worst Daily Loss Date Utc: 2026-02-06
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 39.183119
- Max Capital Utilization Pct: 102.073977
- Max Gross Exposure: 1,075.413749
- Max Gross Exposure Equity Multiple: 1.020740

## Trade performance

- Trade Count: 2906
- Net Pnl: -601.119858
- Gross Pnl: 106.945869
- Total Fees: 709.097749
- Funding Pnl: 1.032022
- Winning Trades: 1322
- Losing Trades: 1584
- Breakeven Trades: 0
- Win Rate Pct: 45.492085
- Profit Factor: 0.847640
- Expectancy: -0.206855
- Average Win: 2.529708
- Average Loss: 2.490779
- Payoff Ratio: 1.015629
- Max Consecutive Losses: 23
- Average Duration Minutes: 211.277701
- Median Duration Minutes: 104.000000
- Max Duration Minutes: 4,118.000000
- Recovery Factor: -0.834496

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 584 | -127.016321 | -3.576981 | 123.078141 | -0.361199 | 44.863014 | 0.819983 | -0.217494 | 2.208258 | 2.191242 | 1.007765 |
| BTC | 397 | -76.835029 | 20.113859 | 97.222091 | 0.273202 | 46.599496 | 0.859371 | -0.193539 | 2.538004 | 2.577197 | 0.984792 |
| DOGE | 677 | -108.190768 | 60.335626 | 169.257289 | 0.730895 | 46.233383 | 0.882352 | -0.159809 | 2.592398 | 2.526404 | 1.026121 |
| ETH | 519 | -168.280592 | -29.803665 | 138.451288 | -0.025639 | 45.664740 | 0.781731 | -0.324240 | 2.543032 | 2.733969 | 0.930161 |
| SOL | 729 | -120.797147 | 59.877030 | 181.088940 | 0.414763 | 44.581619 | 0.879547 | -0.165703 | 2.714034 | 2.482322 | 1.093345 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 933 | -241.383089 | -1.338932 | 238.074433 | -1.969724 | 43.729904 | 0.820137 | -0.258717 | 2.697693 | 2.556270 | 1.055324 |
| SHORT | 1973 | -359.736769 | 108.284801 | 471.023316 | 3.001746 | 46.325393 | 0.861818 | -0.182330 | 2.454721 | 2.458312 | 0.998540 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 167 | -67.304519 | -30.057361 | 36.944199 | -0.302960 | 42.514970 | 0.703621 | -0.403021 | 2.250487 | 2.365511 | 0.951374 |
| AVAX | SHORT | 417 | -59.711802 | 26.480380 | 86.133943 | -0.058239 | 45.803357 | 0.875208 | -0.143194 | 2.192561 | 2.117217 | 1.035587 |
| BTC | LONG | 141 | -14.247338 | 23.662537 | 37.168844 | -0.741032 | 45.390071 | 0.928688 | -0.101045 | 2.899075 | 2.594652 | 1.117327 |
| BTC | SHORT | 256 | -62.587691 | -3.548678 | 60.053246 | 1.014234 | 47.265625 | 0.819412 | -0.244483 | 2.347024 | 2.567241 | 0.914220 |
| DOGE | LONG | 146 | -4.308335 | 30.641286 | 34.210042 | -0.739579 | 41.780822 | 0.976367 | -0.029509 | 2.917879 | 2.144694 | 1.360511 |
| DOGE | SHORT | 531 | -103.882433 | 29.694340 | 135.047247 | 1.470475 | 47.457627 | 0.859107 | -0.195635 | 2.513611 | 2.642696 | 0.951154 |
| ETH | LONG | 196 | -66.742468 | -13.600559 | 52.512376 | -0.629533 | 45.408163 | 0.767022 | -0.340523 | 2.468914 | 2.677344 | 0.922150 |
| ETH | SHORT | 323 | -101.538123 | -16.203106 | 85.938911 | 0.603894 | 45.820433 | 0.790428 | -0.314360 | 2.587603 | 2.768591 | 0.934628 |
| SOL | LONG | 283 | -88.780427 | -11.984835 | 77.238972 | 0.443380 | 43.462898 | 0.801115 | -0.313712 | 2.907395 | 2.789937 | 1.042100 |
| SOL | SHORT | 446 | -32.016720 | 71.861865 | 103.849968 | -0.028617 | 45.291480 | 0.942464 | -0.071786 | 2.596294 | 2.280607 | 1.138422 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 2 | -1.413845 | 0.358792 | 0.000000 | -1.772637 |
| stop | 2325 | -2,707.293829 | 566.223406 | 0.861513 | -3,272.655723 |
| stop_gap | 4 | -1.271353 | 0.729151 | 0.000000 | -2.000504 |
| target | 574 | 2,816.894787 | 141.784894 | 0.170509 | 2,675.280403 |
| target_gap | 1 | 0.030108 | 0.001505 | 0.000000 | 0.028603 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 1,035.232119 | 35.232119 | 3.523212 | False |
| 2025-12 | 1,035.232119 | 895.075467 | -140.156652 | -13.538669 | False |
| 2026-01 | 895.075467 | 874.170303 | -20.905164 | -2.335576 | False |
| 2026-02 | 874.170303 | 815.372659 | -58.797644 | -6.726109 | False |
| 2026-03 | 815.372659 | 635.885381 | -179.487277 | -22.012913 | False |
| 2026-04 | 635.885381 | 614.494956 | -21.390425 | -3.363881 | False |
| 2026-05 | 614.494956 | 562.044204 | -52.450752 | -8.535587 | False |
| 2026-06 | 562.044204 | 545.720585 | -16.323618 | -2.904330 | False |
| 2026-07 | 545.720585 | 485.638599 | -60.081986 | -11.009661 | False |
| 2026-08 | 485.638599 | 516.783206 | 31.144607 | 6.413124 | False |
| 2026-09 | 516.783206 | 429.586424 | -87.196783 | -16.872991 | False |
| 2026-10 | 429.586424 | 393.522381 | -36.064043 | -8.395061 | False |
| 2026-11 | 393.522381 | 398.880142 | 5.357761 | 1.361488 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
