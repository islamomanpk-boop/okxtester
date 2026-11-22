# Multi-Day Close-to-Close Pump and Dump Frequency — Five Assets (V1)

**Status:** Descriptive research; not a backtest or trading signal.  
**Assets:** BTC, ETH, SOL, DOGE, AVAX  
**Daily data:** 394 complete UTC daily candles per asset, built from the 569,125 common 1-minute timestamps.  
**Windows:** Rolling 2, 3, 5 and 7 complete-day close-to-close returns.  
**Thresholds:** 3%, 5%, 7%, 10%, 15%, separately for pumps and dumps.  
**Execution:** Read-only; no files were written or changed.

## Method

For a window of N days, the measured return is:

`(close[t] / close[t-N] - 1) * 100`

A pump qualifies when the return is greater than or equal to the positive threshold. A dump qualifies when the return is less than or equal to the negative threshold. The reported dump percentage is the magnitude threshold, not a positive return.

The number of measured rolling windows is 392 for 2D, 391 for 3D, 389 for 5D, and 387 for 7D. Percentages below are the count of qualifying rolling windows divided by the number of measured windows.

## BTC

| Window | Threshold | Pump count (%) | Dump count (%) |
|---|---:|---:|---:|
| 2D | 3% | 49 (12.5%) | 63 (16.1%) |
| 2D | 5% | 18 (4.6%) | 21 (5.4%) |
| 2D | 7% | 5 (1.3%) | 9 (2.3%) |
| 2D | 10% | 3 (0.8%) | 3 (0.8%) |
| 2D | 15% | 0 (0.0%) | 1 (0.3%) |
| 3D | 3% | 63 (16.1%) | 78 (19.9%) |
| 3D | 5% | 23 (5.9%) | 39 (10.0%) |
| 3D | 7% | 7 (1.8%) | 16 (4.1%) |
| 3D | 10% | 6 (1.5%) | 5 (1.3%) |
| 3D | 15% | 1 (0.3%) | 1 (0.3%) |
| 5D | 3% | 77 (19.8%) | 105 (27.0%) |
| 5D | 5% | 37 (9.5%) | 55 (14.1%) |
| 5D | 7% | 19 (4.9%) | 31 (8.0%) |
| 5D | 10% | 8 (2.1%) | 14 (3.6%) |
| 5D | 15% | 4 (1.0%) | 2 (0.5%) |
| 7D | 3% | 87 (22.5%) | 117 (30.2%) |
| 7D | 5% | 50 (12.9%) | 75 (19.4%) |
| 7D | 7% | 23 (5.9%) | 43 (11.1%) |
| 7D | 10% | 12 (3.1%) | 25 (6.5%) |
| 7D | 15% | 6 (1.6%) | 7 (1.8%) |

## ETH

| Window | Threshold | Pump count (%) | Dump count (%) |
|---|---:|---:|---:|
| 2D | 3% | 65 (16.6%) | 93 (23.7%) |
| 2D | 5% | 37 (9.4%) | 39 (9.9%) |
| 2D | 7% | 19 (4.8%) | 21 (5.4%) |
| 2D | 10% | 7 (1.8%) | 9 (2.3%) |
| 2D | 15% | 2 (0.5%) | 3 (0.8%) |
| 3D | 3% | 83 (21.2%) | 110 (28.1%) |
| 3D | 5% | 52 (13.3%) | 59 (15.1%) |
| 3D | 7% | 28 (7.2%) | 41 (10.5%) |
| 3D | 10% | 9 (2.3%) | 13 (3.3%) |
| 3D | 15% | 3 (0.8%) | 4 (1.0%) |
| 5D | 3% | 91 (23.4%) | 113 (29.0%) |
| 5D | 5% | 67 (17.2%) | 83 (21.3%) |
| 5D | 7% | 41 (10.5%) | 61 (15.7%) |
| 5D | 10% | 20 (5.1%) | 29 (7.5%) |
| 5D | 15% | 5 (1.3%) | 9 (2.3%) |
| 7D | 3% | 97 (25.1%) | 134 (34.6%) |
| 7D | 5% | 67 (17.3%) | 102 (26.4%) |
| 7D | 7% | 44 (11.4%) | 74 (19.1%) |
| 7D | 10% | 25 (6.5%) | 47 (12.1%) |
| 7D | 15% | 8 (2.1%) | 15 (3.9%) |

## SOL

| Window | Threshold | Pump count (%) | Dump count (%) |
|---|---:|---:|---:|
| 2D | 3% | 86 (21.9%) | 98 (25.0%) |
| 2D | 5% | 42 (10.7%) | 55 (14.0%) |
| 2D | 7% | 20 (5.1%) | 24 (6.1%) |
| 2D | 10% | 8 (2.0%) | 9 (2.3%) |
| 2D | 15% | 0 (0.0%) | 2 (0.5%) |
| 3D | 3% | 93 (23.8%) | 124 (31.7%) |
| 3D | 5% | 60 (15.3%) | 76 (19.4%) |
| 3D | 7% | 30 (7.7%) | 42 (10.7%) |
| 3D | 10% | 11 (2.8%) | 19 (4.9%) |
| 3D | 15% | 3 (0.8%) | 5 (1.3%) |
| 5D | 3% | 97 (24.9%) | 137 (35.2%) |
| 5D | 5% | 67 (17.2%) | 92 (23.7%) |
| 5D | 7% | 51 (13.1%) | 62 (15.9%) |
| 5D | 10% | 26 (6.7%) | 37 (9.5%) |
| 5D | 15% | 10 (2.6%) | 15 (3.9%) |
| 7D | 3% | 102 (26.4%) | 156 (40.3%) |
| 7D | 5% | 74 (19.1%) | 114 (29.5%) |
| 7D | 7% | 54 (14.0%) | 80 (20.7%) |
| 7D | 10% | 36 (9.3%) | 53 (13.7%) |
| 7D | 15% | 14 (3.6%) | 25 (6.5%) |

