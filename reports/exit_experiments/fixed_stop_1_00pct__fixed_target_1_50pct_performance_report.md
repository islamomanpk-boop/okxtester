# Performance report: fixed_stop_1_00pct__fixed_target_1_50pct

## Run metadata
- Experiment Id: fixed_stop_1_00pct__fixed_target_1_50pct
- Stop Model: fixed_stop_1_00pct
- Target Model: fixed_target_1_50pct
- Target Value: 0.015000
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
- Final Equity: 486.951474
- Net Pnl: -513.048526
- Total Return Pct: -51.304853
- Max Drawdown Amount: 654.994332
- Max Drawdown Pct: 60.448703
- Recovery Factor: -0.783287
- Sharpe Ratio: -1.993893
- Sortino Ratio: -2.595717
- Cagr Pct: -48.550003
- Calmar Ratio: -0.803160
- Worst Daily Loss: -64.783772
- Worst Daily Loss Pct: -6.439935
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 40.222976
- Max Capital Utilization Pct: 102.255216
- Max Gross Exposure: 1,069.635491
- Max Gross Exposure Equity Multiple: 1.022552

## Trade performance

- Trade Count: 2653
- Net Pnl: -513.048526
- Gross Pnl: 165.548822
- Total Fees: 680.093806
- Funding Pnl: 1.496458
- Winning Trades: 1116
- Losing Trades: 1537
- Breakeven Trades: 0
- Win Rate Pct: 42.065586
- Profit Factor: 0.884297
- Expectancy: -0.193384
- Average Win: 3.513576
- Average Loss: 2.884970
- Payoff Ratio: 1.217890
- Max Consecutive Losses: 26
- Average Duration Minutes: 243.816811
- Median Duration Minutes: 105.000000
- Max Duration Minutes: 5,080.000000
- Recovery Factor: -0.783287

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 545 | -151.230715 | -30.042698 | 120.966944 | -0.221073 | 40.917431 | 0.814527 | -0.277488 | 2.978250 | 2.532238 | 1.176134 |
| BTC | 369 | -22.052462 | 74.484095 | 96.850018 | 0.313461 | 43.360434 | 0.963725 | -0.059763 | 3.661679 | 2.908713 | 1.258866 |
| DOGE | 597 | -92.030599 | 58.654108 | 151.554254 | 0.869548 | 44.053601 | 0.905974 | -0.154155 | 3.371678 | 2.930484 | 1.150553 |
| ETH | 475 | -194.509875 | -60.624082 | 134.132656 | 0.246863 | 39.368421 | 0.787713 | -0.409494 | 3.859625 | 3.181457 | 1.213163 |
| SOL | 667 | -53.224875 | 123.077399 | 176.589933 | 0.287659 | 42.428786 | 0.952301 | -0.079797 | 3.754880 | 2.905875 | 1.292169 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 850 | -217.044751 | 12.697187 | 227.623165 | -2.118773 | 40.705882 | 0.855642 | -0.255347 | 3.718114 | 2.983159 | 1.246368 |
| SHORT | 1803 | -296.003776 | 152.851635 | 452.470641 | 3.615231 | 42.706600 | 0.898998 | -0.164173 | 3.421666 | 2.837064 | 1.206059 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 159 | -89.694067 | -51.180297 | 38.155597 | -0.358172 | 35.220126 | 0.675166 | -0.564114 | 3.329078 | 2.680800 | 1.241822 |
| AVAX | SHORT | 386 | -61.536649 | 21.137599 | 82.811347 | 0.137099 | 43.264249 | 0.885886 | -0.159421 | 2.860608 | 2.462366 | 1.161731 |
| BTC | LONG | 117 | -9.026695 | 26.421197 | 34.638419 | -0.809474 | 44.444444 | 0.958605 | -0.077151 | 4.019881 | 3.354777 | 1.198256 |
| BTC | SHORT | 252 | -13.025766 | 48.062898 | 62.211599 | 1.122935 | 42.857143 | 0.966589 | -0.051690 | 3.489211 | 2.707365 | 1.288785 |
| DOGE | LONG | 138 | -8.653957 | 23.389482 | 31.314982 | -0.728457 | 44.202899 | 0.956156 | -0.062710 | 3.093900 | 2.563401 | 1.206951 |
| DOGE | SHORT | 459 | -83.376642 | 35.264625 | 120.239273 | 1.598005 | 44.008715 | 0.893298 | -0.181648 | 3.455561 | 3.040467 | 1.136523 |
| ETH | LONG | 181 | -44.754364 | 6.724771 | 50.976865 | -0.502270 | 40.331492 | 0.866370 | -0.247262 | 3.974776 | 3.101046 | 1.281753 |
| ETH | SHORT | 294 | -149.755511 | -67.348853 | 83.155791 | 0.749134 | 38.775510 | 0.742399 | -0.509372 | 3.785887 | 3.229704 | 1.172209 |
| SOL | LONG | 255 | -64.915668 | 7.342033 | 72.537302 | 0.279601 | 40.784314 | 0.863918 | -0.254571 | 3.962680 | 3.159168 | 1.254343 |
| SOL | SHORT | 412 | 11.690792 | 115.735365 | 104.052631 | 0.008058 | 43.446602 | 1.018301 | 0.028376 | 3.634147 | 2.741723 | 1.325497 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 2 | -1.726016 | 0.438012 | 0.000000 | -2.164029 |
| stop | 1531 | -4,029.402603 | 395.661085 | 0.810534 | -4,424.253154 |
| stop_gap | 4 | -7.120345 | 0.694247 | 0.032672 | -7.781920 |
| target | 1116 | 4,203.797787 | 283.300461 | 0.653252 | 3,921.150577 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 1,024.063498 | 24.063498 | 2.406350 | False |
| 2025-12 | 1,024.063498 | 911.835174 | -112.228324 | -10.959118 | False |
| 2026-01 | 911.835174 | 904.955019 | -6.880155 | -0.754539 | False |
| 2026-02 | 904.955019 | 832.540808 | -72.414211 | -8.001968 | False |
| 2026-03 | 832.540808 | 676.184509 | -156.356299 | -18.780617 | False |
| 2026-04 | 676.184509 | 647.585452 | -28.599057 | -4.229475 | False |
| 2026-05 | 647.585452 | 584.159798 | -63.425653 | -9.794175 | False |
| 2026-06 | 584.159798 | 587.677564 | 3.517766 | 0.602192 | False |
| 2026-07 | 587.677564 | 521.408376 | -66.269188 | -11.276454 | False |
| 2026-08 | 521.408376 | 588.303545 | 66.895169 | 12.829707 | False |
| 2026-09 | 588.303545 | 478.101211 | -110.202334 | -18.732223 | False |
| 2026-10 | 478.101211 | 455.530861 | -22.570350 | -4.720831 | False |
| 2026-11 | 455.530861 | 486.951474 | 31.420613 | 6.897582 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
