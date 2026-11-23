# Performance report: fees_0_05pct_zero_slippage

## Run metadata
- Scenario Id: fees_0_05pct_zero_slippage
- Experiment Id: fixed_stop_0_50pct__fixed_target_0_75pct
- Assets: BTC,ETH,SOL,DOGE,AVAX
- Execution Timeframe: 1m
- Execution Window Start Utc: 2025-10-20T08:50:00+00:00
- Execution Window End Utc: 2026-11-19T14:14:00+00:00
- Taker Fee Rate Per Side: 0.000500
- Slippage Bps Per Side: 0.000000
- Funding Data: Historical asset-specific realized funding rates
- Funding Treatment: Applied at funding timestamps; mark price when supplied, otherwise candle close proxy
- Equity Curve Storage: summary-only
- Risk Fraction: 0.005000
- Max Gross Leverage: 1.000000
- Cost Sensitivity Note: Same signals, date window, exit rules, risk fraction, and portfolio constraints; cost-aware sizing means fills, accepted entries, and outcomes can change.
- End Of Data Policy: Open positions forcibly closed at final available candle

## Portfolio risk and return

- Initial Equity: 1,000.000000
- Final Equity: 85.043505
- Net Pnl: -914.956495
- Total Return Pct: -91.495650
- Max Drawdown Amount: 957.816274
- Max Drawdown Pct: 92.035546
- Recovery Factor: -0.955253
- Sharpe Ratio: -6.429986
- Sortino Ratio: -6.721607
- Cagr Pct: -89.731730
- Calmar Ratio: -0.974968
- Worst Daily Loss: -75.363604
- Worst Daily Loss Pct: -8.149698
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 40.457414
- Max Capital Utilization Pct: 101.512490
- Max Gross Exposure: 1,042.653377
- Max Gross Exposure Equity Multiple: 1.015125

## Trade performance

