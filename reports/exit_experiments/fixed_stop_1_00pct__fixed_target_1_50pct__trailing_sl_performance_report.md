# Performance report: fixed_stop_1_00pct__fixed_target_1_50pct__trailing_sl

## Run metadata
- Experiment Id: fixed_stop_1_00pct__fixed_target_1_50pct__trailing_sl
- Stop Model: fixed_stop_1_00pct
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
- Final Equity: 338.153656
- Net Pnl: -661.846344
- Total Return Pct: -66.184634
- Max Drawdown Amount: 789.189875
- Max Drawdown Pct: 71.751979
- Recovery Factor: -0.838640
- Sharpe Ratio: -2.983318
- Sortino Ratio: -3.724744
- Cagr Pct: -63.261173
- Calmar Ratio: -0.881665
- Worst Daily Loss: -69.760847
- Worst Daily Loss Pct: -6.854509
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 38.752165
- Max Capital Utilization Pct: 102.108077
- Max Gross Exposure: 1,083.140005
- Max Gross Exposure Equity Multiple: 1.021081

## Trade performance

- Trade Count: 3120
- Net Pnl: -661.846344
- Gross Pnl: 52.224323
- Total Fees: 715.415411
- Funding Pnl: 1.344744
- Winning Trades: 1422
- Losing Trades: 1698
- Breakeven Trades: 0
- Win Rate Pct: 45.576923
- Profit Factor: 0.833267
- Expectancy: -0.212130
- Average Win: 2.326050
- Average Loss: 2.337744
- Payoff Ratio: 0.994998
- Max Consecutive Losses: 24
- Average Duration Minutes: 193.510897
- Median Duration Minutes: 93.000000
- Max Duration Minutes: 4,122.000000
- Recovery Factor: -0.838640

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 625 | -109.287835 | 8.569605 | 117.713991 | -0.143449 | 45.120000 | 0.835079 | -0.174861 | 1.962344 | 1.931979 | 1.015717 |
| BTC | 431 | -86.529935 | 14.628614 | 101.515915 | 0.357367 | 47.563805 | 0.843060 | -0.200766 | 2.267450 | 2.439634 | 0.929422 |
| DOGE | 733 | -159.799091 | 10.141374 | 170.632133 | 0.691668 | 46.657572 | 0.829115 | -0.218007 | 2.267043 | 2.391631 | 0.947907 |
| ETH | 551 | -157.155825 | -16.320685 | 140.886098 | 0.050958 | 45.372051 | 0.803841 | -0.285219 | 2.576037 | 2.661678 | 0.967824 |
| SOL | 780 | -149.073658 | 35.205415 | 184.667273 | 0.388201 | 43.974359 | 0.853730 | -0.191120 | 2.536726 | 2.332198 | 1.087697 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1007 | -284.666190 | -45.038586 | 237.983995 | -1.643609 | 43.892751 | 0.789477 | -0.282687 | 2.415203 | 2.393249 | 1.009173 |
| SHORT | 2113 | -377.180154 | 97.262909 | 477.431416 | 2.988353 | 46.379555 | 0.855890 | -0.178505 | 2.285840 | 2.310065 | 0.989513 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 180 | -69.482616 | -34.211274 | 35.054668 | -0.216674 | 41.111111 | 0.683675 | -0.386015 | 2.029371 | 2.072227 | 0.979319 |
| AVAX | SHORT | 445 | -39.805219 | 42.780879 | 82.659323 | 0.073225 | 46.741573 | 0.910149 | -0.089450 | 1.938497 | 1.869252 | 1.037045 |
| BTC | LONG | 152 | -18.978709 | 19.488042 | 37.840277 | -0.626474 | 48.026316 | 0.901546 | -0.124860 | 2.380659 | 2.440087 | 0.975645 |
| BTC | SHORT | 279 | -67.551226 | -4.859428 | 63.675639 | 0.983841 | 47.311828 | 0.811620 | -0.242119 | 2.204842 | 2.439390 | 0.903850 |
| DOGE | LONG | 162 | -28.219735 | 5.933048 | 33.534788 | -0.617995 | 44.444444 | 0.848009 | -0.174196 | 2.186763 | 2.062963 | 1.060011 |
| DOGE | SHORT | 571 | -131.579355 | 4.208326 | 137.097344 | 1.309663 | 47.285464 | 0.824435 | -0.230437 | 2.288451 | 2.489904 | 0.919092 |
| ETH | LONG | 211 | -58.637989 | -5.366560 | 52.746561 | -0.524868 | 44.075829 | 0.803016 | -0.277905 | 2.570325 | 2.522697 | 1.018880 |
| ETH | SHORT | 340 | -98.517836 | -10.954125 | 88.139537 | 0.575826 | 46.176471 | 0.804329 | -0.289758 | 2.579420 | 2.751294 | 0.937530 |
| SOL | LONG | 302 | -109.347141 | -30.881842 | 78.807700 | 0.342402 | 43.046358 | 0.760423 | -0.362077 | 2.669776 | 2.653593 | 1.006098 |
| SOL | SHORT | 478 | -39.726517 | 66.087257 | 105.859573 | 0.045799 | 44.560669 | 0.929407 | -0.083110 | 2.455521 | 2.123594 | 1.156304 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 2 | -1.198597 | 0.304169 | 0.000000 | -1.502766 |
| stop | 2131 | -3,305.328373 | 488.080069 | 1.229140 | -3,792.179301 |
| stop_gap | 5 | -2.903395 | 0.502314 | 0.000000 | -3.405709 |
| target | 982 | 3,361.654688 | 226.528859 | 0.115604 | 3,135.241433 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 1,046.166661 | 46.166661 | 4.616666 | False |
| 2025-12 | 1,046.166661 | 911.486261 | -134.680400 | -12.873704 | False |
| 2026-01 | 911.486261 | 865.311965 | -46.174296 | -5.065825 | False |
| 2026-02 | 865.311965 | 751.389778 | -113.922187 | -13.165447 | False |
| 2026-03 | 751.389778 | 575.203316 | -176.186462 | -23.448078 | False |
| 2026-04 | 575.203316 | 548.518148 | -26.685168 | -4.639258 | False |
| 2026-05 | 548.518148 | 501.997171 | -46.520976 | -8.481210 | False |
| 2026-06 | 501.997171 | 496.303888 | -5.693283 | -1.134127 | False |
| 2026-07 | 496.303888 | 434.573467 | -61.730421 | -12.438029 | False |
| 2026-08 | 434.573467 | 464.801574 | 30.228107 | 6.955811 | False |
| 2026-09 | 464.801574 | 371.335125 | -93.466449 | -20.108893 | False |
| 2026-10 | 371.335125 | 343.004506 | -28.330619 | -7.629394 | False |
| 2026-11 | 343.004506 | 338.153656 | -4.850850 | -1.414223 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
