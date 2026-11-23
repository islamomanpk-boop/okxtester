# Performance report: signal_extreme_atr_buffer_0_10__fixed_target_1_00pct__trailing_tp

## Run metadata
- Experiment Id: signal_extreme_atr_buffer_0_10__fixed_target_1_00pct__trailing_tp
- Stop Model: signal_extreme_atr_buffer_0_10
- Target Model: fixed_target_1_00pct
- Target Value: 0.010000
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
- Final Equity: 29.745327
- Net Pnl: -970.254673
- Total Return Pct: -97.025467
- Max Drawdown Amount: 990.456953
- Max Drawdown Pct: 97.088820
- Recovery Factor: -0.979603
- Sharpe Ratio: -8.855775
- Sortino Ratio: -8.541013
- Cagr Pct: -96.108073
- Calmar Ratio: -0.989898
- Worst Daily Loss: -61.318984
- Worst Daily Loss Pct: -7.847821
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 40.287618
- Max Capital Utilization Pct: 102.390525
- Max Gross Exposure: 1,019.163211
- Max Gross Exposure Equity Multiple: 1.023905

## Trade performance

- Trade Count: 4864
- Net Pnl: -970.254673
- Gross Pnl: -150.467289
- Total Fees: 820.607416
- Funding Pnl: 0.820032
- Winning Trades: 1500
- Losing Trades: 3364
- Breakeven Trades: 0
- Win Rate Pct: 30.838816
- Profit Factor: 0.689197
- Expectancy: -0.199477
- Average Win: 1.434344
- Average Loss: 0.927994
- Payoff Ratio: 1.545640
- Max Consecutive Losses: 35
- Average Duration Minutes: 87.357113
- Median Duration Minutes: 37.000000
- Max Duration Minutes: 3,470.000000
- Recovery Factor: -0.979603

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 936 | -116.445607 | -19.339653 | 97.161957 | 0.056003 | 30.555556 | 0.690136 | -0.124408 | 0.906817 | 0.578147 | 1.568490 |
| BTC | 847 | -191.375732 | -27.768047 | 163.693818 | 0.086133 | 27.508855 | 0.662102 | -0.225945 | 1.609423 | 0.922429 | 1.744766 |
| DOGE | 1135 | -208.370768 | -9.562353 | 199.229226 | 0.420812 | 32.070485 | 0.725009 | -0.183587 | 1.509248 | 0.982798 | 1.535665 |
| ETH | 812 | -261.134571 | -101.975573 | 159.111218 | -0.047780 | 31.157635 | 0.601613 | -0.321594 | 1.558679 | 1.172595 | 1.329257 |
| SOL | 1134 | -192.927995 | 8.178338 | 201.411197 | 0.304864 | 32.098765 | 0.748263 | -0.170131 | 1.575436 | 0.995307 | 1.582864 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1571 | -360.711226 | -55.398169 | 304.591868 | -0.721189 | 28.771483 | 0.674291 | -0.229606 | 1.652113 | 0.989693 | 1.669319 |
| SHORT | 3293 | -609.543447 | -95.069120 | 516.015548 | 1.541221 | 31.825084 | 0.697393 | -0.185103 | 1.340421 | 0.897240 | 1.493937 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 264 | -56.758058 | -26.506006 | 30.213241 | -0.038811 | 27.272727 | 0.520437 | -0.214993 | 0.855494 | 0.616425 | 1.387831 |
| AVAX | SHORT | 672 | -59.687549 | 7.166353 | 66.948716 | 0.094814 | 31.845238 | 0.768151 | -0.088821 | 0.924085 | 0.562100 | 1.643987 |
| BTC | LONG | 301 | -53.875675 | 8.939768 | 62.517990 | -0.297453 | 25.913621 | 0.727439 | -0.178989 | 1.843451 | 0.886390 | 2.079730 |
| BTC | SHORT | 546 | -137.500057 | -36.707815 | 101.175828 | 0.383586 | 28.388278 | 0.627074 | -0.251832 | 1.491653 | 0.942983 | 1.581845 |
| DOGE | LONG | 260 | -53.799912 | -14.968913 | 38.537718 | -0.293281 | 29.230769 | 0.629404 | -0.206923 | 1.202255 | 0.788974 | 1.523820 |
| DOGE | SHORT | 875 | -154.570856 | 5.406560 | 160.691508 | 0.714093 | 32.914286 | 0.747666 | -0.176652 | 1.590260 | 1.043553 | 1.523890 |
| ETH | LONG | 312 | -96.523276 | -34.589178 | 61.682718 | -0.251380 | 29.487179 | 0.601155 | -0.309369 | 1.581346 | 1.100032 | 1.437545 |
| ETH | SHORT | 500 | -164.611295 | -67.386394 | 97.428500 | 0.203599 | 32.200000 | 0.601882 | -0.329223 | 1.545727 | 1.219685 | 1.267316 |
| SOL | LONG | 434 | -99.754306 | 11.726161 | 111.640201 | 0.159734 | 30.875576 | 0.753248 | -0.229849 | 2.272499 | 1.347564 | 1.686376 |
| SOL | SHORT | 700 | -93.173690 | -3.547824 | 89.770995 | 0.145129 | 32.857143 | 0.742698 | -0.133105 | 1.169321 | 0.770463 | 1.517686 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | 0.001738 | 0.029774 | 0.000000 | -0.028036 |
| stop | 3338 | -2,533.915264 | 583.156179 | 0.345965 | -3,116.725479 |
| stop_gap | 10 | -2.523420 | 0.732253 | 0.014538 | -3.241135 |
| trailing_take_profit | 1249 | 1,921.398339 | 191.905256 | 0.481718 | 1,729.974801 |
| trailing_take_profit_gap | 266 | 464.571318 | 44.783954 | -0.022189 | 419.765175 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 841.418598 | -158.581402 | -15.858140 | False |
| 2025-12 | 841.418598 | 658.812358 | -182.606240 | -21.702187 | False |
| 2026-01 | 658.812358 | 585.800995 | -73.011364 | -11.082270 | False |
| 2026-02 | 585.800995 | 456.004052 | -129.796942 | -22.157173 | False |
| 2026-03 | 456.004052 | 295.541418 | -160.462635 | -35.188862 | False |
| 2026-04 | 295.541418 | 217.745387 | -77.796031 | -26.323224 | False |
| 2026-05 | 217.745387 | 152.147535 | -65.597852 | -30.125944 | False |
| 2026-06 | 152.147535 | 117.992769 | -34.154766 | -22.448452 | False |
| 2026-07 | 117.992769 | 86.713790 | -31.278979 | -26.509234 | False |
| 2026-08 | 86.713790 | 74.792239 | -11.921551 | -13.748160 | False |
| 2026-09 | 74.792239 | 45.526715 | -29.265525 | -39.129093 | False |
| 2026-10 | 45.526715 | 34.020223 | -11.506491 | -25.274153 | False |
| 2026-11 | 34.020223 | 29.745327 | -4.274896 | -12.565751 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
