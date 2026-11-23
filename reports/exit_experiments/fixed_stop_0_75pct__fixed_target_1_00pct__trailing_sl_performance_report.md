# Performance report: fixed_stop_0_75pct__fixed_target_1_00pct__trailing_sl

## Run metadata
- Experiment Id: fixed_stop_0_75pct__fixed_target_1_00pct__trailing_sl
- Stop Model: fixed_stop_0_75pct
- Target Model: fixed_target_1_00pct
- Target Value: 0.010000
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
- Final Equity: 119.100786
- Net Pnl: -880.899214
- Total Return Pct: -88.089921
- Max Drawdown Amount: 917.470878
- Max Drawdown Pct: 88.676513
- Recovery Factor: -0.960139
- Sharpe Ratio: -5.647407
- Sortino Ratio: -6.108397
- Cagr Pct: -85.985279
- Calmar Ratio: -0.969651
- Worst Daily Loss: -78.293503
- Worst Daily Loss Pct: -8.380519
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 38.870947
- Max Capital Utilization Pct: 101.733307
- Max Gross Exposure: 1,037.328095
- Max Gross Exposure Equity Multiple: 1.017333

## Trade performance

- Trade Count: 4299
- Net Pnl: -880.899214
- Gross Pnl: 8.596580
- Total Fees: 890.676394
- Funding Pnl: 1.180600
- Winning Trades: 1894
- Losing Trades: 2405
- Breakeven Trades: 0
- Win Rate Pct: 44.056757
- Profit Factor: 0.769333
- Expectancy: -0.204908
- Average Win: 1.551229
- Average Loss: 1.587911
- Payoff Ratio: 0.976899
- Max Consecutive Losses: 23
- Average Duration Minutes: 113.012794
- Median Duration Minutes: 53.000000
- Max Duration Minutes: 3,360.000000
- Recovery Factor: -0.960139

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 886 | -102.225327 | 32.098899 | 134.295729 | -0.028497 | 44.469526 | 0.811914 | -0.115378 | 1.119994 | 1.104681 | 1.013862 |
| BTC | 620 | -81.069728 | 45.509812 | 126.815924 | 0.236383 | 45.483871 | 0.844462 | -0.130758 | 1.560821 | 1.542075 | 1.012157 |
| DOGE | 993 | -240.540607 | -19.897659 | 221.203634 | 0.560685 | 43.806647 | 0.750657 | -0.242236 | 1.664727 | 1.728847 | 0.962911 |
| ETH | 751 | -246.875716 | -66.818857 | 180.034491 | -0.022368 | 42.476698 | 0.697141 | -0.328729 | 1.781430 | 1.886926 | 0.944091 |
| SOL | 1049 | -210.187835 | 17.704384 | 228.326615 | 0.434396 | 44.232602 | 0.784280 | -0.200370 | 1.646908 | 1.665561 | 0.988801 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1460 | -380.841194 | -60.587783 | 319.169599 | -1.083812 | 42.123288 | 0.725626 | -0.260850 | 1.637719 | 1.642649 | 0.996999 |
| SHORT | 2839 | -500.058020 | 69.184363 | 571.506795 | 2.264412 | 45.051074 | 0.794290 | -0.176139 | 1.509640 | 1.558262 | 0.968798 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 263 | -49.847856 | -9.643339 | 40.058010 | -0.146507 | 38.783270 | 0.693645 | -0.189536 | 1.106521 | 1.010639 | 1.094872 |
| AVAX | SHORT | 623 | -52.377471 | 41.742238 | 94.237719 | 0.118010 | 46.869984 | 0.862451 | -0.084073 | 1.124701 | 1.150423 | 0.977641 |
| BTC | LONG | 230 | -28.373004 | 23.033131 | 51.056611 | -0.349524 | 45.652174 | 0.858159 | -0.123361 | 1.634869 | 1.600274 | 1.021618 |
| BTC | SHORT | 390 | -52.696724 | 22.476681 | 75.759312 | 0.585907 | 45.384615 | 0.835931 | -0.135120 | 1.516894 | 1.507920 | 1.005951 |
| DOGE | LONG | 230 | -60.167339 | -11.961338 | 47.790922 | -0.415079 | 43.478261 | 0.715222 | -0.261597 | 1.511105 | 1.625214 | 0.929788 |
| DOGE | SHORT | 763 | -180.373268 | -7.936321 | 173.412712 | 0.975765 | 43.905636 | 0.760594 | -0.236400 | 1.710584 | 1.760324 | 0.971744 |
| ETH | LONG | 309 | -90.542374 | -17.909502 | 72.285693 | -0.347178 | 41.747573 | 0.720424 | -0.293017 | 1.808633 | 1.799200 | 1.005243 |
| ETH | SHORT | 442 | -156.333343 | -48.909356 | 107.748798 | 0.324810 | 42.986425 | 0.681794 | -0.353695 | 1.762961 | 1.949587 | 0.904274 |
| SOL | LONG | 428 | -151.910621 | -44.106735 | 107.978363 | 0.174476 | 41.822430 | 0.690078 | -0.354931 | 1.889645 | 1.968502 | 0.959940 |
| SOL | SHORT | 621 | -58.277214 | 61.811119 | 120.348253 | 0.259920 | 45.893720 | 0.879641 | -0.093844 | 1.494453 | 1.441060 | 1.037051 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | -0.360295 | 0.069395 | -0.000383 | -0.430073 |
| stop | 2706 | -3,216.342515 | 561.099598 | 0.679020 | -3,776.763093 |
| stop_gap | 5 | 0.510290 | 0.974575 | -0.031750 | -0.496035 |
| target | 1584 | 3,221.665462 | 328.215714 | 0.533713 | 2,893.983461 |
| target_gap | 3 | 3.123638 | 0.317112 | 0.000000 | 2.806527 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 978.785260 | -21.214740 | -2.121474 | False |
| 2025-12 | 978.785260 | 762.666944 | -216.118316 | -22.080259 | False |
| 2026-01 | 762.666944 | 699.455108 | -63.211837 | -8.288262 | False |
| 2026-02 | 699.455108 | 608.826910 | -90.628197 | -12.956971 | False |
| 2026-03 | 608.826910 | 459.261616 | -149.565294 | -24.566144 | False |
| 2026-04 | 459.261616 | 411.748968 | -47.512648 | -10.345443 | False |
| 2026-05 | 411.748968 | 331.443710 | -80.305258 | -19.503451 | False |
| 2026-06 | 331.443710 | 302.131736 | -29.311975 | -8.843726 | False |
| 2026-07 | 302.131736 | 244.085788 | -58.045948 | -19.212132 | False |
| 2026-08 | 244.085788 | 230.472808 | -13.612980 | -5.577129 | False |
| 2026-09 | 230.472808 | 160.579871 | -69.892937 | -30.325893 | False |
| 2026-10 | 160.579871 | 133.098946 | -27.480925 | -17.113556 | False |
| 2026-11 | 133.098946 | 119.100786 | -13.998160 | -10.517108 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
