# Performance report: signal_extreme_exact__target_1_5R__trailing_sl

## Run metadata
- Experiment Id: signal_extreme_exact__target_1_5R__trailing_sl
- Stop Model: signal_extreme_exact
- Target Model: target_1_5R
- Target Value: 1.500000
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
- Final Equity: 2.575632
- Net Pnl: -997.424368
- Total Return Pct: -99.742437
- Max Drawdown Amount: 1,016.323319
- Max Drawdown Pct: 99.747214
- Recovery Factor: -0.981405
- Sharpe Ratio: -13.214296
- Sortino Ratio: -11.130436
- Cagr Pct: -99.593662
- Calmar Ratio: -0.998461
- Worst Daily Loss: -59.086120
- Worst Daily Loss Pct: -7.065411
- Worst Daily Loss Date Utc: 2025-11-22
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 32.332916
- Max Capital Utilization Pct: 102.362226
- Max Gross Exposure: 1,011.334459
- Max Gross Exposure Equity Multiple: 1.023622

## Trade performance

- Trade Count: 7047
- Net Pnl: -997.424368
- Gross Pnl: -173.244253
- Total Fees: 825.016015
- Funding Pnl: 0.835901
- Winning Trades: 2441
- Losing Trades: 4606
- Breakeven Trades: 0
- Win Rate Pct: 34.638853
- Profit Factor: 0.543250
- Expectancy: -0.141539
- Average Win: 0.485997
- Average Loss: 0.474108
- Payoff Ratio: 1.025076
- Max Consecutive Losses: 23
- Average Duration Minutes: 48.111253
- Median Duration Minutes: 18.000000
- Max Duration Minutes: 4,050.000000
- Recovery Factor: -0.981405

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1287 | -131.211471 | -30.570444 | 100.656970 | 0.015944 | 35.586636 | 0.484591 | -0.101951 | 0.269358 | 0.307090 | 0.877132 |
| BTC | 1300 | -201.203274 | -38.292444 | 163.027123 | 0.116292 | 33.000000 | 0.489481 | -0.154772 | 0.449678 | 0.452486 | 0.993795 |
| DOGE | 1667 | -189.254333 | -3.579435 | 185.982479 | 0.307581 | 35.572885 | 0.611805 | -0.113530 | 0.502984 | 0.453933 | 1.108059 |
| ETH | 1214 | -219.682324 | -53.506669 | 166.163868 | -0.011787 | 33.113674 | 0.538464 | -0.180957 | 0.637559 | 0.586184 | 1.087644 |
| SOL | 1579 | -256.072966 | -47.295261 | 209.185575 | 0.407870 | 35.402153 | 0.551964 | -0.162174 | 0.564351 | 0.560338 | 1.007161 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2505 | -324.614318 | -57.820934 | 266.618157 | -0.175226 | 32.934132 | 0.500064 | -0.129587 | 0.393573 | 0.386495 | 1.018312 |
| SHORT | 4542 | -672.810050 | -115.423319 | 558.397858 | 1.011127 | 35.579040 | 0.561525 | -0.148131 | 0.533181 | 0.524413 | 1.016721 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 376 | -39.784263 | -17.063508 | 22.702320 | -0.018436 | 30.585106 | 0.330113 | -0.105809 | 0.170480 | 0.227546 | 0.749212 |
| AVAX | SHORT | 911 | -91.427207 | -13.506937 | 77.954651 | 0.034380 | 37.650933 | 0.531594 | -0.100359 | 0.302510 | 0.343641 | 0.880308 |
| BTC | LONG | 501 | -53.471498 | -0.241574 | 53.164376 | -0.065548 | 33.133733 | 0.507794 | -0.106730 | 0.332318 | 0.324288 | 1.024764 |
| BTC | SHORT | 799 | -147.731777 | -38.050870 | 109.862747 | 0.181840 | 32.916145 | 0.482513 | -0.184896 | 0.523754 | 0.532610 | 0.983372 |
| DOGE | LONG | 406 | -30.090003 | -5.018120 | 24.955853 | -0.116030 | 36.453202 | 0.501517 | -0.074113 | 0.204548 | 0.233966 | 0.874266 |
| DOGE | SHORT | 1261 | -159.164330 | 1.438685 | 161.026626 | 0.423611 | 35.289453 | 0.627390 | -0.126221 | 0.602240 | 0.523482 | 1.150450 |
| ETH | LONG | 566 | -55.082293 | 3.752522 | 58.750416 | -0.084398 | 32.155477 | 0.609510 | -0.097319 | 0.472402 | 0.367343 | 1.286000 |
| ETH | SHORT | 648 | -164.600032 | -57.259191 | 107.413452 | 0.072611 | 33.950617 | 0.508541 | -0.254012 | 0.774189 | 0.782527 | 0.989344 |
| SOL | LONG | 656 | -146.186261 | -39.250255 | 107.045192 | 0.109186 | 32.621951 | 0.477651 | -0.222845 | 0.624660 | 0.633175 | 0.986551 |
| SOL | SHORT | 923 | -109.886705 | -8.045007 | 102.140382 | 0.298685 | 37.378115 | 0.623265 | -0.119054 | 0.526941 | 0.504639 | 1.044194 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| stop | 4875 | -1,557.280024 | 572.618259 | 0.284903 | -2,129.613380 |
| stop_gap | 56 | -10.438792 | 7.459950 | 0.007678 | -17.891064 |
| target | 2111 | 1,392.513259 | 244.036456 | 0.543319 | 1,149.020121 |
| target_gap | 5 | 1.961304 | 0.901349 | 0.000000 | 1.059955 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 695.557217 | -304.442783 | -30.444278 | False |
| 2025-12 | 695.557217 | 460.065966 | -235.491250 | -33.856489 | False |
| 2026-01 | 460.065966 | 325.616321 | -134.449646 | -29.223993 | False |
| 2026-02 | 325.616321 | 240.219200 | -85.397121 | -26.226302 | False |
| 2026-03 | 240.219200 | 125.831499 | -114.387701 | -47.618051 | False |
| 2026-04 | 125.831499 | 77.992129 | -47.839370 | -38.018596 | False |
| 2026-05 | 77.992129 | 46.518696 | -31.473433 | -40.354627 | False |
| 2026-06 | 46.518696 | 29.797302 | -16.721395 | -35.945536 | False |
| 2026-07 | 29.797302 | 16.852371 | -12.944931 | -43.443300 | False |
| 2026-08 | 16.852371 | 13.084389 | -3.767981 | -22.358762 | False |
| 2026-09 | 13.084389 | 7.391497 | -5.692892 | -43.509040 | False |
| 2026-10 | 7.391497 | 3.907843 | -3.483655 | -47.130568 | False |
| 2026-11 | 3.907843 | 2.575632 | -1.332210 | -34.090687 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
