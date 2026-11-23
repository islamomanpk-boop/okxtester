# Performance report: fees_0_05pct_slippage_5bps

## Run metadata
- Scenario Id: fees_0_05pct_slippage_5bps
- Experiment Id: fixed_stop_0_50pct__fixed_target_0_75pct
- Assets: BTC,ETH,SOL,DOGE,AVAX
- Execution Timeframe: 1m
- Execution Window Start Utc: 2025-10-20T08:50:00+00:00
- Execution Window End Utc: 2026-11-19T14:14:00+00:00
- Taker Fee Rate Per Side: 0.000500
- Slippage Bps Per Side: 5.000000
- Funding Data: Historical asset-specific realized funding rates
- Funding Treatment: Applied at funding timestamps; mark price when supplied, otherwise candle close proxy
- Equity Curve Storage: summary-only
- Risk Fraction: 0.005000
- Max Gross Leverage: 1.000000
- Cost Sensitivity Note: Same signals, date window, exit rules, risk fraction, and portfolio constraints; cost-aware sizing means fills, accepted entries, and outcomes can change.
- End Of Data Policy: Open positions forcibly closed at final available candle

## Portfolio risk and return

- Initial Equity: 1,000.000000
- Final Equity: 3.009207
- Net Pnl: -996.990793
- Total Return Pct: -99.699079
- Max Drawdown Amount: 1,015.176461
- Max Drawdown Pct: 99.704633
- Recovery Factor: -0.982086
- Sharpe Ratio: -12.607252
- Sortino Ratio: -10.606656
- Cagr Pct: -99.530875
- Calmar Ratio: -0.998257
- Worst Daily Loss: -75.195394
- Worst Daily Loss Pct: -10.757447
- Worst Daily Loss Date Utc: 2025-12-03
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 38.734682
- Max Capital Utilization Pct: 101.574126
- Max Gross Exposure: 1,016.559041
- Max Gross Exposure Equity Multiple: 1.015741

## Trade performance

