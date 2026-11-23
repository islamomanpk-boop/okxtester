# Performance report: fixed_stop_0_50pct__fixed_target_1_50pct__trailing_tp

## Run metadata
- Experiment Id: fixed_stop_0_50pct__fixed_target_1_50pct__trailing_tp
- Stop Model: fixed_stop_0_50pct
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
- Final Equity: 116.574438
- Net Pnl: -883.425562
- Total Return Pct: -88.342556
- Max Drawdown Amount: 945.543991
- Max Drawdown Pct: 89.674688
- Recovery Factor: -0.934304
- Sharpe Ratio: -4.983363
- Sortino Ratio: -5.467454
- Cagr Pct: -86.260047
- Calmar Ratio: -0.961922
- Worst Daily Loss: -81.230867
- Worst Daily Loss Pct: -7.799390
- Worst Daily Loss Date Utc: 2025-11-18
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 45.706781
- Max Capital Utilization Pct: 102.093863
- Max Gross Exposure: 1,055.199641
- Max Gross Exposure Equity Multiple: 1.020939

## Trade performance

- Trade Count: 3884
- Net Pnl: -883.425562
- Gross Pnl: 35.394184
- Total Fees: 920.754151
- Funding Pnl: 1.934405
- Winning Trades: 1029
- Losing Trades: 2855
- Breakeven Trades: 0
- Win Rate Pct: 26.493306
- Profit Factor: 0.791199
- Expectancy: -0.227453
- Average Win: 3.253169
- Average Loss: 1.481939
- Payoff Ratio: 2.195211
- Max Consecutive Losses: 46
- Average Duration Minutes: 134.438208
- Median Duration Minutes: 47.000000
- Max Duration Minutes: 3,753.000000
- Recovery Factor: -0.934304

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 793 | -165.663447 | -23.429854 | 142.182311 | -0.051281 | 24.085750 | 0.751269 | -0.208907 | 2.619745 | 1.106370 | 2.367874 |
| BTC | 564 | -91.107620 | 37.995798 | 129.410564 | 0.307146 | 28.191489 | 0.845289 | -0.161538 | 3.130709 | 1.454050 | 2.153096 |
| DOGE | 865 | -191.525971 | 39.318395 | 231.748649 | 0.904284 | 27.861272 | 0.819447 | -0.221417 | 3.606837 | 1.699958 | 2.121721 |
| ETH | 708 | -209.963230 | -25.076730 | 184.954861 | 0.068361 | 25.706215 | 0.753905 | -0.296558 | 3.534158 | 1.622015 | 2.178869 |
| SOL | 954 | -225.165294 | 6.586576 | 232.457766 | 0.705896 | 26.834382 | 0.787991 | -0.236022 | 3.269111 | 1.521573 | 2.148508 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1276 | -359.854068 | -20.761928 | 337.763716 | -1.328424 | 24.451411 | 0.770596 | -0.282017 | 3.874329 | 1.627225 | 2.380943 |
| SHORT | 2608 | -523.571494 | 56.156113 | 582.990435 | 3.262829 | 27.492331 | 0.803338 | -0.200756 | 2.982874 | 1.407875 | 2.118706 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 243 | -72.239661 | -25.595185 | 46.441273 | -0.203203 | 20.987654 | 0.676310 | -0.297283 | 2.959526 | 1.162372 | 2.546108 |
| AVAX | SHORT | 550 | -93.423786 | 2.165331 | 95.741039 | 0.151922 | 25.454545 | 0.789044 | -0.169861 | 2.495968 | 1.080145 | 2.310772 |
| BTC | LONG | 192 | -24.653132 | 27.157052 | 51.368780 | -0.441405 | 27.604167 | 0.893292 | -0.128402 | 3.893962 | 1.662109 | 2.342784 |
| BTC | SHORT | 372 | -66.454487 | 10.838746 | 78.041784 | 0.748551 | 28.494624 | 0.814299 | -0.178641 | 2.749083 | 1.345328 | 2.043429 |
| DOGE | LONG | 194 | -70.877784 | -17.005770 | 53.235574 | -0.636439 | 24.742268 | 0.718490 | -0.365349 | 3.768740 | 1.724502 | 2.185408 |
| DOGE | SHORT | 671 | -120.648186 | 56.324165 | 178.513075 | 1.540723 | 28.763040 | 0.850867 | -0.179804 | 3.566571 | 1.692461 | 2.107328 |
| ETH | LONG | 277 | -53.738799 | 18.224546 | 71.511506 | -0.451839 | 25.270758 | 0.834731 | -0.194003 | 3.877433 | 1.570817 | 2.468418 |
| ETH | SHORT | 431 | -156.224431 | -43.301276 | 113.443355 | 0.520200 | 25.986079 | 0.704132 | -0.362470 | 3.319611 | 1.655238 | 2.005519 |
| SOL | LONG | 370 | -138.344691 | -23.542571 | 115.206583 | 0.404462 | 24.324324 | 0.742614 | -0.373905 | 4.435057 | 1.919642 | 2.310356 |
| SOL | SHORT | 584 | -86.820603 | 30.129147 | 117.251183 | 0.301433 | 28.424658 | 0.834488 | -0.148665 | 2.636972 | 1.254923 | 2.101301 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | 0.005503 | 0.094255 | 0.000000 | -0.088752 |
| stop | 2846 | -3,543.875505 | 681.939511 | 1.596612 | -4,224.218405 |
| stop_gap | 8 | -5.576296 | 1.060335 | 0.007147 | -6.629485 |
| trailing_take_profit | 802 | 2,764.181400 | 182.609001 | 0.090699 | 2,581.663097 |
| trailing_take_profit_gap | 227 | 820.659083 | 55.051048 | 0.239948 | 765.847983 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 952.786418 | -47.213582 | -4.721358 | False |
| 2025-12 | 952.786418 | 850.718909 | -102.067509 | -10.712528 | False |
| 2026-01 | 850.718909 | 752.632504 | -98.086405 | -11.529825 | False |
| 2026-02 | 752.632504 | 618.463026 | -134.169478 | -17.826692 | False |
| 2026-03 | 618.463026 | 487.004436 | -131.458590 | -21.255691 | False |
| 2026-04 | 487.004436 | 438.273114 | -48.731322 | -10.006340 | False |
| 2026-05 | 438.273114 | 346.074808 | -92.198306 | -21.036724 | False |
| 2026-06 | 346.074808 | 322.386920 | -23.687888 | -6.844730 | False |
| 2026-07 | 322.386920 | 258.235068 | -64.151852 | -19.899025 | False |
| 2026-08 | 258.235068 | 240.374606 | -17.860462 | -6.916358 | False |
| 2026-09 | 240.374606 | 146.472044 | -93.902562 | -39.065093 | False |
| 2026-10 | 146.472044 | 124.125870 | -22.346173 | -15.256272 | False |
| 2026-11 | 124.125870 | 116.574438 | -7.551432 | -6.083689 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
