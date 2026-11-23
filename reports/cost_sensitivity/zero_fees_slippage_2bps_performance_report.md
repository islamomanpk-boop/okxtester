# Performance report: zero_fees_slippage_2bps

## Run metadata
- Scenario Id: zero_fees_slippage_2bps
- Experiment Id: fixed_stop_0_50pct__fixed_target_0_75pct
- Assets: BTC,ETH,SOL,DOGE,AVAX
- Execution Timeframe: 1m
- Execution Window Start Utc: 2025-10-20T08:50:00+00:00
- Execution Window End Utc: 2026-11-19T14:14:00+00:00
- Taker Fee Rate Per Side: 0.000000
- Slippage Bps Per Side: 2.000000
- Funding Data: Historical asset-specific realized funding rates
- Funding Treatment: Applied at funding timestamps; mark price when supplied, otherwise candle close proxy
- Equity Curve Storage: summary-only
- Risk Fraction: 0.005000
- Max Gross Leverage: 1.000000
- Cost Sensitivity Note: Same signals, date window, exit rules, risk fraction, and portfolio constraints; cost-aware sizing means fills, accepted entries, and outcomes can change.
- End Of Data Policy: Open positions forcibly closed at final available candle

## Portfolio risk and return

- Initial Equity: 1,000.000000
- Final Equity: 604.414866
- Net Pnl: -395.585134
- Total Return Pct: -39.558513
- Max Drawdown Amount: 692.993577
- Max Drawdown Pct: 55.495925
- Recovery Factor: -0.570835
- Sharpe Ratio: -1.081786
- Sortino Ratio: -1.487632
- Cagr Pct: -37.185830
- Calmar Ratio: -0.670064
- Worst Daily Loss: -79.254401
- Worst Daily Loss Pct: -7.490590
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 42.995480
- Max Capital Utilization Pct: 101.952031
- Max Gross Exposure: 1,239.111116
- Max Gross Exposure Equity Multiple: 1.019520

## Trade performance

