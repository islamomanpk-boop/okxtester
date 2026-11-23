# Performance report: fixed_stop_1_00pct__fixed_target_0_75pct__trailing_tp

## Run metadata
- Experiment Id: fixed_stop_1_00pct__fixed_target_0_75pct__trailing_tp
- Stop Model: fixed_stop_1_00pct
- Target Model: fixed_target_0_75pct
- Target Value: 0.007500
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
- Final Equity: 204.619061
- Net Pnl: -795.380939
- Total Return Pct: -79.538094
- Max Drawdown Amount: 890.327488
- Max Drawdown Pct: 81.668516
- Recovery Factor: -0.893358
- Sharpe Ratio: -4.682969
- Sortino Ratio: -5.300987
- Cagr Pct: -76.898415
- Calmar Ratio: -0.941592
- Worst Daily Loss: -70.234257
- Worst Daily Loss Pct: -6.951355
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 36.174689
- Max Capital Utilization Pct: 102.373639
- Max Gross Exposure: 1,076.579152
- Max Gross Exposure Equity Multiple: 1.023736

## Trade performance

- Trade Count: 3802
- Net Pnl: -795.380939
- Gross Pnl: -22.982560
- Total Fees: 773.831349
- Funding Pnl: 1.432970
- Winning Trades: 2188
- Losing Trades: 1614
- Breakeven Trades: 0
- Win Rate Pct: 57.548659
- Profit Factor: 0.785055
- Expectancy: -0.209201
- Average Win: 1.327704
- Average Loss: 2.292687
- Payoff Ratio: 0.579104
- Max Consecutive Losses: 19
- Average Duration Minutes: 144.726723
- Median Duration Minutes: 68.000000
- Max Duration Minutes: 3,948.000000
- Recovery Factor: -0.893358

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 769 | -105.711936 | 13.649014 | 119.272591 | -0.088359 | 56.697009 | 0.818315 | -0.137467 | 1.092044 | 1.747276 | 0.624998 |
| BTC | 533 | -102.694708 | 8.008008 | 111.056752 | 0.354037 | 59.662289 | 0.805859 | -0.192673 | 1.340484 | 2.460320 | 0.544842 |
| DOGE | 869 | -184.410402 | 1.295008 | 186.246627 | 0.541218 | 57.652474 | 0.793468 | -0.212210 | 1.414131 | 2.426331 | 0.582827 |
| ETH | 680 | -223.793702 | -67.718454 | 156.064178 | -0.011071 | 56.911765 | 0.704584 | -0.329108 | 1.379225 | 2.585508 | 0.533445 |
| SOL | 951 | -178.770191 | 21.783865 | 201.191201 | 0.637145 | 57.413249 | 0.809645 | -0.187981 | 1.392621 | 2.318868 | 0.600561 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1263 | -347.786392 | -80.588061 | 265.918107 | -1.280224 | 55.977831 | 0.732571 | -0.275365 | 1.347515 | 2.338992 | 0.576109 |
| SHORT | 2539 | -447.594547 | 57.605501 | 507.913242 | 2.713194 | 58.330051 | 0.813496 | -0.176288 | 1.318246 | 2.268353 | 0.581147 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 230 | -69.544612 | -32.624073 | 36.720680 | -0.199859 | 51.739130 | 0.641613 | -0.302368 | 1.046256 | 1.748190 | 0.598480 |
| AVAX | SHORT | 539 | -36.167324 | 46.273087 | 82.551911 | 0.111500 | 58.812616 | 0.906736 | -0.067101 | 1.109232 | 1.746819 | 0.635001 |
| BTC | LONG | 189 | -38.530473 | 4.535711 | 42.649462 | -0.416722 | 59.788360 | 0.805624 | -0.203865 | 1.413235 | 2.608237 | 0.541835 |
| BTC | SHORT | 344 | -64.164235 | 3.472297 | 68.407290 | 0.770759 | 59.593023 | 0.806000 | -0.186524 | 1.300383 | 2.379444 | 0.546507 |
| DOGE | LONG | 209 | -39.394833 | 0.367088 | 39.259931 | -0.501990 | 58.851675 | 0.788428 | -0.188492 | 1.193545 | 2.165127 | 0.551259 |
| DOGE | SHORT | 660 | -145.015569 | 0.927920 | 146.986696 | 1.043208 | 57.272727 | 0.794796 | -0.219721 | 1.485909 | 2.505990 | 0.592943 |
| ETH | LONG | 264 | -96.857037 | -36.330015 | 60.080968 | -0.446054 | 56.439394 | 0.669100 | -0.366883 | 1.314436 | 2.545287 | 0.516420 |
| ETH | SHORT | 416 | -126.936666 | -31.388439 | 95.983210 | 0.434983 | 57.211538 | 0.726927 | -0.305136 | 1.419786 | 2.611493 | 0.543668 |
| SOL | LONG | 371 | -103.459438 | -16.536772 | 87.207066 | 0.284400 | 54.716981 | 0.759002 | -0.278866 | 1.605105 | 2.555332 | 0.628140 |
| SOL | SHORT | 580 | -75.310754 | 38.320637 | 113.984135 | 0.352745 | 59.137931 | 0.852287 | -0.129846 | 1.266866 | 2.151248 | 0.588898 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 2 | -0.725279 | 0.184055 | 0.000000 | -0.909334 |
| stop | 1606 | -3,365.665112 | 330.447291 | 0.325800 | -3,695.786603 |
| stop_gap | 2 | -2.709940 | 0.264071 | 0.000000 | -2.974011 |
| trailing_take_profit | 2074 | 3,062.244361 | 417.396767 | 0.981346 | 2,645.828940 |
| trailing_take_profit_gap | 118 | 283.873411 | 25.539166 | 0.125825 | 258.460069 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 1,051.604996 | 51.604996 | 5.160500 | False |
| 2025-12 | 1,051.604996 | 911.867208 | -139.737788 | -13.288049 | False |
| 2026-01 | 911.867208 | 871.083071 | -40.784137 | -4.472596 | False |
| 2026-02 | 871.083071 | 730.653764 | -140.429307 | -16.121230 | False |
| 2026-03 | 730.653764 | 525.403495 | -205.250269 | -28.091317 | False |
| 2026-04 | 525.403495 | 474.875074 | -50.528422 | -9.617070 | False |
| 2026-05 | 474.875074 | 421.390507 | -53.484566 | -11.262871 | False |
| 2026-06 | 421.390507 | 369.002694 | -52.387813 | -12.432129 | False |
| 2026-07 | 369.002694 | 318.314330 | -50.688364 | -13.736584 | False |
| 2026-08 | 318.314330 | 323.997384 | 5.683053 | 1.785359 | False |
| 2026-09 | 323.997384 | 254.330614 | -69.666770 | -21.502263 | False |
| 2026-10 | 254.330614 | 218.019999 | -36.310615 | -14.276934 | False |
| 2026-11 | 218.019999 | 204.619061 | -13.400938 | -6.146656 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
