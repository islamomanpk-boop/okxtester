# Performance report: fixed_stop_0_75pct__fixed_target_1_00pct__trailing_tp

## Run metadata
- Experiment Id: fixed_stop_0_75pct__fixed_target_1_00pct__trailing_tp
- Stop Model: fixed_stop_0_75pct
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
- Final Equity: 143.413343
- Net Pnl: -856.586657
- Total Return Pct: -85.658666
- Max Drawdown Amount: 891.383482
- Max Drawdown Pct: 87.065422
- Recovery Factor: -0.960963
- Sharpe Ratio: -4.811440
- Sortino Ratio: -5.382914
- Cagr Pct: -83.362436
- Calmar Ratio: -0.957469
- Worst Daily Loss: -74.654714
- Worst Daily Loss Pct: -8.474406
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 40.446609
- Max Capital Utilization Pct: 102.155122
- Max Gross Exposure: 1,025.402674
- Max Gross Exposure Equity Multiple: 1.021551

## Trade performance

- Trade Count: 3718
- Net Pnl: -856.586657
- Gross Pnl: -66.975047
- Total Fees: 791.118817
- Funding Pnl: 1.507207
- Winning Trades: 1624
- Losing Trades: 2094
- Breakeven Trades: 0
- Win Rate Pct: 43.679398
- Profit Factor: 0.780962
- Expectancy: -0.230389
- Average Win: 1.880599
- Average Loss: 1.867564
- Payoff Ratio: 1.006980
- Max Consecutive Losses: 21
- Average Duration Minutes: 137.840775
- Median Duration Minutes: 62.000000
- Max Duration Minutes: 3,582.000000
- Recovery Factor: -0.960963

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 760 | -134.767150 | -14.861307 | 119.988578 | 0.082736 | 42.631579 | 0.779083 | -0.177325 | 1.466875 | 1.399162 | 1.048395 |
| BTC | 537 | -94.100462 | 17.405322 | 111.887263 | 0.381479 | 45.437616 | 0.825907 | -0.175234 | 1.829583 | 1.844774 | 0.991766 |
| DOGE | 838 | -163.970457 | 29.278987 | 193.915505 | 0.666061 | 44.630072 | 0.826134 | -0.195669 | 2.083196 | 2.032512 | 1.024936 |
| ETH | 676 | -264.450298 | -104.919832 | 159.527172 | -0.003294 | 42.455621 | 0.672761 | -0.391199 | 1.894339 | 2.077444 | 0.911861 |
| SOL | 907 | -199.298289 | 6.121784 | 205.800299 | 0.380225 | 43.550165 | 0.802463 | -0.219734 | 2.049662 | 1.970537 | 1.040154 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1221 | -347.713162 | -69.245765 | 277.381842 | -1.085555 | 41.769042 | 0.750059 | -0.284777 | 2.046017 | 1.956655 | 1.045671 |
| SHORT | 2497 | -508.873494 | 2.270718 | 513.736975 | 2.592762 | 44.613536 | 0.798026 | -0.203794 | 1.804869 | 1.821762 | 0.990727 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 226 | -61.745258 | -24.243776 | 37.376677 | -0.124804 | 36.725664 | 0.687780 | -0.273209 | 1.638760 | 1.382953 | 1.184971 |
| AVAX | SHORT | 534 | -73.021892 | 9.382469 | 82.611901 | 0.207540 | 45.131086 | 0.822879 | -0.136745 | 1.407678 | 1.407072 | 1.000430 |
| BTC | LONG | 190 | -40.667008 | 2.322829 | 42.529974 | -0.459864 | 43.684211 | 0.804589 | -0.214037 | 2.017391 | 1.944957 | 1.037242 |
| BTC | SHORT | 347 | -53.433453 | 15.082493 | 69.357289 | 0.841343 | 46.397695 | 0.839254 | -0.153987 | 1.732763 | 1.787142 | 0.969572 |
| DOGE | LONG | 175 | -37.625484 | 1.518843 | 38.794315 | -0.350011 | 44.000000 | 0.802060 | -0.215003 | 1.979999 | 1.939647 | 1.020804 |
| DOGE | SHORT | 663 | -126.344974 | 27.760144 | 155.121190 | 1.016072 | 44.796380 | 0.832211 | -0.190566 | 2.109950 | 2.057378 | 1.025553 |
| ETH | LONG | 266 | -88.383066 | -25.903222 | 62.097571 | -0.382273 | 43.233083 | 0.710281 | -0.332267 | 1.884192 | 2.020299 | 0.932630 |
| ETH | SHORT | 410 | -176.067232 | -79.016610 | 97.429601 | 0.378979 | 41.951220 | 0.650008 | -0.429432 | 1.901123 | 2.113699 | 0.899429 |
| SOL | LONG | 364 | -119.292346 | -22.940438 | 96.583305 | 0.231397 | 41.758242 | 0.756625 | -0.327726 | 2.439909 | 2.312069 | 1.055293 |
| SOL | SHORT | 543 | -80.005943 | 29.062223 | 109.216994 | 0.148828 | 44.751381 | 0.845774 | -0.147341 | 1.805557 | 1.729188 | 1.044165 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | -0.433843 | 0.083561 | -0.000462 | -0.517866 |
| stop | 2089 | -3,460.833323 | 449.932798 | 0.706230 | -3,910.059892 |
| stop_gap | 2 | -0.015640 | 0.002028 | -0.000011 | -0.017679 |
| trailing_take_profit | 1466 | 3,022.925916 | 308.887653 | 0.688530 | 2,714.726793 |
| trailing_take_profit_gap | 160 | 371.381844 | 32.212777 | 0.112920 | 339.281987 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 930.882952 | -69.117048 | -6.911705 | False |
| 2025-12 | 930.882952 | 731.679451 | -199.203501 | -21.399414 | False |
| 2026-01 | 731.679451 | 708.838751 | -22.840700 | -3.121681 | False |
| 2026-02 | 708.838751 | 605.064711 | -103.774040 | -14.640007 | False |
| 2026-03 | 605.064711 | 476.069759 | -128.994952 | -21.319199 | False |
| 2026-04 | 476.069759 | 447.922638 | -28.147121 | -5.912394 | False |
| 2026-05 | 447.922638 | 375.274868 | -72.647770 | -16.218821 | False |
| 2026-06 | 375.274868 | 349.896330 | -25.378538 | -6.762653 | False |
| 2026-07 | 349.896330 | 279.283527 | -70.612803 | -20.181064 | False |
| 2026-08 | 279.283527 | 277.994263 | -1.289264 | -0.461633 | False |
| 2026-09 | 277.994263 | 181.818784 | -96.175479 | -34.596210 | False |
| 2026-10 | 181.818784 | 149.850278 | -31.968507 | -17.582620 | False |
| 2026-11 | 149.850278 | 143.413343 | -6.436934 | -4.295577 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
