# Performance report: signal_extreme_atr_buffer_0_10__target_2R

## Run metadata
- Experiment Id: signal_extreme_atr_buffer_0_10__target_2R
- Stop Model: signal_extreme_atr_buffer_0_10
- Target Model: target_2R
- Target Value: 2.000000
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
- Final Equity: 44.808115
- Net Pnl: -955.191885
- Total Return Pct: -95.519188
- Max Drawdown Amount: 970.644612
- Max Drawdown Pct: 95.862530
- Recovery Factor: -0.984080
- Sharpe Ratio: -7.504796
- Sortino Ratio: -7.700410
- Cagr Pct: -94.318085
- Calmar Ratio: -0.983889
- Worst Daily Loss: -60.249564
- Worst Daily Loss Pct: -7.721675
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 39.589658
- Max Capital Utilization Pct: 102.508170
- Max Gross Exposure: 999.344601
- Max Gross Exposure Equity Multiple: 1.025082

## Trade performance

- Trade Count: 4458
- Net Pnl: -955.191885
- Gross Pnl: -196.326334
- Total Fees: 759.651954
- Funding Pnl: 0.786403
- Winning Trades: 1454
- Losing Trades: 3004
- Breakeven Trades: 0
- Win Rate Pct: 32.615523
- Profit Factor: 0.681147
- Expectancy: -0.214265
- Average Win: 1.403383
- Average Loss: 0.997241
- Payoff Ratio: 1.407266
- Max Consecutive Losses: 22
- Average Duration Minutes: 109.289592
- Median Duration Minutes: 38.000000
- Max Duration Minutes: 8,591.000000
- Recovery Factor: -0.984080

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 848 | -133.637045 | -35.360495 | 98.207920 | -0.068630 | 32.193396 | 0.656154 | -0.157591 | 0.934125 | 0.675919 | 1.382008 |
| BTC | 819 | -162.293114 | -11.466750 | 150.881871 | 0.055507 | 33.333333 | 0.681611 | -0.198160 | 1.272669 | 0.933575 | 1.363221 |
| DOGE | 1022 | -192.976546 | -17.396197 | 176.061558 | 0.481208 | 33.170254 | 0.725378 | -0.188822 | 1.503607 | 1.028842 | 1.461455 |
| ETH | 802 | -244.008736 | -93.671121 | 150.229367 | -0.108248 | 31.296758 | 0.628467 | -0.304250 | 1.644438 | 1.191947 | 1.379624 |
| SOL | 967 | -222.276444 | -38.431771 | 184.271238 | 0.426565 | 32.885212 | 0.698757 | -0.229862 | 1.621346 | 1.136925 | 1.426080 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1478 | -368.730833 | -81.151339 | 286.862843 | -0.716650 | 31.190798 | 0.648493 | -0.249480 | 1.475635 | 1.031464 | 1.430622 |
| SHORT | 2980 | -586.461052 | -115.174994 | 472.789111 | 1.503053 | 33.322148 | 0.698743 | -0.196799 | 1.369840 | 0.979724 | 1.398189 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 236 | -42.576089 | -12.569266 | 29.939888 | -0.066935 | 28.813559 | 0.617171 | -0.180407 | 1.009385 | 0.661990 | 1.524774 |
| AVAX | SHORT | 612 | -91.060956 | -22.791230 | 68.268032 | -0.001694 | 33.496732 | 0.671780 | -0.148792 | 0.909161 | 0.681668 | 1.333730 |
| BTC | LONG | 310 | -60.341302 | -1.403926 | 58.670534 | -0.266841 | 33.225806 | 0.674227 | -0.194649 | 1.212465 | 0.894808 | 1.355001 |
| BTC | SHORT | 509 | -101.951812 | -10.062824 | 92.211337 | 0.322348 | 33.398821 | 0.685825 | -0.200298 | 1.309145 | 0.957246 | 1.367616 |
| DOGE | LONG | 228 | -50.756568 | -16.620580 | 33.847150 | -0.288838 | 30.701754 | 0.614573 | -0.222617 | 1.156179 | 0.833475 | 1.387179 |
| DOGE | SHORT | 794 | -142.219978 | -0.775616 | 142.214408 | 0.770047 | 33.879093 | 0.750933 | -0.179118 | 1.594015 | 1.087638 | 1.465575 |
| ETH | LONG | 320 | -97.035840 | -35.416128 | 61.293436 | -0.326276 | 29.687500 | 0.593437 | -0.303237 | 1.490923 | 1.060771 | 1.405509 |
| ETH | SHORT | 482 | -146.972896 | -58.254992 | 88.935931 | 0.218027 | 32.365145 | 0.648465 | -0.304923 | 1.737924 | 1.282482 | 1.355126 |
| SOL | LONG | 384 | -118.021034 | -15.141439 | 103.111835 | 0.232240 | 32.552083 | 0.691203 | -0.307346 | 2.113403 | 1.475662 | 1.432173 |
| SOL | SHORT | 583 | -104.255410 | -23.290332 | 81.159403 | 0.194325 | 33.104631 | 0.706874 | -0.178826 | 1.302655 | 0.911969 | 1.428399 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | -0.163099 | 0.016286 | 0.000777 | -0.178608 |
| stop | 2994 | -2,469.592281 | 523.365041 | 0.178495 | -2,992.778826 |
| stop_gap | 9 | -2.084001 | 0.663449 | -0.006175 | -2.753624 |
| target | 1448 | 2,273.452392 | 235.192729 | 0.613305 | 2,038.872968 |
| target_gap | 6 | 2.060655 | 0.414449 | 0.000000 | 1.646206 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 831.914116 | -168.085884 | -16.808588 | False |
| 2025-12 | 831.914116 | 662.699178 | -169.214938 | -20.340434 | False |
| 2026-01 | 662.699178 | 577.269946 | -85.429231 | -12.891103 | False |
| 2026-02 | 577.269946 | 475.085448 | -102.184499 | -17.701337 | False |
| 2026-03 | 475.085448 | 299.239797 | -175.845651 | -37.013479 | False |
| 2026-04 | 299.239797 | 224.693205 | -74.546592 | -24.911991 | False |
| 2026-05 | 224.693205 | 152.860236 | -71.832969 | -31.969355 | False |
| 2026-06 | 152.860236 | 140.106452 | -12.753783 | -8.343428 | False |
| 2026-07 | 140.106452 | 100.195761 | -39.910691 | -28.485976 | False |
| 2026-08 | 100.195761 | 92.350181 | -7.845581 | -7.830252 | False |
| 2026-09 | 92.350181 | 64.214287 | -28.135894 | -30.466528 | False |
| 2026-10 | 64.214287 | 47.517423 | -16.696864 | -26.001790 | False |
| 2026-11 | 47.517423 | 44.808115 | -2.709307 | -5.701714 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