- Trade Count: 5896
- Net Pnl: -914.956495
- Gross Pnl: 434.777968
- Total Fees: 1,351.255845
- Funding Pnl: 1.521382
- Winning Trades: 2495
- Losing Trades: 3401
- Breakeven Trades: 0
- Win Rate Pct: 42.316825
- Profit Factor: 0.803495
- Expectancy: -0.155183
- Average Win: 1.499473
- Average Loss: 1.369051
- Payoff Ratio: 1.095265
- Max Consecutive Losses: 19
- Average Duration Minutes: 72.126018
- Median Duration Minutes: 32.000000
- Max Duration Minutes: 3,160.000000
- Recovery Factor: -0.955253

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1185 | -181.435125 | 15.066278 | 196.615188 | 0.113785 | 41.687764 | 0.741062 | -0.153110 | 1.051123 | 1.014023 | 1.036587 |
| BTC | 885 | -92.919139 | 104.487714 | 197.623090 | 0.216236 | 43.841808 | 0.859436 | -0.104993 | 1.464240 | 1.330069 | 1.100875 |
| DOGE | 1360 | -185.494609 | 155.126372 | 341.152116 | 0.531134 | 42.720588 | 0.839273 | -0.136393 | 1.667131 | 1.481512 | 1.125290 |
| ETH | 1022 | -232.259887 | 47.776157 | 279.958755 | -0.077289 | 40.313112 | 0.764237 | -0.227260 | 1.827385 | 1.614988 | 1.131516 |
| SOL | 1444 | -222.847735 | 112.321447 | 335.906697 | 0.737515 | 42.936288 | 0.807086 | -0.154327 | 1.503740 | 1.401901 | 1.072643 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2066 | -403.546031 | 86.314742 | 488.748515 | -1.112259 | 40.561471 | 0.765068 | -0.195327 | 1.568223 | 1.398792 | 1.121126 |
| SHORT | 3830 | -511.410464 | 348.463226 | 862.507331 | 2.633641 | 43.263708 | 0.825958 | -0.133528 | 1.464704 | 1.352243 | 1.083166 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 367 | -74.043769 | -12.196070 | 61.637736 | -0.209964 | 38.692098 | 0.674952 | -0.201754 | 1.082746 | 1.012416 | 1.069467 |
| AVAX | SHORT | 818 | -107.391356 | 27.262348 | 134.977453 | 0.323749 | 43.031785 | 0.772907 | -0.131285 | 1.038366 | 1.014799 | 1.023224 |
| BTC | LONG | 334 | -19.179869 | 59.458756 | 78.322269 | -0.316356 | 44.311377 | 0.924272 | -0.057425 | 1.581707 | 1.361680 | 1.161585 |
| BTC | SHORT | 551 | -73.739270 | 45.028958 | 119.300820 | 0.532592 | 43.557169 | 0.819165 | -0.133828 | 1.391802 | 1.311163 | 1.061502 |
| DOGE | LONG | 318 | -56.022749 | 9.100235 | 64.686948 | -0.436036 | 40.880503 | 0.754954 | -0.176172 | 1.327681 | 1.216071 | 1.091779 |
| DOGE | SHORT | 1042 | -129.471860 | 146.026137 | 276.465168 | 0.967170 | 43.282150 | 0.860103 | -0.124253 | 1.764977 | 1.565950 | 1.127097 |
| ETH | LONG | 448 | -122.210511 | -10.672215 | 111.162803 | -0.375492 | 38.616071 | 0.698535 | -0.272791 | 1.636869 | 1.474141 | 1.110388 |
| ETH | SHORT | 574 | -110.049376 | 58.448372 | 168.795952 | 0.298204 | 41.637631 | 0.810179 | -0.191724 | 1.965290 | 1.730608 | 1.135607 |
| SOL | LONG | 599 | -132.089133 | 40.624037 | 172.938759 | 0.225589 | 40.901503 | 0.780816 | -0.220516 | 1.920619 | 1.702375 | 1.128200 |
| SOL | SHORT | 845 | -90.758601 | 71.697411 | 162.967938 | 0.511926 | 44.378698 | 0.835739 | -0.107407 | 1.231380 | 1.175587 | 1.047459 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | -0.187794 | 0.071341 | 0.000000 | -0.259135 |
| stop | 3392 | -3,871.153906 | 774.734768 | 0.617538 | -4,645.271136 |
| stop_gap | 8 | -8.875466 | 1.756645 | 0.021033 | -10.611077 |
| target | 2491 | 4,313.534283 | 574.498585 | 0.882811 | 3,739.918509 |
| target_gap | 4 | 1.460851 | 0.194507 | 0.000000 | 1.266344 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 965.141822 | -34.858178 | -3.485818 | False |
| 2025-12 | 965.141822 | 809.035893 | -156.105929 | -16.174403 | False |
| 2026-01 | 809.035893 | 740.919457 | -68.116436 | -8.419458 | False |
| 2026-02 | 740.919457 | 603.310340 | -137.609117 | -18.572750 | False |
| 2026-03 | 603.310340 | 406.363116 | -196.947224 | -32.644430 | False |
| 2026-04 | 406.363116 | 327.139942 | -79.223174 | -19.495661 | False |
| 2026-05 | 327.139942 | 279.214230 | -47.925712 | -14.649912 | False |
| 2026-06 | 279.214230 | 243.329557 | -35.884673 | -12.852022 | False |
| 2026-07 | 243.329557 | 192.688391 | -50.641166 | -20.811761 | False |
| 2026-08 | 192.688391 | 170.147732 | -22.540659 | -11.697985 | False |
| 2026-09 | 170.147732 | 108.863826 | -61.283906 | -36.018056 | False |
| 2026-10 | 108.863826 | 91.634384 | -17.229442 | -15.826600 | False |
| 2026-11 | 91.634384 | 85.043505 | -6.590879 | -7.192583 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
