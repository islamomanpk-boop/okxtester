# Performance report: signal_extreme_exact__target_2R__trailing_sl

## Run metadata
- Experiment Id: signal_extreme_exact__target_2R__trailing_sl
- Stop Model: signal_extreme_exact
- Target Model: target_2R
- Target Value: 2.000000
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
- Final Equity: 3.094683
- Net Pnl: -996.905317
- Total Return Pct: -99.690532
- Max Drawdown Amount: 1,017.826947
- Max Drawdown Pct: 99.696874
- Recovery Factor: -0.979445
- Sharpe Ratio: -12.915411
- Sortino Ratio: -11.027819
- Cagr Pct: -99.518582
- Calmar Ratio: -0.998212
- Worst Daily Loss: -60.562618
- Worst Daily Loss Pct: -6.258846
- Worst Daily Loss Date Utc: 2025-11-18
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 32.500721
- Max Capital Utilization Pct: 102.362168
- Max Gross Exposure: 1,017.667984
- Max Gross Exposure Equity Multiple: 1.023622

## Trade performance

- Trade Count: 6872
- Net Pnl: -996.905317
- Gross Pnl: -111.095132
- Total Fees: 886.519726
- Funding Pnl: 0.709541
- Winning Trades: 2265
- Losing Trades: 4607
- Breakeven Trades: 0
- Win Rate Pct: 32.959837
- Profit Factor: 0.563974
- Expectancy: -0.145068
- Average Win: 0.569289
- Average Loss: 0.496276
- Payoff Ratio: 1.147121
- Max Consecutive Losses: 25
- Average Duration Minutes: 49.904249
- Median Duration Minutes: 19.000000
- Max Duration Minutes: 4,748.000000
- Recovery Factor: -0.979445

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1235 | -128.410525 | -20.749479 | 107.658824 | -0.002222 | 33.846154 | 0.526297 | -0.103976 | 0.341310 | 0.331797 | 1.028672 |
| BTC | 1294 | -185.081109 | -12.113866 | 172.960368 | -0.006875 | 31.607419 | 0.537483 | -0.143030 | 0.525866 | 0.452159 | 1.163012 |
| DOGE | 1618 | -184.740836 | 13.375526 | 198.405520 | 0.289157 | 33.621755 | 0.636510 | -0.114179 | 0.594671 | 0.473223 | 1.256639 |
| ETH | 1184 | -234.074848 | -50.088997 | 183.996412 | 0.010561 | 32.685811 | 0.545832 | -0.197698 | 0.726919 | 0.646666 | 1.124104 |
| SOL | 1541 | -264.598000 | -41.518317 | 223.498602 | 0.418919 | 32.900714 | 0.552645 | -0.171705 | 0.644723 | 0.572024 | 1.127091 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2428 | -346.715508 | -50.522580 | 295.946249 | -0.246679 | 31.507414 | 0.509173 | -0.142799 | 0.470164 | 0.424769 | 1.106870 |
| SHORT | 4444 | -650.189809 | -60.572552 | 590.573477 | 0.956220 | 33.753375 | 0.588476 | -0.146307 | 0.619843 | 0.536669 | 1.154981 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 359 | -43.571726 | -18.855867 | 24.695227 | -0.020632 | 30.640669 | 0.315751 | -0.121370 | 0.182785 | 0.255735 | 0.714744 |
| AVAX | SHORT | 876 | -84.838799 | -1.893612 | 82.963597 | 0.018410 | 35.159817 | 0.590941 | -0.096848 | 0.397926 | 0.365141 | 1.089788 |
| BTC | LONG | 500 | -54.246233 | 5.471404 | 59.631161 | -0.086476 | 32.200000 | 0.531431 | -0.108492 | 0.382135 | 0.341505 | 1.118976 |
| BTC | SHORT | 794 | -130.834876 | -17.585270 | 113.329207 | 0.079601 | 31.234257 | 0.539946 | -0.164779 | 0.619175 | 0.520861 | 1.188752 |
| DOGE | LONG | 393 | -34.760990 | -6.071643 | 28.560722 | -0.128624 | 32.824427 | 0.506369 | -0.088450 | 0.276418 | 0.266738 | 1.036289 |
| DOGE | SHORT | 1225 | -149.979847 | 19.447169 | 169.844798 | 0.417781 | 33.877551 | 0.657442 | -0.122433 | 0.693597 | 0.540522 | 1.283199 |
| ETH | LONG | 538 | -64.265310 | 4.898599 | 69.038693 | -0.125216 | 31.412639 | 0.613982 | -0.119452 | 0.604837 | 0.451173 | 1.340588 |
| ETH | SHORT | 646 | -169.809538 | -54.987597 | 114.957719 | 0.135777 | 33.746130 | 0.513314 | -0.262863 | 0.821561 | 0.815210 | 1.007791 |
| SOL | LONG | 638 | -149.871250 | -35.965073 | 114.020446 | 0.114269 | 30.721003 | 0.483276 | -0.234908 | 0.715153 | 0.656202 | 1.089837 |
| SOL | SHORT | 903 | -114.726750 | -5.553244 | 109.478156 | 0.304650 | 34.440753 | 0.619393 | -0.127051 | 0.600336 | 0.509175 | 1.179038 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| stop | 5487 | -1,382.361846 | 701.512128 | 0.334737 | -2,083.539237 |
| stop_gap | 81 | -8.108397 | 12.710249 | 0.003165 | -20.815480 |
| target | 1300 | 1,278.598383 | 172.075166 | 0.371639 | 1,106.894855 |
| target_gap | 4 | 0.776728 | 0.222183 | 0.000000 | 0.554545 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 738.389463 | -261.610537 | -26.161054 | False |
| 2025-12 | 738.389463 | 484.027490 | -254.361973 | -34.448213 | False |
| 2026-01 | 484.027490 | 360.469233 | -123.558256 | -25.527115 | False |
| 2026-02 | 360.469233 | 267.910745 | -92.558489 | -25.677223 | False |
| 2026-03 | 267.910745 | 144.879642 | -123.031103 | -45.922422 | False |
| 2026-04 | 144.879642 | 91.019968 | -53.859674 | -37.175460 | False |
| 2026-05 | 91.019968 | 54.380106 | -36.639862 | -40.254752 | False |
| 2026-06 | 54.380106 | 35.245620 | -19.134485 | -35.186554 | False |
| 2026-07 | 35.245620 | 20.224701 | -15.020919 | -42.617832 | False |
| 2026-08 | 20.224701 | 15.486585 | -4.738117 | -23.427375 | False |
| 2026-09 | 15.486585 | 8.766288 | -6.720297 | -43.394312 | False |
| 2026-10 | 8.766288 | 4.897194 | -3.869093 | -44.136054 | False |
| 2026-11 | 4.897194 | 3.094683 | -1.802511 | -36.807020 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
