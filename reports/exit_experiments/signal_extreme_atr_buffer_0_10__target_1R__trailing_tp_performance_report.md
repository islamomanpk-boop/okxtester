# Performance report: signal_extreme_atr_buffer_0_10__target_1R__trailing_tp

## Run metadata
- Experiment Id: signal_extreme_atr_buffer_0_10__target_1R__trailing_tp
- Stop Model: signal_extreme_atr_buffer_0_10
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
- Final Equity: 3.336313
- Net Pnl: -996.663687
- Total Return Pct: -99.666369
- Max Drawdown Amount: 1,008.734165
- Max Drawdown Pct: 99.670426
- Recovery Factor: -0.988034
- Sharpe Ratio: -13.114615
- Sortino Ratio: -11.091585
- Cagr Pct: -99.483969
- Calmar Ratio: -0.998129
- Worst Daily Loss: -56.310757
- Worst Daily Loss Pct: -5.840656
- Worst Daily Loss Date Utc: 2025-11-18
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 32.832635
- Max Capital Utilization Pct: 102.373269
- Max Gross Exposure: 1,007.537892
- Max Gross Exposure Equity Multiple: 1.023733

## Trade performance

- Trade Count: 6786
- Net Pnl: -996.663687
- Gross Pnl: -206.338025
- Total Fees: 791.199597
- Funding Pnl: 0.873934
- Winning Trades: 2976
- Losing Trades: 3810
- Breakeven Trades: 0
- Win Rate Pct: 43.854996
- Profit Factor: 0.564648
- Expectancy: -0.146871
- Average Win: 0.434363
- Average Loss: 0.600874
- Payoff Ratio: 0.722886
- Max Consecutive Losses: 19
- Average Duration Minutes: 51.891541
- Median Duration Minutes: 21.000000
- Max Duration Minutes: 4,420.000000
- Recovery Factor: -0.988034

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1235 | -91.225042 | 2.687126 | 94.088579 | 0.176412 | 44.777328 | 0.643234 | -0.073866 | 0.297423 | 0.374926 | 0.793283 |
| BTC | 1278 | -195.693669 | -32.635778 | 163.159294 | 0.101403 | 41.001565 | 0.519960 | -0.153125 | 0.404519 | 0.540665 | 0.748187 |
| DOGE | 1600 | -219.275260 | -38.286026 | 181.270521 | 0.281287 | 44.875000 | 0.587212 | -0.137047 | 0.434444 | 0.602274 | 0.721339 |
| ETH | 1172 | -216.605956 | -62.809968 | 153.793548 | -0.002440 | 43.430034 | 0.553014 | -0.184817 | 0.526496 | 0.730909 | 0.720331 |
| SOL | 1501 | -273.863761 | -75.293379 | 198.887654 | 0.317272 | 44.770153 | 0.551167 | -0.182454 | 0.500454 | 0.736030 | 0.679937 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2419 | -332.740724 | -57.923478 | 274.517650 | -0.299596 | 42.786275 | 0.530831 | -0.137553 | 0.363741 | 0.512437 | 0.709826 |
| SHORT | 4367 | -663.922963 | -148.414547 | 516.681947 | 1.173530 | 44.446989 | 0.579826 | -0.152032 | 0.472021 | 0.651326 | 0.724708 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 367 | -38.158063 | -15.315559 | 22.829600 | -0.012904 | 41.144414 | 0.405902 | -0.103973 | 0.172652 | 0.297355 | 0.580628 |
| AVAX | SHORT | 868 | -53.066979 | 18.002685 | 71.258979 | 0.189316 | 46.313364 | 0.722846 | -0.061137 | 0.344289 | 0.410882 | 0.837926 |
| BTC | LONG | 498 | -63.566860 | -7.255964 | 56.235555 | -0.075341 | 40.963855 | 0.483921 | -0.127644 | 0.292186 | 0.418955 | 0.697416 |
| BTC | SHORT | 780 | -132.126809 | -25.379814 | 106.923740 | 0.176744 | 41.025641 | 0.535564 | -0.169393 | 0.476131 | 0.618454 | 0.769873 |
| DOGE | LONG | 367 | -28.114171 | -4.048193 | 23.938527 | -0.127451 | 44.959128 | 0.544352 | -0.076605 | 0.203560 | 0.305453 | 0.666419 |
| DOGE | SHORT | 1233 | -191.161089 | -34.237833 | 157.331994 | 0.408738 | 44.849959 | 0.592845 | -0.155037 | 0.503333 | 0.690448 | 0.728996 |
| ETH | LONG | 539 | -51.706821 | 8.791006 | 60.350050 | -0.147777 | 43.784787 | 0.657196 | -0.095931 | 0.420034 | 0.497805 | 0.843773 |
| ETH | SHORT | 633 | -164.899134 | -71.600974 | 93.443498 | 0.145337 | 43.127962 | 0.505932 | -0.260504 | 0.618529 | 0.927105 | 0.667163 |
| SOL | LONG | 648 | -151.194810 | -40.094767 | 111.163918 | 0.063876 | 43.055556 | 0.511132 | -0.233325 | 0.566597 | 0.838144 | 0.676013 |
| SOL | SHORT | 853 | -122.668951 | -35.198611 | 87.723736 | 0.253396 | 46.072685 | 0.592318 | -0.143809 | 0.453498 | 0.654117 | 0.693298 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| stop | 3547 | -1,852.616912 | 422.859010 | 0.328199 | -2,275.147723 |
| stop_gap | 10 | -1.085191 | 0.319083 | 0.000000 | -1.404274 |
| trailing_take_profit | 2813 | 1,472.262027 | 320.903004 | 0.534713 | 1,151.893736 |
| trailing_take_profit_gap | 416 | 175.102052 | 47.118501 | 0.011023 | 127.994574 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 750.186460 | -249.813540 | -24.981354 | False |
| 2025-12 | 750.186460 | 510.541723 | -239.644737 | -31.944690 | False |
| 2026-01 | 510.541723 | 356.649114 | -153.892610 | -30.143004 | False |
| 2026-02 | 356.649114 | 260.095845 | -96.553269 | -27.072342 | False |
| 2026-03 | 260.095845 | 134.142368 | -125.953476 | -48.425793 | False |
| 2026-04 | 134.142368 | 85.771628 | -48.370740 | -36.059256 | False |
| 2026-05 | 85.771628 | 54.002887 | -31.768741 | -37.038753 | False |
| 2026-06 | 54.002887 | 34.074048 | -19.928838 | -36.903283 | False |
| 2026-07 | 34.074048 | 19.681176 | -14.392872 | -42.239983 | False |
| 2026-08 | 19.681176 | 15.913682 | -3.767494 | -19.142625 | False |
| 2026-09 | 15.913682 | 8.638845 | -7.274838 | -45.714359 | False |
| 2026-10 | 8.638845 | 4.786046 | -3.852798 | -44.598536 | False |
| 2026-11 | 4.786046 | 3.336313 | -1.449734 | -30.290842 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
