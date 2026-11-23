# Performance report: fixed_stop_0_50pct__fixed_target_1_00pct__trailing_sl

## Run metadata
- Experiment Id: fixed_stop_0_50pct__fixed_target_1_00pct__trailing_sl
- Stop Model: fixed_stop_0_50pct
- Target Model: fixed_target_1_00pct
- Target Value: 0.010000
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
- Final Equity: 15.751706
- Net Pnl: -984.248294
- Total Return Pct: -98.424829
- Max Drawdown Amount: 990.626004
- Max Drawdown Pct: 98.436169
- Recovery Factor: -0.993562
- Sharpe Ratio: -10.406984
- Sortino Ratio: -9.344462
- Cagr Pct: -97.836346
- Calmar Ratio: -0.993906
- Worst Daily Loss: -57.800656
- Worst Daily Loss Pct: -7.526537
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 37.741599
- Max Capital Utilization Pct: 101.313061
- Max Gross Exposure: 1,002.897805
- Max Gross Exposure Equity Multiple: 1.013131

## Trade performance

- Trade Count: 6360
- Net Pnl: -984.248294
- Gross Pnl: -112.210834
- Total Fees: 872.862436
- Funding Pnl: 0.824976
- Winning Trades: 2516
- Losing Trades: 3844
- Breakeven Trades: 0
- Win Rate Pct: 39.559748
- Profit Factor: 0.646308
- Expectancy: -0.154756
- Average Win: 0.714838
- Average Loss: 0.723928
- Payoff Ratio: 0.987443
- Max Consecutive Losses: 18
- Average Duration Minutes: 62.154245
- Median Duration Minutes: 31.000000
- Max Duration Minutes: 1,903.000000
- Recovery Factor: -0.993562

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1280 | -124.711222 | -13.921624 | 110.801663 | 0.012065 | 38.515625 | 0.647857 | -0.097431 | 0.465392 | 0.449999 | 1.034206 |
| BTC | 932 | -136.047778 | -8.892609 | 127.289677 | 0.134508 | 39.806867 | 0.659407 | -0.145974 | 0.709964 | 0.712022 | 0.997109 |
| DOGE | 1475 | -233.134574 | -7.472757 | 225.959403 | 0.297586 | 39.661017 | 0.677128 | -0.158057 | 0.835777 | 0.811308 | 1.030160 |
| ETH | 1106 | -264.837779 | -78.580943 | 186.190632 | -0.066205 | 39.783002 | 0.566125 | -0.239455 | 0.785370 | 0.916517 | 0.856907 |
| SOL | 1567 | -225.516942 | -3.342902 | 222.621062 | 0.447022 | 40.012763 | 0.676318 | -0.143916 | 0.751524 | 0.741194 | 1.013937 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2244 | -326.659646 | -41.965547 | 284.267954 | -0.426145 | 37.923351 | 0.637953 | -0.145570 | 0.676380 | 0.647709 | 1.044265 |
| SHORT | 4116 | -657.588648 | -70.245287 | 588.594482 | 1.251120 | 40.451895 | 0.650316 | -0.159764 | 0.734495 | 0.767247 | 0.957312 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 378 | -33.921547 | -5.554509 | 28.312657 | -0.054382 | 35.978836 | 0.628188 | -0.089740 | 0.421408 | 0.376996 | 1.117804 |
| AVAX | SHORT | 902 | -90.789675 | -8.367115 | 82.489006 | 0.066446 | 39.578714 | 0.654682 | -0.100654 | 0.482148 | 0.482415 | 0.999445 |
| BTC | LONG | 364 | -52.581632 | -4.785610 | 47.693225 | -0.102798 | 40.384615 | 0.648031 | -0.144455 | 0.658580 | 0.688447 | 0.956618 |
| BTC | SHORT | 568 | -83.466145 | -4.106999 | 79.596452 | 0.237306 | 39.436620 | 0.666204 | -0.146947 | 0.743685 | 0.726894 | 1.023099 |
| DOGE | LONG | 357 | -35.800529 | -3.671610 | 31.961684 | -0.167235 | 38.095238 | 0.652122 | -0.100282 | 0.493460 | 0.465661 | 1.059698 |
| DOGE | SHORT | 1118 | -197.334045 | -3.801147 | 193.997719 | 0.464821 | 40.161002 | 0.681284 | -0.176506 | 0.939463 | 0.925490 | 1.015098 |
| ETH | LONG | 481 | -78.425957 | -11.918803 | 66.259689 | -0.247465 | 39.916840 | 0.623907 | -0.163048 | 0.677614 | 0.721550 | 0.939110 |
| ETH | SHORT | 625 | -186.411822 | -66.662140 | 119.930943 | 0.181261 | 39.680000 | 0.536142 | -0.298259 | 0.868793 | 1.065975 | 0.815022 |
| SOL | LONG | 664 | -125.929981 | -16.035016 | 110.040700 | 0.145735 | 36.144578 | 0.640399 | -0.189654 | 0.934433 | 0.825929 | 1.131372 |
| SOL | SHORT | 903 | -99.586961 | 12.692114 | 112.580362 | 0.301286 | 42.857143 | 0.712616 | -0.110285 | 0.638093 | 0.671568 | 0.950154 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | -0.017428 | 0.012744 | 0.000000 | -0.030172 |
| stop | 5109 | -1,800.495345 | 695.679628 | 0.698199 | -2,495.476773 |
| stop_gap | 38 | 9.742416 | 6.212301 | -0.008749 | 3.521366 |
| target | 1210 | 1,670.682795 | 170.158117 | 0.135525 | 1,500.660203 |
| target_gap | 2 | 7.876728 | 0.799645 | 0.000000 | 7.077083 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 825.055824 | -174.944176 | -17.494418 | False |
| 2025-12 | 825.055824 | 574.703212 | -250.352612 | -30.343718 | False |
| 2026-01 | 574.703212 | 509.660376 | -65.042836 | -11.317639 | False |
| 2026-02 | 509.660376 | 348.243182 | -161.417194 | -31.671521 | False |
| 2026-03 | 348.243182 | 202.022655 | -146.220527 | -41.988052 | False |
| 2026-04 | 202.022655 | 138.229104 | -63.793551 | -31.577424 | False |
| 2026-05 | 138.229104 | 106.588476 | -31.640627 | -22.889989 | False |
| 2026-06 | 106.588476 | 83.099496 | -23.488981 | -22.037073 | False |
| 2026-07 | 83.099496 | 62.430315 | -20.669180 | -24.872811 | False |
| 2026-08 | 62.430315 | 50.893936 | -11.536379 | -18.478810 | False |
| 2026-09 | 50.893936 | 28.767231 | -22.126705 | -43.476113 | False |
| 2026-10 | 28.767231 | 21.101396 | -7.665835 | -26.647801 | False |
| 2026-11 | 21.101396 | 15.751706 | -5.349691 | -25.352306 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
