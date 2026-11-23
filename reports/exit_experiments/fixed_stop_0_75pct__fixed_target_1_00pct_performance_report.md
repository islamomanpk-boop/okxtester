# Performance report: fixed_stop_0_75pct__fixed_target_1_00pct

## Run metadata
- Experiment Id: fixed_stop_0_75pct__fixed_target_1_00pct
- Stop Model: fixed_stop_0_75pct
- Target Model: fixed_target_1_00pct
- Target Value: 0.010000
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
- Final Equity: 147.209029
- Net Pnl: -852.790971
- Total Return Pct: -85.279097
- Max Drawdown Amount: 884.595177
- Max Drawdown Pct: 86.516183
- Recovery Factor: -0.964047
- Sharpe Ratio: -4.966917
- Sortino Ratio: -5.552214
- Cagr Pct: -82.956177
- Calmar Ratio: -0.958852
- Worst Daily Loss: -78.675365
- Worst Daily Loss Pct: -8.760314
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 40.732447
- Max Capital Utilization Pct: 102.156602
- Max Gross Exposure: 1,021.827630
- Max Gross Exposure Equity Multiple: 1.021566

## Trade performance

- Trade Count: 3909
- Net Pnl: -852.790971
- Gross Pnl: -27.928521
- Total Fees: 826.201465
- Funding Pnl: 1.339015
- Winning Trades: 1727
- Losing Trades: 2182
- Breakeven Trades: 0
- Win Rate Pct: 44.180097
- Profit Factor: 0.788879
- Expectancy: -0.218161
- Average Win: 1.845144
- Average Loss: 1.851217
- Payoff Ratio: 0.996720
- Max Consecutive Losses: 21
- Average Duration Minutes: 130.663341
- Median Duration Minutes: 57.000000
- Max Duration Minutes: 3,471.000000
- Recovery Factor: -0.964047

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 813 | -115.257403 | 10.518227 | 125.800753 | 0.025124 | 44.034440 | 0.810426 | -0.141768 | 1.376320 | 1.336219 | 1.030010 |
| BTC | 568 | -84.865447 | 35.089118 | 120.326491 | 0.371926 | 45.774648 | 0.850743 | -0.149411 | 1.860464 | 1.846059 | 1.007803 |
| DOGE | 892 | -245.481574 | -43.800379 | 202.281311 | 0.600115 | 44.506726 | 0.756336 | -0.275204 | 1.919339 | 2.035271 | 0.943038 |
| ETH | 686 | -218.374299 | -53.212552 | 165.147562 | -0.014185 | 41.982507 | 0.737237 | -0.318330 | 2.127408 | 2.088110 | 1.018820 |
| SOL | 950 | -188.812248 | 23.477065 | 212.645348 | 0.356035 | 44.631579 | 0.815660 | -0.198750 | 1.970400 | 1.947266 | 1.011880 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1292 | -347.578089 | -56.562541 | 289.869737 | -1.145811 | 42.492260 | 0.758681 | -0.269023 | 1.990433 | 1.938528 | 1.026776 |
| SHORT | 2617 | -505.212882 | 28.634020 | 536.331728 | 2.484826 | 45.013374 | 0.805615 | -0.193050 | 1.777433 | 1.806135 | 0.984108 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 237 | -59.370931 | -21.076109 | 38.161064 | -0.133758 | 38.818565 | 0.697743 | -0.250510 | 1.489719 | 1.354655 | 1.099703 |
| AVAX | SHORT | 576 | -55.886471 | 31.594336 | 87.639689 | 0.158882 | 46.180556 | 0.864206 | -0.097025 | 1.337099 | 1.327596 | 1.007158 |
| BTC | LONG | 207 | -37.874446 | 10.606400 | 48.013223 | -0.467623 | 45.893720 | 0.834448 | -0.182968 | 2.009492 | 2.042645 | 0.983770 |
| BTC | SHORT | 361 | -46.991001 | 24.482718 | 72.313268 | 0.839549 | 45.706371 | 0.861714 | -0.130169 | 1.774660 | 1.733724 | 1.023612 |
| DOGE | LONG | 192 | -48.726244 | -7.267544 | 41.048192 | -0.410509 | 42.187500 | 0.760900 | -0.253783 | 1.914373 | 1.835950 | 1.042715 |
| DOGE | SHORT | 700 | -196.755330 | -36.532835 | 161.233119 | 1.010623 | 45.142857 | 0.755179 | -0.281079 | 1.920612 | 2.092887 | 0.917685 |
| ETH | LONG | 272 | -81.469858 | -16.976929 | 64.099254 | -0.393676 | 42.647059 | 0.746019 | -0.299522 | 2.062942 | 2.056225 | 1.003267 |
| ETH | SHORT | 414 | -136.904441 | -36.235623 | 101.048308 | 0.379491 | 41.545894 | 0.731716 | -0.330687 | 2.170886 | 2.108664 | 1.029507 |
| SOL | LONG | 384 | -120.136609 | -21.848359 | 98.548004 | 0.259754 | 42.968750 | 0.755105 | -0.312856 | 2.245009 | 2.240014 | 1.002230 |
| SOL | SHORT | 566 | -68.675639 | 45.325424 | 114.097344 | 0.096281 | 45.759717 | 0.871321 | -0.121335 | 1.795455 | 1.738432 | 1.032802 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | -0.445326 | 0.085773 | -0.000474 | -0.531572 |
| stop | 2179 | -3,573.616931 | 464.592329 | 0.618456 | -4,037.590803 |
| stop_gap | 2 | -1.092170 | 0.140154 | 0.000000 | -1.232324 |
| target | 1724 | 3,544.297948 | 361.085964 | 0.721032 | 3,183.933016 |
| target_gap | 3 | 2.927959 | 0.297246 | 0.000000 | 2.630712 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 941.965536 | -58.034464 | -5.803446 | False |
| 2025-12 | 941.965536 | 731.118481 | -210.847054 | -22.383733 | False |
| 2026-01 | 731.118481 | 697.594265 | -33.524217 | -4.585333 | False |
| 2026-02 | 697.594265 | 611.842047 | -85.752218 | -12.292564 | False |
| 2026-03 | 611.842047 | 478.310939 | -133.531108 | -21.824441 | False |
| 2026-04 | 478.310939 | 432.851332 | -45.459607 | -9.504196 | False |
| 2026-05 | 432.851332 | 358.150481 | -74.700851 | -17.257854 | False |
| 2026-06 | 358.150481 | 333.617000 | -24.533481 | -6.850048 | False |
| 2026-07 | 333.617000 | 268.895484 | -64.721516 | -19.399945 | False |
| 2026-08 | 268.895484 | 261.678326 | -7.217158 | -2.684001 | False |
| 2026-09 | 261.678326 | 178.786618 | -82.891709 | -31.676949 | False |
| 2026-10 | 178.786618 | 153.537878 | -25.248740 | -14.122276 | False |
| 2026-11 | 153.537878 | 147.209029 | -6.328849 | -4.122011 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
