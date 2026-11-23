# Performance report: fixed_stop_0_75pct__fixed_target_2_00pct__trailing_tp

## Run metadata
- Experiment Id: fixed_stop_0_75pct__fixed_target_2_00pct__trailing_tp
- Stop Model: fixed_stop_0_75pct
- Target Model: fixed_target_2_00pct
- Target Value: 0.020000
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
- Final Equity: 422.468214
- Net Pnl: -577.531786
- Total Return Pct: -57.753179
- Max Drawdown Amount: 671.983375
- Max Drawdown Pct: 64.305293
- Recovery Factor: -0.859444
- Sharpe Ratio: -1.968217
- Sortino Ratio: -2.572363
- Cagr Pct: -54.875584
- Calmar Ratio: -0.853360
- Worst Daily Loss: -73.518725
- Worst Daily Loss Pct: -7.399112
- Worst Daily Loss Date Utc: 2026-02-06
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 45.375385
- Max Capital Utilization Pct: 103.162551
- Max Gross Exposure: 1,044.984137
- Max Gross Exposure Equity Multiple: 1.031626

## Trade performance

- Trade Count: 2479
- Net Pnl: -577.531786
- Gross Pnl: 140.771993
- Total Fees: 719.970345
- Funding Pnl: 1.666566
- Winning Trades: 723
- Losing Trades: 1756
- Breakeven Trades: 0
- Win Rate Pct: 29.164986
- Profit Factor: 0.871473
- Expectancy: -0.232970
- Average Win: 5.416241
- Average Loss: 2.558926
- Payoff Ratio: 2.116607
- Max Consecutive Losses: 48
- Average Duration Minutes: 246.584510
- Median Duration Minutes: 97.000000
- Max Duration Minutes: 6,443.000000
- Recovery Factor: -0.859444

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 496 | -197.325876 | -71.011200 | 126.214767 | -0.099909 | 27.419355 | 0.759032 | -0.397834 | 4.570317 | 2.274692 | 2.009203 |
| BTC | 366 | 8.531833 | 116.706842 | 108.416563 | 0.241555 | 31.693989 | 1.013222 | 0.023311 | 5.636437 | 2.581179 | 2.183667 |
| DOGE | 569 | -102.992701 | 67.722864 | 171.750334 | 1.034769 | 30.579965 | 0.903282 | -0.181007 | 5.528082 | 2.695896 | 2.050555 |
| ETH | 450 | -237.065672 | -100.043798 | 137.182549 | 0.160676 | 27.111111 | 0.732805 | -0.526813 | 5.329276 | 2.704992 | 1.970163 |
| SOL | 598 | -48.679371 | 127.397286 | 176.406132 | 0.329475 | 29.264214 | 0.954808 | -0.081404 | 5.877110 | 2.546510 | 2.307908 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 793 | -218.608876 | 46.758759 | 262.678183 | -2.689453 | 27.616646 | 0.867421 | -0.275673 | 6.531002 | 2.872645 | 2.273515 |
| SHORT | 1686 | -358.922910 | 94.013234 | 457.292163 | 4.356018 | 29.893238 | 0.873822 | -0.212884 | 4.931850 | 2.406578 | 2.049321 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 149 | -82.531264 | -39.384112 | 42.833873 | -0.313280 | 23.489933 | 0.708769 | -0.553901 | 5.738760 | 2.485859 | 2.308563 |
| AVAX | SHORT | 347 | -114.794612 | -31.627088 | 83.380894 | 0.213370 | 29.106628 | 0.785631 | -0.330820 | 4.165411 | 2.176834 | 1.913518 |
| BTC | LONG | 123 | -12.554993 | 31.338637 | 42.952239 | -0.941392 | 29.268293 | 0.952930 | -0.102073 | 7.060412 | 3.065860 | 2.302914 |
| BTC | SHORT | 243 | 21.086826 | 85.368204 | 65.464324 | 1.182946 | 32.921811 | 1.055702 | 0.086777 | 4.995648 | 2.322485 | 2.150993 |
| DOGE | LONG | 127 | 1.364159 | 42.777316 | 40.561856 | -0.851301 | 29.921260 | 1.005610 | 0.010741 | 6.435524 | 2.732424 | 2.355243 |
| DOGE | SHORT | 442 | -104.356860 | 24.945548 | 131.188478 | 1.886070 | 30.769231 | 0.872998 | -0.236101 | 5.274533 | 2.685272 | 1.964245 |
| ETH | LONG | 169 | -70.096274 | -13.072842 | 56.284246 | -0.739187 | 27.810651 | 0.802500 | -0.414771 | 6.060049 | 2.909169 | 2.083086 |
| ETH | SHORT | 281 | -166.969398 | -86.970957 | 80.898303 | 0.899862 | 26.690391 | 0.686336 | -0.594197 | 4.871324 | 2.584071 | 1.885135 |
| SOL | LONG | 225 | -54.790503 | 25.099760 | 80.045969 | 0.155706 | 28.000000 | 0.890567 | -0.243513 | 7.077552 | 3.090594 | 2.290029 |
| SOL | SHORT | 373 | 6.111133 | 102.297527 | 96.360163 | 0.173769 | 30.026810 | 1.010600 | 0.016384 | 5.201861 | 2.208802 | 2.355060 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | 0.014227 | 0.243676 | 0.000000 | -0.229449 |
| stop | 1753 | -3,973.288388 | 516.514210 | 0.604702 | -4,489.197896 |
| stop_gap | 2 | -3.584229 | 0.462267 | 0.000000 | -4.046496 |
| trailing_take_profit | 602 | 3,429.074791 | 170.488909 | 0.589927 | 3,259.175808 |
| trailing_take_profit_gap | 121 | 688.555593 | 32.261284 | 0.471937 | 656.766246 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 996.309125 | -3.690875 | -0.369087 | False |
| 2025-12 | 996.309125 | 857.912474 | -138.396651 | -13.890935 | False |
| 2026-01 | 857.912474 | 842.785300 | -15.127174 | -1.763254 | False |
| 2026-02 | 842.785300 | 810.533579 | -32.251721 | -3.826802 | False |
| 2026-03 | 810.533579 | 687.951463 | -122.582117 | -15.123632 | False |
| 2026-04 | 687.951463 | 675.619745 | -12.331718 | -1.792527 | False |
| 2026-05 | 675.619745 | 591.186688 | -84.433056 | -12.497127 | False |
| 2026-06 | 591.186688 | 608.589103 | 17.402414 | 2.943641 | False |
| 2026-07 | 608.589103 | 526.561410 | -82.027693 | -13.478337 | False |
| 2026-08 | 526.561410 | 585.246024 | 58.684614 | 11.144876 | False |
| 2026-09 | 585.246024 | 435.641159 | -149.604864 | -25.562731 | False |
| 2026-10 | 435.641159 | 388.986956 | -46.654203 | -10.709319 | False |
| 2026-11 | 388.986956 | 422.468214 | 33.481258 | 8.607296 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
