# Performance report: fixed_stop_0_50pct__fixed_target_1_00pct__trailing_tp

## Run metadata
- Experiment Id: fixed_stop_0_50pct__fixed_target_1_00pct__trailing_tp
- Stop Model: fixed_stop_0_50pct
- Target Model: fixed_target_1_00pct
- Target Value: 0.010000
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
- Final Equity: 37.588892
- Net Pnl: -962.411108
- Total Return Pct: -96.241111
- Max Drawdown Amount: 1,007.193155
- Max Drawdown Pct: 96.405278
- Recovery Factor: -0.955538
- Sharpe Ratio: -7.503873
- Sortino Ratio: -7.476577
- Cagr Pct: -95.169051
- Calmar Ratio: -0.987177
- Worst Daily Loss: -66.035345
- Worst Daily Loss Pct: -6.381533
- Worst Daily Loss Date Utc: 2025-11-18
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 42.190684
- Max Capital Utilization Pct: 101.667171
- Max Gross Exposure: 1,045.325061
- Max Gross Exposure Equity Multiple: 1.016672

## Trade performance

- Trade Count: 4897
- Net Pnl: -962.411108
- Gross Pnl: -68.282492
- Total Fees: 895.240176
- Funding Pnl: 1.111560
- Winning Trades: 1661
- Losing Trades: 3236
- Breakeven Trades: 0
- Win Rate Pct: 33.918726
- Profit Factor: 0.737701
- Expectancy: -0.196531
- Average Win: 1.629577
- Average Loss: 1.133850
- Payoff Ratio: 1.437207
- Max Consecutive Losses: 32
- Average Duration Minutes: 94.502961
- Median Duration Minutes: 37.000000
- Max Duration Minutes: 3,366.000000
- Recovery Factor: -0.955538

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 982 | -123.737977 | -9.021701 | 114.709168 | -0.007107 | 31.975560 | 0.739661 | -0.126006 | 1.119611 | 0.711521 | 1.573547 |
| BTC | 718 | -114.498657 | 13.415247 | 128.076450 | 0.162546 | 36.072423 | 0.776920 | -0.159469 | 1.539633 | 1.118221 | 1.376859 |
| DOGE | 1123 | -215.527808 | 13.691798 | 229.798530 | 0.578924 | 35.262689 | 0.767568 | -0.191921 | 1.797332 | 1.275476 | 1.409146 |
| ETH | 852 | -246.759612 | -61.461860 | 185.159302 | -0.138450 | 32.981221 | 0.680768 | -0.289624 | 1.872665 | 1.353728 | 1.383340 |
| SOL | 1222 | -261.887054 | -24.905975 | 237.496727 | 0.515647 | 33.633388 | 0.732858 | -0.214310 | 1.748036 | 1.208792 | 1.446102 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1665 | -367.894845 | -52.994434 | 314.069308 | -0.831103 | 32.552553 | 0.716749 | -0.220958 | 1.717591 | 1.156571 | 1.485072 |
| SHORT | 3232 | -594.516263 | -15.288058 | 581.170868 | 1.942663 | 34.622525 | 0.749182 | -0.183947 | 1.586947 | 1.121775 | 1.414675 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 301 | -59.014215 | -25.403662 | 33.486825 | -0.123727 | 28.239203 | 0.601121 | -0.196061 | 1.046305 | 0.684955 | 1.527555 |
| AVAX | SHORT | 681 | -64.723762 | 16.381961 | 81.222343 | 0.116620 | 33.627019 | 0.802277 | -0.095042 | 1.146820 | 0.724216 | 1.583534 |
| BTC | LONG | 257 | -14.010431 | 35.103975 | 48.865657 | -0.248749 | 37.354086 | 0.923426 | -0.054515 | 1.759958 | 1.136437 | 1.548663 |
| BTC | SHORT | 461 | -100.488226 | -21.688728 | 79.210793 | 0.411295 | 35.357918 | 0.695764 | -0.217979 | 1.409871 | 1.108380 | 1.272011 |
| DOGE | LONG | 247 | -53.666688 | -11.123960 | 42.235447 | -0.307280 | 32.793522 | 0.694863 | -0.217274 | 1.508774 | 1.059502 | 1.424040 |
| DOGE | SHORT | 876 | -161.861120 | 24.815758 | 187.563083 | 0.886205 | 35.958904 | 0.784586 | -0.184773 | 1.871532 | 1.339383 | 1.397309 |
| ETH | LONG | 357 | -98.852109 | -27.923289 | 70.569274 | -0.359546 | 32.212885 | 0.662723 | -0.276897 | 1.689016 | 1.211111 | 1.394600 |
| ETH | SHORT | 495 | -147.907503 | -33.538571 | 114.590028 | 0.221096 | 33.535354 | 0.691789 | -0.298803 | 1.999893 | 1.458631 | 1.371075 |
| SOL | LONG | 503 | -142.351403 | -23.647497 | 118.912104 | 0.208199 | 32.803181 | 0.714696 | -0.283005 | 2.161182 | 1.476173 | 1.464044 |
| SOL | SHORT | 719 | -119.535652 | -1.258478 | 118.584622 | 0.307448 | 34.214186 | 0.751683 | -0.166253 | 1.470927 | 1.017724 | 1.445309 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | 0.001774 | 0.030392 | 0.000000 | -0.028618 |
| stop | 3223 | -3,073.005137 | 591.378443 | 0.520590 | -3,663.862990 |
| stop_gap | 10 | -4.387840 | 0.833975 | 0.016076 | -5.205738 |
| trailing_take_profit | 1356 | 2,445.420815 | 247.382362 | 0.743506 | 2,198.781959 |
| trailing_take_profit_gap | 307 | 563.687896 | 55.615005 | -0.168612 | 507.904279 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 928.354132 | -71.645868 | -7.164587 | False |
| 2025-12 | 928.354132 | 734.362691 | -193.991441 | -20.896276 | False |
| 2026-01 | 734.362691 | 643.773844 | -90.588848 | -12.335709 | False |
| 2026-02 | 643.773844 | 470.990496 | -172.783347 | -26.839138 | False |
| 2026-03 | 470.990496 | 323.297851 | -147.692645 | -31.357882 | False |
| 2026-04 | 323.297851 | 254.383068 | -68.914783 | -21.316190 | False |
| 2026-05 | 254.383068 | 197.492092 | -56.890975 | -22.364293 | False |
| 2026-06 | 197.492092 | 170.356221 | -27.135872 | -13.740232 | False |
| 2026-07 | 170.356221 | 128.123731 | -42.232490 | -24.790694 | False |
| 2026-08 | 128.123731 | 112.399258 | -15.724473 | -12.272881 | False |
| 2026-09 | 112.399258 | 58.662108 | -53.737150 | -47.809168 | False |
| 2026-10 | 58.662108 | 45.170611 | -13.491497 | -22.998657 | False |
| 2026-11 | 45.170611 | 37.588892 | -7.581719 | -16.784628 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
