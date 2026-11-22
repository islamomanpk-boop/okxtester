# 15M and 4H Normal Candle Movement — Empirical Results V1

Date recorded: 2026-11-22  
Project: Price Action V1  
Branch: `price-action-v1`

## Purpose

Describe ordinary 15-minute and 4-hour OHLC movement for BTC, ETH, SOL, DOGE, and AVAX using the existing one-minute datasets. This is a descriptive baseline, not a sideways-market classification and not a strategy or profitability test.

## Data and method

- Source files: `~/okx_scalping_data/{BTC,ETH,SOL,DOGE,AVAX}_USDT_USDT_1m.csv`.
- Read-only calculation; no local files were written or changed.
- Inner-joined the five assets on common minute timestamps: 569,125 common candles.
- Resampled each asset independently using UTC-aligned epoch boundaries, left-labelled and left-closed.
- Kept only fully observed 15M candles (15 common minute observations) and 4H candles (240 common minute observations).
- Each asset had 37,941 complete 15M candles and 2,370 complete 4H candles.
- Candle range = (high - low) / open × 100.
- Candle body = absolute(close / open - 1) × 100.
- Close move = absolute percentage change from the previous resampled candle close.
- Threshold frequencies count candles with range or body greater than or equal to 0.25%, 0.50%, 1.00%, or 2.00%.

## 15-minute results

| Asset | Mean range | Median range | P75 range | P90 range | P95 range | Mean body | Median body | P75 body | P90 body | P95 body |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | 0.307% | 0.239% | 0.382% | 0.588% | 0.762% | 0.151% | 0.097% | 0.193% | 0.342% | 0.472% |
| ETH | 0.425% | 0.324% | 0.519% | 0.810% | 1.077% | 0.200% | 0.126% | 0.250% | 0.449% | 0.631% |
| SOL | 0.484% | 0.385% | 0.588% | 0.884% | 1.140% | 0.233% | 0.154% | 0.297% | 0.515% | 0.705% |
| DOGE | 0.494% | 0.388% | 0.590% | 0.904% | 1.173% | 0.237% | 0.157% | 0.302% | 0.520% | 0.722% |
| AVAX | 0.518% | 0.413% | 0.631% | 0.943% | 1.208% | 0.259% | 0.174% | 0.335% | 0.578% | 0.788% |

### 15M threshold frequencies

Each cell is count (percentage of 37,941 candles).

| Asset | Range ≥0.25% | Range ≥0.50% | Range ≥1.00% | Range ≥2.00% | Body ≥0.25% | Body ≥0.50% | Body ≥1.00% | Body ≥2.00% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | 17,962 (47.3%) | 5,476 (14.4%) | 839 (2.2%) | 68 (0.2%) | 6,530 (17.2%) | 1,669 (4.4%) | 234 (0.6%) | 16 (0.0%) |
| ETH | 24,734 (65.2%) | 10,111 (26.6%) | 2,287 (6.0%) | 286 (0.8%) | 9,481 (25.0%) | 3,091 (8.1%) | 630 (1.7%) | 80 (0.2%) |
| SOL | 28,964 (76.3%) | 12,798 (33.7%) | 2,744 (7.2%) | 331 (0.9%) | 11,859 (31.3%) | 4,034 (10.6%) | 763 (2.0%) | 85 (0.2%) |
| DOGE | 29,254 (77.1%) | 12,830 (33.8%) | 2,935 (7.7%) | 394 (1.0%) | 12,122 (31.9%) | 4,088 (10.8%) | 823 (2.2%) | 104 (0.3%) |
| AVAX | 30,482 (80.3%) | 14,297 (37.7%) | 3,221 (8.5%) | 396 (1.0%) | 13,624 (35.9%) | 5,000 (13.2%) | 977 (2.6%) | 106 (0.3%) |

## 4-hour results

