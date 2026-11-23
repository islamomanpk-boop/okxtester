# Performance report: fixed_stop_0_50pct__fixed_target_1_50pct__trailing_sl

## Run metadata
- Experiment Id: fixed_stop_0_50pct__fixed_target_1_50pct__trailing_sl
- Stop Model: fixed_stop_0_50pct
- Target Model: fixed_target_1_50pct
- Target Value: 0.015000
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
- Final Equity: 17.427587
- Net Pnl: -982.572413
- Total Return Pct: -98.257241
- Max Drawdown Amount: 994.500489
- Max Drawdown Pct: 98.279275
- Recovery Factor: -0.988006
- Sharpe Ratio: -9.799903
- Sortino Ratio: -9.027394
- Cagr Pct: -97.624586
- Calmar Ratio: -0.993338
- Worst Daily Loss: -57.215390
- Worst Daily Loss Pct: -7.383564
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 38.122881
- Max Capital Utilization Pct: 101.313052
- Max Gross Exposure: 1,008.993613
- Max Gross Exposure Equity Multiple: 1.013131

## Trade performance

- Trade Count: 6098
- Net Pnl: -982.572413
- Gross Pnl: -102.277053
- Total Fees: 881.325202
- Funding Pnl: 1.029841
- Winning Trades: 2397
- Losing Trades: 3701
- Breakeven Trades: 0
- Win Rate Pct: 39.307970
- Profit Factor: 0.650509
- Expectancy: -0.161130
- Average Win: 0.762983
- Average Loss: 0.759644
- Payoff Ratio: 1.004395
- Max Consecutive Losses: 19
- Average Duration Minutes: 65.609872
- Median Duration Minutes: 33.000000
- Max Duration Minutes: 2,169.000000
- Recovery Factor: -0.988006

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1232 | -119.638027 | -7.001605 | 112.768611 | 0.132188 | 37.012987 | 0.673759 | -0.097109 | 0.541839 | 0.472573 | 1.146572 |
| BTC | 889 | -129.623156 | -4.588142 | 125.193863 | 0.158849 | 40.719910 | 0.663164 | -0.145808 | 0.704978 | 0.730219 | 0.965434 |
| DOGE | 1410 | -237.420734 | -7.483443 | 230.264555 | 0.327264 | 39.929078 | 0.675406 | -0.168383 | 0.877473 | 0.863563 | 1.016108 |
| ETH | 1074 | -259.374863 | -72.487709 | 186.828487 | -0.058667 | 39.571695 | 0.578972 | -0.241504 | 0.839239 | 0.949232 | 0.884124 |
| SOL | 1493 | -236.515632 | -10.716154 | 226.269685 | 0.470207 | 39.584729 | 0.668007 | -0.158416 | 0.805237 | 0.789812 | 1.019530 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2121 | -363.044116 | -74.011514 | 288.609692 | -0.422910 | 37.906648 | 0.606890 | -0.171166 | 0.697108 | 0.701229 | 0.994123 |
| SHORT | 3977 | -619.528297 | -28.265538 | 592.715509 | 1.452751 | 40.055318 | 0.671847 | -0.155778 | 0.796231 | 0.791914 | 1.005450 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 357 | -41.200351 | -11.853338 | 29.318190 | -0.028823 | 33.613445 | 0.583588 | -0.115407 | 0.481175 | 0.417474 | 1.152587 |
| AVAX | SHORT | 875 | -78.437677 | 4.851734 | 83.450421 | 0.161011 | 38.400000 | 0.707076 | -0.089643 | 0.563504 | 0.496800 | 1.134268 |
| BTC | LONG | 341 | -57.751555 | -9.145363 | 48.476816 | -0.129377 | 41.935484 | 0.612305 | -0.169359 | 0.637831 | 0.752331 | 0.847807 |
| BTC | SHORT | 548 | -71.871601 | 4.557221 | 76.717048 | 0.288226 | 39.963504 | 0.695283 | -0.131153 | 0.748823 | 0.716911 | 1.044513 |
| DOGE | LONG | 338 | -36.463227 | -2.806282 | 33.476475 | -0.180470 | 38.461538 | 0.660792 | -0.107879 | 0.546401 | 0.516804 | 1.057268 |
| DOGE | SHORT | 1072 | -200.957507 | -4.677160 | 196.788081 | 0.507734 | 40.391791 | 0.677923 | -0.187460 | 0.976872 | 0.976436 | 1.000446 |
| ETH | LONG | 465 | -80.564911 | -13.219241 | 67.085852 | -0.259819 | 39.569892 | 0.619552 | -0.173258 | 0.713034 | 0.753606 | 0.946164 |
| ETH | SHORT | 609 | -178.809952 | -59.268469 | 119.742635 | 0.201152 | 39.573071 | 0.557717 | -0.293612 | 0.935595 | 1.098609 | 0.851617 |
| SOL | LONG | 620 | -147.064072 | -36.987290 | 110.252361 | 0.175579 | 36.612903 | 0.587313 | -0.237200 | 0.921996 | 0.906761 | 1.016801 |
| SOL | SHORT | 873 | -89.451561 | 26.271136 | 116.017324 | 0.294628 | 41.695304 | 0.748769 | -0.102465 | 0.732423 | 0.699516 | 1.047043 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | -0.019282 | 0.014100 | 0.000000 | -0.033382 |
| stop | 5572 | -1,187.688524 | 799.854291 | 0.884997 | -1,986.657818 |
| stop_gap | 70 | 42.651486 | 11.241035 | 0.018053 | 31.428505 |
| target | 455 | 1,042.779267 | 70.215775 | 0.126791 | 972.690282 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 835.364965 | -164.635035 | -16.463503 | False |
| 2025-12 | 835.364965 | 613.937016 | -221.427949 | -26.506732 | False |
| 2026-01 | 613.937016 | 542.209808 | -71.727209 | -11.683154 | False |
| 2026-02 | 542.209808 | 386.138487 | -156.071320 | -28.784304 | False |
| 2026-03 | 386.138487 | 218.863866 | -167.274621 | -43.319852 | False |
| 2026-04 | 218.863866 | 157.097723 | -61.766143 | -28.221261 | False |
| 2026-05 | 157.097723 | 121.853623 | -35.244099 | -22.434507 | False |
| 2026-06 | 121.853623 | 92.298147 | -29.555476 | -24.254901 | False |
| 2026-07 | 92.298147 | 68.734141 | -23.564006 | -25.530313 | False |
| 2026-08 | 68.734141 | 55.048005 | -13.686137 | -19.911701 | False |
| 2026-09 | 55.048005 | 31.094116 | -23.953889 | -43.514545 | False |
| 2026-10 | 31.094116 | 22.633173 | -8.460943 | -27.210754 | False |
| 2026-11 | 22.633173 | 17.427587 | -5.205586 | -22.999807 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
