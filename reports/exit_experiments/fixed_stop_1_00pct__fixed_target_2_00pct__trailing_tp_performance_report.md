# Performance report: fixed_stop_1_00pct__fixed_target_2_00pct__trailing_tp

## Run metadata
- Experiment Id: fixed_stop_1_00pct__fixed_target_2_00pct__trailing_tp
- Stop Model: fixed_stop_1_00pct
- Target Model: fixed_target_2_00pct
- Target Value: 0.020000
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
- Final Equity: 656.646090
- Net Pnl: -343.353910
- Total Return Pct: -34.335391
- Max Drawdown Amount: 521.966725
- Max Drawdown Pct: 47.722254
- Recovery Factor: -0.657808
- Sharpe Ratio: -0.955935
- Sortino Ratio: -1.348683
- Cagr Pct: -32.188863
- Calmar Ratio: -0.674504
- Worst Daily Loss: -81.075707
- Worst Daily Loss Pct: -7.519868
- Worst Daily Loss Date Utc: 2026-02-06
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 42.650272
- Max Capital Utilization Pct: 102.820916
- Max Gross Exposure: 1,074.648026
- Max Gross Exposure Equity Multiple: 1.028209

## Trade performance

- Trade Count: 2124
- Net Pnl: -343.353910
- Gross Pnl: 256.348118
- Total Fees: 601.413451
- Funding Pnl: 1.711424
- Winning Trades: 760
- Losing Trades: 1364
- Breakeven Trades: 0
- Win Rate Pct: 35.781544
- Profit Factor: 0.921547
- Expectancy: -0.161654
- Average Win: 5.306829
- Average Loss: 3.208610
- Payoff Ratio: 1.653934
- Max Consecutive Losses: 43
- Average Duration Minutes: 325.008004
- Median Duration Minutes: 137.000000
- Max Duration Minutes: 7,218.000000
- Recovery Factor: -0.657808

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 430 | -146.947699 | -32.735133 | 114.042834 | -0.169732 | 33.953488 | 0.828829 | -0.341739 | 4.873535 | 3.022830 | 1.612242 |
| BTC | 295 | 49.932793 | 137.001918 | 87.420422 | 0.351297 | 39.661017 | 1.083559 | 0.169264 | 5.534257 | 3.357165 | 1.648491 |
| DOGE | 495 | -26.165141 | 111.384076 | 138.627304 | 1.078086 | 37.575758 | 0.973670 | -0.052859 | 5.201973 | 3.215962 | 1.617548 |
| ETH | 375 | -168.956225 | -57.690486 | 111.374554 | 0.108815 | 32.800000 | 0.800319 | -0.450550 | 5.505487 | 3.357663 | 1.639678 |
| SOL | 529 | -51.217639 | 98.387741 | 149.948338 | 0.342958 | 35.538752 | 0.952604 | -0.096820 | 5.475552 | 3.168977 | 1.727861 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 664 | -126.942504 | 77.045812 | 201.018291 | -2.970025 | 33.885542 | 0.913737 | -0.191178 | 5.976131 | 3.352100 | 1.782802 |
| SHORT | 1460 | -216.411406 | 179.302305 | 400.395161 | 4.681449 | 36.643836 | 0.925503 | -0.148227 | 5.025346 | 3.140510 | 1.600169 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 121 | -72.166461 | -37.308872 | 34.499382 | -0.358208 | 29.752066 | 0.732958 | -0.596417 | 5.502139 | 3.179335 | 1.730594 |
| AVAX | SHORT | 309 | -74.781237 | 4.573739 | 79.543452 | 0.188475 | 35.598706 | 0.872873 | -0.242010 | 4.667810 | 2.955982 | 1.579107 |
| BTC | LONG | 96 | 50.595281 | 83.376622 | 31.814164 | -0.967177 | 39.583333 | 1.238299 | 0.527034 | 6.918788 | 3.660667 | 1.890035 |
| BTC | SHORT | 199 | -0.662487 | 53.625296 | 55.606258 | 1.318474 | 39.698492 | 0.998280 | -0.003329 | 4.868281 | 3.210472 | 1.516375 |
| DOGE | LONG | 109 | 7.886162 | 38.671958 | 29.812175 | -0.973621 | 36.697248 | 1.038340 | 0.072350 | 5.339350 | 2.980983 | 1.791137 |
| DOGE | SHORT | 386 | -34.051303 | 72.712118 | 108.815129 | 2.051707 | 37.823834 | 0.956790 | -0.088216 | 5.164335 | 3.283518 | 1.572806 |
| ETH | LONG | 135 | -79.426758 | -36.177285 | 42.440176 | -0.809298 | 31.851852 | 0.757567 | -0.588346 | 5.772025 | 3.561128 | 1.620841 |
| ETH | SHORT | 240 | -89.529467 | -21.513201 | 68.934378 | 0.918113 | 33.333333 | 0.827332 | -0.373039 | 5.362222 | 3.240670 | 1.654665 |
| SOL | LONG | 203 | -33.830727 | 28.483388 | 62.452395 | 0.138279 | 33.497537 | 0.925761 | -0.166654 | 6.203934 | 3.375543 | 1.837907 |
| SOL | SHORT | 326 | -17.386912 | 69.904353 | 87.495944 | 0.204679 | 36.809816 | 0.972178 | -0.053334 | 5.062801 | 3.033607 | 1.668905 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 2 | -3.263334 | 0.591622 | -0.001642 | -3.856598 |
| stop | 1360 | -3,978.411454 | 390.665940 | 0.918204 | -4,368.159189 |
| stop_gap | 2 | -4.125825 | 0.402049 | 0.000000 | -4.527873 |
| trailing_take_profit | 679 | 3,735.061403 | 188.215361 | 0.493979 | 3,547.340021 |
| trailing_take_profit_gap | 81 | 507.087327 | 21.538480 | 0.300882 | 485.849730 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 1,043.993645 | 43.993645 | 4.399365 | False |
| 2025-12 | 1,043.993645 | 924.487714 | -119.505931 | -11.446998 | False |
| 2026-01 | 924.487714 | 923.415528 | -1.072186 | -0.115976 | False |
| 2026-02 | 923.415528 | 869.314186 | -54.101342 | -5.858830 | False |
| 2026-03 | 869.314186 | 750.764918 | -118.549268 | -13.637103 | False |
| 2026-04 | 750.764918 | 730.362835 | -20.402083 | -2.717506 | False |
| 2026-05 | 730.362835 | 679.806006 | -50.556829 | -6.922152 | False |
| 2026-06 | 679.806006 | 708.227567 | 28.421561 | 4.180834 | False |
| 2026-07 | 708.227567 | 646.747018 | -61.480549 | -8.680903 | False |
| 2026-08 | 646.747018 | 757.966559 | 111.219541 | 17.196761 | False |
| 2026-09 | 757.966559 | 627.657654 | -130.308905 | -17.191907 | False |
| 2026-10 | 627.657654 | 600.686965 | -26.970689 | -4.297038 | False |
| 2026-11 | 600.686965 | 656.646090 | 55.959124 | 9.315855 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