| Asset | Mean range | Median range | P75 range | P90 range | P95 range | Mean body | Median body | P75 body | P90 body | P95 body |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | 1.316% | 1.083% | 1.652% | 2.465% | 3.027% | 0.609% | 0.399% | 0.797% | 1.422% | 1.892% |
| ETH | 1.826% | 1.480% | 2.258% | 3.378% | 4.454% | 0.818% | 0.506% | 1.058% | 1.939% | 2.794% |
| SOL | 2.043% | 1.664% | 2.553% | 3.692% | 4.614% | 0.948% | 0.634% | 1.278% | 2.206% | 2.889% |
| DOGE | 2.102% | 1.699% | 2.613% | 3.794% | 4.790% | 0.947% | 0.613% | 1.266% | 2.220% | 2.902% |
| AVAX | 2.273% | 1.867% | 2.782% | 4.034% | 5.154% | 1.068% | 0.693% | 1.369% | 2.473% | 3.364% |

### 4H threshold frequencies

Each cell is count (percentage of 2,370 candles).

| Asset | Range ≥0.25% | Range ≥0.50% | Range ≥1.00% | Range ≥2.00% | Body ≥0.25% | Body ≥0.50% | Body ≥1.00% | Body ≥2.00% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | 2,332 (98.4%) | 2,083 (87.9%) | 1,296 (54.7%) | 391 (16.5%) | 1,558 (65.7%) | 998 (42.1%) | 434 (18.3%) | 111 (4.7%) |
| ETH | 2,362 (99.7%) | 2,249 (94.9%) | 1,737 (73.3%) | 752 (31.7%) | 1,679 (70.8%) | 1,195 (50.4%) | 631 (26.6%) | 224 (9.5%) |
| SOL | 2,370 (100.0%) | 2,343 (98.9%) | 1,933 (81.6%) | 913 (38.5%) | 1,807 (76.2%) | 1,383 (58.4%) | 795 (33.5%) | 291 (12.3%) |
| DOGE | 2,370 (100.0%) | 2,354 (99.3%) | 1,972 (83.2%) | 924 (39.0%) | 1,841 (77.7%) | 1,370 (57.8%) | 783 (33.0%) | 298 (12.6%) |
| AVAX | 2,370 (100.0%) | 2,367 (99.9%) | 2,100 (88.6%) | 1,073 (45.3%) | 1,879 (79.3%) | 1,462 (61.7%) | 863 (36.4%) | 355 (15.0%) |

## Main descriptive observations

1. Across both timeframes, BTC has the smallest typical candle range and AVAX the largest.
2. ETH, SOL, and DOGE generally sit between BTC and AVAX; SOL and DOGE are close on several 15M measures.
3. The median 15M high-low range spans 0.239% (BTC) to 0.413% (AVAX); median 4H range spans 1.083% to 1.867%.
4. A candle's high-low range is materially larger than its open-to-close body. Range therefore must not be mistaken for directional progress or a capturable move.
5. At 4H, at least 2% high-low range occurred in 16.5% of BTC candles and 45.3% of AVAX candles. These are descriptive full-sample frequencies, not trade signals.
6. This full-sample baseline mixes trending, ranging, high-volatility, and low-volatility periods. It cannot answer how much a coin moves specifically while sideways.

## Interpretation limits and next research step

- This is not a strategy test and says nothing about net profitability after fees, slippage, funding, and execution.
- High-low range does not reveal the order in which highs and lows occurred.
- OHLC candle ranges do not imply that a trader could capture the entire range.
- The sample is one historical period and data provenance remains incompletely verified: project configuration identifies OKX USDT perpetual markets, but the original 1M CSV source/API and instrument identifiers have not been independently established.
- Next: define and compare causal, explicitly confirmed 4H sideways/range states; then measure 15M internal movement only inside those 4H states. Keep range-boundary confirmation and breakout timing free of lookahead. Report range duration, range height, 15M/4H candle movement, boundary tests, excursions, and breakout/failed-breakout outcomes separately.
