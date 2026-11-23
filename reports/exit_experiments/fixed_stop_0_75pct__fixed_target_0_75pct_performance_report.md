# Performance report: fixed_stop_0_75pct__fixed_target_0_75pct

## Run metadata
- Experiment Id: fixed_stop_0_75pct__fixed_target_0_75pct
- Stop Model: fixed_stop_0_75pct
- Target Model: fixed_target_0_75pct
- Target Value: 0.007500
- Trailing Mode: none
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
- Final Equity: 89.641590
- Net Pnl: -910.358410
- Total Return Pct: -91.035841
- Max Drawdown Amount: 928.938080
- Max Drawdown Pct: 91.204457
- Recovery Factor: -0.979999
- Sharpe Ratio: -6.704409
- Sortino Ratio: -6.899590
- Cagr Pct: -89.220048
- Calmar Ratio: -0.978242
- Worst Daily Loss: -79.451854
- Worst Daily Loss Pct: -9.065692
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 38.520999
- Max Capital Utilization Pct: 101.733307
- Max Gross Exposure: 1,020.410886
- Max Gross Exposure Equity Multiple: 1.017333

## Trade performance

- Trade Count: 4677
- Net Pnl: -910.358410
- Gross Pnl: -37.261354
- Total Fees: 874.417172
- Funding Pnl: 1.320116
- Winning Trades: 2382
- Losing Trades: 2295
- Breakeven Trades: 0
- Win Rate Pct: 50.930083
- Profit Factor: 0.755542
- Expectancy: -0.194646
- Average Win: 1.181201
- Average Loss: 1.622649
- Payoff Ratio: 0.727946
- Max Consecutive Losses: 18
- Average Duration Minutes: 101.217447
- Median Duration Minutes: 45.000000
- Max Duration Minutes: 3,160.000000
- Recovery Factor: -0.979999

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 954 | -96.204918 | 27.199329 | 123.524715 | 0.120468 | 51.467505 | 0.810325 | -0.100844 | 0.837078 | 1.095486 | 0.764115 |
| BTC | 699 | -119.907029 | 11.351942 | 131.422537 | 0.163566 | 52.360515 | 0.781856 | -0.171541 | 1.174211 | 1.650655 | 0.711360 |
| DOGE | 1070 | -259.402243 | -40.777979 | 219.101723 | 0.477460 | 50.093458 | 0.727414 | -0.242432 | 1.291480 | 1.782089 | 0.724700 |
| ETH | 797 | -211.437246 | -35.314944 | 176.067223 | -0.055080 | 49.811794 | 0.723980 | -0.265291 | 1.396940 | 1.915056 | 0.729451 |
| SOL | 1157 | -223.406975 | 0.280298 | 224.300975 | 0.613702 | 51.166811 | 0.764697 | -0.193092 | 1.226414 | 1.680432 | 0.729821 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1630 | -363.149760 | -51.963086 | 310.306614 | -0.880059 | 49.141104 | 0.729731 | -0.222791 | 1.224105 | 1.620818 | 0.755239 |
| SHORT | 3047 | -547.208651 | 14.701732 | 564.110558 | 2.200176 | 51.887102 | 0.770111 | -0.179589 | 1.159464 | 1.623685 | 0.714095 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 295 | -30.453869 | 6.926401 | 37.257408 | -0.122862 | 49.491525 | 0.801785 | -0.103233 | 0.843742 | 1.031142 | 0.818260 |
| AVAX | SHORT | 659 | -65.751049 | 20.272928 | 86.267307 | 0.243330 | 52.352049 | 0.814037 | -0.099774 | 0.834258 | 1.126019 | 0.740891 |
| BTC | LONG | 259 | -33.495283 | 19.300076 | 52.365308 | -0.430051 | 52.509653 | 0.840946 | -0.129325 | 1.302168 | 1.712115 | 0.760561 |
| BTC | SHORT | 440 | -86.411745 | -7.948134 | 79.057229 | 0.593617 | 52.272727 | 0.745157 | -0.196390 | 1.098550 | 1.614658 | 0.680361 |
| DOGE | LONG | 261 | -64.947469 | -20.292159 | 44.291913 | -0.363396 | 46.743295 | 0.674348 | -0.248841 | 1.102383 | 1.434807 | 0.768314 |
| DOGE | SHORT | 809 | -194.454774 | -20.485820 | 174.809811 | 0.840856 | 51.174289 | 0.741484 | -0.240364 | 1.347204 | 1.904297 | 0.707455 |
| ETH | LONG | 331 | -81.159624 | -12.412604 | 68.465935 | -0.281085 | 48.640483 | 0.726788 | -0.245195 | 1.340981 | 1.747397 | 0.767416 |
| ETH | SHORT | 466 | -130.277622 | -22.902340 | 107.601288 | 0.226006 | 50.643777 | 0.722202 | -0.279566 | 1.435115 | 2.038977 | 0.703841 |
| SOL | LONG | 484 | -153.093515 | -45.484800 | 107.926051 | 0.317336 | 48.760331 | 0.682992 | -0.316309 | 1.397621 | 1.947307 | 0.717720 |
| SOL | SHORT | 673 | -70.313460 | 45.765098 | 116.374924 | 0.296366 | 52.897474 | 0.849278 | -0.104478 | 1.112917 | 1.471646 | 0.756239 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | -0.271177 | 0.052230 | -0.000289 | -0.323696 |
| stop | 2293 | -3,293.905043 | 428.216168 | 0.680365 | -3,721.440846 |
| stop_gap | 1 | -1.940316 | 0.249961 | -0.025098 | -2.215376 |
| target | 2380 | 3,258.380375 | 445.834021 | 0.665139 | 2,813.211492 |
| target_gap | 2 | 0.474807 | 0.064791 | 0.000000 | 0.410016 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 921.270011 | -78.729989 | -7.872999 | False |
| 2025-12 | 921.270011 | 718.988845 | -202.281166 | -21.956773 | False |
| 2026-01 | 718.988845 | 668.199870 | -50.788975 | -7.063945 | False |
| 2026-02 | 668.199870 | 554.311527 | -113.888344 | -17.044054 | False |
| 2026-03 | 554.311527 | 403.384361 | -150.927166 | -27.227860 | False |
| 2026-04 | 403.384361 | 345.158651 | -58.225710 | -14.434300 | False |
| 2026-05 | 345.158651 | 280.063674 | -65.094977 | -18.859437 | False |
| 2026-06 | 280.063674 | 244.438327 | -35.625347 | -12.720446 | False |
| 2026-07 | 244.438327 | 195.900981 | -48.537345 | -19.856684 | False |
| 2026-08 | 195.900981 | 178.687315 | -17.213667 | -8.786922 | False |
| 2026-09 | 178.687315 | 126.063013 | -52.624301 | -29.450496 | False |
| 2026-10 | 126.063013 | 103.532416 | -22.530598 | -17.872489 | False |
| 2026-11 | 103.532416 | 89.641590 | -13.890826 | -13.416886 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
