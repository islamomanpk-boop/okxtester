# Performance report: fixed_stop_0_50pct__fixed_target_2_00pct

## Run metadata
- Experiment Id: fixed_stop_0_50pct__fixed_target_2_00pct
- Stop Model: fixed_stop_0_50pct
- Target Model: fixed_target_2_00pct
- Target Value: 0.020000
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
- Final Equity: 205.452011
- Net Pnl: -794.547989
- Total Return Pct: -79.454799
- Max Drawdown Amount: 866.021559
- Max Drawdown Pct: 81.707536
- Recovery Factor: -0.917469
- Sharpe Ratio: -3.530877
- Sortino Ratio: -4.073201
- Cagr Pct: -76.811580
- Calmar Ratio: -0.940080
- Worst Daily Loss: -94.930764
- Worst Daily Loss Pct: -9.067624
- Worst Daily Loss Date Utc: 2025-11-18
- Max Concurrent Positions: 5
- Average Capital Utilization Pct: 48.030453
- Max Capital Utilization Pct: 102.535768
- Max Gross Exposure: 1,055.620101
- Max Gross Exposure Equity Multiple: 1.025358

## Trade performance

- Trade Count: 3332
- Net Pnl: -794.547989
- Gross Pnl: 169.057180
- Total Fees: 966.098173
- Funding Pnl: 2.493004
- Winning Trades: 737
- Losing Trades: 2595
- Breakeven Trades: 0
- Win Rate Pct: 22.118848
- Profit Factor: 0.830969
- Expectancy: -0.238460
- Average Win: 5.299959
- Average Loss: 1.811414
- Payoff Ratio: 2.925869
- Max Consecutive Losses: 66
- Average Duration Minutes: 171.172869
- Median Duration Minutes: 51.000000
- Max Duration Minutes: 5,020.000000
- Recovery Factor: -0.917469

## Per-asset performance

| asset | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | 672 | -236.284950 | -87.119541 | 149.247476 | 0.082067 | 19.940476 | 0.686831 | -0.351615 | 3.867256 | 1.402411 | 2.757576 |
| BTC | 492 | -59.313276 | 79.366196 | 138.994703 | 0.315232 | 24.390244 | 0.910364 | -0.120555 | 5.020026 | 1.778807 | 2.822130 |
| DOGE | 767 | -121.520410 | 125.415443 | 248.512801 | 1.576949 | 23.598435 | 0.897765 | -0.158436 | 5.895671 | 2.028391 | 2.906576 |
| ETH | 604 | -230.014368 | -42.817163 | 187.120485 | -0.076720 | 20.695364 | 0.752575 | -0.380818 | 5.596949 | 1.940779 | 2.883868 |
| SOL | 797 | -147.414986 | 94.212245 | 242.222708 | 0.595476 | 22.208281 | 0.873587 | -0.184962 | 5.755478 | 1.880862 | 3.060021 |

## LONG versus SHORT

| side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LONG | 1085 | -332.030347 | 32.340879 | 362.109690 | -2.261535 | 20.921659 | 0.812471 | -0.306019 | 6.337099 | 2.063580 | 3.070924 |
| SHORT | 2247 | -462.517642 | 136.716301 | 603.988483 | 4.754539 | 22.696929 | 0.842148 | -0.205838 | 4.838331 | 1.686855 | 2.868256 |

## Asset and direction

