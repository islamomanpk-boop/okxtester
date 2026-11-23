# Performance report: signal_extreme_exact__target_1_5R__trailing_tp

## Run metadata
- Experiment Id: signal_extreme_exact__target_1_5R__trailing_tp
- Stop Model: signal_extreme_exact
- Target Model: target_1_5R
- Target Value: 1.500000
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
- Final Equity: 8.028279
- Net Pnl: -991.971721
- Total Return Pct: -99.197172
- Max Drawdown Amount: 1,017.672440
- Max Drawdown Pct: 99.217288
- Recovery Factor: -0.974746
- Sharpe Ratio: -11.173253
- Sortino Ratio: -10.008340
- Cagr Pct: -98.838906
- Calmar Ratio: -0.996186
- Worst Daily Loss: -57.596846
- Worst Daily Loss Pct: -6.627028
- Worst Daily Loss Date Utc: 2025-11-22
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 35.009858
- Max Capital Utilization Pct: 102.520907
- Max Gross Exposure: 1,017.810666
- Max Gross Exposure Equity Multiple: 1.025209

## Trade performance

- Trade Count: 6125
- Net Pnl: -991.971721
- Gross Pnl: -170.178966
- Total Fees: 822.420881
- Funding Pnl: 0.628126
- Winning Trades: 2266
- Losing Trades: 3859
- Breakeven Trades: 0
- Win Rate Pct: 36.995918
- Profit Factor: 0.604964
- Expectancy: -0.161955
- Average Win: 0.670396
- Average Loss: 0.650710
- Payoff Ratio: 1.030253
- Max Consecutive Losses: 20
- Average Duration Minutes: 62.183673
- Median Duration Minutes: 22.000000
- Max Duration Minutes: 4,420.000000
- Recovery Factor: -0.974746

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1166 | -137.866477 | -32.770590 | 105.135304 | 0.039417 | 36.963979 | 0.565462 | -0.118239 | 0.416253 | 0.431662 | 0.964304 |
| BTC | 1187 | -194.289217 | -23.546031 | 170.807015 | 0.063829 | 35.973041 | 0.568000 | -0.163681 | 0.598254 | 0.591768 | 1.010960 |
| DOGE | 1412 | -205.212648 | -11.023641 | 194.494853 | 0.305846 | 38.385269 | 0.656960 | -0.145335 | 0.725100 | 0.687606 | 1.054529 |
| ETH | 1048 | -207.688792 | -44.088735 | 163.581158 | -0.018900 | 36.354962 | 0.611914 | -0.198176 | 0.859508 | 0.802341 | 1.071250 |
| SOL | 1312 | -246.914587 | -58.749969 | 188.402552 | 0.237934 | 36.966463 | 0.595683 | -0.188197 | 0.750064 | 0.738447 | 1.015732 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2171 | -334.102084 | -42.282700 | 291.439647 | -0.379737 | 35.836020 | 0.589908 | -0.153893 | 0.617735 | 0.584853 | 1.056223 |
| SHORT | 3954 | -657.869636 | -127.896265 | 530.981234 | 1.007864 | 37.632777 | 0.612194 | -0.166381 | 0.697930 | 0.687911 | 1.014564 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 340 | -53.488477 | -25.246720 | 28.232064 | -0.009693 | 32.941176 | 0.390770 | -0.157319 | 0.306325 | 0.385074 | 0.795496 |
| AVAX | SHORT | 826 | -84.377999 | -7.523870 | 76.903239 | 0.049110 | 38.619855 | 0.632299 | -0.102153 | 0.454849 | 0.452613 | 1.004940 |
| BTC | LONG | 456 | -57.742707 | 5.040562 | 62.692520 | -0.090749 | 37.061404 | 0.600030 | -0.126629 | 0.512573 | 0.503023 | 1.018985 |
| BTC | SHORT | 731 | -136.546509 | -28.586592 | 108.114495 | 0.154578 | 35.294118 | 0.552858 | -0.186794 | 0.654378 | 0.645615 | 1.013573 |
| DOGE | LONG | 346 | -30.270721 | 0.127723 | 30.234418 | -0.164026 | 36.416185 | 0.647947 | -0.087488 | 0.442165 | 0.390834 | 1.131337 |
| DOGE | SHORT | 1066 | -174.941927 | -11.151364 | 164.260434 | 0.469872 | 39.024390 | 0.658472 | -0.164111 | 0.810797 | 0.788051 | 1.028863 |
| ETH | LONG | 473 | -59.955540 | 4.692373 | 64.444231 | -0.203683 | 35.517970 | 0.664652 | -0.126756 | 0.707325 | 0.586184 | 1.206660 |
| ETH | SHORT | 575 | -147.733252 | -48.781108 | 99.136927 | 0.184784 | 37.043478 | 0.585456 | -0.256927 | 0.979539 | 0.984462 | 0.995000 |
| SOL | LONG | 556 | -132.644638 | -26.896639 | 105.836413 | 0.088414 | 36.510791 | 0.582571 | -0.238569 | 0.911927 | 0.900187 | 1.013042 |
| SOL | SHORT | 756 | -114.269948 | -31.853330 | 82.566138 | 0.149520 | 37.301587 | 0.609907 | -0.151151 | 0.633546 | 0.617995 | 1.025162 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| stop | 3750 | -1,979.141783 | 510.073785 | 0.106887 | -2,489.108680 |
| stop_gap | 30 | -11.217467 | 4.306076 | 0.011954 | -15.511589 |
| trailing_take_profit | 1893 | 1,528.349444 | 245.374225 | 0.444141 | 1,283.419360 |
| trailing_take_profit_gap | 452 | 291.830840 | 62.666796 | 0.065144 | 229.229189 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 729.176586 | -270.823414 | -27.082341 | False |
| 2025-12 | 729.176586 | 531.155454 | -198.021131 | -27.156814 | False |
| 2026-01 | 531.155454 | 396.291402 | -134.864052 | -25.390693 | False |
| 2026-02 | 396.291402 | 294.377768 | -101.913634 | -25.716842 | False |
| 2026-03 | 294.377768 | 176.289659 | -118.088109 | -40.114479 | False |
| 2026-04 | 176.289659 | 120.863197 | -55.426462 | -31.440564 | False |
| 2026-05 | 120.863197 | 75.358124 | -45.505073 | -37.650066 | False |
| 2026-06 | 75.358124 | 54.294700 | -21.063424 | -27.951099 | False |
| 2026-07 | 54.294700 | 33.787536 | -20.507164 | -37.770103 | False |
| 2026-08 | 33.787536 | 29.774006 | -4.013530 | -11.878731 | False |
| 2026-09 | 29.774006 | 17.621243 | -12.152763 | -40.816688 | False |
| 2026-10 | 17.621243 | 10.662345 | -6.958898 | -39.491525 | False |
| 2026-11 | 10.662345 | 8.028279 | -2.634066 | -24.704376 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