- Trade Count: 5982
- Net Pnl: -395.585134
- Gross Pnl: -399.964697
- Total Fees: 0.000000
- Funding Pnl: 4.379564
- Winning Trades: 2421
- Losing Trades: 3561
- Breakeven Trades: 0
- Win Rate Pct: 40.471414
- Profit Factor: 0.959038
- Expectancy: -0.066129
- Average Win: 3.825619
- Average Loss: 2.711993
- Payoff Ratio: 1.410630
- Max Consecutive Losses: 23
- Average Duration Minutes: 71.410565
- Median Duration Minutes: 31.000000
- Max Duration Minutes: 3,160.000000
- Recovery Factor: -0.570835

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1198 | -197.844752 | -198.207122 | 0.000000 | 0.362371 | 39.649416 | 0.896096 | -0.165146 | 3.592143 | 2.633627 | 1.363953 |
| BTC | 893 | 24.710097 | 24.017763 | 0.000000 | 0.692334 | 41.657335 | 1.018164 | 0.027671 | 3.723356 | 2.611091 | 1.425977 |
| DOGE | 1357 | -76.478078 | -78.392994 | 0.000000 | 1.914916 | 41.120118 | 0.968011 | -0.056358 | 4.147428 | 2.992169 | 1.386094 |
| ETH | 1054 | -7.199347 | -6.993191 | 0.000000 | -0.206156 | 39.563567 | 0.995831 | -0.006830 | 4.124359 | 2.711236 | 1.521210 |
| SOL | 1480 | -138.773055 | -140.389154 | 0.000000 | 1.616099 | 40.472973 | 0.939004 | -0.093766 | 3.566517 | 2.582425 | 1.381073 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2120 | -328.451144 | -325.288373 | 0.000000 | -3.162770 | 39.245283 | 0.913704 | -0.154930 | 4.179874 | 2.955052 | 1.414484 |
| SHORT | 3862 | -67.133990 | -74.676324 | 0.000000 | 7.542334 | 41.144485 | 0.988527 | -0.017383 | 3.640130 | 2.574264 | 1.414047 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 367 | -118.203736 | -117.673824 | 0.000000 | -0.529912 | 38.147139 | 0.829878 | -0.322081 | 4.118655 | 3.060861 | 1.345587 |
| AVAX | SHORT | 831 | -79.641016 | -80.533299 | 0.000000 | 0.892282 | 40.312876 | 0.934143 | -0.095838 | 3.372108 | 2.438099 | 1.383089 |
| BTC | LONG | 338 | 17.167965 | 18.038925 | 0.000000 | -0.870960 | 42.011834 | 1.029775 | 0.050793 | 4.181442 | 2.941821 | 1.421379 |
| BTC | SHORT | 555 | 7.542132 | 5.978839 | 0.000000 | 1.563294 | 41.441441 | 1.009623 | 0.013589 | 3.440538 | 2.411636 | 1.426641 |
| DOGE | LONG | 331 | -65.427376 | -64.249365 | 0.000000 | -1.178011 | 39.879154 | 0.890935 | -0.197666 | 4.048987 | 3.014541 | 1.343152 |
| DOGE | SHORT | 1026 | -11.050702 | -14.143629 | 0.000000 | 3.092927 | 41.520468 | 0.993829 | -0.010771 | 4.177930 | 2.984748 | 1.399760 |
| ETH | LONG | 464 | -70.425131 | -69.584692 | 0.000000 | -0.840440 | 38.577586 | 0.915348 | -0.151778 | 4.254242 | 2.919068 | 1.457397 |
| ETH | SHORT | 590 | 63.225784 | 62.591501 | 0.000000 | 0.634283 | 40.338983 | 1.070634 | 0.107162 | 4.026675 | 2.542962 | 1.583458 |
| SOL | LONG | 620 | -91.562866 | -91.819418 | 0.000000 | 0.256552 | 38.548387 | 0.916977 | -0.147682 | 4.231394 | 2.894661 | 1.461792 |
| SOL | SHORT | 860 | -47.210189 | -48.569736 | 0.000000 | 1.359547 | 41.860465 | 0.959727 | -0.054896 | 3.125113 | 2.344502 | 1.332954 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | 0.033936 | 0.000000 | 0.000000 | 0.033936 |
| stop | 3548 | -9,634.080473 | 0.000000 | 1.859577 | -9,632.220896 |
| stop_gap | 13 | -25.234058 | 0.000000 | 0.047324 | -25.186735 |
| target | 2417 | 9,258.922777 | 0.000000 | 2.472663 | 9,261.395440 |
| target_gap | 3 | 0.393120 | 0.000000 | 0.000000 | 0.393120 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 1,078.372313 | 78.372313 | 7.837231 | False |
| 2025-12 | 1,078.372313 | 1,010.089015 | -68.283299 | -6.332071 | False |
| 2026-01 | 1,010.089015 | 1,063.206192 | 53.117178 | 5.258663 | False |
| 2026-02 | 1,063.206192 | 1,095.757804 | 32.551612 | 3.061646 | False |
| 2026-03 | 1,095.757804 | 893.746860 | -202.010944 | -18.435729 | False |
| 2026-04 | 893.746860 | 828.053437 | -65.693423 | -7.350339 | False |
| 2026-05 | 828.053437 | 812.029980 | -16.023457 | -1.935075 | False |
| 2026-06 | 812.029980 | 878.561682 | 66.531702 | 8.193257 | False |
| 2026-07 | 878.561682 | 807.582302 | -70.979380 | -8.079043 | False |
| 2026-08 | 807.582302 | 797.367129 | -10.215174 | -1.264908 | False |
| 2026-09 | 797.367129 | 615.618559 | -181.748569 | -22.793587 | False |
| 2026-10 | 615.618559 | 583.822942 | -31.795617 | -5.164824 | False |
| 2026-11 | 583.822942 | 604.414866 | 20.591924 | 3.527084 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
