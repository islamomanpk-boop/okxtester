# Performance report: signal_extreme_atr_buffer_0_10__fixed_target_2_00pct__trailing_sl

## Run metadata
- Experiment Id: signal_extreme_atr_buffer_0_10__fixed_target_2_00pct__trailing_sl
- Stop Model: signal_extreme_atr_buffer_0_10
- Target Model: fixed_target_2_00pct
- Target Value: 0.020000
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
- Final Equity: 8.405681
- Net Pnl: -991.594319
- Total Return Pct: -99.159432
- Max Drawdown Amount: 1,004.527619
- Max Drawdown Pct: 99.170164
- Recovery Factor: -0.987125
- Sharpe Ratio: -10.692931
- Sortino Ratio: -9.838992
- Cagr Pct: -98.788587
- Calmar Ratio: -0.996152
- Worst Daily Loss: -60.639871
- Worst Daily Loss Pct: -7.958738
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 34.194323
- Max Capital Utilization Pct: 102.335358
- Max Gross Exposure: 1,006.969578
- Max Gross Exposure Equity Multiple: 1.023354

## Trade performance

- Trade Count: 6265
- Net Pnl: -991.594319
- Gross Pnl: -97.788156
- Total Fees: 894.447424
- Funding Pnl: 0.641261
- Winning Trades: 2148
- Losing Trades: 4117
- Breakeven Trades: 0
- Win Rate Pct: 34.285714
- Profit Factor: 0.611028
- Expectancy: -0.158275
- Average Win: 0.725175
- Average Loss: 0.619206
- Payoff Ratio: 1.171137
- Max Consecutive Losses: 24
- Average Duration Minutes: 58.297207
- Median Duration Minutes: 26.000000
- Max Duration Minutes: 2,485.000000
- Recovery Factor: -0.987125

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1126 | -97.443477 | 8.367272 | 105.840645 | 0.029896 | 34.458259 | 0.669777 | -0.086540 | 0.509383 | 0.399843 | 1.273958 |
| BTC | 1155 | -198.738045 | -22.896039 | 175.845465 | 0.003460 | 32.640693 | 0.543223 | -0.172068 | 0.626921 | 0.559238 | 1.121027 |
| DOGE | 1497 | -162.546532 | 44.280496 | 207.136773 | 0.309745 | 34.869739 | 0.722274 | -0.108582 | 0.809826 | 0.600283 | 1.349074 |
| ETH | 1083 | -248.336278 | -68.772021 | 179.505404 | -0.058852 | 34.533703 | 0.544208 | -0.229304 | 0.792804 | 0.768470 | 1.031666 |
| SOL | 1404 | -284.529987 | -58.767864 | 226.119136 | 0.357013 | 34.686610 | 0.587026 | -0.202657 | 0.830487 | 0.751338 | 1.105344 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2192 | -401.910507 | -65.841001 | 335.587335 | -0.482171 | 32.253650 | 0.538929 | -0.183353 | 0.664468 | 0.586996 | 1.131980 |
| SHORT | 4073 | -589.683812 | -31.947156 | 558.860089 | 1.123432 | 35.379327 | 0.648492 | -0.144779 | 0.754960 | 0.637379 | 1.184476 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 326 | -52.968614 | -23.432679 | 29.496049 | -0.039886 | 30.368098 | 0.357669 | -0.162480 | 0.297925 | 0.363274 | 0.820110 |
| AVAX | SHORT | 800 | -44.474864 | 31.799950 | 76.344596 | 0.069782 | 36.125000 | 0.790826 | -0.055594 | 0.581821 | 0.416088 | 1.398311 |
| BTC | LONG | 456 | -72.354277 | -0.992491 | 71.187241 | -0.174545 | 31.578947 | 0.527656 | -0.158672 | 0.561299 | 0.490966 | 1.143254 |
| BTC | SHORT | 699 | -126.383768 | -21.903548 | 104.658225 | 0.178005 | 33.333333 | 0.551681 | -0.180807 | 0.667478 | 0.604949 | 1.103363 |
| DOGE | LONG | 348 | -38.773114 | -4.895535 | 33.731720 | -0.145859 | 32.758621 | 0.568878 | -0.111417 | 0.448792 | 0.384339 | 1.167697 |
| DOGE | SHORT | 1149 | -123.773418 | 49.176031 | 173.405053 | 0.455604 | 35.509138 | 0.750125 | -0.107723 | 0.910703 | 0.668476 | 1.362359 |
| ETH | LONG | 484 | -76.514633 | 2.583854 | 78.864263 | -0.234224 | 33.264463 | 0.623485 | -0.158088 | 0.786976 | 0.629157 | 1.250842 |
| ETH | SHORT | 599 | -171.821644 | -71.355876 | 100.641140 | 0.175372 | 35.559265 | 0.497050 | -0.286847 | 0.797210 | 0.885045 | 0.900756 |
| SOL | LONG | 578 | -161.299870 | -39.104151 | 122.308061 | 0.112343 | 32.698962 | 0.529589 | -0.279066 | 0.960803 | 0.881470 | 1.090002 |
| SOL | SHORT | 826 | -123.230118 | -19.663713 | 103.811075 | 0.244670 | 36.077482 | 0.643932 | -0.149189 | 0.747837 | 0.655465 | 1.140926 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| stop | 5883 | -825.206481 | 847.088766 | 0.571703 | -1,671.723543 |
| stop_gap | 95 | 47.955440 | 13.229464 | -0.039607 | 34.686369 |
| target | 287 | 679.462885 | 34.129194 | 0.109164 | 645.442855 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 820.015802 | -179.984198 | -17.998420 | False |
| 2025-12 | 820.015802 | 596.318009 | -223.697793 | -27.279693 | False |
| 2026-01 | 596.318009 | 457.841602 | -138.476407 | -23.221906 | False |
| 2026-02 | 457.841602 | 349.097742 | -108.743860 | -23.751415 | False |
| 2026-03 | 349.097742 | 193.439213 | -155.658529 | -44.588810 | False |
| 2026-04 | 193.439213 | 124.945137 | -68.494076 | -35.408579 | False |
| 2026-05 | 124.945137 | 81.943781 | -43.001356 | -34.416190 | False |
| 2026-06 | 81.943781 | 53.816874 | -28.126907 | -34.324639 | False |
| 2026-07 | 53.816874 | 36.719860 | -17.097014 | -31.768872 | False |
| 2026-08 | 36.719860 | 30.644202 | -6.075658 | -16.545973 | False |
| 2026-09 | 30.644202 | 18.851608 | -11.792595 | -38.482303 | False |
| 2026-10 | 18.851608 | 11.400128 | -7.451480 | -39.527025 | False |
| 2026-11 | 11.400128 | 8.405681 | -2.994447 | -26.266785 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
