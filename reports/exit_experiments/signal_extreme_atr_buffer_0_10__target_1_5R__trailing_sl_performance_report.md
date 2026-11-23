# Performance report: signal_extreme_atr_buffer_0_10__target_1_5R__trailing_sl

## Run metadata
- Experiment Id: signal_extreme_atr_buffer_0_10__target_1_5R__trailing_sl
- Stop Model: signal_extreme_atr_buffer_0_10
- Target Model: target_1_5R
- Target Value: 1.500000
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
- Final Equity: 6.907342
- Net Pnl: -993.092658
- Total Return Pct: -99.309266
- Max Drawdown Amount: 1,010.407181
- Max Drawdown Pct: 99.321022
- Recovery Factor: -0.982864
- Sharpe Ratio: -11.704777
- Sortino Ratio: -10.387490
- Cagr Pct: -98.989467
- Calmar Ratio: -0.996662
- Worst Daily Loss: -56.358093
- Worst Daily Loss Pct: -7.618236
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 34.271367
- Max Capital Utilization Pct: 102.266115
- Max Gross Exposure: 1,009.439323
- Max Gross Exposure Equity Multiple: 1.022661

## Trade performance

- Trade Count: 6417
- Net Pnl: -993.092658
- Gross Pnl: -141.051659
- Total Fees: 852.889137
- Funding Pnl: 0.848137
- Winning Trades: 2301
- Losing Trades: 4116
- Breakeven Trades: 0
- Win Rate Pct: 35.857878
- Profit Factor: 0.607725
- Expectancy: -0.154760
- Average Win: 0.668635
- Average Loss: 0.615068
- Payoff Ratio: 1.087090
- Max Consecutive Losses: 24
- Average Duration Minutes: 58.531089
- Median Duration Minutes: 24.000000
- Max Duration Minutes: 4,051.000000
- Recovery Factor: -0.982864

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1165 | -117.613286 | -18.599728 | 99.012615 | -0.000942 | 35.879828 | 0.588467 | -0.100956 | 0.402344 | 0.382588 | 1.051639 |
| BTC | 1186 | -210.488259 | -39.863559 | 170.794924 | 0.170224 | 34.485666 | 0.540067 | -0.177477 | 0.604307 | 0.588996 | 1.025995 |
| DOGE | 1525 | -190.726576 | 9.528173 | 200.565484 | 0.310735 | 37.114754 | 0.674327 | -0.125067 | 0.697725 | 0.610677 | 1.142544 |
| ETH | 1113 | -217.798793 | -44.725766 | 173.008878 | -0.064149 | 35.399820 | 0.603075 | -0.195686 | 0.839890 | 0.763165 | 1.100536 |
| SOL | 1428 | -256.465745 | -47.390779 | 209.507236 | 0.432269 | 35.994398 | 0.607745 | -0.179598 | 0.773071 | 0.715344 | 1.080698 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2244 | -368.391457 | -64.931740 | 303.053852 | -0.405865 | 34.135472 | 0.553963 | -0.164167 | 0.597298 | 0.558810 | 1.068874 |
| SHORT | 4173 | -624.701202 | -76.119919 | 549.835285 | 1.254002 | 36.784088 | 0.633757 | -0.149701 | 0.704234 | 0.646588 | 1.089153 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 336 | -41.322434 | -16.088946 | 25.196407 | -0.037081 | 30.654762 | 0.437707 | -0.122983 | 0.312298 | 0.315404 | 0.990153 |
| AVAX | SHORT | 829 | -76.290851 | -2.510782 | 73.816208 | 0.036139 | 37.997587 | 0.640653 | -0.092028 | 0.431788 | 0.413043 | 1.045383 |
| BTC | LONG | 449 | -63.796744 | -3.522033 | 60.183601 | -0.091110 | 35.857461 | 0.542295 | -0.142086 | 0.469487 | 0.483973 | 0.970069 |
| BTC | SHORT | 737 | -146.691515 | -36.341526 | 110.611323 | 0.261334 | 33.649932 | 0.539091 | -0.199039 | 0.691831 | 0.650850 | 1.062965 |
| DOGE | LONG | 354 | -36.371065 | -4.790319 | 31.432173 | -0.148572 | 36.723164 | 0.562487 | -0.102743 | 0.359695 | 0.371122 | 0.969209 |
| DOGE | SHORT | 1171 | -154.355511 | 14.318492 | 169.133311 | 0.459308 | 37.233134 | 0.692830 | -0.131815 | 0.798514 | 0.683684 | 1.167958 |
| ETH | LONG | 514 | -68.529516 | 3.001505 | 71.308690 | -0.222330 | 33.463035 | 0.647982 | -0.133326 | 0.733410 | 0.569228 | 1.288429 |
| ETH | SHORT | 599 | -149.269277 | -47.727271 | 101.700188 | 0.158182 | 37.061770 | 0.578382 | -0.249197 | 0.922388 | 0.939097 | 0.982208 |
| SOL | LONG | 591 | -158.371698 | -43.531946 | 114.932981 | 0.093229 | 33.840948 | 0.527588 | -0.267972 | 0.884345 | 0.857393 | 1.031435 |
| SOL | SHORT | 837 | -98.094047 | -3.858833 | 94.574254 | 0.339040 | 37.514934 | 0.692093 | -0.117197 | 0.702195 | 0.609146 | 1.152754 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| stop | 4425 | -1,908.010403 | 584.957266 | 0.290934 | -2,492.676735 |
| stop_gap | 35 | -0.793085 | 3.869276 | 0.000000 | -4.662361 |
| target | 1955 | 1,767.032475 | 263.881587 | 0.557203 | 1,503.708090 |
| target_gap | 2 | 0.719355 | 0.181008 | 0.000000 | 0.538347 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 798.585120 | -201.414880 | -20.141488 | False |
| 2025-12 | 798.585120 | 559.469835 | -239.115285 | -29.942367 | False |
| 2026-01 | 559.469835 | 429.496973 | -129.972862 | -23.231433 | False |
| 2026-02 | 429.496973 | 318.503736 | -110.993238 | -25.842612 | False |
| 2026-03 | 318.503736 | 174.454893 | -144.048843 | -45.226736 | False |
| 2026-04 | 174.454893 | 111.244331 | -63.210563 | -36.233184 | False |
| 2026-05 | 111.244331 | 70.955058 | -40.289272 | -36.216922 | False |
| 2026-06 | 70.955058 | 49.293513 | -21.661545 | -30.528543 | False |
| 2026-07 | 49.293513 | 30.829013 | -18.464500 | -37.458275 | False |
| 2026-08 | 30.829013 | 26.700251 | -4.128762 | -13.392456 | False |
| 2026-09 | 26.700251 | 15.477178 | -11.223073 | -42.033585 | False |
| 2026-10 | 15.477178 | 9.356719 | -6.120459 | -39.545059 | False |
| 2026-11 | 9.356719 | 6.907342 | -2.449377 | -26.177738 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
