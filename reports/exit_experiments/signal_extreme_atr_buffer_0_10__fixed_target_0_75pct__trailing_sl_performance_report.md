# Performance report: signal_extreme_atr_buffer_0_10__fixed_target_0_75pct__trailing_sl

## Run metadata
- Experiment Id: signal_extreme_atr_buffer_0_10__fixed_target_0_75pct__trailing_sl
- Stop Model: signal_extreme_atr_buffer_0_10
- Target Model: fixed_target_0_75pct
- Target Value: 0.007500
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
- Final Equity: 4.059206
- Net Pnl: -995.940794
- Total Return Pct: -99.594079
- Max Drawdown Amount: 1,007.567011
- Max Drawdown Pct: 99.598744
- Recovery Factor: -0.988461
- Sharpe Ratio: -12.832377
- Sortino Ratio: -10.908889
- Cagr Pct: -99.381504
- Calmar Ratio: -0.997819
- Worst Daily Loss: -56.867232
- Worst Daily Loss Pct: -8.212038
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 33.180728
- Max Capital Utilization Pct: 102.187501
- Max Gross Exposure: 1,007.279925
- Max Gross Exposure Equity Multiple: 1.021875

## Trade performance

- Trade Count: 7082
- Net Pnl: -995.940794
- Gross Pnl: -184.060219
- Total Fees: 812.595597
- Funding Pnl: 0.715021
- Winning Trades: 2693
- Losing Trades: 4389
- Breakeven Trades: 0
- Win Rate Pct: 38.025981
- Profit Factor: 0.568910
- Expectancy: -0.140630
- Average Win: 0.488059
- Average Loss: 0.526381
- Payoff Ratio: 0.927199
- Max Consecutive Losses: 23
- Average Duration Minutes: 45.788901
- Median Duration Minutes: 22.000000
- Max Duration Minutes: 1,808.000000
- Recovery Factor: -0.988461

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1317 | -119.753074 | -23.097941 | 96.740534 | 0.085401 | 39.179954 | 0.558108 | -0.090929 | 0.293116 | 0.338328 | 0.866366 |
| BTC | 1304 | -192.653563 | -31.481528 | 161.212926 | 0.040891 | 34.585890 | 0.536526 | -0.147740 | 0.494500 | 0.487307 | 1.014760 |
| DOGE | 1611 | -204.515681 | -19.215787 | 185.603127 | 0.303233 | 38.050900 | 0.614474 | -0.126950 | 0.531760 | 0.531548 | 1.000399 |
| ETH | 1210 | -210.984782 | -45.481560 | 165.372579 | -0.130644 | 37.933884 | 0.568444 | -0.174368 | 0.605465 | 0.650989 | 0.930068 |
| SOL | 1640 | -268.033694 | -64.783404 | 203.666431 | 0.416140 | 39.878049 | 0.556407 | -0.163435 | 0.514067 | 0.612813 | 0.838864 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2472 | -329.429737 | -54.719984 | 274.354770 | -0.354982 | 36.488673 | 0.541208 | -0.133264 | 0.430829 | 0.457349 | 0.942014 |
| SHORT | 4610 | -666.511057 | -129.340235 | 538.240826 | 1.070004 | 38.850325 | 0.581402 | -0.144579 | 0.516882 | 0.564827 | 0.915116 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 368 | -39.002266 | -17.230892 | 21.743799 | -0.027575 | 37.500000 | 0.371044 | -0.105984 | 0.166731 | 0.269614 | 0.618407 |
| AVAX | SHORT | 949 | -80.750807 | -5.867049 | 74.996735 | 0.112976 | 39.831401 | 0.613614 | -0.085090 | 0.339257 | 0.366007 | 0.926914 |
| BTC | LONG | 508 | -52.605353 | 6.866052 | 59.375057 | -0.096347 | 35.039370 | 0.587127 | -0.103554 | 0.420267 | 0.386099 | 1.088493 |
| BTC | SHORT | 796 | -140.048210 | -38.347579 | 101.837869 | 0.137238 | 34.296482 | 0.514160 | -0.175940 | 0.542901 | 0.551167 | 0.985003 |
| DOGE | LONG | 381 | -26.351612 | -0.091131 | 26.143402 | -0.117078 | 36.482940 | 0.602393 | -0.069164 | 0.287223 | 0.273866 | 1.048771 |
| DOGE | SHORT | 1230 | -178.164069 | -19.124656 | 159.459725 | 0.420312 | 38.536585 | 0.616198 | -0.144849 | 0.603470 | 0.614033 | 0.982798 |
| ETH | LONG | 537 | -64.588151 | 1.479725 | 65.883105 | -0.184772 | 36.126629 | 0.618923 | -0.120276 | 0.540722 | 0.494135 | 1.094281 |
| ETH | SHORT | 673 | -146.396631 | -46.961285 | 99.489474 | 0.054127 | 39.375929 | 0.541658 | -0.217528 | 0.652861 | 0.782855 | 0.833949 |
| SOL | LONG | 678 | -146.882355 | -45.743737 | 101.209408 | 0.070790 | 37.315634 | 0.498438 | -0.216641 | 0.576946 | 0.689058 | 0.837297 |
| SOL | SHORT | 962 | -121.151340 | -19.039666 | 102.457023 | 0.345350 | 41.683992 | 0.610926 | -0.125937 | 0.474395 | 0.555051 | 0.854687 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| stop | 5190 | -1,541.795953 | 620.320108 | 0.591122 | -2,161.524939 |
| stop_gap | 67 | 6.405573 | 7.469581 | 0.000000 | -1.064008 |
| target | 1824 | 1,351.275118 | 184.798396 | 0.123900 | 1,166.600622 |
| target_gap | 1 | 0.055043 | 0.007511 | 0.000000 | 0.047532 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 755.132819 | -244.867181 | -24.486718 | False |
| 2025-12 | 755.132819 | 493.681405 | -261.451414 | -34.623235 | False |
| 2026-01 | 493.681405 | 363.855479 | -129.825926 | -26.297512 | False |
| 2026-02 | 363.855479 | 264.641210 | -99.214269 | -27.267493 | False |
| 2026-03 | 264.641210 | 143.148070 | -121.493140 | -45.908625 | False |
| 2026-04 | 143.148070 | 89.104010 | -54.044061 | -37.753957 | False |
| 2026-05 | 89.104010 | 56.657533 | -32.446476 | -36.414159 | False |
| 2026-06 | 56.657533 | 35.286651 | -21.370882 | -37.719401 | False |
| 2026-07 | 35.286651 | 22.173920 | -13.112731 | -37.160600 | False |
| 2026-08 | 22.173920 | 17.184450 | -4.989470 | -22.501525 | False |
| 2026-09 | 17.184450 | 10.247075 | -6.937375 | -40.370073 | False |
| 2026-10 | 10.247075 | 6.027785 | -4.219289 | -41.175551 | False |
| 2026-11 | 6.027785 | 4.059206 | -1.968579 | -32.658419 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
