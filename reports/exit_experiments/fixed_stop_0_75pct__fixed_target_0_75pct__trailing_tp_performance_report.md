# Performance report: fixed_stop_0_75pct__fixed_target_0_75pct__trailing_tp

## Run metadata
- Experiment Id: fixed_stop_0_75pct__fixed_target_0_75pct__trailing_tp
- Stop Model: fixed_stop_0_75pct
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
- Final Equity: 104.889013
- Net Pnl: -895.110987
- Total Return Pct: -89.511099
- Max Drawdown Amount: 926.581276
- Max Drawdown Pct: 89.870556
- Recovery Factor: -0.966036
- Sharpe Ratio: -6.064684
- Sortino Ratio: -6.446362
- Cagr Pct: -87.537072
- Calmar Ratio: -0.974035
- Worst Daily Loss: -73.451893
- Worst Daily Loss Pct: -8.000840
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 37.993164
- Max Capital Utilization Pct: 101.735185
- Max Gross Exposure: 1,031.966533
- Max Gross Exposure Equity Multiple: 1.017352

## Trade performance

- Trade Count: 4328
- Net Pnl: -895.110987
- Gross Pnl: -3.240156
- Total Fees: 893.161862
- Funding Pnl: 1.291031
- Winning Trades: 2189
- Losing Trades: 2139
- Breakeven Trades: 0
- Win Rate Pct: 50.577634
- Profit Factor: 0.767183
- Expectancy: -0.206819
- Average Win: 1.347459
- Average Loss: 1.797428
- Payoff Ratio: 0.749659
- Max Consecutive Losses: 17
- Average Duration Minutes: 110.290665
- Median Duration Minutes: 51.000000
- Max Duration Minutes: 3,168.000000
- Recovery Factor: -0.966036

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 882 | -99.708151 | 24.615335 | 124.514369 | 0.190883 | 50.000000 | 0.813065 | -0.113048 | 0.983394 | 1.209490 | 0.813065 |
| BTC | 633 | -107.797082 | 21.224362 | 129.126488 | 0.105045 | 52.922591 | 0.803793 | -0.170296 | 1.318230 | 1.843638 | 0.715016 |
| DOGE | 999 | -231.843203 | -6.622120 | 225.829684 | 0.608601 | 50.150150 | 0.762682 | -0.232075 | 1.487198 | 1.961706 | 0.758115 |
| ETH | 761 | -244.720597 | -59.735868 | 184.920492 | -0.064238 | 50.197109 | 0.694681 | -0.321578 | 1.457598 | 2.114837 | 0.689225 |
| SOL | 1053 | -211.041953 | 17.278136 | 228.770829 | 0.450740 | 50.332384 | 0.785408 | -0.200420 | 1.457387 | 1.880415 | 0.775035 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1484 | -406.127417 | -82.452937 | 322.499251 | -1.175230 | 48.315364 | 0.714766 | -0.273671 | 1.419401 | 1.856373 | 0.764610 |
| SHORT | 2844 | -488.983569 | 79.212781 | 570.662611 | 2.466261 | 51.758087 | 0.798013 | -0.171935 | 1.312416 | 1.764476 | 0.743800 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 273 | -60.491251 | -20.322133 | 40.064799 | -0.104319 | 45.054945 | 0.670929 | -0.221580 | 1.002709 | 1.225496 | 0.818206 |
| AVAX | SHORT | 609 | -39.216900 | 44.937468 | 84.449570 | 0.295202 | 52.216749 | 0.887811 | -0.064396 | 0.975924 | 1.201239 | 0.812431 |
| BTC | LONG | 229 | -28.589302 | 23.310943 | 51.428267 | -0.471978 | 52.401747 | 0.863457 | -0.124844 | 1.506586 | 1.920914 | 0.784307 |
| BTC | SHORT | 404 | -79.207780 | -2.086581 | 77.698221 | 0.577023 | 53.217822 | 0.767053 | -0.196059 | 1.213102 | 1.799072 | 0.674293 |
| DOGE | LONG | 237 | -68.554049 | -20.233393 | 47.944130 | -0.376527 | 46.835443 | 0.684039 | -0.289258 | 1.337079 | 1.721983 | 0.776476 |
| DOGE | SHORT | 762 | -163.289154 | 13.611272 | 177.885554 | 0.985128 | 51.181102 | 0.785134 | -0.214290 | 1.529925 | 2.042902 | 0.748897 |
| ETH | LONG | 311 | -93.955214 | -20.090730 | 73.492543 | -0.371942 | 49.839228 | 0.700390 | -0.302107 | 1.417010 | 2.010204 | 0.704909 |
| ETH | SHORT | 450 | -150.765383 | -39.645138 | 111.427949 | 0.307704 | 50.444444 | 0.691011 | -0.335034 | 1.485312 | 2.188033 | 0.678835 |
| SOL | LONG | 434 | -154.537601 | -45.117625 | 109.569512 | 0.149536 | 47.926267 | 0.690970 | -0.356077 | 1.661226 | 2.212710 | 0.750765 |
| SOL | SHORT | 619 | -56.504352 | 62.395761 | 119.201317 | 0.301204 | 52.019386 | 0.883107 | -0.091283 | 1.325714 | 1.627557 | 0.814543 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | -0.317302 | 0.061114 | -0.000338 | -0.378755 |
| stop | 2130 | -3,399.049898 | 441.854371 | 0.528262 | -3,840.376007 |
| stop_gap | 4 | -3.212805 | 0.414760 | -0.016577 | -3.644142 |
| trailing_take_profit | 2018 | 3,069.246555 | 414.390427 | 0.766166 | 2,655.622294 |
| trailing_take_profit_gap | 175 | 330.093294 | 36.441189 | 0.013518 | 293.665623 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 969.615361 | -30.384639 | -3.038464 | False |
| 2025-12 | 969.615361 | 785.251318 | -184.364043 | -19.014142 | False |
| 2026-01 | 785.251318 | 741.903528 | -43.347790 | -5.520244 | False |
| 2026-02 | 741.903528 | 629.870623 | -112.032905 | -15.100738 | False |
| 2026-03 | 629.870623 | 459.581113 | -170.289510 | -27.035633 | False |
| 2026-04 | 459.581113 | 399.246014 | -60.335099 | -13.128281 | False |
| 2026-05 | 399.246014 | 323.519633 | -75.726381 | -18.967348 | False |
| 2026-06 | 323.519633 | 281.106865 | -42.412768 | -13.109797 | False |
| 2026-07 | 281.106865 | 224.454221 | -56.652644 | -20.153419 | False |
| 2026-08 | 224.454221 | 212.798579 | -11.655643 | -5.192882 | False |
| 2026-09 | 212.798579 | 144.490674 | -68.307904 | -32.099793 | False |
| 2026-10 | 144.490674 | 118.035003 | -26.455672 | -18.309605 | False |
| 2026-11 | 118.035003 | 104.889013 | -13.145989 | -11.137365 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
