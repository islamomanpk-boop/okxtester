# Performance report: signal_extreme_atr_buffer_0_10__fixed_target_2_00pct__trailing_tp

## Run metadata
- Experiment Id: signal_extreme_atr_buffer_0_10__fixed_target_2_00pct__trailing_tp
- Stop Model: signal_extreme_atr_buffer_0_10
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
- Final Equity: 214.473644
- Net Pnl: -785.526356
- Total Return Pct: -78.552636
- Max Drawdown Amount: 814.211152
- Max Drawdown Pct: 80.624900
- Recovery Factor: -0.964770
- Sharpe Ratio: -3.545676
- Sortino Ratio: -4.320625
- Cagr Pct: -75.872774
- Calmar Ratio: -0.941059
- Worst Daily Loss: -67.428192
- Worst Daily Loss Pct: -7.899855
- Worst Daily Loss Date Utc: 2026-02-06
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 45.856084
- Max Capital Utilization Pct: 103.047360
- Max Gross Exposure: 1,000.707190
- Max Gross Exposure Equity Multiple: 1.030474

## Trade performance

- Trade Count: 3147
- Net Pnl: -785.526356
- Gross Pnl: 16.761218
- Total Fees: 804.264767
- Funding Pnl: 1.977193
- Winning Trades: 692
- Losing Trades: 2455
- Breakeven Trades: 0
- Win Rate Pct: 21.989196
- Profit Factor: 0.787809
- Expectancy: -0.249611
- Average Win: 4.214532
- Average Loss: 1.507936
- Payoff Ratio: 2.794901
- Max Consecutive Losses: 59
- Average Duration Minutes: 173.597394
- Median Duration Minutes: 55.000000
- Max Duration Minutes: 4,405.000000
- Recovery Factor: -0.964770

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 605 | -166.171266 | -43.529851 | 122.825357 | 0.183941 | 20.826446 | 0.709634 | -0.274663 | 3.223103 | 1.194744 | 2.697736 |
| BTC | 538 | -143.529104 | 1.102794 | 144.699625 | 0.067727 | 18.773234 | 0.759496 | -0.266783 | 4.487691 | 1.365643 | 3.286138 |
| DOGE | 723 | -136.952192 | 65.756703 | 203.948420 | 1.239525 | 23.513140 | 0.854157 | -0.189422 | 4.718157 | 1.698081 | 2.778523 |
| ETH | 546 | -199.576179 | -58.164010 | 141.414088 | 0.001919 | 21.978022 | 0.713339 | -0.365524 | 4.138617 | 1.634296 | 2.532354 |
| SOL | 735 | -139.297614 | 51.595582 | 191.377277 | 0.484081 | 23.809524 | 0.844822 | -0.189521 | 4.333529 | 1.602974 | 2.703431 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 983 | -293.709554 | 19.976769 | 311.970842 | -1.715480 | 20.345880 | 0.783330 | -0.298789 | 5.309261 | 1.731241 | 3.066737 |
| SHORT | 2164 | -491.816802 | -3.215551 | 492.293924 | 3.692674 | 22.735675 | 0.790397 | -0.227272 | 3.769520 | 1.403362 | 2.686065 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 167 | -62.706677 | -22.482028 | 40.094701 | -0.129947 | 18.562874 | 0.662140 | -0.375489 | 3.964288 | 1.364703 | 2.904873 |
| AVAX | SHORT | 438 | -103.464590 | -21.047823 | 82.730655 | 0.313889 | 21.689498 | 0.732430 | -0.236221 | 2.981242 | 1.127355 | 2.644459 |
| BTC | LONG | 172 | -39.111360 | 23.013465 | 61.605376 | -0.519449 | 18.023256 | 0.830025 | -0.227392 | 6.160947 | 1.631920 | 3.775275 |
| BTC | SHORT | 366 | -104.417744 | -21.910671 | 83.094249 | 0.587176 | 19.125683 | 0.715239 | -0.285294 | 3.746678 | 1.238801 | 3.024438 |
| DOGE | LONG | 169 | -49.398410 | 1.933248 | 50.718910 | -0.612749 | 20.710059 | 0.782294 | -0.292298 | 5.071607 | 1.693318 | 2.995070 |
| DOGE | SHORT | 554 | -87.553782 | 63.823455 | 153.229510 | 1.852274 | 24.368231 | 0.877054 | -0.158039 | 4.626521 | 1.699604 | 2.722117 |
| ETH | LONG | 207 | -77.936701 | -18.022755 | 59.279333 | -0.634613 | 20.289855 | 0.711987 | -0.376506 | 4.587248 | 1.640007 | 2.797091 |
| ETH | SHORT | 339 | -121.639478 | -40.141255 | 82.134755 | 0.636532 | 23.008850 | 0.714199 | -0.358819 | 3.897047 | 1.630686 | 2.389820 |
| SOL | LONG | 268 | -64.556405 | 35.534839 | 100.272523 | 0.181278 | 22.761194 | 0.854062 | -0.240882 | 6.193431 | 2.136984 | 2.898211 |
| SOL | SHORT | 467 | -74.741209 | 16.060743 | 91.104754 | 0.302803 | 24.411135 | 0.835845 | -0.160045 | 3.338319 | 1.289829 | 2.588188 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | 0.012534 | 0.214680 | 0.000000 | -0.202147 |
| stop | 2446 | -3,049.388278 | 651.589903 | 1.347663 | -3,699.630518 |
| stop_gap | 7 | -1.562852 | 0.316714 | -0.011364 | -1.890929 |
| trailing_take_profit | 515 | 2,197.965207 | 109.008688 | 0.635873 | 2,089.592392 |
| trailing_take_profit_gap | 178 | 869.734607 | 43.134782 | 0.005022 | 826.604847 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 900.962237 | -99.037763 | -9.903776 | False |
| 2025-12 | 900.962237 | 793.345078 | -107.617159 | -11.944691 | False |
| 2026-01 | 793.345078 | 762.300230 | -31.044848 | -3.913158 | False |
| 2026-02 | 762.300230 | 673.656924 | -88.643307 | -11.628398 | False |
| 2026-03 | 673.656924 | 542.137092 | -131.519832 | -19.523266 | False |
| 2026-04 | 542.137092 | 477.115790 | -65.021302 | -11.993517 | False |
| 2026-05 | 477.115790 | 394.319893 | -82.795896 | -17.353418 | False |
| 2026-06 | 394.319893 | 389.280606 | -5.039287 | -1.277969 | False |
| 2026-07 | 389.280606 | 313.430077 | -75.850529 | -19.484795 | False |
| 2026-08 | 313.430077 | 310.823412 | -2.606665 | -0.831658 | False |
| 2026-09 | 310.823412 | 231.257615 | -79.565797 | -25.598393 | False |
| 2026-10 | 231.257615 | 207.243332 | -24.014283 | -10.384213 | False |
| 2026-11 | 207.243332 | 214.473644 | 7.230313 | 3.488803 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
