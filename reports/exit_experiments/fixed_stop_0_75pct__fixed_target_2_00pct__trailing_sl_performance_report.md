# Performance report: fixed_stop_0_75pct__fixed_target_2_00pct__trailing_sl

## Run metadata
- Experiment Id: fixed_stop_0_75pct__fixed_target_2_00pct__trailing_sl
- Stop Model: fixed_stop_0_75pct
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
- Final Equity: 146.702304
- Net Pnl: -853.297696
- Total Return Pct: -85.329770
- Max Drawdown Amount: 932.610091
- Max Drawdown Pct: 86.520294
- Recovery Factor: -0.914957
- Sharpe Ratio: -4.931869
- Sortino Ratio: -5.535472
- Cagr Pct: -83.010366
- Calmar Ratio: -0.959432
- Worst Daily Loss: -72.163255
- Worst Daily Loss Pct: -7.416476
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 39.754524
- Max Capital Utilization Pct: 101.733307
- Max Gross Exposure: 1,079.495502
- Max Gross Exposure Equity Multiple: 1.017333

## Trade performance

- Trade Count: 3810
- Net Pnl: -853.297696
- Gross Pnl: 37.811006
- Total Fees: 892.452212
- Funding Pnl: 1.343510
- Winning Trades: 1668
- Losing Trades: 2142
- Breakeven Trades: 0
- Win Rate Pct: 43.779528
- Profit Factor: 0.778428
- Expectancy: -0.223963
- Average Win: 1.797246
- Average Loss: 1.797901
- Payoff Ratio: 0.999636
- Max Consecutive Losses: 23
- Average Duration Minutes: 132.295538
- Median Duration Minutes: 65.000000
- Max Duration Minutes: 3,360.000000
- Recovery Factor: -0.914957

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 776 | -124.605163 | 9.186534 | 133.837384 | 0.045687 | 42.912371 | 0.782172 | -0.160574 | 1.343629 | 1.291273 | 1.040547 |
| BTC | 544 | -92.388754 | 32.599535 | 125.236153 | 0.247864 | 45.404412 | 0.825996 | -0.169832 | 1.775584 | 1.787737 | 0.993202 |
| DOGE | 889 | -240.536486 | -16.410581 | 224.755844 | 0.629938 | 44.544432 | 0.750657 | -0.270570 | 1.828646 | 1.956755 | 0.934530 |
| ETH | 676 | -203.091748 | -19.315074 | 183.779851 | 0.003177 | 43.786982 | 0.746977 | -0.300432 | 2.025570 | 2.112265 | 0.958957 |
| SOL | 925 | -192.675545 | 31.750593 | 224.842981 | 0.416844 | 42.810811 | 0.803547 | -0.208298 | 1.990141 | 1.854010 | 1.073425 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1274 | -402.248216 | -75.566140 | 325.306297 | -1.375779 | 41.208791 | 0.721571 | -0.315736 | 1.985639 | 1.928850 | 1.029442 |
| SHORT | 2536 | -451.049480 | 113.377146 | 567.145915 | 2.719289 | 45.070978 | 0.812562 | -0.177859 | 1.710714 | 1.727491 | 0.990288 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 229 | -63.621932 | -22.282150 | 41.136023 | -0.203759 | 36.244541 | 0.655864 | -0.277825 | 1.460875 | 1.266264 | 1.153689 |
| AVAX | SHORT | 547 | -60.983232 | 31.468683 | 92.701360 | 0.249446 | 45.703839 | 0.842485 | -0.111487 | 1.304704 | 1.303566 | 1.000873 |
| BTC | LONG | 204 | -36.534482 | 16.895002 | 52.980100 | -0.449384 | 44.607843 | 0.829491 | -0.179091 | 1.953110 | 1.896172 | 1.030028 |
| BTC | SHORT | 340 | -55.854272 | 15.704533 | 72.256053 | 0.697248 | 45.882353 | 0.823631 | -0.164277 | 1.672027 | 1.721144 | 0.971463 |
| DOGE | LONG | 204 | -67.337852 | -18.061513 | 48.769323 | -0.507016 | 43.137255 | 0.697016 | -0.330088 | 1.760349 | 1.915936 | 0.918793 |
| DOGE | SHORT | 685 | -173.198634 | 1.650932 | 175.986520 | 1.136955 | 44.963504 | 0.766714 | -0.252845 | 1.848159 | 1.969315 | 0.938478 |
| ETH | LONG | 268 | -61.540059 | 12.631643 | 73.732795 | -0.438907 | 43.656716 | 0.804101 | -0.229627 | 2.158983 | 2.080405 | 1.037771 |
| ETH | SHORT | 408 | -141.551689 | -31.946717 | 110.047056 | 0.442084 | 43.872549 | 0.710243 | -0.346940 | 1.938367 | 2.133273 | 0.908636 |
| SOL | LONG | 369 | -173.213891 | -64.749123 | 108.688055 | 0.223287 | 39.566396 | 0.659816 | -0.469414 | 2.301116 | 2.283304 | 1.007801 |
| SOL | SHORT | 556 | -19.461654 | 96.499716 | 116.154926 | 0.193556 | 44.964029 | 0.958732 | -0.035003 | 1.808532 | 1.541159 | 1.173488 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | -0.443793 | 0.085477 | -0.000472 | -0.529743 |
| stop | 3406 | -1,774.246718 | 798.069041 | 1.260727 | -2,571.055031 |
| stop_gap | 20 | 17.343527 | 3.868750 | -0.035925 | 13.438852 |
| target | 383 | 1,795.157990 | 90.428944 | 0.119180 | 1,704.848226 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 1,019.207958 | 19.207958 | 1.920796 | False |
| 2025-12 | 1,019.207958 | 860.527173 | -158.680785 | -15.569029 | False |
| 2026-01 | 860.527173 | 798.298713 | -62.228460 | -7.231435 | False |
| 2026-02 | 798.298713 | 715.973098 | -82.325615 | -10.312633 | False |
| 2026-03 | 715.973098 | 544.369342 | -171.603756 | -23.967906 | False |
| 2026-04 | 544.369342 | 494.305697 | -50.063645 | -9.196632 | False |
| 2026-05 | 494.305697 | 399.967085 | -94.338612 | -19.085075 | False |
| 2026-06 | 399.967085 | 368.568224 | -31.398861 | -7.850361 | False |
| 2026-07 | 368.568224 | 304.754156 | -63.814068 | -17.314045 | False |
| 2026-08 | 304.754156 | 287.597534 | -17.156622 | -5.629660 | False |
| 2026-09 | 287.597534 | 199.924995 | -87.672539 | -30.484454 | False |
| 2026-10 | 199.924995 | 163.372037 | -36.552959 | -18.283336 | False |
| 2026-11 | 163.372037 | 146.702304 | -16.669733 | -10.203541 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
