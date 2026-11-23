# Performance report: signal_extreme_exact__target_1_5R

## Run metadata
- Experiment Id: signal_extreme_exact__target_1_5R
- Stop Model: signal_extreme_exact
- Target Model: target_1_5R
- Target Value: 1.500000
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
- Final Equity: 9.363114
- Net Pnl: -990.636886
- Total Return Pct: -99.063689
- Max Drawdown Amount: 1,014.614295
- Max Drawdown Pct: 99.085613
- Recovery Factor: -0.976368
- Sharpe Ratio: -10.754427
- Sortino Ratio: -9.850089
- Cagr Pct: -98.661690
- Calmar Ratio: -0.995722
- Worst Daily Loss: -57.134675
- Worst Daily Loss Pct: -8.307372
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 35.585140
- Max Capital Utilization Pct: 102.520907
- Max Gross Exposure: 1,012.526547
- Max Gross Exposure Equity Multiple: 1.025209

## Trade performance

- Trade Count: 6080
- Net Pnl: -990.636886
- Gross Pnl: -148.289765
- Total Fees: 843.018388
- Funding Pnl: 0.671267
- Winning Trades: 2319
- Losing Trades: 3761
- Breakeven Trades: 0
- Win Rate Pct: 38.141447
- Profit Factor: 0.616093
- Expectancy: -0.162934
- Average Win: 0.685543
- Average Loss: 0.686097
- Payoff Ratio: 0.999192
- Max Consecutive Losses: 20
- Average Duration Minutes: 63.873355
- Median Duration Minutes: 21.000000
- Max Duration Minutes: 4,050.000000
- Recovery Factor: -0.976368

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1124 | -140.726838 | -33.622839 | 107.146968 | 0.042969 | 38.790036 | 0.562354 | -0.125202 | 0.414741 | 0.467375 | 0.887384 |
| BTC | 1171 | -193.677606 | -14.675491 | 179.110137 | 0.108023 | 37.147737 | 0.591324 | -0.165395 | 0.644223 | 0.643906 | 1.000493 |
| DOGE | 1403 | -198.155856 | -5.954500 | 192.493691 | 0.292336 | 39.272986 | 0.668353 | -0.141237 | 0.724746 | 0.701280 | 1.033461 |
| ETH | 1042 | -205.326147 | -40.998086 | 164.329451 | 0.001390 | 36.948177 | 0.621443 | -0.197050 | 0.875496 | 0.825558 | 1.060489 |
| SOL | 1340 | -252.750440 | -53.038848 | 199.938141 | 0.226550 | 38.208955 | 0.608175 | -0.188620 | 0.766227 | 0.779057 | 0.983532 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2128 | -339.155770 | -37.753745 | 301.036423 | -0.365603 | 37.124060 | 0.597805 | -0.159378 | 0.638110 | 0.630241 | 1.012485 |
| SHORT | 3952 | -651.481115 | -110.536020 | 541.981965 | 1.036870 | 38.689271 | 0.624971 | -0.164848 | 0.710050 | 0.716941 | 0.990389 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 321 | -49.790471 | -20.914258 | 28.857921 | -0.018291 | 34.890966 | 0.439189 | -0.155111 | 0.348147 | 0.424799 | 0.819558 |
| AVAX | SHORT | 803 | -90.936367 | -12.708581 | 78.289047 | 0.061261 | 40.348692 | 0.609331 | -0.113246 | 0.437760 | 0.485951 | 0.900832 |
| BTC | LONG | 435 | -60.511845 | 6.048497 | 66.462653 | -0.097690 | 37.701149 | 0.608006 | -0.139108 | 0.572303 | 0.569629 | 1.004693 |
| BTC | SHORT | 736 | -133.165760 | -20.723989 | 112.647484 | 0.205712 | 36.820652 | 0.583265 | -0.180932 | 0.687747 | 0.687194 | 1.000805 |
| DOGE | LONG | 338 | -35.931879 | -3.306179 | 32.445260 | -0.180440 | 38.757396 | 0.614719 | -0.106307 | 0.437631 | 0.450539 | 0.971350 |
| DOGE | SHORT | 1065 | -162.223976 | -2.648321 | 160.048431 | 0.472776 | 39.436620 | 0.678273 | -0.152323 | 0.814299 | 0.781751 | 1.041634 |
| ETH | LONG | 481 | -54.392311 | 7.877051 | 62.090244 | -0.179119 | 36.590437 | 0.679936 | -0.113082 | 0.656532 | 0.557187 | 1.178298 |
| ETH | SHORT | 561 | -150.933836 | -48.875137 | 102.239207 | 0.180508 | 37.254902 | 0.594754 | -0.269044 | 1.059886 | 1.058097 | 1.001691 |
| SOL | LONG | 553 | -138.529264 | -27.458856 | 111.180345 | 0.109937 | 37.432188 | 0.588820 | -0.250505 | 0.958345 | 0.973719 | 0.984211 |
| SOL | SHORT | 787 | -114.221176 | -25.579992 | 88.757796 | 0.116613 | 38.754765 | 0.629335 | -0.145135 | 0.635839 | 0.639320 | 0.994556 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| stop | 3684 | -2,047.327860 | 514.528089 | 0.156719 | -2,561.699230 |
| stop_gap | 30 | -11.752380 | 4.388779 | 0.013450 | -16.127709 |
| target | 2362 | 1,908.678620 | 323.156396 | 0.501099 | 1,586.023323 |
| target_gap | 4 | 2.111855 | 0.945124 | 0.000000 | 1.166731 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 730.987957 | -269.012043 | -26.901204 | False |
| 2025-12 | 730.987957 | 541.082423 | -189.905534 | -25.979297 | False |
| 2026-01 | 541.082423 | 408.795337 | -132.287086 | -24.448602 | False |
| 2026-02 | 408.795337 | 326.775206 | -82.020131 | -20.063862 | False |
| 2026-03 | 326.775206 | 194.571267 | -132.203939 | -40.457151 | False |
| 2026-04 | 194.571267 | 133.595606 | -60.975661 | -31.338471 | False |
| 2026-05 | 133.595606 | 83.206717 | -50.388889 | -37.717475 | False |
| 2026-06 | 83.206717 | 60.536757 | -22.669961 | -27.245349 | False |
| 2026-07 | 60.536757 | 38.093692 | -22.443065 | -37.073451 | False |
| 2026-08 | 38.093692 | 33.530651 | -4.563041 | -11.978468 | False |
| 2026-09 | 33.530651 | 20.921632 | -12.609019 | -37.604455 | False |
| 2026-10 | 20.921632 | 12.361761 | -8.559872 | -40.913976 | False |
| 2026-11 | 12.361761 | 9.363114 | -2.998646 | -24.257437 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
