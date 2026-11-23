# Performance report: fixed_stop_0_50pct__fixed_target_1_50pct

## Run metadata
- Experiment Id: fixed_stop_0_50pct__fixed_target_1_50pct
- Stop Model: fixed_stop_0_50pct
- Target Model: fixed_target_1_50pct
- Target Value: 0.015000
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
- Final Equity: 116.946760
- Net Pnl: -883.053240
- Total Return Pct: -88.305324
- Max Drawdown Amount: 980.411264
- Max Drawdown Pct: 90.191754
- Recovery Factor: -0.900697
- Sharpe Ratio: -5.055396
- Sortino Ratio: -5.536908
- Cagr Pct: -86.219525
- Calmar Ratio: -0.955958
- Worst Daily Loss: -82.507582
- Worst Daily Loss Pct: -7.679721
- Worst Daily Loss Date Utc: 2025-11-18
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 45.696331
- Max Capital Utilization Pct: 102.408320
- Max Gross Exposure: 1,090.135461
- Max Gross Exposure Equity Multiple: 1.024083

## Trade performance

- Trade Count: 3897
- Net Pnl: -883.053240
- Gross Pnl: 61.250904
- Total Fees: 946.563379
- Funding Pnl: 2.259236
- Winning Trades: 1045
- Losing Trades: 2852
- Breakeven Trades: 0
- Win Rate Pct: 26.815499
- Profit Factor: 0.795711
- Expectancy: -0.226598
- Average Win: 3.291406
- Average Loss: 1.515628
- Payoff Ratio: 2.171644
- Max Consecutive Losses: 47
- Average Duration Minutes: 133.595073
- Median Duration Minutes: 47.000000
- Max Duration Minutes: 3,707.000000
- Recovery Factor: -0.900697

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 799 | -148.278923 | -7.749112 | 140.674153 | 0.144342 | 24.655820 | 0.771145 | -0.185581 | 2.536230 | 1.076273 | 2.356494 |
| BTC | 570 | -118.600800 | 18.665461 | 137.613820 | 0.347558 | 28.421053 | 0.810232 | -0.208072 | 3.125780 | 1.531807 | 2.040584 |
| DOGE | 863 | -224.940530 | 12.192202 | 238.081741 | 0.949008 | 28.157590 | 0.793331 | -0.260650 | 3.553369 | 1.755499 | 2.024137 |
| ETH | 715 | -198.608306 | -10.771600 | 187.916041 | 0.079335 | 26.013986 | 0.770519 | -0.277774 | 3.585272 | 1.636047 | 2.191423 |
| SOL | 950 | -192.624680 | 48.913953 | 242.277625 | 0.738992 | 27.052632 | 0.824216 | -0.202763 | 3.514304 | 1.581242 | 2.222496 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1282 | -356.973512 | -9.706768 | 346.085482 | -1.181263 | 25.117005 | 0.775543 | -0.278450 | 3.830481 | 1.656655 | 2.312178 |
| SHORT | 2615 | -526.079728 | 70.957672 | 600.477898 | 3.440498 | 27.648184 | 0.807451 | -0.201178 | 3.051320 | 1.444072 | 2.112997 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 246 | -63.593445 | -16.721790 | 46.728175 | -0.143479 | 21.544715 | 0.710427 | -0.258510 | 2.943728 | 1.137881 | 2.587026 |
| AVAX | SHORT | 553 | -84.685478 | 8.972678 | 93.945978 | 0.287821 | 26.039783 | 0.802278 | -0.153138 | 2.386248 | 1.047201 | 2.278692 |
| BTC | LONG | 194 | -27.073479 | 26.852654 | 53.459439 | -0.466695 | 28.350515 | 0.885751 | -0.139554 | 3.816282 | 1.704813 | 2.238534 |
| BTC | SHORT | 376 | -91.527321 | -8.187193 | 84.154381 | 0.814253 | 28.457447 | 0.764110 | -0.243424 | 2.770849 | 1.442410 | 1.920986 |
| DOGE | LONG | 191 | -78.188000 | -24.837719 | 52.758807 | -0.591474 | 25.130890 | 0.687310 | -0.409361 | 3.580443 | 1.748596 | 2.047610 |
| DOGE | SHORT | 672 | -146.752530 | 37.029922 | 185.322934 | 1.540482 | 29.017857 | 0.824953 | -0.218382 | 3.546705 | 1.757568 | 2.017962 |
| ETH | LONG | 281 | -75.914303 | -3.262191 | 72.221097 | -0.431015 | 25.622776 | 0.771568 | -0.270158 | 3.561300 | 1.590086 | 2.239691 |
| ETH | SHORT | 434 | -122.694003 | -7.509409 | 115.694944 | 0.510350 | 26.267281 | 0.769866 | -0.282705 | 3.600412 | 1.666065 | 2.161027 |
| SOL | LONG | 370 | -112.204285 | 8.262279 | 120.917964 | 0.451400 | 25.405405 | 0.796522 | -0.303255 | 4.672627 | 1.997939 | 2.338723 |
| SOL | SHORT | 580 | -80.420395 | 40.651674 | 121.359661 | 0.287592 | 28.103448 | 0.852269 | -0.138656 | 2.846314 | 1.305443 | 2.180344 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | 0.005521 | 0.094556 | 0.000000 | -0.089036 |
| stop | 2844 | -3,622.411114 | 697.061970 | 1.811819 | -4,317.661265 |
| stop_gap | 7 | -4.058550 | 0.770664 | 0.007223 | -4.821991 |
| target | 1045 | 3,687.715047 | 248.636188 | 0.440194 | 3,439.519053 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 989.987333 | -10.012667 | -1.001267 | False |
| 2025-12 | 989.987333 | 897.068132 | -92.919200 | -9.385898 | False |
| 2026-01 | 897.068132 | 810.317962 | -86.750170 | -9.670410 | False |
| 2026-02 | 810.317962 | 655.039016 | -155.278946 | -19.162718 | False |
| 2026-03 | 655.039016 | 518.595119 | -136.443897 | -20.829889 | False |
| 2026-04 | 518.595119 | 437.764174 | -80.830945 | -15.586523 | False |
| 2026-05 | 437.764174 | 346.895923 | -90.868251 | -20.757352 | False |
| 2026-06 | 346.895923 | 315.996090 | -30.899833 | -8.907523 | False |
| 2026-07 | 315.996090 | 248.977038 | -67.019052 | -21.208823 | False |
| 2026-08 | 248.977038 | 226.942036 | -22.035003 | -8.850215 | False |
| 2026-09 | 226.942036 | 136.025922 | -90.916113 | -40.061381 | False |
| 2026-10 | 136.025922 | 119.599155 | -16.426768 | -12.076204 | False |
| 2026-11 | 119.599155 | 116.946760 | -2.652394 | -2.217737 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
