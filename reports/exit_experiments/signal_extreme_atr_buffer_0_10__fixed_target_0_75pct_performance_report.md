# Performance report: signal_extreme_atr_buffer_0_10__fixed_target_0_75pct

## Run metadata
- Experiment Id: signal_extreme_atr_buffer_0_10__fixed_target_0_75pct
- Stop Model: signal_extreme_atr_buffer_0_10
- Target Model: fixed_target_0_75pct
- Target Value: 0.007500
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
- Final Equity: 16.404603
- Net Pnl: -983.595397
- Total Return Pct: -98.359540
- Max Drawdown Amount: 1,000.195699
- Max Drawdown Pct: 98.388799
- Recovery Factor: -0.983403
- Sharpe Ratio: -10.269853
- Sortino Ratio: -9.429766
- Cagr Pct: -97.753652
- Calmar Ratio: -0.993545
- Worst Daily Loss: -63.077527
- Worst Daily Loss Pct: -8.448039
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 38.119841
- Max Capital Utilization Pct: 102.187501
- Max Gross Exposure: 1,015.284727
- Max Gross Exposure Equity Multiple: 1.021875

## Trade performance

- Trade Count: 5864
- Net Pnl: -983.595397
- Gross Pnl: -144.045913
- Total Fees: 840.501044
- Funding Pnl: 0.951560
- Winning Trades: 2246
- Losing Trades: 3618
- Breakeven Trades: 0
- Win Rate Pct: 38.301501
- Profit Factor: 0.661148
- Expectancy: -0.167735
- Average Win: 0.854467
- Average Loss: 0.802302
- Payoff Ratio: 1.065019
- Max Consecutive Losses: 26
- Average Duration Minutes: 64.473909
- Median Duration Minutes: 31.000000
- Max Duration Minutes: 1,808.000000
- Recovery Factor: -0.983403

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1144 | -122.382793 | -19.388001 | 103.072462 | 0.077670 | 39.860140 | 0.655935 | -0.106978 | 0.511653 | 0.517001 | 0.989656 |
| BTC | 1039 | -177.859885 | -12.106239 | 165.790335 | 0.036689 | 34.167469 | 0.660619 | -0.171184 | 0.975245 | 0.766187 | 1.272855 |
| DOGE | 1300 | -222.709567 | -23.688442 | 199.533203 | 0.512077 | 38.923077 | 0.679816 | -0.171315 | 0.934502 | 0.876030 | 1.066747 |
| ETH | 994 | -241.467860 | -70.396179 | 170.926011 | -0.145671 | 37.223340 | 0.609839 | -0.242925 | 1.020069 | 0.991816 | 1.028486 |
| SOL | 1387 | -219.175291 | -18.467053 | 201.179033 | 0.470794 | 40.302812 | 0.690649 | -0.158021 | 0.875356 | 0.855676 | 1.023000 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1970 | -333.623223 | -41.547940 | 291.465030 | -0.610254 | 36.751269 | 0.656621 | -0.169352 | 0.881169 | 0.779767 | 1.130042 |
| SHORT | 3894 | -649.972173 | -102.497973 | 549.036014 | 1.561814 | 39.085773 | 0.663426 | -0.166916 | 0.841765 | 0.814140 | 1.033933 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 320 | -39.270548 | -12.446789 | 26.745069 | -0.078690 | 38.437500 | 0.571582 | -0.122720 | 0.425963 | 0.465299 | 0.915460 |
| AVAX | SHORT | 824 | -83.112245 | -6.941211 | 76.327393 | 0.156360 | 40.412621 | 0.685220 | -0.100864 | 0.543305 | 0.537745 | 1.010339 |
| BTC | LONG | 383 | -54.928828 | 5.833283 | 60.555639 | -0.206472 | 33.942559 | 0.692698 | -0.143417 | 0.952434 | 0.706503 | 1.348096 |
| BTC | SHORT | 656 | -122.931057 | -17.939522 | 105.234696 | 0.243161 | 34.298780 | 0.644015 | -0.187395 | 0.988425 | 0.801222 | 1.233647 |
| DOGE | LONG | 301 | -30.726599 | 1.568386 | 32.091095 | -0.203889 | 37.873754 | 0.710773 | -0.102082 | 0.662370 | 0.568111 | 1.165916 |
| DOGE | SHORT | 999 | -191.982969 | -25.256827 | 167.442108 | 0.715967 | 39.239239 | 0.674236 | -0.192175 | 1.013643 | 0.970891 | 1.044033 |
| ETH | LONG | 421 | -74.432779 | -7.639917 | 66.536535 | -0.256326 | 35.866983 | 0.667392 | -0.176800 | 0.989089 | 0.828834 | 1.193350 |
| ETH | SHORT | 573 | -167.035081 | -62.756261 | 104.389476 | 0.110656 | 38.219895 | 0.577242 | -0.291510 | 1.041429 | 1.116125 | 0.933076 |
| SOL | LONG | 545 | -134.264469 | -28.862902 | 105.536691 | 0.135124 | 37.798165 | 0.638256 | -0.246357 | 1.149972 | 1.094863 | 1.050334 |
| SOL | SHORT | 842 | -84.910822 | 10.395849 | 95.642341 | 0.335671 | 41.923990 | 0.748294 | -0.100844 | 0.715099 | 0.689858 | 1.036588 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | 0.000959 | 0.016421 | 0.000000 | -0.015462 |
| stop | 3607 | -2,365.441399 | 536.018114 | 0.484250 | -2,900.975263 |
| stop_gap | 10 | -1.362368 | 0.371486 | -0.004492 | -1.738346 |
| target | 2243 | 2,222.175257 | 304.015654 | 0.471802 | 1,918.631406 |
| target_gap | 3 | 0.581638 | 0.079369 | 0.000000 | 0.502269 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 801.353026 | -198.646974 | -19.864697 | False |
| 2025-12 | 801.353026 | 593.754936 | -207.598091 | -25.905947 | False |
| 2026-01 | 593.754936 | 492.578922 | -101.176013 | -17.040029 | False |
| 2026-02 | 492.578922 | 375.859001 | -116.719922 | -23.695679 | False |
| 2026-03 | 375.859001 | 218.349559 | -157.509441 | -41.906524 | False |
| 2026-04 | 218.349559 | 159.842368 | -58.507191 | -26.795195 | False |
| 2026-05 | 159.842368 | 114.739689 | -45.102679 | -28.216974 | False |
| 2026-06 | 114.739689 | 81.582995 | -33.156694 | -28.897319 | False |
| 2026-07 | 81.582995 | 53.470386 | -28.112609 | -34.458908 | False |
| 2026-08 | 53.470386 | 44.789395 | -8.680991 | -16.235138 | False |
| 2026-09 | 44.789395 | 28.326795 | -16.462600 | -36.755576 | False |
| 2026-10 | 28.326795 | 20.374663 | -7.952131 | -28.072825 | False |
| 2026-11 | 20.374663 | 16.404603 | -3.970060 | -19.485279 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
