# Performance report: fixed_stop_1_00pct__fixed_target_1_00pct__trailing_tp

## Run metadata
- Experiment Id: fixed_stop_1_00pct__fixed_target_1_00pct__trailing_tp
- Stop Model: fixed_stop_1_00pct
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
- Final Equity: 269.753537
- Net Pnl: -730.246463
- Total Return Pct: -73.024646
- Max Drawdown Amount: 821.405986
- Max Drawdown Pct: 76.538584
- Recovery Factor: -0.889020
- Sharpe Ratio: -3.696805
- Sortino Ratio: -4.335513
- Cagr Pct: -70.181611
- Calmar Ratio: -0.916944
- Worst Daily Loss: -70.025617
- Worst Daily Loss Pct: -7.075957
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 38.261556
- Max Capital Utilization Pct: 102.245461
- Max Gross Exposure: 1,061.443609
- Max Gross Exposure Equity Multiple: 1.022455

## Trade performance

- Trade Count: 3232
- Net Pnl: -730.246463
- Gross Pnl: -47.590235
- Total Fees: 683.912589
- Funding Pnl: 1.256361
- Winning Trades: 1624
- Losing Trades: 1608
- Breakeven Trades: 0
- Win Rate Pct: 50.247525
- Profit Factor: 0.809401
- Expectancy: -0.225943
- Average Win: 1.909535
- Average Loss: 2.382669
- Payoff Ratio: 0.801427
- Max Consecutive Losses: 23
- Average Duration Minutes: 182.879641
- Median Duration Minutes: 84.000000
- Max Duration Minutes: 3,948.000000
- Recovery Factor: -0.889020

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 635 | -77.854424 | 28.646330 | 106.390282 | -0.110472 | 48.661417 | 0.871353 | -0.122605 | 1.706548 | 1.856373 | 0.919291 |
| BTC | 454 | -67.054241 | 32.050809 | 99.423784 | 0.318734 | 53.524229 | 0.874065 | -0.147697 | 1.915212 | 2.523463 | 0.758962 |
| DOGE | 755 | -170.120110 | -5.167911 | 165.536708 | 0.584510 | 50.596026 | 0.817146 | -0.225325 | 1.990156 | 2.494262 | 0.797894 |
| ETH | 578 | -254.611927 | -119.866323 | 134.791192 | 0.045588 | 49.826990 | 0.675758 | -0.440505 | 1.842505 | 2.707770 | 0.680451 |
| SOL | 810 | -160.605762 | 16.746860 | 177.770623 | 0.418001 | 49.629630 | 0.835797 | -0.198279 | 2.033544 | 2.397280 | 0.848271 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1044 | -281.837166 | -52.524929 | 227.808119 | -1.504117 | 48.850575 | 0.781386 | -0.269959 | 1.975217 | 2.414228 | 0.818157 |
| SHORT | 2188 | -448.409297 | 4.934694 | 456.104470 | 2.760479 | 50.914077 | 0.823609 | -0.204940 | 1.879465 | 2.366977 | 0.794036 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 184 | -63.366659 | -30.407378 | 32.779109 | -0.180172 | 43.478261 | 0.691493 | -0.344384 | 1.775387 | 1.974977 | 0.898940 |
| AVAX | SHORT | 451 | -14.487765 | 59.053707 | 73.611173 | 0.069700 | 50.776053 | 0.963761 | -0.032124 | 1.682499 | 1.800811 | 0.934301 |
| BTC | LONG | 158 | -23.514032 | 14.695273 | 37.657361 | -0.551945 | 53.797468 | 0.883006 | -0.148823 | 2.087889 | 2.753214 | 0.758346 |
| BTC | SHORT | 296 | -43.540208 | 17.355536 | 61.766423 | 0.870679 | 53.378378 | 0.868644 | -0.147095 | 1.822316 | 2.401928 | 0.758689 |
| DOGE | LONG | 170 | -25.737265 | 6.759365 | 31.921207 | -0.575423 | 50.000000 | 0.856039 | -0.151396 | 1.800495 | 2.103287 | 0.856039 |
| DOGE | SHORT | 585 | -144.382844 | -11.927276 | 133.615501 | 1.159932 | 50.769231 | 0.807894 | -0.246808 | 2.044436 | 2.609654 | 0.783413 |
| ETH | LONG | 219 | -94.269349 | -43.553368 | 50.245512 | -0.470468 | 50.228311 | 0.665327 | -0.430454 | 1.703696 | 2.584183 | 0.659279 |
| ETH | SHORT | 359 | -160.342578 | -76.312954 | 84.545680 | 0.516056 | 49.582173 | 0.681593 | -0.446637 | 1.928285 | 2.782195 | 0.693080 |
| SOL | LONG | 313 | -74.949860 | -0.018821 | 75.204930 | 0.273890 | 47.923323 | 0.822545 | -0.239456 | 2.316070 | 2.591168 | 0.893832 |
| SOL | SHORT | 497 | -85.655902 | 16.765681 | 102.565693 | 0.144111 | 50.704225 | 0.845868 | -0.172346 | 1.865373 | 2.268286 | 0.822371 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 2 | -0.956151 | 0.242643 | 0.000000 | -1.198794 |
| stop | 1602 | -3,484.956304 | 342.209713 | 0.319663 | -3,826.846355 |
| stop_gap | 2 | -2.902855 | 0.282872 | 0.000000 | -3.185727 |
| trailing_take_profit | 1523 | 3,135.890090 | 319.575271 | 0.802986 | 2,817.117805 |
| trailing_take_profit_gap | 103 | 305.334984 | 21.602090 | 0.133713 | 283.866607 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 1,027.479744 | 27.479744 | 2.747974 | False |
| 2025-12 | 1,027.479744 | 891.458901 | -136.020843 | -13.238299 | False |
| 2026-01 | 891.458901 | 855.303282 | -36.155619 | -4.055781 | False |
| 2026-02 | 855.303282 | 707.728487 | -147.574795 | -17.254090 | False |
| 2026-03 | 707.728487 | 542.113376 | -165.615111 | -23.400939 | False |
| 2026-04 | 542.113376 | 515.066105 | -27.047271 | -4.989228 | False |
| 2026-05 | 515.066105 | 462.931089 | -52.135016 | -10.122005 | False |
| 2026-06 | 462.931089 | 426.213023 | -36.718066 | -7.931648 | False |
| 2026-07 | 426.213023 | 367.754880 | -58.458143 | -13.715710 | False |
| 2026-08 | 367.754880 | 395.695171 | 27.940291 | 7.597531 | False |
| 2026-09 | 395.695171 | 300.855203 | -94.839968 | -23.967937 | False |
| 2026-10 | 300.855203 | 269.972342 | -30.882861 | -10.265025 | False |
| 2026-11 | 269.972342 | 269.753537 | -0.218805 | -0.081047 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
