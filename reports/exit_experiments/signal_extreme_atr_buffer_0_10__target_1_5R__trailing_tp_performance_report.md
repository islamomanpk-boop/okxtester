# Performance report: signal_extreme_atr_buffer_0_10__target_1_5R__trailing_tp

## Run metadata
- Experiment Id: signal_extreme_atr_buffer_0_10__target_1_5R__trailing_tp
- Stop Model: signal_extreme_atr_buffer_0_10
- Target Model: target_1_5R
- Target Value: 1.500000
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
- Final Equity: 16.129695
- Net Pnl: -983.870305
- Total Return Pct: -98.387031
- Max Drawdown Amount: 1,004.919106
- Max Drawdown Pct: 98.430929
- Recovery Factor: -0.979054
- Sharpe Ratio: -9.588445
- Sortino Ratio: -9.245038
- Cagr Pct: -97.788440
- Calmar Ratio: -0.993473
- Worst Daily Loss: -58.834673
- Worst Daily Loss Pct: -7.968697
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 36.501043
- Max Capital Utilization Pct: 102.348969
- Max Gross Exposure: 1,011.678345
- Max Gross Exposure Equity Multiple: 1.023490

## Trade performance

- Trade Count: 5457
- Net Pnl: -983.870305
- Gross Pnl: -198.106645
- Total Fees: 786.408522
- Funding Pnl: 0.644862
- Winning Trades: 2095
- Losing Trades: 3362
- Breakeven Trades: 0
- Win Rate Pct: 38.391057
- Profit Factor: 0.632212
- Expectancy: -0.180295
- Average Win: 0.807269
- Average Loss: 0.795687
- Payoff Ratio: 1.014556
- Max Consecutive Losses: 22
- Average Duration Minutes: 75.485981
- Median Duration Minutes: 30.000000
- Max Duration Minutes: 4,420.000000
- Recovery Factor: -0.979054

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1003 | -125.426508 | -25.864442 | 99.635423 | 0.073357 | 37.686939 | 0.624043 | -0.125051 | 0.550776 | 0.533792 | 1.031818 |
| BTC | 1065 | -209.842126 | -40.540003 | 169.347031 | 0.044908 | 38.122066 | 0.577879 | -0.197035 | 0.707565 | 0.754345 | 0.937985 |
| DOGE | 1228 | -188.948439 | -9.099059 | 180.157196 | 0.307815 | 39.413681 | 0.698215 | -0.153867 | 0.903211 | 0.841536 | 1.073289 |
| ETH | 962 | -206.309602 | -54.616143 | 151.612375 | -0.081084 | 38.253638 | 0.629081 | -0.214459 | 0.950824 | 0.936385 | 1.015420 |
| SOL | 1199 | -253.343630 | -67.986999 | 185.656497 | 0.299865 | 38.281902 | 0.617335 | -0.211296 | 0.890430 | 0.894664 | 0.995268 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1915 | -367.019507 | -69.580059 | 296.937753 | -0.501695 | 37.650131 | 0.598869 | -0.191655 | 0.759975 | 0.766299 | 0.991747 |
| SHORT | 3542 | -616.850798 | -128.526587 | 489.470768 | 1.146557 | 38.791643 | 0.649544 | -0.174153 | 0.832087 | 0.811872 | 1.024899 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 295 | -55.810296 | -27.155295 | 28.605217 | -0.049784 | 33.559322 | 0.427084 | -0.189187 | 0.420243 | 0.497012 | 0.845539 |
| AVAX | SHORT | 708 | -69.616212 | 1.290853 | 71.030205 | 0.123141 | 39.406780 | 0.705272 | -0.098328 | 0.597094 | 0.550595 | 1.084451 |
| BTC | LONG | 414 | -62.874519 | 4.571106 | 67.236556 | -0.209069 | 39.855072 | 0.628132 | -0.151871 | 0.643655 | 0.679027 | 0.947909 |
| BTC | SHORT | 651 | -146.967607 | -45.111109 | 102.110475 | 0.253977 | 37.019969 | 0.551977 | -0.225757 | 0.751320 | 0.800087 | 0.939048 |
| DOGE | LONG | 295 | -36.375512 | -6.093879 | 30.088113 | -0.193520 | 36.949153 | 0.633335 | -0.123307 | 0.576430 | 0.533368 | 1.080737 |
| DOGE | SHORT | 933 | -152.572927 | -3.005179 | 150.069083 | 0.501336 | 40.192926 | 0.710431 | -0.163529 | 0.998195 | 0.944258 | 1.057121 |
| ETH | LONG | 417 | -70.239733 | -5.341687 | 64.677297 | -0.220749 | 38.369305 | 0.651995 | -0.168441 | 0.822474 | 0.785352 | 1.047267 |
| ETH | SHORT | 545 | -136.069869 | -49.274455 | 86.935078 | 0.139665 | 38.165138 | 0.616031 | -0.249669 | 1.049554 | 1.051564 | 0.998088 |
| SOL | LONG | 494 | -141.719448 | -35.560304 | 106.330571 | 0.171427 | 38.056680 | 0.592089 | -0.286881 | 1.094192 | 1.135384 | 0.963720 |
| SOL | SHORT | 705 | -111.624182 | -32.426695 | 79.325926 | 0.128438 | 38.439716 | 0.645214 | -0.158332 | 0.749075 | 0.724939 | 1.033294 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| stop | 3327 | -2,183.310808 | 487.808550 | 0.164254 | -2,670.955104 |
| stop_gap | 12 | -2.003844 | 0.584545 | -0.004169 | -2.592559 |
| trailing_take_profit | 1794 | 1,734.542952 | 252.539027 | 0.475939 | 1,482.479863 |
| trailing_take_profit_gap | 324 | 252.665055 | 45.476399 | 0.008838 | 207.197494 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 785.302141 | -214.697859 | -21.469786 | False |
| 2025-12 | 785.302141 | 581.163507 | -204.138634 | -25.994916 | False |
| 2026-01 | 581.163507 | 456.129566 | -125.033940 | -21.514417 | False |
| 2026-02 | 456.129566 | 350.296152 | -105.833414 | -23.202489 | False |
| 2026-03 | 350.296152 | 200.809345 | -149.486807 | -42.674407 | False |
| 2026-04 | 200.809345 | 140.958977 | -59.850368 | -29.804573 | False |
| 2026-05 | 140.958977 | 93.474921 | -47.484056 | -33.686436 | False |
| 2026-06 | 93.474921 | 72.773095 | -20.701826 | -22.146931 | False |
| 2026-07 | 72.773095 | 49.832305 | -22.940790 | -31.523724 | False |
| 2026-08 | 49.832305 | 45.893242 | -3.939064 | -7.904639 | False |
| 2026-09 | 45.893242 | 28.009790 | -17.883452 | -38.967507 | False |
| 2026-10 | 28.009790 | 18.924151 | -9.085639 | -32.437368 | False |
| 2026-11 | 18.924151 | 16.129695 | -2.794456 | -14.766613 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
