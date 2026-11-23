# Performance report: fixed_stop_0_50pct__fixed_target_2_00pct__trailing_tp

## Run metadata
- Experiment Id: fixed_stop_0_50pct__fixed_target_2_00pct__trailing_tp
- Stop Model: fixed_stop_0_50pct
- Target Model: fixed_target_2_00pct
- Target Value: 0.020000
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
- Final Equity: 184.968191
- Net Pnl: -815.031809
- Total Return Pct: -81.503181
- Max Drawdown Amount: 894.013438
- Max Drawdown Pct: 83.627664
- Recovery Factor: -0.911655
- Sharpe Ratio: -3.720823
- Sortino Ratio: -4.298441
- Cagr Pct: -78.955137
- Calmar Ratio: -0.944127
- Worst Daily Loss: -95.492409
- Worst Daily Loss Pct: -9.043311
- Worst Daily Loss Date Utc: 2025-11-18
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 48.402115
- Max Capital Utilization Pct: 102.535687
- Max Gross Exposure: 1,064.720754
- Max Gross Exposure Equity Multiple: 1.025357

## Trade performance

- Trade Count: 3307
- Net Pnl: -815.031809
- Gross Pnl: 92.219705
- Total Fees: 909.503351
- Funding Pnl: 2.251836
- Winning Trades: 730
- Losing Trades: 2577
- Breakeven Trades: 0
- Win Rate Pct: 22.074388
- Profit Factor: 0.816987
- Expectancy: -0.246457
- Average Win: 4.984083
- Average Loss: 1.728138
- Payoff Ratio: 2.884076
- Max Consecutive Losses: 66
- Average Duration Minutes: 172.308437
- Median Duration Minutes: 52.000000
- Max Duration Minutes: 6,442.000000
- Recovery Factor: -0.911655

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 673 | -259.592799 | -119.372676 | 140.291311 | 0.071189 | 19.762259 | 0.640156 | -0.385725 | 3.472262 | 1.335933 | 2.599129 |
| BTC | 487 | -79.566642 | 51.115362 | 130.779488 | 0.097485 | 23.819302 | 0.873424 | -0.163381 | 4.733095 | 1.694355 | 2.793450 |
| DOGE | 759 | -103.081050 | 130.429174 | 234.879184 | 1.368960 | 23.978920 | 0.908390 | -0.135812 | 5.616130 | 1.950115 | 2.879896 |
| ETH | 588 | -226.426741 | -53.486253 | 173.023508 | 0.083019 | 21.088435 | 0.737401 | -0.385079 | 5.127632 | 1.858304 | 2.759307 |
| SOL | 800 | -146.364578 | 83.534098 | 230.529859 | 0.631183 | 21.875000 | 0.868841 | -0.182956 | 5.540393 | 1.785493 | 3.103004 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1081 | -353.766236 | -11.415426 | 340.117210 | -2.233599 | 20.444033 | 0.789421 | -0.327258 | 6.000915 | 1.953452 | 3.071955 |
| SHORT | 2226 | -461.265574 | 103.635131 | 569.386140 | 4.485435 | 22.866128 | 0.833685 | -0.207217 | 4.542590 | 1.615285 | 2.812253 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 203 | -78.133537 | -32.663894 | 45.154063 | -0.315580 | 16.748768 | 0.664540 | -0.384894 | 4.552389 | 1.378194 | 3.303156 |
| AVAX | SHORT | 470 | -181.459262 | -86.708782 | 95.137249 | 0.386769 | 21.063830 | 0.628529 | -0.386084 | 3.101309 | 1.316682 | 2.355398 |
| BTC | LONG | 168 | -8.820300 | 48.001077 | 56.209535 | -0.611843 | 22.619048 | 0.966532 | -0.052502 | 6.703256 | 2.027262 | 3.306557 |
| BTC | SHORT | 319 | -70.746341 | 3.114284 | 74.569953 | 0.709327 | 24.451411 | 0.806207 | -0.221775 | 3.773272 | 1.514778 | 2.490973 |
| DOGE | LONG | 175 | -40.676551 | 19.423574 | 59.340420 | -0.759706 | 22.285714 | 0.859015 | -0.232437 | 6.354866 | 2.121443 | 2.995539 |
| DOGE | SHORT | 584 | -62.404499 | 111.005600 | 175.538765 | 2.128666 | 24.486301 | 0.925416 | -0.106857 | 5.414656 | 1.897280 | 2.853905 |
| ETH | LONG | 228 | -112.277451 | -43.441400 | 68.163677 | -0.672375 | 20.614035 | 0.675268 | -0.492445 | 4.967583 | 1.910242 | 2.600499 |
| ETH | SHORT | 360 | -114.149290 | -10.044853 | 104.859832 | 0.755394 | 21.388889 | 0.778994 | -0.317081 | 5.225324 | 1.825086 | 2.863057 |
| SOL | LONG | 307 | -113.858396 | -2.734784 | 111.249517 | 0.125904 | 20.521173 | 0.792698 | -0.370874 | 6.910811 | 2.250982 | 3.070132 |
| SOL | SHORT | 493 | -32.506182 | 86.268882 | 119.280343 | 0.505279 | 22.718053 | 0.942639 | -0.065935 | 4.769533 | 1.487385 | 3.206656 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | 0.008732 | 0.149555 | 0.000000 | -0.140823 |
| stop | 2569 | -3,730.631754 | 717.855589 | 1.438348 | -4,447.048995 |
| stop_gap | 7 | -5.237034 | 0.994395 | 0.008921 | -6.222507 |
| trailing_take_profit | 532 | 2,819.410660 | 140.578541 | 0.243217 | 2,679.075337 |
| trailing_take_profit_gap | 198 | 1,008.669101 | 49.925271 | 0.561350 | 959.305180 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 955.397564 | -44.602436 | -4.460244 | False |
| 2025-12 | 955.397564 | 879.920855 | -75.476709 | -7.900032 | False |
| 2026-01 | 879.920855 | 840.622557 | -39.298298 | -4.466117 | False |
| 2026-02 | 840.622557 | 731.315686 | -109.306871 | -13.003086 | False |
| 2026-03 | 731.315686 | 610.431065 | -120.884621 | -16.529745 | False |
| 2026-04 | 610.431065 | 548.529597 | -61.901469 | -10.140616 | False |
| 2026-05 | 548.529597 | 464.398811 | -84.130785 | -15.337511 | False |
| 2026-06 | 464.398811 | 448.704737 | -15.694074 | -3.379439 | False |
| 2026-07 | 448.704737 | 377.554974 | -71.149763 | -15.856700 | False |
| 2026-08 | 377.554974 | 357.230302 | -20.324672 | -5.383235 | False |
| 2026-09 | 357.230302 | 211.657838 | -145.572464 | -40.750312 | False |
| 2026-10 | 211.657838 | 189.467687 | -22.190151 | -10.483973 | False |
| 2026-11 | 189.467687 | 184.968191 | -4.499497 | -2.374810 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
