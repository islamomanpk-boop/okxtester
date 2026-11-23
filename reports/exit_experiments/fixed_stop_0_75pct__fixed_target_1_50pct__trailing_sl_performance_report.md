# Performance report: fixed_stop_0_75pct__fixed_target_1_50pct__trailing_sl

## Run metadata
- Experiment Id: fixed_stop_0_75pct__fixed_target_1_50pct__trailing_sl
- Stop Model: fixed_stop_0_75pct
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
- Final Equity: 140.253841
- Net Pnl: -859.746159
- Total Return Pct: -85.974616
- Max Drawdown Amount: 927.309398
- Max Drawdown Pct: 87.151111
- Recovery Factor: -0.927141
- Sharpe Ratio: -5.017781
- Sortino Ratio: -5.610273
- Cagr Pct: -83.701230
- Calmar Ratio: -0.960415
- Worst Daily Loss: -75.852795
- Worst Daily Loss Pct: -7.870212
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 39.439738
- Max Capital Utilization Pct: 101.733307
- Max Gross Exposure: 1,067.723989
- Max Gross Exposure Equity Multiple: 1.017333

## Trade performance

- Trade Count: 3968
- Net Pnl: -859.746159
- Gross Pnl: 43.461251
- Total Fees: 904.513414
- Funding Pnl: 1.306004
- Winning Trades: 1746
- Losing Trades: 2222
- Breakeven Trades: 0
- Win Rate Pct: 44.002016
- Profit Factor: 0.778947
- Expectancy: -0.216670
- Average Win: 1.735150
- Average Loss: 1.750368
- Payoff Ratio: 0.991306
- Max Consecutive Losses: 23
- Average Duration Minutes: 125.558972
- Median Duration Minutes: 61.000000
- Max Duration Minutes: 3,360.000000
- Recovery Factor: -0.927141

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 815 | -124.901913 | 10.912638 | 135.860264 | 0.045713 | 42.822086 | 0.784966 | -0.153254 | 1.306435 | 1.246454 | 1.048121 |
| BTC | 563 | -121.804445 | 3.479709 | 125.556315 | 0.272161 | 45.115453 | 0.774237 | -0.216349 | 1.644566 | 1.746033 | 0.941887 |
| DOGE | 915 | -237.587281 | -9.443777 | 228.759403 | 0.615899 | 44.262295 | 0.757252 | -0.259658 | 1.830011 | 1.919101 | 0.953577 |
| ETH | 709 | -195.440374 | -9.451501 | 185.999891 | 0.011018 | 43.018336 | 0.761365 | -0.275656 | 2.044429 | 2.027206 | 1.008496 |
| SOL | 966 | -180.012146 | 47.964182 | 228.337541 | 0.361214 | 44.824017 | 0.814652 | -0.186348 | 1.827255 | 1.822164 | 1.002794 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1327 | -399.759824 | -72.877642 | 325.664303 | -1.217879 | 41.296157 | 0.720535 | -0.301251 | 1.880820 | 1.836263 | 1.024265 |
| SHORT | 2641 | -459.986335 | 116.338893 | 578.849111 | 2.523883 | 45.361605 | 0.812928 | -0.174171 | 1.668517 | 1.703998 | 0.979178 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 238 | -74.327732 | -32.363188 | 41.849551 | -0.114994 | 34.873950 | 0.610559 | -0.312301 | 1.403970 | 1.231337 | 1.140200 |
| AVAX | SHORT | 577 | -50.574181 | 43.275826 | 94.010713 | 0.160707 | 46.100520 | 0.870319 | -0.087650 | 1.276001 | 1.253989 | 1.017554 |
| BTC | LONG | 207 | -49.529348 | 2.251884 | 51.365881 | -0.415351 | 45.410628 | 0.760316 | -0.239272 | 1.671435 | 1.828710 | 0.913997 |
| BTC | SHORT | 356 | -72.275097 | 1.227825 | 74.190434 | 0.687512 | 44.943820 | 0.782879 | -0.203020 | 1.628781 | 1.698368 | 0.959027 |
| DOGE | LONG | 211 | -72.504442 | -23.761494 | 48.278428 | -0.464520 | 42.654028 | 0.663597 | -0.343623 | 1.589154 | 1.781226 | 0.892169 |
| DOGE | SHORT | 704 | -165.082839 | 14.317717 | 180.480975 | 1.080419 | 44.744318 | 0.783700 | -0.234493 | 1.898827 | 1.961988 | 0.967808 |
| ETH | LONG | 285 | -66.650763 | 8.813533 | 75.067114 | -0.397182 | 41.403509 | 0.796560 | -0.233862 | 2.211593 | 1.961789 | 1.127335 |
| ETH | SHORT | 424 | -128.789610 | -18.265034 | 110.932777 | 0.408200 | 44.103774 | 0.737898 | -0.303749 | 1.938946 | 2.073302 | 0.935197 |
| SOL | LONG | 386 | -136.747538 | -27.818377 | 109.103330 | 0.174168 | 42.227979 | 0.720810 | -0.354268 | 2.165968 | 2.196414 | 0.986138 |
| SOL | SHORT | 580 | -43.264608 | 75.782558 | 119.234212 | 0.187046 | 46.551724 | 0.910130 | -0.074594 | 1.622772 | 1.552946 | 1.044964 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | -0.424286 | 0.081720 | -0.000452 | -0.506457 |
| stop | 3190 | -2,582.612830 | 725.358284 | 1.208066 | -3,306.763049 |
| stop_gap | 14 | 8.824335 | 2.634230 | -0.033503 | 6.156602 |
| target | 762 | 2,610.950181 | 175.988319 | 0.131893 | 2,435.093755 |
| target_gap | 1 | 6.723851 | 0.450860 | 0.000000 | 6.272990 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 1,015.556043 | 15.556043 | 1.555604 | False |
| 2025-12 | 1,015.556043 | 850.236721 | -165.319322 | -16.278700 | False |
| 2026-01 | 850.236721 | 793.244227 | -56.992494 | -6.703133 | False |
| 2026-02 | 793.244227 | 689.642017 | -103.602210 | -13.060569 | False |
| 2026-03 | 689.642017 | 520.779678 | -168.862339 | -24.485506 | False |
| 2026-04 | 520.779678 | 458.579699 | -62.199979 | -11.943626 | False |
| 2026-05 | 458.579699 | 371.425872 | -87.153827 | -19.005165 | False |
| 2026-06 | 371.425872 | 350.493194 | -20.932678 | -5.635762 | False |
| 2026-07 | 350.493194 | 288.121878 | -62.371316 | -17.795300 | False |
| 2026-08 | 288.121878 | 274.598469 | -13.523409 | -4.693642 | False |
| 2026-09 | 274.598469 | 187.857236 | -86.741233 | -31.588389 | False |
| 2026-10 | 187.857236 | 155.967841 | -31.889395 | -16.975335 | False |
| 2026-11 | 155.967841 | 140.253841 | -15.714000 | -10.075154 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
