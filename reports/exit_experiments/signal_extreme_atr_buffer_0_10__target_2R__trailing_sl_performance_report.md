# Performance report: signal_extreme_atr_buffer_0_10__target_2R__trailing_sl

## Run metadata
- Experiment Id: signal_extreme_atr_buffer_0_10__target_2R__trailing_sl
- Stop Model: signal_extreme_atr_buffer_0_10
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
- Final Equity: 7.889285
- Net Pnl: -992.110715
- Total Return Pct: -99.211072
- Max Drawdown Amount: 1,005.835736
- Max Drawdown Pct: 99.221753
- Recovery Factor: -0.986355
- Sharpe Ratio: -11.217361
- Sortino Ratio: -10.119952
- Cagr Pct: -98.857483
- Calmar Ratio: -0.996329
- Worst Daily Loss: -57.622204
- Worst Daily Loss Pct: -5.879819
- Worst Daily Loss Date Utc: 2025-11-18
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 34.494989
- Max Capital Utilization Pct: 102.349912
- Max Gross Exposure: 1,010.250393
- Max Gross Exposure Equity Multiple: 1.023499

## Trade performance

- Trade Count: 6206
- Net Pnl: -992.110715
- Gross Pnl: -135.043943
- Total Fees: 857.886771
- Funding Pnl: 0.819999
- Winning Trades: 2141
- Losing Trades: 4065
- Breakeven Trades: 0
- Win Rate Pct: 34.498872
- Profit Factor: 0.603095
- Expectancy: -0.159863
- Average Win: 0.704115
- Average Loss: 0.614913
- Payoff Ratio: 1.145064
- Max Consecutive Losses: 24
- Average Duration Minutes: 61.722365
- Median Duration Minutes: 26.000000
- Max Duration Minutes: 4,751.000000
- Recovery Factor: -0.986355

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1146 | -123.233062 | -19.023984 | 104.207923 | -0.001155 | 34.554974 | 0.590000 | -0.107533 | 0.447817 | 0.400758 | 1.117424 |
| BTC | 1168 | -199.630378 | -25.405300 | 174.257839 | 0.032762 | 32.277397 | 0.553240 | -0.170916 | 0.655729 | 0.564905 | 1.160777 |
| DOGE | 1462 | -176.587253 | 15.166056 | 192.125315 | 0.372006 | 35.567715 | 0.681779 | -0.120785 | 0.727564 | 0.589088 | 1.235069 |
| ETH | 1060 | -225.108363 | -54.448823 | 170.578990 | -0.080551 | 34.622642 | 0.579249 | -0.212366 | 0.844434 | 0.772029 | 1.093786 |
| SOL | 1370 | -267.551660 | -51.331892 | 216.716704 | 0.496936 | 35.109489 | 0.596011 | -0.195293 | 0.820631 | 0.744967 | 1.101568 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2149 | -370.629320 | -63.460808 | 306.802015 | -0.366496 | 32.712890 | 0.546848 | -0.172466 | 0.636221 | 0.565624 | 1.124812 |
| SHORT | 4057 | -621.481396 | -71.583134 | 551.084756 | 1.186495 | 35.444910 | 0.630451 | -0.153187 | 0.737306 | 0.642126 | 1.148227 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 320 | -45.356409 | -18.781826 | 26.539752 | -0.034832 | 31.250000 | 0.400928 | -0.141739 | 0.303547 | 0.344141 | 0.882041 |
| AVAX | SHORT | 826 | -77.876652 | -0.242159 | 77.668170 | 0.033677 | 35.835351 | 0.653662 | -0.094282 | 0.496557 | 0.424259 | 1.170408 |
| BTC | LONG | 453 | -68.376574 | -3.324000 | 64.907561 | -0.145013 | 31.788079 | 0.522845 | -0.150942 | 0.520305 | 0.463756 | 1.121938 |
| BTC | SHORT | 715 | -131.253803 | -22.081300 | 109.350278 | 0.177775 | 32.587413 | 0.567589 | -0.183572 | 0.739425 | 0.629751 | 1.174155 |
| DOGE | LONG | 330 | -36.410117 | -6.214902 | 30.054461 | -0.140754 | 33.939394 | 0.558143 | -0.110334 | 0.410646 | 0.377993 | 1.086385 |
| DOGE | SHORT | 1132 | -140.177136 | 21.380957 | 162.070853 | 0.512760 | 36.042403 | 0.703340 | -0.123831 | 0.814562 | 0.652650 | 1.248084 |
| ETH | LONG | 482 | -68.920754 | 0.976018 | 69.691218 | -0.205553 | 32.780083 | 0.632215 | -0.142989 | 0.749830 | 0.578376 | 1.296440 |
| ETH | SHORT | 578 | -156.187610 | -55.424841 | 100.887772 | 0.125003 | 36.159170 | 0.550697 | -0.270221 | 0.915953 | 0.942065 | 0.972283 |
| SOL | LONG | 564 | -151.565466 | -36.116100 | 115.609022 | 0.159656 | 33.510638 | 0.539433 | -0.268733 | 0.939256 | 0.877560 | 1.070304 |
| SOL | SHORT | 806 | -115.986194 | -15.215792 | 101.107682 | 0.337280 | 36.228288 | 0.651892 | -0.143903 | 0.743850 | 0.648230 | 1.147509 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| stop | 4990 | -1,568.900808 | 688.718028 | 0.477588 | -2,257.141249 |
| stop_gap | 49 | 2.588915 | 7.140954 | 0.000000 | -4.552039 |
| target | 1165 | 1,430.766786 | 161.933313 | 0.342411 | 1,269.175884 |
| target_gap | 2 | 0.501165 | 0.094477 | 0.000000 | 0.406688 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 826.571396 | -173.428604 | -17.342860 | False |
| 2025-12 | 826.571396 | 574.458576 | -252.112821 | -30.501034 | False |
| 2026-01 | 574.458576 | 441.166945 | -133.291630 | -23.203001 | False |
| 2026-02 | 441.166945 | 321.899883 | -119.267062 | -27.034451 | False |
| 2026-03 | 321.899883 | 177.015990 | -144.883894 | -45.008992 | False |
| 2026-04 | 177.015990 | 119.109896 | -57.906094 | -32.712352 | False |
| 2026-05 | 119.109896 | 77.649922 | -41.459974 | -34.808169 | False |
| 2026-06 | 77.649922 | 53.054628 | -24.595293 | -31.674589 | False |
| 2026-07 | 53.054628 | 34.791637 | -18.262992 | -34.422994 | False |
| 2026-08 | 34.791637 | 29.557058 | -5.234579 | -15.045509 | False |
| 2026-09 | 29.557058 | 16.961427 | -12.595631 | -42.614630 | False |
| 2026-10 | 16.961427 | 10.370144 | -6.591283 | -38.860425 | False |
| 2026-11 | 10.370144 | 7.889285 | -2.480860 | -23.923099 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
