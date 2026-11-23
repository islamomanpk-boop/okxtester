# Performance report: fixed_stop_0_50pct__fixed_target_0_75pct__trailing_sl

## Run metadata
- Experiment Id: fixed_stop_0_50pct__fixed_target_0_75pct__trailing_sl
- Stop Model: fixed_stop_0_50pct
- Target Model: fixed_target_0_75pct
- Target Value: 0.007500
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
- Final Equity: 13.399863
- Net Pnl: -986.600137
- Total Return Pct: -98.660014
- Max Drawdown Amount: 990.635843
- Max Drawdown Pct: 98.666560
- Recovery Factor: -0.995926
- Sharpe Ratio: -10.528631
- Sortino Ratio: -9.408240
- Cagr Pct: -98.136492
- Calmar Ratio: -0.994628
- Worst Daily Loss: -66.168749
- Worst Daily Loss Pct: -8.675431
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 37.350517
- Max Capital Utilization Pct: 101.313195
- Max Gross Exposure: 999.055458
- Max Gross Exposure Equity Multiple: 1.013132

## Trade performance

- Trade Count: 6644
- Net Pnl: -986.600137
- Gross Pnl: -100.935745
- Total Fees: 886.449892
- Funding Pnl: 0.785499
- Winning Trades: 2623
- Losing Trades: 4021
- Breakeven Trades: 0
- Win Rate Pct: 39.479229
- Profit Factor: 0.649349
- Expectancy: -0.148495
- Average Win: 0.696539
- Average Loss: 0.699732
- Payoff Ratio: 0.995437
- Max Consecutive Losses: 20
- Average Duration Minutes: 58.194160
- Median Duration Minutes: 28.000000
- Max Duration Minutes: 1,904.000000
- Recovery Factor: -0.995926

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1332 | -131.592356 | -21.284411 | 110.364647 | 0.056702 | 38.663664 | 0.630147 | -0.098793 | 0.435348 | 0.435491 | 0.999670 |
| BTC | 993 | -128.507401 | 1.232914 | 129.834107 | 0.093792 | 40.584089 | 0.681094 | -0.129413 | 0.681032 | 0.682989 | 0.997135 |
| DOGE | 1521 | -245.829627 | -22.232799 | 223.830059 | 0.233231 | 40.105194 | 0.652432 | -0.161624 | 0.756483 | 0.776382 | 0.974369 |
| ETH | 1162 | -252.400011 | -59.515168 | 192.819055 | -0.065788 | 38.554217 | 0.604438 | -0.217212 | 0.860890 | 0.893668 | 0.963322 |
| SOL | 1636 | -228.270742 | 0.863719 | 229.602023 | 0.467563 | 39.547677 | 0.678265 | -0.139530 | 0.743784 | 0.717390 | 1.036791 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2364 | -322.731024 | -33.569921 | 288.757893 | -0.403209 | 37.732657 | 0.646316 | -0.136519 | 0.661158 | 0.619894 | 1.066566 |
| SHORT | 4280 | -663.869114 | -67.365824 | 597.691999 | 1.188709 | 40.443925 | 0.650804 | -0.155110 | 0.714771 | 0.745837 | 0.958348 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 404 | -35.412615 | -6.658819 | 28.695937 | -0.057859 | 36.633663 | 0.617246 | -0.087655 | 0.385865 | 0.361409 | 1.067669 |
| AVAX | SHORT | 928 | -96.179741 | -14.625592 | 81.668710 | 0.114561 | 39.547414 | 0.634681 | -0.103642 | 0.455303 | 0.469297 | 0.970180 |
| BTC | LONG | 386 | -32.730923 | 14.466823 | 47.108119 | -0.089627 | 41.450777 | 0.764879 | -0.084795 | 0.665487 | 0.615968 | 1.080392 |
| BTC | SHORT | 607 | -95.776478 | -13.233909 | 82.725988 | 0.183419 | 40.032949 | 0.636873 | -0.157787 | 0.691268 | 0.724600 | 0.953999 |
| DOGE | LONG | 368 | -41.197026 | -9.922216 | 31.098895 | -0.175914 | 38.315217 | 0.596971 | -0.111948 | 0.432776 | 0.450302 | 0.961081 |
| DOGE | SHORT | 1153 | -204.632601 | -12.310582 | 192.731164 | 0.409145 | 40.676496 | 0.661801 | -0.177478 | 0.853802 | 0.884599 | 0.965185 |
| ETH | LONG | 510 | -70.928056 | -2.051140 | 68.633565 | -0.243352 | 38.235294 | 0.673804 | -0.139075 | 0.751344 | 0.690286 | 1.088453 |
| ETH | SHORT | 652 | -181.471955 | -57.464029 | 124.185490 | 0.177564 | 38.803681 | 0.568580 | -0.278331 | 0.945323 | 1.054232 | 0.896693 |
| SOL | LONG | 696 | -142.462403 | -29.404569 | 113.221377 | 0.163543 | 35.632184 | 0.605472 | -0.204687 | 0.881586 | 0.806017 | 1.093756 |
| SOL | SHORT | 940 | -85.808339 | 30.268288 | 116.380646 | 0.304020 | 42.446809 | 0.753710 | -0.091285 | 0.658132 | 0.643998 | 1.021947 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | -0.014826 | 0.010841 | 0.000000 | -0.025667 |
| stop | 4552 | -2,163.792955 | 601.307520 | 0.436875 | -2,764.663599 |
| stop_gap | 33 | -0.967646 | 2.800373 | 0.006748 | -3.761271 |
| target | 2055 | 2,063.170233 | 282.239806 | 0.341876 | 1,781.272304 |
| target_gap | 3 | 0.669448 | 0.091352 | 0.000000 | 0.578097 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 813.155607 | -186.844393 | -18.684439 | False |
| 2025-12 | 813.155607 | 571.075618 | -242.079990 | -29.770438 | False |
| 2026-01 | 571.075618 | 485.620936 | -85.454682 | -14.963812 | False |
| 2026-02 | 485.620936 | 333.631904 | -151.989032 | -31.297875 | False |
| 2026-03 | 333.631904 | 190.794264 | -142.837639 | -42.812944 | False |
| 2026-04 | 190.794264 | 127.838240 | -62.956025 | -32.996812 | False |
| 2026-05 | 127.838240 | 98.184805 | -29.653435 | -23.196060 | False |
| 2026-06 | 98.184805 | 71.821097 | -26.363707 | -26.851108 | False |
| 2026-07 | 71.821097 | 52.772527 | -19.048570 | -26.522249 | False |
| 2026-08 | 52.772527 | 41.591727 | -11.180800 | -21.186781 | False |
| 2026-09 | 41.591727 | 23.462498 | -18.129229 | -43.588547 | False |
| 2026-10 | 23.462498 | 17.709478 | -5.753020 | -24.520067 | False |
| 2026-11 | 17.709478 | 13.399863 | -4.309615 | -24.335077 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
