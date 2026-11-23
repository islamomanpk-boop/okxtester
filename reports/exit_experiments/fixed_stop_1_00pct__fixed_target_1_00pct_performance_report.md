# Performance report: fixed_stop_1_00pct__fixed_target_1_00pct

## Run metadata
- Experiment Id: fixed_stop_1_00pct__fixed_target_1_00pct
- Stop Model: fixed_stop_1_00pct
- Target Model: fixed_target_1_00pct
- Target Value: 0.010000
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
- Final Equity: 270.514295
- Net Pnl: -729.485705
- Total Return Pct: -72.948571
- Max Drawdown Amount: 784.521754
- Max Drawdown Pct: 76.215870
- Recovery Factor: -0.929848
- Sharpe Ratio: -3.815796
- Sortino Ratio: -4.502508
- Cagr Pct: -70.103957
- Calmar Ratio: -0.919808
- Worst Daily Loss: -67.906853
- Worst Daily Loss Pct: -7.186838
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 38.380366
- Max Capital Utilization Pct: 102.373657
- Max Gross Exposure: 1,028.105136
- Max Gross Exposure Equity Multiple: 1.023737

## Trade performance

- Trade Count: 3517
- Net Pnl: -729.485705
- Gross Pnl: -24.613291
- Total Fees: 706.125761
- Funding Pnl: 1.253346
- Winning Trades: 1804
- Losing Trades: 1713
- Breakeven Trades: 0
- Win Rate Pct: 51.293716
- Profit Factor: 0.812410
- Expectancy: -0.207417
- Average Win: 1.751240
- Average Loss: 2.270124
- Payoff Ratio: 0.771429
- Max Consecutive Losses: 23
- Average Duration Minutes: 168.140745
- Median Duration Minutes: 73.000000
- Max Duration Minutes: 3,984.000000
- Recovery Factor: -0.929848

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 715 | -111.812722 | 2.952781 | 114.674974 | -0.090529 | 50.489510 | 0.821862 | -0.156381 | 1.428978 | 1.773089 | 0.805925 |
| BTC | 497 | -91.895597 | 10.739989 | 103.067465 | 0.431879 | 52.917505 | 0.835606 | -0.184901 | 1.776047 | 2.388872 | 0.743467 |
| DOGE | 799 | -175.684124 | -9.253306 | 166.999653 | 0.568834 | 52.315394 | 0.809457 | -0.219880 | 1.785493 | 2.420000 | 0.737807 |
| ETH | 614 | -185.465318 | -45.040979 | 140.467015 | 0.042675 | 50.000000 | 0.767041 | -0.302061 | 1.989129 | 2.593251 | 0.767041 |
| SOL | 892 | -164.627943 | 15.988224 | 180.916654 | 0.300487 | 51.008969 | 0.832679 | -0.184560 | 1.800610 | 2.251500 | 0.799738 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1150 | -277.620679 | -39.050924 | 237.192123 | -1.377632 | 50.173913 | 0.790255 | -0.241409 | 1.812810 | 2.309969 | 0.784777 |
| SHORT | 2367 | -451.865026 | 14.437633 | 468.933638 | 2.630978 | 51.837769 | 0.823842 | -0.190902 | 1.722287 | 2.250097 | 0.765428 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 207 | -67.404038 | -32.906306 | 34.339408 | -0.158324 | 45.410628 | 0.674249 | -0.325623 | 1.484201 | 1.831141 | 0.810533 |
| AVAX | SHORT | 508 | -44.408684 | 35.859087 | 80.335566 | 0.067795 | 52.559055 | 0.894455 | -0.087419 | 1.409536 | 1.745870 | 0.807354 |
| BTC | LONG | 179 | -22.717733 | 16.768746 | 38.994222 | -0.492257 | 54.748603 | 0.889041 | -0.126915 | 1.857367 | 2.527651 | 0.734820 |
| BTC | SHORT | 318 | -69.177864 | -6.028757 | 64.073243 | 0.924135 | 51.886792 | 0.804724 | -0.217540 | 1.727748 | 2.315400 | 0.746198 |
| DOGE | LONG | 177 | -32.259686 | 1.477379 | 33.170001 | -0.567064 | 53.107345 | 0.822260 | -0.182258 | 1.587654 | 2.186737 | 0.726038 |
| DOGE | SHORT | 622 | -143.424439 | -10.730685 | 133.829652 | 1.135898 | 52.090032 | 0.806320 | -0.230586 | 1.842890 | 2.484969 | 0.741615 |
| ETH | LONG | 237 | -59.533150 | -5.853833 | 53.231210 | -0.448107 | 49.789030 | 0.798482 | -0.251195 | 1.999068 | 2.482548 | 0.805249 |
| ETH | SHORT | 377 | -125.932168 | -39.187146 | 87.235805 | 0.490783 | 50.132626 | 0.748490 | -0.334038 | 1.982924 | 2.663323 | 0.744530 |
| SOL | LONG | 350 | -95.706071 | -18.536910 | 77.457281 | 0.288120 | 49.428571 | 0.780002 | -0.273446 | 1.961418 | 2.457804 | 0.798037 |
| SOL | SHORT | 542 | -68.921871 | 34.525134 | 103.459372 | 0.012367 | 52.029520 | 0.874431 | -0.127162 | 1.701959 | 2.111055 | 0.806213 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 2 | -0.958847 | 0.243327 | 0.000000 | -1.202175 |
| stop | 1709 | -3,537.683829 | 347.374211 | 0.566142 | -3,884.491897 |
| stop_gap | 2 | -2.760215 | 0.268973 | 0.000000 | -3.029188 |
| target | 1800 | 3,512.786555 | 357.832369 | 0.687119 | 3,155.641305 |
| target_gap | 4 | 4.003046 | 0.406881 | 0.000085 | 3.596249 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 979.392416 | -20.607584 | -2.060758 | False |
| 2025-12 | 979.392416 | 821.296658 | -158.095758 | -16.142228 | False |
| 2026-01 | 821.296658 | 785.249624 | -36.047033 | -4.389039 | False |
| 2026-02 | 785.249624 | 659.065076 | -126.184548 | -16.069355 | False |
| 2026-03 | 659.065076 | 520.120215 | -138.944861 | -21.082116 | False |
| 2026-04 | 520.120215 | 482.864037 | -37.256178 | -7.162994 | False |
| 2026-05 | 482.864037 | 432.987597 | -49.876440 | -10.329293 | False |
| 2026-06 | 432.987597 | 406.773671 | -26.213927 | -6.054198 | False |
| 2026-07 | 406.773671 | 350.667008 | -56.106663 | -13.793091 | False |
| 2026-08 | 350.667008 | 364.418966 | 13.751958 | 3.921657 | False |
| 2026-09 | 364.418966 | 289.893245 | -74.525722 | -20.450561 | False |
| 2026-10 | 289.893245 | 269.400861 | -20.492383 | -7.068941 | False |
| 2026-11 | 269.400861 | 270.514295 | 1.113434 | 0.413300 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
