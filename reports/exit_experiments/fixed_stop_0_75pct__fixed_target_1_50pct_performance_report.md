# Performance report: fixed_stop_0_75pct__fixed_target_1_50pct

## Run metadata
- Experiment Id: fixed_stop_0_75pct__fixed_target_1_50pct
- Stop Model: fixed_stop_0_75pct
- Target Model: fixed_target_1_50pct
- Target Value: 0.015000
- Trailing Mode: none
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
- Final Equity: 287.672350
- Net Pnl: -712.327650
- Total Return Pct: -71.232765
- Max Drawdown Amount: 794.085399
- Max Drawdown Pct: 76.488811
- Recovery Factor: -0.897042
- Sharpe Ratio: -3.150960
- Sortino Ratio: -3.812110
- Cagr Pct: -68.356893
- Calmar Ratio: -0.893685
- Worst Daily Loss: -75.721143
- Worst Daily Loss Pct: -8.114480
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 43.049724
- Max Capital Utilization Pct: 102.336916
- Max Gross Exposure: 1,044.403671
- Max Gross Exposure Equity Multiple: 1.023369

## Trade performance

- Trade Count: 3000
- Net Pnl: -712.327650
- Gross Pnl: 38.828332
- Total Fees: 752.958885
- Funding Pnl: 1.802904
- Winning Trades: 1064
- Losing Trades: 1936
- Breakeven Trades: 0
- Win Rate Pct: 35.466667
- Profit Factor: 0.834100
- Expectancy: -0.237443
- Average Win: 3.365979
- Average Loss: 2.217835
- Payoff Ratio: 1.517687
- Max Consecutive Losses: 37
- Average Duration Minutes: 189.245000
- Median Duration Minutes: 78.000000
- Max Duration Minutes: 3,707.000000
- Recovery Factor: -0.897042

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 626 | -143.503770 | -17.641891 | 125.945055 | 0.083176 | 34.345048 | 0.802854 | -0.229239 | 2.718159 | 1.771065 | 1.534759 |
| BTC | 437 | -103.206802 | 7.193601 | 110.775612 | 0.375209 | 36.384439 | 0.836408 | -0.236171 | 3.318693 | 2.269349 | 1.462399 |
| DOGE | 678 | -155.438436 | 22.496655 | 178.732765 | 0.797675 | 36.283186 | 0.846781 | -0.229260 | 3.492055 | 2.348343 | 1.487030 |
| ETH | 553 | -201.685464 | -52.883291 | 148.993197 | 0.191024 | 33.453888 | 0.768899 | -0.364712 | 3.627199 | 2.371514 | 1.529486 |
| SOL | 706 | -108.493177 | 79.663257 | 188.512256 | 0.355821 | 36.685552 | 0.896450 | -0.153673 | 3.626440 | 2.343940 | 1.547156 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 970 | -317.482247 | -49.296649 | 266.607200 | -1.578397 | 33.298969 | 0.794474 | -0.327301 | 3.799535 | 2.387530 | 1.591408 |
| SHORT | 2030 | -394.845403 | 88.124981 | 486.351685 | 3.381301 | 36.502463 | 0.856367 | -0.194505 | 3.176993 | 2.132659 | 1.489686 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 193 | -94.128299 | -51.301661 | 42.668174 | -0.158464 | 27.979275 | 0.643615 | -0.487711 | 3.147988 | 1.900141 | 1.656713 |
| AVAX | SHORT | 433 | -49.375471 | 33.659770 | 83.276881 | 0.241639 | 37.182448 | 0.893539 | -0.114031 | 2.573992 | 1.705104 | 1.509581 |
| BTC | LONG | 151 | -54.115520 | -10.945747 | 42.524316 | -0.645457 | 34.437086 | 0.781683 | -0.358381 | 3.726165 | 2.503799 | 1.488205 |
| BTC | SHORT | 286 | -49.091282 | 18.139349 | 68.251297 | 1.020665 | 37.412587 | 0.871825 | -0.171648 | 3.120670 | 2.139681 | 1.458474 |
| DOGE | LONG | 145 | -46.307455 | -7.474217 | 38.258936 | -0.574302 | 33.793103 | 0.791520 | -0.319362 | 3.588001 | 2.313745 | 1.550733 |
| DOGE | SHORT | 533 | -109.130981 | 29.970872 | 140.473829 | 1.371976 | 36.960600 | 0.862272 | -0.204749 | 3.468190 | 2.358228 | 1.470677 |
| ETH | LONG | 212 | -40.879225 | 18.630857 | 59.105958 | -0.404123 | 35.377358 | 0.876445 | -0.192827 | 3.866378 | 2.415019 | 1.600972 |
| ETH | SHORT | 341 | -160.806239 | -71.514147 | 89.887238 | 0.595147 | 32.258065 | 0.703233 | -0.471573 | 3.464122 | 2.345713 | 1.476789 |
| SOL | LONG | 269 | -82.051748 | 1.794120 | 84.049816 | 0.203948 | 34.572491 | 0.828973 | -0.305025 | 4.276423 | 2.725904 | 1.568809 |
| SOL | SHORT | 437 | -26.441429 | 77.869138 | 104.462440 | 0.151873 | 37.986270 | 0.953447 | -0.060507 | 3.262294 | 2.095875 | 1.556530 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | -0.870245 | 0.167615 | -0.000926 | -1.038786 |
| stop | 1934 | -3,799.786928 | 493.984709 | 1.082894 | -4,292.688743 |
| stop_gap | 1 | -0.001619 | 0.000210 | 0.000000 | -0.001829 |
| target | 1063 | 3,839.480665 | 258.805918 | 0.720892 | 3,581.395639 |
| target_gap | 1 | 0.006459 | 0.000433 | 0.000044 | 0.006069 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 982.847729 | -17.152271 | -1.715227 | False |
| 2025-12 | 982.847729 | 805.710739 | -177.136989 | -18.022831 | False |
| 2026-01 | 805.710739 | 792.996716 | -12.714024 | -1.577989 | False |
| 2026-02 | 792.996716 | 730.997829 | -61.998887 | -7.818303 | False |
| 2026-03 | 730.997829 | 587.574332 | -143.423497 | -19.620236 | False |
| 2026-04 | 587.574332 | 545.748042 | -41.826290 | -7.118468 | False |
| 2026-05 | 545.748042 | 446.528634 | -99.219408 | -18.180442 | False |
| 2026-06 | 446.528634 | 440.863556 | -5.665078 | -1.268693 | False |
| 2026-07 | 440.863556 | 368.013256 | -72.850300 | -16.524455 | False |
| 2026-08 | 368.013256 | 399.331195 | 31.317939 | 8.510003 | False |
| 2026-09 | 399.331195 | 287.396613 | -111.934582 | -28.030513 | False |
| 2026-10 | 287.396613 | 257.497801 | -29.898812 | -10.403328 | False |
| 2026-11 | 257.497801 | 287.672350 | 30.174550 | 11.718372 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
