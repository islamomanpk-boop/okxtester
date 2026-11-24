# Sideways Rejection Episode and Retest Anatomy V1 — Rejection Candle Anatomy Addendum

**Date:** 2026-11-24  
**Parent results checkpoint:** `2026-11-24_sideways_rejection_episode_retest_anatomy_v1_results.md`  
**Source:** `event_anatomy_v1.csv` from workflow run 45414635491.

## Purpose

The V1 group summary focuses on post-confirmation path outcomes. This addendum reports descriptive distributions from the event-level 15-minute rejection-candle anatomy file. It introduces no new event definitions or thresholds.

## Broad cohort (n=1,154)

| Measure | Median | 25th percentile | 75th percentile |
|---|---:|---:|---:|
| Rejection range / channel width | 0.135 W | 0.087 W | 0.205 W |
| Body / candle range | 0.510 | 0.300 | 0.683 |
| Outward-facing wick / candle range | 0.319 | 0.154 | 0.513 |
| Inward-facing wick / candle range | 0.116 | 0.037 | 0.236 |
| Signed close distance inward from tested boundary / channel width | 0.134 W | 0.115 W | 0.166 W |

The outward-facing wick is longer than the inward-facing wick in 823/1,154 events (71.3%). This is a geometric description of the source-labelled rejection candles, not an independent validation of rejection quality or future direction.

Only 134/1,154 (11.6%) broad events close more than 0.20 channel widths inward from the tested boundary, using the normalized signed close-distance field. Most rejection closes therefore remain relatively near the tested boundary under this normalization.

## Strict cohort (n=838; nested sensitivity subgroup)

| Measure | Median | 25th percentile | 75th percentile |
|---|---:|---:|---:|
| Rejection range / channel width | 0.141 W | 0.091 W | 0.211 W |
| Body / candle range | 0.513 | 0.303 | 0.686 |
| Outward-facing wick / candle range | 0.320 | 0.152 | 0.513 |
| Inward-facing wick / candle range | 0.111 | 0.034 | 0.228 |
| Signed close distance inward from tested boundary / channel width | 0.135 W | 0.116 W | 0.166 W |

The outward-facing wick is longer in 599/838 (71.5%) strict events. Broad and strict are nested and must not be treated as independent samples.

## Asset variation (broad cohort)

| Asset | Events | Median range / width | Median body / range | Median outward wick / range | Outward wick longer |
|---|---:|---:|---:|---:|---:|
| BTC | 220 | 0.145 | 0.560 | 0.297 | 71.4% |
| ETH | 217 | 0.142 | 0.545 | 0.290 | 66.4% |
| SOL | 242 | 0.121 | 0.500 | 0.310 | 69.8% |
| DOGE | 216 | 0.140 | 0.469 | 0.339 | 74.5% |
| AVAX | 259 | 0.126 | 0.480 | 0.346 | 74.1% |

The medians differ across assets, but the groups are selected historical events and event counts are not independent across time. These are not asset rankings.

## Directional geometry

Broad upper events (n=596) have a median close location within the candle range of 0.320; broad lower events (n=558) have a median of 0.661. This mirror-like difference is consistent with the direction-relative location of a close inside an upper- versus lower-boundary rejection candle. The signed inward close distance is similar: median 0.134 W for both directions.

## Chronological variation

Across 14 monthly buckets (2025-10 through 2026-11), the broad cohort's median rejection range/channel-width ratio varies from 0.101 W to 0.176 W. The fraction with a longer outward-facing wick varies from 52.4% to 74.8%. Some buckets are small (the smallest contains 9 events), so month-to-month variation should not be interpreted as stable regime effects.

## Interpretation limits

- The event ledger already selected events labelled as strong rejections; this addendum does not evaluate the detector's classification against an independent label.
- Wick/body geometry is descriptive and cannot establish the intrabar path, order flow, intent, or executable prices.
- Strict is nested within broad.
- No predictive, causal, or profitability claim is supported.
- No candle-shape threshold or strategy rule is authorized from these distributions.

**Disposition:** Anatomy fields are now summarized at overall, asset, direction, and chronological levels. Proceed to a separately frozen next-stage study only after defining an ex-ante sequence landmark and strictly post-landmark outcomes.
