# Performance report: fixed_stop_1_00pct__fixed_target_2_00pct

## Run metadata
- Experiment Id: fixed_stop_1_00pct__fixed_target_2_00pct
- Stop Model: fixed_stop_1_00pct
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
- Final Equity: 641.569706
- Net Pnl: -358.430294
- Total Return Pct: -35.843029
- Max Drawdown Amount: 536.858064
- Max Drawdown Pct: 49.757489
- Recovery Factor: -0.667644
- Sharpe Ratio: -1.028271
- Sortino Ratio: -1.454202
- Cagr Pct: -33.627992
- Calmar Ratio: -0.675838
- Worst Daily Loss: -78.293626
- Worst Daily Loss Pct: -7.353799
- Worst Daily Loss Date Utc: 2026-02-06
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 42.483616
- Max Capital Utilization Pct: 102.820916
- Max Gross Exposure: 1,058.419107
- Max Gross Exposure Equity Multiple: 1.028209

## Trade performance

- Trade Count: 2180
- Net Pnl: -358.430294
- Gross Pnl: 245.449952
- Total Fees: 605.536719
- Funding Pnl: 1.656472
- Winning Trades: 780
- Losing Trades: 1400
- Breakeven Trades: 0
- Win Rate Pct: 35.779817
- Profit Factor: 0.918222
- Expectancy: -0.164418
- Average Win: 5.159632
- Average Loss: 3.130674
- Payoff Ratio: 1.648090
- Max Consecutive Losses: 46
- Average Duration Minutes: 315.996789
- Median Duration Minutes: 129.000000
- Max Duration Minutes: 6,473.000000
- Recovery Factor: -0.667644

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 442 | -133.476451 | -19.209335 | 114.111512 | -0.155604 | 33.710407 | 0.842999 | -0.301983 | 4.809961 | 2.901572 | 1.657709 |
| BTC | 306 | 30.332711 | 115.654076 | 85.517820 | 0.196455 | 39.542484 | 1.051633 | 0.099127 | 5.105811 | 3.175516 | 1.607868 |
| DOGE | 500 | -35.516223 | 101.717630 | 138.280493 | 1.046640 | 37.600000 | 0.963920 | -0.071032 | 5.047179 | 3.155083 | 1.599698 |
| ETH | 386 | -153.000037 | -39.337313 | 113.905701 | 0.242977 | 32.642487 | 0.821411 | -0.396373 | 5.585038 | 3.295057 | 1.694975 |
| SOL | 546 | -66.770295 | 86.624894 | 153.721193 | 0.326004 | 35.897436 | 0.939531 | -0.122290 | 5.293067 | 3.154890 | 1.677734 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 691 | -141.253151 | 66.096846 | 204.458687 | -2.891310 | 34.153401 | 0.905010 | -0.204418 | 5.702481 | 3.268217 | 1.744829 |
| SHORT | 1489 | -217.177143 | 179.353107 | 401.078032 | 4.547782 | 36.534587 | 0.925005 | -0.145854 | 4.924131 | 3.064449 | 1.606857 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 126 | -67.997222 | -33.026719 | 34.548590 | -0.421913 | 30.158730 | 0.746254 | -0.539660 | 5.262530 | 3.045152 | 1.728167 |
| AVAX | SHORT | 316 | -65.479229 | 13.817384 | 79.562922 | 0.266309 | 35.126582 | 0.887529 | -0.207213 | 4.655028 | 2.839938 | 1.639130 |
| BTC | LONG | 99 | 57.523043 | 90.515335 | 32.099315 | -0.892977 | 43.434343 | 1.282610 | 0.581041 | 6.071283 | 3.634681 | 1.670376 |
| BTC | SHORT | 207 | -27.190331 | 25.138742 | 53.418505 | 1.089432 | 37.681159 | 0.929179 | -0.131354 | 4.573564 | 2.976188 | 1.536718 |
| DOGE | LONG | 117 | 4.126185 | 36.927885 | 31.818950 | -0.982749 | 35.042735 | 1.018613 | 0.035267 | 5.507681 | 2.916957 | 1.888160 |
| DOGE | SHORT | 383 | -39.642408 | 64.789745 | 106.461542 | 2.029389 | 38.381201 | 0.948023 | -0.103505 | 4.918739 | 3.231767 | 1.521997 |
| ETH | LONG | 142 | -84.480786 | -40.707416 | 43.036746 | -0.736625 | 30.985915 | 0.746728 | -0.594935 | 5.660847 | 3.403654 | 1.663168 |
| ETH | SHORT | 244 | -68.519251 | 1.370103 | 70.868955 | 0.979602 | 33.606557 | 0.869027 | -0.280817 | 5.544360 | 3.229363 | 1.716859 |
| SOL | LONG | 207 | -50.424371 | 12.387761 | 62.955086 | 0.142954 | 33.816425 | 0.890448 | -0.243596 | 5.855029 | 3.359682 | 1.742733 |
| SOL | SHORT | 339 | -16.345924 | 74.237133 | 90.766107 | 0.183051 | 37.168142 | 0.974616 | -0.048218 | 4.980866 | 3.023169 | 1.647564 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 2 | -2.274066 | 0.577091 | 0.000000 | -2.851157 |
| stop | 1396 | -3,984.899138 | 391.291608 | 0.640280 | -4,375.550465 |
| stop_gap | 2 | -4.138218 | 0.403260 | 0.000000 | -4.541478 |
| target | 779 | 4,236.725304 | 213.262957 | 1.016192 | 4,024.478539 |
| target_gap | 1 | 0.036070 | 0.001803 | 0.000000 | 0.034267 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 1,015.467155 | 15.467155 | 1.546715 | False |
| 2025-12 | 1,015.467155 | 924.087308 | -91.379847 | -8.998799 | False |
| 2026-01 | 924.087308 | 905.722730 | -18.364578 | -1.987321 | False |
| 2026-02 | 905.722730 | 871.436016 | -34.286714 | -3.785564 | False |
| 2026-03 | 871.436016 | 743.331127 | -128.104889 | -14.700435 | False |
| 2026-04 | 743.331127 | 730.815047 | -12.516080 | -1.683783 | False |
| 2026-05 | 730.815047 | 675.726955 | -55.088092 | -7.537898 | False |
| 2026-06 | 675.726955 | 679.464374 | 3.737419 | 0.553096 | False |
| 2026-07 | 679.464374 | 619.707005 | -59.757369 | -8.794776 | False |
| 2026-08 | 619.707005 | 717.304794 | 97.597790 | 15.749022 | False |
| 2026-09 | 717.304794 | 597.224013 | -120.080782 | -16.740552 | False |
| 2026-10 | 597.224013 | 573.496565 | -23.727448 | -3.972956 | False |
| 2026-11 | 573.496565 | 641.569706 | 68.073142 | 11.869843 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
