# Performance report: fixed_stop_0_50pct__fixed_target_0_75pct__trailing_tp

## Run metadata
- Experiment Id: fixed_stop_0_50pct__fixed_target_0_75pct__trailing_tp
- Stop Model: fixed_stop_0_50pct
- Target Model: fixed_target_0_75pct
- Target Value: 0.007500
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
- Final Equity: 25.201899
- Net Pnl: -974.798101
- Total Return Pct: -97.479810
- Max Drawdown Amount: 1,006.567420
- Max Drawdown Pct: 97.559506
- Recovery Factor: -0.968438
- Sharpe Ratio: -9.148100
- Sortino Ratio: -8.622541
- Cagr Pct: -96.660478
- Calmar Ratio: -0.990785
- Worst Daily Loss: -53.220094
- Worst Daily Loss Pct: -5.172857
- Worst Daily Loss Date Utc: 2025-11-15
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 40.129156
- Max Capital Utilization Pct: 101.618632
- Max Gross Exposure: 1,032.959765
- Max Gross Exposure Equity Multiple: 1.016186

## Trade performance

- Trade Count: 5731
- Net Pnl: -974.798101
- Gross Pnl: -21.228103
- Total Fees: 954.837833
- Funding Pnl: 1.267835
- Winning Trades: 2294
- Losing Trades: 3437
- Breakeven Trades: 0
- Win Rate Pct: 40.027918
- Profit Factor: 0.721292
- Expectancy: -0.170092
- Average Win: 1.099724
- Average Loss: 1.017622
- Payoff Ratio: 1.080681
- Max Consecutive Losses: 24
- Average Duration Minutes: 74.745071
- Median Duration Minutes: 33.000000
- Max Duration Minutes: 3,161.000000
- Recovery Factor: -0.968438

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1158 | -129.813001 | -10.564754 | 119.280365 | 0.032118 | 38.860104 | 0.710031 | -0.112101 | 0.706370 | 0.632316 | 1.117116 |
| BTC | 846 | -102.865753 | 37.782389 | 140.688316 | 0.040174 | 41.843972 | 0.791690 | -0.121591 | 1.104366 | 1.003681 | 1.100315 |
| DOGE | 1316 | -244.336864 | -0.681393 | 244.295894 | 0.640423 | 40.501520 | 0.726968 | -0.185666 | 1.220570 | 1.142913 | 1.067947 |
| ETH | 1007 | -254.804434 | -48.483988 | 206.238680 | -0.081766 | 39.225422 | 0.666090 | -0.253033 | 1.286807 | 1.246884 | 1.032018 |
| SOL | 1404 | -242.978050 | 0.719642 | 244.334578 | 0.636886 | 40.028490 | 0.729447 | -0.173061 | 1.165663 | 1.066604 | 1.092873 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2000 | -376.087577 | -46.779965 | 328.690953 | -0.616658 | 38.650000 | 0.692861 | -0.188044 | 1.097540 | 0.997951 | 1.099793 |
| SHORT | 3731 | -598.710525 | 25.551862 | 626.146880 | 1.884494 | 40.766551 | 0.736608 | -0.160469 | 1.100834 | 1.028543 | 1.070285 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 359 | -51.471859 | -18.336393 | 33.074525 | -0.060941 | 36.490251 | 0.613844 | -0.143376 | 0.624587 | 0.584617 | 1.068369 |
| AVAX | SHORT | 799 | -78.341142 | 7.771639 | 86.205840 | 0.093059 | 39.924906 | 0.750813 | -0.098049 | 0.739954 | 0.654972 | 1.129750 |
| BTC | LONG | 315 | -30.065966 | 24.396944 | 54.223323 | -0.239587 | 42.222222 | 0.837401 | -0.095448 | 1.164227 | 1.015979 | 1.145916 |
| BTC | SHORT | 531 | -72.799787 | 13.385445 | 86.464993 | 0.279761 | 41.619586 | 0.764328 | -0.137099 | 1.068340 | 0.996461 | 1.072134 |
| DOGE | LONG | 314 | -47.431303 | -6.053261 | 41.080415 | -0.297627 | 39.171975 | 0.694844 | -0.151055 | 0.878063 | 0.813785 | 1.078985 |
| DOGE | SHORT | 1002 | -196.905561 | 5.371868 | 203.215479 | 0.938050 | 40.918164 | 0.733720 | -0.196513 | 1.323322 | 1.249100 | 1.059420 |
| ETH | LONG | 432 | -113.607729 | -36.544845 | 76.766501 | -0.296383 | 37.962963 | 0.605846 | -0.262981 | 1.064779 | 1.075491 | 0.990040 |
| ETH | SHORT | 575 | -141.196704 | -11.939143 | 129.472179 | 0.214617 | 40.173913 | 0.702657 | -0.245559 | 1.444438 | 1.380412 | 1.046381 |
| SOL | LONG | 580 | -133.510720 | -10.242410 | 123.546189 | 0.277879 | 38.275862 | 0.711404 | -0.230191 | 1.482478 | 1.292237 | 1.147218 |
| SOL | SHORT | 824 | -109.467330 | 10.962052 | 120.788389 | 0.359007 | 41.262136 | 0.748617 | -0.132849 | 0.958802 | 0.899711 | 1.065678 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | 0.001190 | 0.020377 | 0.000000 | -0.019187 |
| stop | 3423 | -2,929.857165 | 563.841200 | 0.278803 | -3,493.419562 |
| stop_gap | 10 | -3.235958 | 0.615410 | 0.004181 | -3.847188 |
| trailing_take_profit | 1970 | 2,456.578967 | 332.323353 | 1.013488 | 2,125.269102 |
| trailing_take_profit_gap | 327 | 455.284863 | 58.037493 | -0.028637 | 397.218733 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 897.887013 | -102.112987 | -10.211299 | False |
| 2025-12 | 897.887013 | 689.615368 | -208.271645 | -23.195752 | False |
| 2026-01 | 689.615368 | 594.334033 | -95.281335 | -13.816591 | False |
| 2026-02 | 594.334033 | 454.284831 | -140.049202 | -23.564056 | False |
| 2026-03 | 454.284831 | 272.338669 | -181.946161 | -40.051120 | False |
| 2026-04 | 272.338669 | 206.272574 | -66.066095 | -24.258801 | False |
| 2026-05 | 206.272574 | 163.370647 | -42.901928 | -20.798658 | False |
| 2026-06 | 163.370647 | 129.828899 | -33.541748 | -20.531074 | False |
| 2026-07 | 129.828899 | 93.402105 | -36.426794 | -28.057539 | False |
| 2026-08 | 93.402105 | 80.456536 | -12.945569 | -13.860039 | False |
| 2026-09 | 80.456536 | 43.448211 | -37.008325 | -45.997910 | False |
| 2026-10 | 43.448211 | 31.879225 | -11.568985 | -26.627070 | False |
| 2026-11 | 31.879225 | 25.201899 | -6.677326 | -20.945699 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
