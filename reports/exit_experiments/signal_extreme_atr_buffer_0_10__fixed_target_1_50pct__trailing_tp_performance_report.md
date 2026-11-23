# Performance report: signal_extreme_atr_buffer_0_10__fixed_target_1_50pct__trailing_tp

## Run metadata
- Experiment Id: signal_extreme_atr_buffer_0_10__fixed_target_1_50pct__trailing_tp
- Stop Model: signal_extreme_atr_buffer_0_10
- Target Model: fixed_target_1_50pct
- Target Value: 0.015000
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
- Final Equity: 103.494592
- Net Pnl: -896.505408
- Total Return Pct: -89.650541
- Max Drawdown Amount: 917.107538
- Max Drawdown Pct: 90.279279
- Recovery Factor: -0.977536
- Sharpe Ratio: -5.603410
- Sortino Ratio: -6.166467
- Cagr Pct: -87.690165
- Calmar Ratio: -0.971321
- Worst Daily Loss: -58.992458
- Worst Daily Loss Pct: -5.894895
- Worst Daily Loss Date Utc: 2025-11-18
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 42.758830
- Max Capital Utilization Pct: 102.639200
- Max Gross Exposure: 1,021.772948
- Max Gross Exposure Equity Multiple: 1.026392

## Trade performance

- Trade Count: 3789
- Net Pnl: -896.505408
- Gross Pnl: -95.357416
- Total Fees: 802.454482
- Funding Pnl: 1.306489
- Winning Trades: 960
- Losing Trades: 2829
- Breakeven Trades: 0
- Win Rate Pct: 25.336500
- Profit Factor: 0.738881
- Expectancy: -0.236607
- Average Win: 2.642517
- Average Loss: 1.213617
- Payoff Ratio: 2.177390
- Max Consecutive Losses: 50
- Average Duration Minutes: 127.955925
- Median Duration Minutes: 50.000000
- Max Duration Minutes: 3,470.000000
- Recovery Factor: -0.977536

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 752 | -142.661154 | -23.240719 | 119.515815 | 0.095380 | 25.132979 | 0.719886 | -0.189709 | 1.939867 | 0.904611 | 2.144421 |
| BTC | 663 | -173.764139 | -26.321966 | 147.580694 | 0.138521 | 21.870287 | 0.697199 | -0.262088 | 2.759249 | 1.107829 | 2.490682 |
| DOGE | 858 | -186.045895 | 11.132839 | 197.882710 | 0.703975 | 27.156177 | 0.783954 | -0.216837 | 2.897398 | 1.377824 | 2.102881 |
| ETH | 650 | -210.686420 | -63.249999 | 147.411156 | -0.025265 | 25.230769 | 0.682577 | -0.324133 | 2.762529 | 1.365723 | 2.022760 |
| SOL | 866 | -183.347801 | 6.322429 | 190.064107 | 0.393878 | 26.443418 | 0.777838 | -0.211718 | 2.803240 | 1.295588 | 2.163681 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1195 | -360.619562 | -56.289615 | 303.044311 | -1.285636 | 23.012552 | 0.709155 | -0.301774 | 3.197400 | 1.347722 | 2.372447 |
| SHORT | 2594 | -535.885846 | -39.067801 | 499.410170 | 2.592126 | 26.407093 | 0.755685 | -0.206587 | 2.419754 | 1.148988 | 2.105988 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 217 | -69.592878 | -30.820424 | 38.661135 | -0.111320 | 22.119816 | 0.585991 | -0.320705 | 2.052126 | 0.994644 | 2.063175 |
| AVAX | SHORT | 535 | -73.068276 | 7.579705 | 80.854680 | 0.206700 | 26.355140 | 0.785850 | -0.136576 | 1.901651 | 0.865993 | 2.195921 |
| BTC | LONG | 220 | -59.576012 | -2.364574 | 56.818445 | -0.392993 | 20.000000 | 0.701964 | -0.270800 | 3.189076 | 1.135769 | 2.807856 |
| BTC | SHORT | 443 | -114.188127 | -23.957391 | 90.762249 | 0.531514 | 22.799097 | 0.694651 | -0.257761 | 2.571998 | 1.093450 | 2.352186 |
| DOGE | LONG | 197 | -56.524449 | -11.063399 | 44.986541 | -0.474509 | 23.857868 | 0.710263 | -0.286926 | 2.948178 | 1.300592 | 2.266797 |
| DOGE | SHORT | 661 | -129.521446 | 22.196237 | 152.896168 | 1.178485 | 28.139183 | 0.805538 | -0.195948 | 2.884567 | 1.402213 | 2.057154 |
| ETH | LONG | 245 | -50.080318 | 9.900012 | 59.562888 | -0.417441 | 24.489796 | 0.795980 | -0.204409 | 3.256460 | 1.326853 | 2.454272 |
| ETH | SHORT | 405 | -160.606102 | -73.150011 | 87.848268 | 0.392177 | 25.679012 | 0.616026 | -0.396558 | 2.477569 | 1.389612 | 1.782921 |
| SOL | LONG | 316 | -124.845905 | -21.941230 | 103.015302 | 0.110627 | 24.050633 | 0.710574 | -0.395082 | 4.033049 | 1.797323 | 2.243919 |
| SOL | SHORT | 550 | -58.501896 | 28.263659 | 87.048805 | 0.283251 | 27.818182 | 0.851492 | -0.106367 | 2.192355 | 0.992272 | 2.209428 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | 0.006048 | 0.103594 | 0.000000 | -0.097546 |
| stop | 2820 | -2,812.821444 | 620.599591 | 0.911325 | -3,432.509710 |
| stop_gap | 6 | -0.269898 | 0.085383 | 0.000000 | -0.355281 |
| trailing_take_profit | 755 | 2,121.928401 | 140.728614 | 0.571018 | 1,981.770805 |
| trailing_take_profit_gap | 207 | 595.799476 | 40.937298 | -0.175854 | 554.686324 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 875.665210 | -124.334790 | -12.433479 | False |
| 2025-12 | 875.665210 | 756.138992 | -119.526218 | -13.649762 | False |
| 2026-01 | 756.138992 | 671.217192 | -84.921801 | -11.230978 | False |
| 2026-02 | 671.217192 | 590.961234 | -80.255958 | -11.956779 | False |
| 2026-03 | 590.961234 | 428.999945 | -161.961289 | -27.406415 | False |
| 2026-04 | 428.999945 | 352.229085 | -76.770860 | -17.895308 | False |
| 2026-05 | 352.229085 | 253.105044 | -99.124041 | -28.141924 | False |
| 2026-06 | 253.105044 | 237.840916 | -15.264128 | -6.030748 | False |
| 2026-07 | 237.840916 | 181.052851 | -56.788065 | -23.876491 | False |
| 2026-08 | 181.052851 | 177.460627 | -3.592223 | -1.984074 | False |
| 2026-09 | 177.460627 | 131.360064 | -46.100563 | -25.977911 | False |
| 2026-10 | 131.360064 | 112.432049 | -18.928015 | -14.409262 | False |
| 2026-11 | 112.432049 | 103.494592 | -8.937457 | -7.949208 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
