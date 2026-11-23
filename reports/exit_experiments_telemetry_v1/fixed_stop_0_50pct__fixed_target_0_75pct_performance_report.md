# Performance report: fixed_stop_0_50pct__fixed_target_0_75pct

## Run metadata
- Experiment Id: fixed_stop_0_50pct__fixed_target_0_75pct
- Stop Model: fixed_stop_0_50pct
- Target Model: fixed_target_0_75pct
- Target Value: 0.007500
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
- Trade Telemetry Version: trailing_exit_telemetry_v1
- Risk Fraction: 0.005000
- Max Gross Leverage: 1.000000
- End Of Data Policy: Open positions forcibly closed at final available candle

## Portfolio risk and return

- Initial Equity: 1,000.000000
- Final Equity: 24.241370
- Net Pnl: -975.758630
- Total Return Pct: -97.575863
- Max Drawdown Amount: 996.320422
- Max Drawdown Pct: 97.626744
- Recovery Factor: -0.979362
- Sharpe Ratio: -9.145419
- Sortino Ratio: -8.588104
- Cagr Pct: -96.778198
- Calmar Ratio: -0.991308
- Worst Daily Loss: -73.938794
- Worst Daily Loss Pct: -8.895924
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 39.867898
- Max Capital Utilization Pct: 101.709751
- Max Gross Exposure: 1,019.625158
- Max Gross Exposure Equity Multiple: 1.017098

## Trade performance

- Trade Count: 5976
- Net Pnl: -975.758630
- Gross Pnl: -20.999966
- Total Fees: 955.900336
- Funding Pnl: 1.141673
- Winning Trades: 2424
- Losing Trades: 3552
- Breakeven Trades: 0
- Win Rate Pct: 40.562249
- Profit Factor: 0.718956
- Expectancy: -0.163280
- Average Win: 1.029764
- Average Loss: 0.977451
- Payoff Ratio: 1.053520
- Max Consecutive Losses: 24
- Average Duration Minutes: 71.072456
- Median Duration Minutes: 31.000000
- Max Duration Minutes: 3,160.000000
- Recovery Factor: -0.979362

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1197 | -152.111810 | -30.873022 | 121.322839 | 0.084051 | 40.016708 | 0.665413 | -0.127078 | 0.631553 | 0.633184 | 0.997425 |
| BTC | 890 | -114.580419 | 26.500599 | 141.139220 | 0.058201 | 41.910112 | 0.769818 | -0.128742 | 1.027350 | 0.962828 | 1.067013 |
| DOGE | 1361 | -247.004957 | -3.424741 | 244.045544 | 0.465328 | 40.999265 | 0.721134 | -0.181488 | 1.144702 | 1.103049 | 1.037761 |
| ETH | 1051 | -230.231302 | -24.229963 | 205.895872 | -0.105468 | 39.581351 | 0.696158 | -0.219059 | 1.268032 | 1.193280 | 1.062644 |
| SOL | 1477 | -231.830140 | 11.027161 | 243.496862 | 0.639561 | 40.487475 | 0.735359 | -0.156960 | 1.077235 | 0.996606 | 1.080904 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2086 | -360.855950 | -37.214878 | 323.064288 | -0.576784 | 39.165868 | 0.696212 | -0.172989 | 1.012240 | 0.936057 | 1.081387 |
| SHORT | 3890 | -614.902680 | 16.214911 | 632.836048 | 1.718457 | 41.311054 | 0.730784 | -0.158073 | 1.038673 | 1.000460 | 1.038195 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 362 | -52.409422 | -19.125230 | 33.196639 | -0.087553 | 38.121547 | 0.595869 | -0.144777 | 0.559962 | 0.578947 | 0.967207 |
| AVAX | SHORT | 835 | -99.702389 | -11.747792 | 88.126200 | 0.171603 | 40.838323 | 0.693168 | -0.119404 | 0.660526 | 0.657777 | 1.004179 |
| BTC | LONG | 336 | -31.132082 | 22.715923 | 53.648275 | -0.199730 | 41.964286 | 0.829741 | -0.092655 | 1.076020 | 0.937697 | 1.147514 |
| BTC | SHORT | 554 | -83.448338 | 3.784676 | 87.490945 | 0.257931 | 41.877256 | 0.735027 | -0.150629 | 0.997771 | 0.978047 | 1.020166 |
| DOGE | LONG | 327 | -48.859606 | -9.547370 | 39.042292 | -0.269944 | 39.449541 | 0.665797 | -0.149418 | 0.754556 | 0.738371 | 1.021921 |
| DOGE | SHORT | 1034 | -198.145351 | 6.122629 | 205.003253 | 0.735272 | 41.489362 | 0.732074 | -0.191630 | 1.262018 | 1.222399 | 1.032411 |
| ETH | LONG | 453 | -95.251214 | -20.434139 | 74.537572 | -0.279503 | 38.189845 | 0.659900 | -0.210268 | 1.068305 | 1.000243 | 1.068046 |
| ETH | SHORT | 598 | -134.980089 | -3.795824 | 131.358299 | 0.174035 | 40.635452 | 0.717417 | -0.225719 | 1.410224 | 1.345534 | 1.048078 |
| SOL | LONG | 608 | -133.203626 | -10.824062 | 122.639510 | 0.259946 | 38.815789 | 0.703369 | -0.219085 | 1.338355 | 1.207138 | 1.108701 |
| SOL | SHORT | 869 | -98.626514 | 21.851222 | 120.857352 | 0.379616 | 41.657077 | 0.769004 | -0.113494 | 0.907002 | 0.842133 | 1.077030 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | 0.001144 | 0.019600 | 0.000000 | -0.018456 |
| stop | 3538 | -2,907.268507 | 559.515596 | 0.345163 | -3,466.438940 |
| stop_gap | 13 | -4.586700 | 0.871285 | 0.009559 | -5.448426 |
| target | 2421 | 2,890.592010 | 395.458091 | 0.786951 | 2,495.920870 |
| target_gap | 3 | 0.262086 | 0.035764 | 0.000000 | 0.226322 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 883.236730 | -116.763270 | -11.676327 | False |
| 2025-12 | 883.236730 | 665.277925 | -217.958805 | -24.677280 | False |
| 2026-01 | 665.277925 | 568.431926 | -96.845999 | -14.557224 | False |
| 2026-02 | 568.431926 | 430.417022 | -138.014904 | -24.279935 | False |
| 2026-03 | 430.417022 | 258.881013 | -171.536009 | -39.853444 | False |
| 2026-04 | 258.881013 | 188.647212 | -70.233801 | -27.129761 | False |
| 2026-05 | 188.647212 | 151.082064 | -37.565148 | -19.912909 | False |
| 2026-06 | 151.082064 | 115.062687 | -36.019377 | -23.840935 | False |
| 2026-07 | 115.062687 | 85.678695 | -29.383992 | -25.537377 | False |
| 2026-08 | 85.678695 | 70.588924 | -15.089771 | -17.612046 | False |
| 2026-09 | 70.588924 | 40.414709 | -30.174215 | -42.746388 | False |
| 2026-10 | 40.414709 | 31.141789 | -9.272920 | -22.944418 | False |
| 2026-11 | 31.141789 | 24.241370 | -6.900418 | -22.158067 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
