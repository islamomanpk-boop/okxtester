# Performance report: fixed_stop_0_75pct__fixed_target_2_00pct

## Run metadata
- Experiment Id: fixed_stop_0_75pct__fixed_target_2_00pct
- Stop Model: fixed_stop_0_75pct
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
- Final Equity: 435.406397
- Net Pnl: -564.593603
- Total Return Pct: -56.459360
- Max Drawdown Amount: 648.410448
- Max Drawdown Pct: 63.361962
- Recovery Factor: -0.870735
- Sharpe Ratio: -1.928570
- Sortino Ratio: -2.506047
- Cagr Pct: -53.600802
- Calmar Ratio: -0.845946
- Worst Daily Loss: -72.368654
- Worst Daily Loss Pct: -7.289726
- Worst Daily Loss Date Utc: 2026-02-06
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 45.221322
- Max Capital Utilization Pct: 103.162551
- Max Gross Exposure: 1,025.900753
- Max Gross Exposure Equity Multiple: 1.031626

## Trade performance

- Trade Count: 2529
- Net Pnl: -564.593603
- Gross Pnl: 177.145711
- Total Fees: 743.759661
- Funding Pnl: 2.020347
- Winning Trades: 743
- Losing Trades: 1786
- Breakeven Trades: 0
- Win Rate Pct: 29.379201
- Profit Factor: 0.877304
- Expectancy: -0.223248
- Average Win: 5.433315
- Average Loss: 2.576454
- Payoff Ratio: 2.108835
- Max Consecutive Losses: 49
- Average Duration Minutes: 243.654013
- Median Duration Minutes: 95.000000
- Max Duration Minutes: 6,472.000000
- Recovery Factor: -0.870735

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 503 | -192.910398 | -63.950895 | 128.904077 | -0.055425 | 27.236581 | 0.767019 | -0.383520 | 4.635745 | 2.262315 | 2.049115 |
| BTC | 382 | 29.392688 | 142.977745 | 114.160516 | 0.575459 | 31.675393 | 1.043977 | 0.076944 | 5.766610 | 2.560793 | 2.251884 |
| DOGE | 579 | -114.270408 | 62.635073 | 177.997420 | 1.091939 | 30.569948 | 0.895656 | -0.197358 | 5.541591 | 2.724209 | 2.034202 |
| ETH | 461 | -197.550136 | -58.071504 | 139.679384 | 0.200752 | 27.548807 | 0.778742 | -0.428525 | 5.474796 | 2.673201 | 2.048030 |
| SOL | 604 | -89.255349 | 93.555292 | 183.018264 | 0.207623 | 29.966887 | 0.920107 | -0.147774 | 5.679202 | 2.641113 | 2.150306 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 818 | -238.377211 | 41.603839 | 277.338204 | -2.642846 | 27.750611 | 0.861765 | -0.291415 | 6.546503 | 2.917823 | 2.243626 |
| SHORT | 1711 | -326.216393 | 135.541872 | 466.421458 | 4.663193 | 30.157802 | 0.886617 | -0.190658 | 4.943599 | 2.407626 | 2.053308 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 152 | -82.879526 | -38.085549 | 44.513364 | -0.280612 | 23.684211 | 0.715327 | -0.545260 | 5.784993 | 2.509821 | 2.304942 |
| AVAX | SHORT | 351 | -110.030872 | -25.865346 | 84.390712 | 0.225187 | 28.774929 | 0.795050 | -0.313478 | 4.226112 | 2.147473 | 1.967947 |
| BTC | LONG | 130 | 17.033114 | 64.484454 | 46.590687 | -0.860653 | 31.538462 | 1.062720 | 0.131024 | 7.039165 | 3.051378 | 2.306881 |
| BTC | SHORT | 252 | 12.359574 | 78.493291 | 67.569829 | 1.436112 | 31.746032 | 1.031149 | 0.049046 | 5.114425 | 2.306944 | 2.216969 |
| DOGE | LONG | 135 | -21.156725 | 25.189010 | 45.435994 | -0.909740 | 28.888889 | 0.923603 | -0.156716 | 6.558342 | 2.884709 | 2.273485 |
| DOGE | SHORT | 444 | -93.113683 | 37.446063 | 132.561426 | 2.001680 | 31.081081 | 0.886197 | -0.209716 | 5.254248 | 2.673856 | 1.965045 |
| ETH | LONG | 175 | -61.714549 | -3.575111 | 57.438050 | -0.701387 | 27.428571 | 0.829025 | -0.352655 | 6.234197 | 2.842173 | 2.193461 |
| ETH | SHORT | 286 | -135.835587 | -54.496393 | 82.241334 | 0.902139 | 27.622378 | 0.744619 | -0.474950 | 5.013388 | 2.569533 | 1.951090 |
| SOL | LONG | 226 | -89.659525 | -6.408964 | 83.360108 | 0.109547 | 27.876106 | 0.828840 | -0.396724 | 6.891647 | 3.213701 | 2.144458 |
| SOL | SHORT | 378 | 0.404176 | 99.964257 | 99.658156 | 0.098076 | 31.216931 | 1.000681 | 0.001069 | 5.031879 | 2.282144 | 2.204891 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | 0.014662 | 0.251138 | 0.000000 | -0.236476 |
| stop | 1783 | -4,069.185276 | 528.950296 | 1.021848 | -4,597.113724 |
| stop_gap | 2 | -3.716974 | 0.479373 | 0.000000 | -4.196346 |
| target | 743 | 4,250.033298 | 214.078854 | 0.998500 | 4,036.952943 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 970.370419 | -29.629581 | -2.962958 | False |
| 2025-12 | 970.370419 | 861.507359 | -108.863060 | -11.218712 | False |
| 2026-01 | 861.507359 | 839.597329 | -21.910030 | -2.543220 | False |
| 2026-02 | 839.597329 | 840.404716 | 0.807387 | 0.096164 | False |
| 2026-03 | 840.404716 | 720.592841 | -119.811874 | -14.256450 | False |
| 2026-04 | 720.592841 | 701.656875 | -18.935966 | -2.627832 | False |
| 2026-05 | 701.656875 | 614.251030 | -87.405845 | -12.457064 | False |
| 2026-06 | 614.251030 | 627.190296 | 12.939266 | 2.106511 | False |
| 2026-07 | 627.190296 | 551.777631 | -75.412665 | -12.023889 | False |
| 2026-08 | 551.777631 | 599.419834 | 47.642203 | 8.634312 | False |
| 2026-09 | 599.419834 | 439.984890 | -159.434944 | -26.598210 | False |
| 2026-10 | 439.984890 | 391.972746 | -48.012144 | -10.912226 | False |
| 2026-11 | 391.972746 | 435.406397 | 43.433651 | 11.080783 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