| asset | side | trade_count | net_pnl | gross_pnl | total_fees | funding_pnl | win_rate_pct | profit_factor | expectancy | average_win | average_loss | payoff_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AVAX | LONG | 201 | -78.026314 | -28.945937 | 48.806447 | -0.273931 | 17.412935 | 0.684243 | -0.388191 | 4.830932 | 1.488608 | 3.245268 |
| AVAX | SHORT | 471 | -158.258636 | -58.173605 | 100.441029 | 0.355998 | 21.019108 | 0.688092 | -0.336006 | 3.526562 | 1.363947 | 2.585557 |
| BTC | LONG | 170 | 24.379573 | 85.411504 | 60.403244 | -0.628686 | 24.705882 | 1.088526 | 0.143409 | 7.137503 | 2.151528 | 3.317412 |
| BTC | SHORT | 322 | -83.692849 | -6.045308 | 78.591459 | 0.943918 | 24.223602 | 0.783359 | -0.259916 | 3.879845 | 1.583282 | 2.450508 |
| DOGE | LONG | 183 | -41.909006 | 22.433895 | 63.611210 | -0.731691 | 21.857923 | 0.863474 | -0.229011 | 6.626431 | 2.146617 | 3.086918 |
| DOGE | SHORT | 584 | -79.611404 | 102.981548 | 184.901592 | 2.308640 | 24.143836 | 0.909704 | -0.136321 | 5.688363 | 1.990227 | 2.858148 |
| ETH | LONG | 229 | -121.451166 | -48.046112 | 72.687967 | -0.717087 | 20.524017 | 0.670931 | -0.530354 | 5.268584 | 2.027883 | 2.598072 |
| ETH | SHORT | 375 | -108.563202 | 5.228949 | 114.432518 | 0.640367 | 20.800000 | 0.806330 | -0.289502 | 5.794810 | 1.887402 | 3.070257 |
| SOL | LONG | 302 | -115.023434 | 1.487528 | 116.600823 | 0.089860 | 20.860927 | 0.798912 | -0.380872 | 7.253697 | 2.393332 | 3.030794 |
| SOL | SHORT | 495 | -32.391552 | 92.724717 | 125.621885 | 0.505616 | 23.030303 | 0.945481 | -0.065437 | 4.927515 | 1.559392 | 3.159895 |

## Exit reasons

| exit_reason | trade_count | gross_pnl | total_fees | funding_pnl | net_pnl |
| --- | --- | --- | --- | --- | --- |
| end_of_data | 1 | 0.009699 | 0.166117 | 0.000000 | -0.156418 |
| stop | 2586 | -3,936.810510 | 757.530718 | 1.719391 | -4,692.621837 |
| stop_gap | 8 | -6.597004 | 1.252226 | 0.009419 | -7.839811 |
| target | 736 | 4,112.418670 | 207.147296 | 0.764194 | 3,906.035567 |
| target_gap | 1 | 0.036325 | 0.001816 | 0.000000 | 0.034509 |

## Monthly UTC returns

| month_utc | starting_equity | ending_equity | net_pnl | return_pct | partial_month |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 1,000.000000 | 1,000.000000 | 0.000000 | 0.000000 | True |
| 2025-11 | 1,000.000000 | 961.932923 | -38.067077 | -3.806708 | False |
| 2025-12 | 961.932923 | 947.147692 | -14.785231 | -1.537034 | False |
| 2026-01 | 947.147692 | 922.267717 | -24.879975 | -2.626832 | False |
| 2026-02 | 922.267717 | 799.165125 | -123.102591 | -13.347815 | False |
| 2026-03 | 799.165125 | 654.598059 | -144.567066 | -18.089762 | False |
| 2026-04 | 654.598059 | 577.601043 | -76.997016 | -11.762488 | False |
| 2026-05 | 577.601043 | 489.429106 | -88.171938 | -15.265197 | False |
| 2026-06 | 489.429106 | 469.839995 | -19.589111 | -4.002441 | False |
| 2026-07 | 469.839995 | 396.290203 | -73.549792 | -15.654221 | False |
| 2026-08 | 396.290203 | 385.547615 | -10.742588 | -2.710788 | False |
| 2026-09 | 385.547615 | 230.081033 | -155.466582 | -40.323575 | False |
| 2026-10 | 230.081033 | 208.413461 | -21.667572 | -9.417366 | False |
| 2026-11 | 208.413461 | 205.452011 | -2.961450 | -1.420949 | True |

## Important simulation limitations

- End-of-data closures are forced simulation closures, not ordinary strategy exits.
- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.
- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.
- Historical backtest results do not establish a predictive edge or guarantee future performance.
