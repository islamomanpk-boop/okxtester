# Performance report: signal_extreme_atr_buffer_0_10__target_1R__trailing_sl

## Run metadata
- Experiment Id: signal_extreme_atr_buffer_0_10__target_1R__trailing_sl
- Stop Model: signal_extreme_atr_buffer_0_10
- Target Model: target_1R
- Target Value: 1.000000
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
- Final Equity: 3.354020
- Net Pnl: -996.645980
- Total Return Pct: -99.664598
- Max Drawdown Amount: 1,011.275394
- Max Drawdown Pct: 99.669434
- Recovery Factor: -0.985534
- Sharpe Ratio: -12.822323
- Sortino Ratio: -10.930190
- Cagr Pct: -99.481440
- Calmar Ratio: -0.998114
- Worst Daily Loss: -56.517623
- Worst Daily Loss Pct: -8.620764
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 33.144434
- Max Capital Utilization Pct: 102.373650
- Max Gross Exposure: 1,005.197635
- Max Gross Exposure Equity Multiple: 1.023737

## Trade performance

- Trade Count: 6856
- Net Pnl: -996.645980
- Gross Pnl: -234.283899
- Total Fees: 763.173271
- Funding Pnl: 0.811189
- Winning Trades: 3224
- Losing Trades: 3632
- Breakeven Trades: 0
- Win Rate Pct: 47.024504
- Profit Factor: 0.554463
- Expectancy: -0.145368
- Average Win: 0.384712
- Average Loss: 0.615902
- Payoff Ratio: 0.624631
- Max Consecutive Losses: 17
- Average Duration Minutes: 52.654026
- Median Duration Minutes: 20.000000
- Max Duration Minutes: 4,013.000000
- Recovery Factor: -0.985534

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1237 | -109.136766 | -17.270918 | 91.850293 | -0.015554 | 47.938561 | 0.577077 | -0.088227 | 0.251125 | 0.400705 | 0.626708 |
| BTC | 1325 | -219.574902 | -58.240511 | 161.493707 | 0.159317 | 45.056604 | 0.470590 | -0.165717 | 0.326933 | 0.569717 | 0.573852 |
| DOGE | 1607 | -210.820771 | -35.324493 | 175.795103 | 0.298826 | 47.666459 | 0.589124 | -0.131189 | 0.394622 | 0.610108 | 0.646806 |
| ETH | 1152 | -190.523100 | -43.906639 | 146.595350 | -0.021110 | 46.875000 | 0.584444 | -0.165385 | 0.496212 | 0.749146 | 0.662370 |
| SOL | 1535 | -266.590442 | -79.541336 | 187.438817 | 0.389711 | 47.426710 | 0.550112 | -0.173675 | 0.447775 | 0.734288 | 0.609808 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2482 | -312.077255 | -50.663782 | 261.164941 | -0.248532 | 46.132151 | 0.546563 | -0.125736 | 0.328534 | 0.514771 | 0.638214 |
| SHORT | 4374 | -684.568725 | -183.620117 | 502.008329 | 1.059721 | 47.530864 | 0.557974 | -0.156509 | 0.415651 | 0.674818 | 0.615946 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 360 | -32.277472 | -12.102065 | 20.148716 | -0.026691 | 45.000000 | 0.430443 | -0.089660 | 0.150578 | 0.286218 | 0.526097 |
| AVAX | SHORT | 877 | -76.859294 | -5.168853 | 71.701577 | 0.011136 | 49.144812 | 0.618342 | -0.087639 | 0.288917 | 0.451530 | 0.639862 |
| BTC | LONG | 515 | -55.670749 | 0.580833 | 56.205736 | -0.045846 | 44.854369 | 0.541767 | -0.108099 | 0.284932 | 0.427782 | 0.666069 |
| BTC | SHORT | 810 | -163.904153 | -58.821344 | 105.287972 | 0.205162 | 45.185185 | 0.441103 | -0.202351 | 0.353441 | 0.660504 | 0.535109 |
| DOGE | LONG | 389 | -31.492834 | -4.907773 | 26.459676 | -0.125385 | 48.843188 | 0.533448 | -0.080958 | 0.189518 | 0.339202 | 0.558716 |
| DOGE | SHORT | 1218 | -179.327937 | -30.416720 | 149.335427 | 0.424211 | 47.290640 | 0.597558 | -0.147231 | 0.462277 | 0.694081 | 0.666028 |
| ETH | LONG | 552 | -48.462687 | 6.941330 | 55.283895 | -0.120122 | 46.014493 | 0.662743 | -0.087795 | 0.374936 | 0.482203 | 0.777548 |
| ETH | SHORT | 600 | -142.060413 | -50.847969 | 91.311455 | 0.099012 | 47.666667 | 0.548701 | -0.236767 | 0.603918 | 1.002487 | 0.602420 |
| SOL | LONG | 666 | -144.173513 | -41.176107 | 103.066919 | 0.069512 | 46.246246 | 0.517636 | -0.216477 | 0.502325 | 0.834887 | 0.601668 |
| SOL | SHORT | 869 | -122.416929 | -38.365230 | 84.371898 | 0.320199 | 48.331415 | 0.583163 | -0.140871 | 0.407771 | 0.654078 | 0.623429 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| stop | 3533 | -1,829.390097 | 403.943728 | 0.282374 | -2,233.051451 |
| stop_gap | 12 | -0.786793 | 0.260873 | 0.000000 | -1.047666 |
| target | 3298 | 1,592.606641 | 358.224948 | 0.528815 | 1,234.910508 |
| target_gap | 13 | 3.286351 | 0.743721 | 0.000000 | 2.542629 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 715.407043 | -284.592957 | -28.459296 | False |
| 2025-12 | 715.407043 | 487.814974 | -227.592068 | -31.812948 | False |
| 2026-01 | 487.814974 | 346.947417 | -140.867557 | -28.877252 | False |
| 2026-02 | 346.947417 | 248.086018 | -98.861399 | -28.494635 | False |
| 2026-03 | 248.086018 | 134.736925 | -113.349093 | -45.689432 | False |
| 2026-04 | 134.736925 | 85.534393 | -49.202532 | -36.517482 | False |
| 2026-05 | 85.534393 | 50.330539 | -35.203855 | -41.157543 | False |
| 2026-06 | 50.330539 | 33.860565 | -16.469973 | -32.723618 | False |
| 2026-07 | 33.860565 | 19.237884 | -14.622682 | -43.184990 | False |
| 2026-08 | 19.237884 | 15.537399 | -3.700484 | -19.235403 | False |
| 2026-09 | 15.537399 | 8.578247 | -6.959153 | -44.789688 | False |
| 2026-10 | 8.578247 | 4.930199 | -3.648047 | -42.526724 | False |
| 2026-11 | 4.930199 | 3.354020 | -1.576179 | -31.969891 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
