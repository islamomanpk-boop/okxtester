# Performance report: signal_extreme_exact__target_1R__trailing_tp

## Run metadata
- Experiment Id: signal_extreme_exact__target_1R__trailing_tp
- Stop Model: signal_extreme_exact
- Target Model: target_1R
- Target Value: 1.000000
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
- Final Equity: 1.219578
- Net Pnl: -998.780422
- Total Return Pct: -99.878042
- Max Drawdown Amount: 1,012.676149
- Max Drawdown Pct: 99.879714
- Recovery Factor: -0.986278
- Sharpe Ratio: -14.541830
- Sortino Ratio: -11.800758
- Cagr Pct: -99.796276
- Calmar Ratio: -0.999165
- Worst Daily Loss: -68.115710
- Worst Daily Loss Pct: -7.094594
- Worst Daily Loss Date Utc: 2025-11-18
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 31.074661
- Max Capital Utilization Pct: 102.362072
- Max Gross Exposure: 1,013.847210
- Max Gross Exposure Equity Multiple: 1.023621

## Trade performance

- Trade Count: 7424
- Net Pnl: -998.780422
- Gross Pnl: -228.318067
- Total Fees: 771.132788
- Funding Pnl: 0.670433
- Winning Trades: 3054
- Losing Trades: 4370
- Breakeven Trades: 0
- Win Rate Pct: 41.136853
- Profit Factor: 0.505928
- Expectancy: -0.134534
- Average Win: 0.334888
- Average Loss: 0.462592
- Payoff Ratio: 0.723938
- Max Consecutive Losses: 20
- Average Duration Minutes: 43.119747
- Median Duration Minutes: 16.000000
- Max Duration Minutes: 4,420.000000
- Recovery Factor: -0.986278

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1318 | -108.600535 | -14.945074 | 93.618704 | -0.036756 | 42.564492 | 0.533900 | -0.082398 | 0.221743 | 0.307792 | 0.720432 |
| BTC | 1394 | -206.972290 | -55.415150 | 151.657279 | 0.100139 | 36.728838 | 0.435427 | -0.148474 | 0.311772 | 0.415646 | 0.750091 |
| DOGE | 1757 | -186.224985 | -15.908186 | 170.552403 | 0.235605 | 42.458736 | 0.578200 | -0.105990 | 0.342193 | 0.436697 | 0.783593 |
| ETH | 1285 | -229.314878 | -73.233720 | 156.063657 | -0.017501 | 40.622568 | 0.493446 | -0.178455 | 0.427932 | 0.593310 | 0.721263 |
| SOL | 1670 | -267.667735 | -68.815936 | 199.240744 | 0.388946 | 42.694611 | 0.492798 | -0.160280 | 0.364749 | 0.551446 | 0.661441 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2682 | -296.896039 | -58.618299 | 238.130455 | -0.147285 | 40.156600 | 0.474849 | -0.110699 | 0.249264 | 0.352245 | 0.707644 |
| SHORT | 4742 | -701.884383 | -169.699768 | 533.002333 | 0.817718 | 41.691270 | 0.517994 | -0.148014 | 0.381533 | 0.526645 | 0.724458 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 390 | -30.645129 | -13.312009 | 17.311294 | -0.021826 | 39.743590 | 0.329988 | -0.078577 | 0.097375 | 0.194631 | 0.500305 |
| AVAX | SHORT | 928 | -77.955406 | -1.633066 | 76.307410 | -0.014930 | 43.750000 | 0.583705 | -0.084004 | 0.269223 | 0.358736 | 0.750478 |
| BTC | LONG | 538 | -51.779292 | -4.752939 | 46.969177 | -0.057176 | 37.546468 | 0.448037 | -0.096244 | 0.208070 | 0.279195 | 0.745250 |
| BTC | SHORT | 856 | -155.192998 | -50.662211 | 104.688102 | 0.157315 | 36.214953 | 0.431090 | -0.181300 | 0.379345 | 0.499616 | 0.759275 |
| DOGE | LONG | 433 | -21.926206 | -2.227821 | 19.605179 | -0.093206 | 42.725173 | 0.527805 | -0.050638 | 0.132478 | 0.187236 | 0.707544 |
| DOGE | SHORT | 1324 | -164.298780 | -13.680366 | 150.947224 | 0.328810 | 42.371601 | 0.584123 | -0.124093 | 0.411350 | 0.517780 | 0.794449 |
| ETH | LONG | 600 | -52.941199 | 1.923550 | 54.803079 | -0.061671 | 40.000000 | 0.592249 | -0.088235 | 0.320400 | 0.360659 | 0.888374 |
| ETH | SHORT | 685 | -176.373678 | -75.157270 | 101.260578 | 0.044170 | 41.167883 | 0.453712 | -0.257480 | 0.519449 | 0.801138 | 0.648390 |
| SOL | LONG | 721 | -139.604213 | -40.249080 | 99.441726 | 0.086593 | 40.915395 | 0.440541 | -0.193626 | 0.372644 | 0.585761 | 0.636171 |
| SOL | SHORT | 949 | -128.063521 | -28.566856 | 99.799018 | 0.302352 | 44.046365 | 0.539670 | -0.134946 | 0.359177 | 0.523916 | 0.685562 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| stop | 3933 | -1,571.590990 | 419.019208 | 0.173158 | -1,990.437041 |
| stop_gap | 26 | -8.719514 | 3.039833 | 0.005430 | -11.753917 |
| trailing_take_profit | 2936 | 1,190.593024 | 296.394011 | 0.465682 | 894.664695 |
| trailing_take_profit_gap | 529 | 161.399414 | 52.679736 | 0.026162 | 108.745841 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 654.342536 | -345.657464 | -34.565746 | False |
| 2025-12 | 654.342536 | 410.326491 | -244.016044 | -37.291790 | False |
| 2026-01 | 410.326491 | 272.020140 | -138.306351 | -33.706415 | False |
| 2026-02 | 272.020140 | 193.449078 | -78.571062 | -28.884281 | False |
| 2026-03 | 193.449078 | 96.274362 | -97.174716 | -50.232711 | False |
| 2026-04 | 96.274362 | 55.724054 | -40.550308 | -42.119529 | False |
| 2026-05 | 55.724054 | 32.535056 | -23.188998 | -41.613982 | False |
| 2026-06 | 32.535056 | 19.341019 | -13.194037 | -40.553294 | False |
| 2026-07 | 19.341019 | 9.969283 | -9.371736 | -48.455234 | False |
| 2026-08 | 9.969283 | 7.553118 | -2.416165 | -24.236096 | False |
| 2026-09 | 7.553118 | 3.847528 | -3.705590 | -49.060402 | False |
| 2026-10 | 3.847528 | 1.929007 | -1.918520 | -49.863717 | False |
| 2026-11 | 1.929007 | 1.219578 | -0.709429 | -36.776912 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