- Trade Count: 6035
- Net Pnl: -996.990793
- Gross Pnl: -392.090699
- Total Fees: 605.541160
- Funding Pnl: 0.641066
- Winning Trades: 2291
- Losing Trades: 3744
- Breakeven Trades: 0
- Win Rate Pct: 37.961889
- Profit Factor: 0.586007
- Expectancy: -0.165201
- Average Win: 0.615994
- Average Loss: 0.643224
- Payoff Ratio: 0.957665
- Max Consecutive Losses: 24
- Average Duration Minutes: 69.110356
- Median Duration Minutes: 30.000000
- Max Duration Minutes: 3,160.000000
- Recovery Factor: -0.982086

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 1210 | -128.876963 | -61.439377 | 67.378521 | -0.059065 | 37.272727 | 0.535300 | -0.106510 | 0.329172 | 0.365394 | 0.900871 |
| BTC | 892 | -119.819880 | -33.869604 | 86.031351 | 0.081075 | 39.349776 | 0.637685 | -0.134327 | 0.600816 | 0.611287 | 0.982870 |
| DOGE | 1399 | -266.853165 | -116.609390 | 150.505901 | 0.262127 | 38.384560 | 0.561553 | -0.190746 | 0.636460 | 0.706070 | 0.901412 |
| ETH | 1053 | -207.357728 | -71.182978 | 136.132500 | -0.042249 | 37.132004 | 0.610741 | -0.196921 | 0.832075 | 0.804682 | 1.034043 |
| SOL | 1481 | -274.083057 | -108.989349 | 165.492887 | 0.399179 | 37.879811 | 0.584005 | -0.185066 | 0.685879 | 0.716153 | 0.957726 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 2111 | -293.918036 | -115.166861 | 178.509374 | -0.241802 | 36.286120 | 0.585682 | -0.139232 | 0.542408 | 0.527437 | 1.028385 |
| SHORT | 3924 | -703.072756 | -276.923838 | 427.031785 | 0.882867 | 38.863405 | 0.586143 | -0.179172 | 0.652956 | 0.708141 | 0.922070 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 363 | -33.445426 | -19.353030 | 14.048840 | -0.043557 | 34.710744 | 0.453674 | -0.092136 | 0.220423 | 0.258307 | 0.853339 |
| AVAX | SHORT | 847 | -95.431537 | -42.086347 | 53.329681 | -0.015509 | 38.370720 | 0.558422 | -0.112670 | 0.371333 | 0.414013 | 0.896912 |
| BTC | LONG | 341 | -31.239223 | -2.225311 | 28.925986 | -0.087925 | 39.589443 | 0.706326 | -0.091611 | 0.556552 | 0.516378 | 1.077801 |
| BTC | SHORT | 551 | -88.580658 | -31.644293 | 57.105364 | 0.169000 | 39.201452 | 0.605137 | -0.160763 | 0.628480 | 0.669649 | 0.938522 |
| DOGE | LONG | 338 | -32.977062 | -16.721162 | 16.139369 | -0.116531 | 36.982249 | 0.511318 | -0.097565 | 0.276036 | 0.316815 | 0.871285 |
| DOGE | SHORT | 1061 | -233.876103 | -99.888228 | 134.366532 | 0.378658 | 38.831291 | 0.567817 | -0.220430 | 0.745812 | 0.833822 | 0.894450 |
| ETH | LONG | 449 | -71.060896 | -27.997975 | 42.902615 | -0.160306 | 34.966592 | 0.583802 | -0.158265 | 0.634888 | 0.584720 | 1.085798 |
| ETH | SHORT | 604 | -136.296832 | -43.185004 | 93.229885 | 0.118057 | 38.741722 | 0.623449 | -0.225657 | 0.964376 | 0.978273 | 0.985795 |
| SOL | LONG | 620 | -125.195430 | -48.869383 | 76.492563 | 0.166517 | 35.967742 | 0.587617 | -0.201928 | 0.799975 | 0.764710 | 1.046116 |
| SOL | SHORT | 861 | -148.887627 | -60.119966 | 89.000323 | 0.232662 | 39.256678 | 0.580918 | -0.172924 | 0.610602 | 0.679295 | 0.898877 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | -0.001258 | 0.002323 | 0.000000 | -0.003582 |
| stop | 3732 | -2,036.675317 | 370.653813 | 0.318506 | -2,407.010625 |
| stop_gap | 11 | -1.032350 | 0.185892 | 0.000000 | -1.218242 |
| target | 2286 | 1,645.232553 | 234.644048 | 0.322560 | 1,410.911065 |
| target_gap | 5 | 0.385674 | 0.055083 | 0.000000 | 0.330591 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 757.362359 | -242.637641 | -24.263764 | False |
| 2025-12 | 757.362359 | 494.566412 | -262.795947 | -34.698839 | False |
| 2026-01 | 494.566412 | 358.019684 | -136.546728 | -27.609382 | False |
| 2026-02 | 358.019684 | 225.976218 | -132.043466 | -36.881622 | False |
| 2026-03 | 225.976218 | 113.723770 | -112.252448 | -49.674452 | False |
| 2026-04 | 113.723770 | 73.635752 | -40.088018 | -35.250342 | False |
| 2026-05 | 73.635752 | 49.258728 | -24.377024 | -33.104875 | False |
| 2026-06 | 49.258728 | 32.396673 | -16.862056 | -34.231610 | False |
| 2026-07 | 32.396673 | 20.685168 | -11.711504 | -36.150331 | False |
| 2026-08 | 20.685168 | 15.146747 | -5.538421 | -26.774842 | False |
| 2026-09 | 15.146747 | 7.345127 | -7.801620 | -51.506900 | False |
| 2026-10 | 7.345127 | 4.772658 | -2.572469 | -35.022803 | False |
| 2026-11 | 4.772658 | 3.009207 | -1.763451 | -36.949027 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