## DOGE

| Window | Threshold | Pump count (%) | Dump count (%) |
|---|---:|---:|---:|
| 2D | 3% | 65 (16.6%) | 105 (26.8%) |
| 2D | 5% | 43 (11.0%) | 57 (14.5%) |
| 2D | 7% | 23 (5.9%) | 28 (7.1%) |
| 2D | 10% | 10 (2.6%) | 7 (1.8%) |
| 2D | 15% | 4 (1.0%) | 1 (0.3%) |
| 3D | 3% | 82 (21.0%) | 132 (33.8%) |
| 3D | 5% | 50 (12.8%) | 83 (21.2%) |
| 3D | 7% | 28 (7.2%) | 40 (10.2%) |
| 3D | 10% | 13 (3.3%) | 13 (3.3%) |
| 3D | 15% | 7 (1.8%) | 3 (0.8%) |
| 5D | 3% | 73 (18.8%) | 167 (42.9%) |
| 5D | 5% | 59 (15.2%) | 112 (28.8%) |
| 5D | 7% | 36 (9.3%) | 73 (18.8%) |
| 5D | 10% | 21 (5.4%) | 31 (8.0%) |
| 5D | 15% | 12 (3.1%) | 5 (1.3%) |
| 7D | 3% | 75 (19.4%) | 179 (46.3%) |
| 7D | 5% | 62 (16.0%) | 135 (34.9%) |
| 7D | 7% | 44 (11.4%) | 93 (24.0%) |
| 7D | 10% | 30 (7.8%) | 48 (12.4%) |
| 7D | 15% | 16 (4.1%) | 12 (3.1%) |

## AVAX

| Window | Threshold | Pump count (%) | Dump count (%) |
|---|---:|---:|---:|
| 2D | 3% | 90 (23.0%) | 102 (26.0%) |
| 2D | 5% | 41 (10.5%) | 64 (16.3%) |
| 2D | 7% | 23 (5.9%) | 39 (9.9%) |
| 2D | 10% | 10 (2.6%) | 12 (3.1%) |
| 2D | 15% | 5 (1.3%) | 4 (1.0%) |
| 3D | 3% | 94 (24.0%) | 130 (33.2%) |
| 3D | 5% | 57 (14.6%) | 83 (21.2%) |
| 3D | 7% | 37 (9.5%) | 49 (12.5%) |
| 3D | 10% | 15 (3.8%) | 22 (5.6%) |
| 3D | 15% | 4 (1.0%) | 5 (1.3%) |
| 5D | 3% | 97 (24.9%) | 151 (38.8%) |
| 5D | 5% | 64 (16.5%) | 105 (27.0%) |
| 5D | 7% | 40 (10.3%) | 73 (18.8%) |
| 5D | 10% | 21 (5.4%) | 40 (10.3%) |
| 5D | 15% | 10 (2.6%) | 10 (2.6%) |
| 7D | 3% | 98 (25.3%) | 162 (41.9%) |
| 7D | 5% | 64 (16.5%) | 122 (31.5%) |
| 7D | 7% | 53 (13.7%) | 88 (22.7%) |
| 7D | 10% | 30 (7.8%) | 53 (13.7%) |
| 7D | 15% | 14 (3.6%) | 21 (5.4%) |

## Descriptive observations

1. In this sample, qualifying multi-day dumps are more frequent than qualifying pumps for most assets, windows and thresholds. There are some exceptions at the largest DOGE pump thresholds and isolated other cells.
2. DOGE stands out for downside frequency over longer windows: 7D declines of at least 3% occurred in 46.3% of rolling windows; declines of at least 5% occurred in 34.9%.
3. SOL and AVAX also show frequent larger downside windows. For 7D moves of at least 10%, SOL had 13.7% dump windows and AVAX 13.7%; their pump windows were 9.3% and 7.8%, respectively.
4. BTC has the lowest frequency of many large multi-day movements in this five-asset comparison, particularly at the longer thresholds, although it still experienced some large moves.
5. DOGE has more 7D pump windows of at least 15% (4.1%) than 7D dump windows of at least 15% (3.1%) in this sample. This is a frequency comparison, not evidence of a directional edge.
6. Counts generally rise with longer windows because there is more time for cumulative close-to-close movement. This does not mean that each longer window is an independent event.

## Critical limitations

- These are **rolling windows**, not unique independent events. Adjacent windows share most of their daily returns, so one sustained move can qualify many times. Counts must not be described as counts of separate market events.
- Thresholds are nested: a 10% window also qualifies for 7%, 5%, and 3%. Do not add counts across thresholds.
- The return is close-to-close. It does not measure the maximum high/low excursion during the multi-day period.
- These frequencies do not describe what happens after a move. A separate post-confirmation follow-up study is required.
- The study is descriptive, with no execution, fees, slippage, funding, or profitability modelling.
- The daily sample contains 394 complete UTC days. Extreme-threshold frequencies are based on relatively few qualifying windows and are uncertain.
- The original exchange/API/instrument provenance of the 1-minute CSVs remains unverified.

## Next research step

Study the reaction **after** a multi-day move has been confirmed at the close: next-day, 3-day and 7-day continuation, pullback/rebound, and full reversal. Use event-window highs/lows for descriptive impulse retracement, but separately measure the path from the confirmation close so that post-confirmation results are causally available. Report raw overlapping triggers and a clearly defined non-overlapping-event sensitivity; do not silently count overlapping windows as independent events.

No strategy backtests or experiments are authorized by this note.
