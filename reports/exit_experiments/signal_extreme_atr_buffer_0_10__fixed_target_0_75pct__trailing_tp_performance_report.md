# Performance report: signal_extreme_atr_buffer_0_10__fixed_target_0_75pct__trailing_tp

## Run metadata
- Experiment Id: signal_extreme_atr_buffer_0_10__fixed_target_0_75pct__trailing_tp
- Stop Model: signal_extreme_atr_buffer_0_10
- Target Model: fixed_target_0_75pct
- Target Value: 0.007500
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
- Final Equity: 14.384839
- Net Pnl: -985.615161
- Total Return Pct: -98.561516
- Max Drawdown Amount: 1,006.115510
- Max Drawdown Pct: 98.592571
- Recovery Factor: -0.979624
- Sharpe Ratio: -10.375327
- Sortino Ratio: -9.504660
- Cagr Pct: -98.010335
- Calmar Ratio: -0.994095
- Worst Daily Loss: -59.955983
- Worst Daily Loss Pct: -7.967751
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 37.821895
- Max Capital Utilization Pct: 102.187501
- Max Gross Exposure: 1,020.902555
- Max Gross Exposure Equity Multiple: 1.021875

## Trade performance

- Trade Count: 5675
- Net Pnl: -985.615161
- Gross Pnl: -155.712802
- Total Fees: 830.777676
- Funding Pnl: 0.875317
- Winning Trades: 2038
- Losing Trades: 3637
- Breakeven Trades: 0
- Win Rate Pct: 35.911894
- Profit Factor: 0.654875
- Expectancy: -0.173677
- Average Win: 0.917667
- Average Loss: 0.785213
- Payoff Ratio: 1.168685
- Max Consecutive Losses: 27
- Average Duration Minutes: 65.535330
- Median Duration Minutes: 32.000000
- Max Duration Minutes: 1,587.000000
- Recovery Factor: -0.979624

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1090 | -102.321327 | -3.814168 | 98.678809 | 0.171650 | 37.155963 | 0.692820 | -0.093873 | 0.569822 | 0.486276 | 1.171807 |
| BTC | 1001 | -188.357364 | -28.494946 | 159.855229 | -0.007189 | 32.567433 | 0.626354 | -0.188169 | 0.968556 | 0.746824 | 1.296899 |
| DOGE | 1276 | -227.395350 | -30.898566 | 196.975979 | 0.479196 | 36.912226 | 0.669869 | -0.178210 | 0.979634 | 0.855656 | 1.144893 |
| ETH | 979 | -268.836041 | -95.979071 | 172.733281 | -0.123689 | 34.627171 | 0.577923 | -0.274603 | 1.085842 | 0.995213 | 1.091065 |
| SOL | 1329 | -198.705080 | 3.473949 | 202.534378 | 0.355349 | 37.396539 | 0.713217 | -0.149515 | 0.994307 | 0.832783 | 1.193957 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1900 | -350.424452 | -58.224609 | 291.633314 | -0.566528 | 33.368421 | 0.637068 | -0.184434 | 0.970209 | 0.762668 | 1.272126 |
| SHORT | 3775 | -635.190708 | -97.488193 | 539.144362 | 1.441846 | 37.192053 | 0.663971 | -0.168262 | 0.893941 | 0.797252 | 1.121278 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 310 | -38.000880 | -11.948163 | 25.985118 | -0.067599 | 33.548387 | 0.575908 | -0.122583 | 0.496197 | 0.434977 | 1.140741 |
| AVAX | SHORT | 780 | -64.320447 | 8.133995 | 72.693691 | 0.239249 | 38.589744 | 0.735844 | -0.082462 | 0.595261 | 0.508338 | 1.170994 |
| BTC | LONG | 370 | -71.618427 | -12.245197 | 59.153238 | -0.219992 | 31.081081 | 0.595861 | -0.193563 | 0.918209 | 0.694951 | 1.321257 |
| BTC | SHORT | 631 | -116.738937 | -16.249749 | 100.701991 | 0.212803 | 33.438986 | 0.642885 | -0.185006 | 0.995996 | 0.778319 | 1.279675 |
| DOGE | LONG | 289 | -31.997210 | -1.796894 | 30.007602 | -0.192713 | 33.910035 | 0.685543 | -0.110717 | 0.711802 | 0.532742 | 1.336109 |
| DOGE | SHORT | 987 | -195.398140 | -29.101672 | 166.968377 | 0.671909 | 37.791287 | 0.667152 | -0.197972 | 1.050003 | 0.956106 | 1.098207 |
| ETH | LONG | 407 | -89.294916 | -20.868982 | 68.199844 | -0.226090 | 33.415233 | 0.614726 | -0.219398 | 1.047611 | 0.855240 | 1.224932 |
| ETH | SHORT | 572 | -179.541124 | -75.110089 | 104.533437 | 0.102401 | 35.489510 | 0.556871 | -0.313883 | 1.111456 | 1.098012 | 1.012243 |
| SOL | LONG | 524 | -119.513019 | -11.365374 | 108.287512 | 0.139866 | 34.541985 | 0.672742 | -0.228078 | 1.357362 | 1.064710 | 1.274866 |
| SOL | SHORT | 805 | -79.192060 | 14.839323 | 94.246866 | 0.215483 | 39.254658 | 0.758325 | -0.098375 | 0.786355 | 0.670102 | 1.173484 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | 0.000841 | 0.014399 | 0.000000 | -0.013558 |
| stop | 3588 | -2,303.512969 | 546.656110 | 0.372042 | -2,849.797037 |
| stop_gap | 10 | -1.597963 | 0.484399 | -0.004300 | -2.086661 |
| trailing_take_profit | 1770 | 1,844.648152 | 242.656530 | 0.547175 | 1,602.538797 |
| trailing_take_profit_gap | 306 | 304.749137 | 40.966239 | -0.039600 | 263.743299 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 813.512297 | -186.487703 | -18.648770 | False |
| 2025-12 | 813.512297 | 604.416474 | -209.095823 | -25.702847 | False |
| 2026-01 | 604.416474 | 499.238217 | -105.178257 | -17.401620 | False |
| 2026-02 | 499.238217 | 375.977632 | -123.260585 | -24.689733 | False |
| 2026-03 | 375.977632 | 210.257984 | -165.719648 | -44.076997 | False |
| 2026-04 | 210.257984 | 148.033541 | -62.224442 | -29.594330 | False |
| 2026-05 | 148.033541 | 101.366610 | -46.666931 | -31.524566 | False |
| 2026-06 | 101.366610 | 71.748779 | -29.617832 | -29.218528 | False |
| 2026-07 | 71.748779 | 47.632193 | -24.116585 | -33.612538 | False |
| 2026-08 | 47.632193 | 40.174302 | -7.457891 | -15.657250 | False |
| 2026-09 | 40.174302 | 25.493841 | -14.680461 | -36.541920 | False |
| 2026-10 | 25.493841 | 17.615824 | -7.878016 | -30.901645 | False |
| 2026-11 | 17.615824 | 14.384839 | -3.230985 | -18.341379 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
