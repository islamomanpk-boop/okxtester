# Phase 3 Past-Only Threshold Stability and Cross-Asset Alignment Audit V1

**Date:** 2026-11-25  
**Project:** OKX Price Action V1 — Phase 3 Sideways / Range  
**Branch:** `price-action-v1`  
**Status:** PRELIMINARY DESCRIPTIVE AUDIT — no threshold policy selected; no candidate generation, forward-outcome analysis or PnL simulation authorized.

## 1. Purpose

Continue the past-only threshold investigation by measuring (a) how quickly each threshold changes, (b) how often strict/broad descriptive labels switch between adjacent snapshots, and (c) whether the five asset feature ledgers are timestamp-aligned and have broadly comparable descriptive cohort rates.

This is a methodological stability and data-alignment audit only. It is not a predictive or trading-performance comparison.

## 2. Inputs and reproducibility scope

Read-only inputs are the five committed ledgers under `reports/sideways_detector_original_v1/`:

- BTC_features_original_v1.csv
- ETH_features_original_v1.csv
- SOL_features_original_v1.csv
- DOGE_features_original_v1.csv
- AVAX_features_original_v1.csv

Each contains 2,358 rows. The evaluation uses the same first-180-prior-snapshot warm-up and the same two past-only methods from the companion checkpoint:

- Rolling-180: quantile from the immediately preceding 180 completed snapshots.
- Expanding-prior: quantile from all preceding completed snapshots.

Quantiles use linear interpolation. For each current snapshot, strict label = current width <= past-only P25 AND directional_efficiency <= 0.30 AND mean_overlap >= 0.70. Broad label substitutes past-only P40. No future row enters a threshold calculation.

## 3. Threshold movement and label stability

Absolute threshold movement is the absolute difference between adjacent evaluated threshold values, expressed in channel-width percentage points. Label turnover is the number of adjacent-snapshot label changes divided by adjacent evaluated pairs, expressed per 100 snapshots. Mean run length is evaluated snapshots divided by the number of contiguous same-label runs. These are descriptive measures, not measures of signal quality.

| Asset | Method | P25 abs-change median | P25 abs-change P95 | P40 abs-change median | P40 abs-change P95 | Strict turnover /100 | Broad turnover /100 | Strict mean run | Broad mean run |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | Rolling-180 | 0.00000 | 0.05664 | 0.00000 | 0.06970 | 9.92 | 12.95 | 10.04 | 7.70 |
| BTC | Expanding-prior | 0.00080 | 0.01158 | 0.00048 | 0.01101 | 11.48 | 14.42 | 8.68 | 6.91 |
| ETH | Rolling-180 | 0.00000 | 0.09897 | 0.00000 | 0.10027 | 9.65 | 14.15 | 10.32 | 7.05 |
| ETH | Expanding-prior | 0.00139 | 0.02607 | 0.00176 | 0.02643 | 11.39 | 15.99 | 8.75 | 6.24 |
| SOL | Rolling-180 | 0.00000 | 0.09787 | 0.00000 | 0.10647 | 10.66 | 14.88 | 9.35 | 6.70 |
| SOL | Expanding-prior | 0.00071 | 0.02014 | 0.00065 | 0.02194 | 12.31 | 15.53 | 8.10 | 6.42 |
| DOGE | Rolling-180 | 0.00000 | 0.07907 | 0.00000 | 0.10487 | 9.74 | 13.00 | 10.23 | 7.67 |
| DOGE | Expanding-prior | 0.00092 | 0.02313 | 0.00018 | 0.02066 | 10.93 | 13.55 | 9.11 | 7.36 |
| AVAX | Rolling-180 | 0.00000 | 0.09005 | 0.00000 | 0.09790 | 8.82 | 13.09 | 11.28 | 7.62 |
| AVAX | Expanding-prior | 0.00027 | 0.02203 | 0.00071 | 0.01790 | 10.56 | 13.00 | 9.43 | 7.67 |

All run lengths are in 4-hour snapshots. Because the rolling quantile can remain unchanged while the 180-observation window shifts, its median absolute threshold movement is zero in these ledgers; this does not mean the rolling threshold is constant. Its 95th-percentile movement is materially larger than expanding-prior in every asset. Conversely, expanding-prior labels switch more frequently in all five assets in this sample. Threshold smoothness and label stability are therefore not the same property.

## 4. Cross-asset cohort-rate comparability

Past-only label rates over 2,178 evaluated snapshots per asset:

| Asset | Rolling strict % | Rolling broad % | Expanding strict % | Expanding broad % |
|---|---:|---:|---:|---:|
| BTC | 19.70 | 28.93 | 23.00 | 31.59 |
| ETH | 19.93 | 27.78 | 24.20 | 33.65 |
| SOL | 20.75 | 30.07 | 24.56 | 32.32 |
| DOGE | 20.25 | 29.20 | 23.46 | 32.37 |
| AVAX | 18.82 | 27.87 | 22.64 | 31.45 |

Across assets, strict-rate ranges are 18.82–20.75% for Rolling-180 and 22.64–24.56% for Expanding-prior. Broad-rate ranges are 27.78–30.07% and 31.45–33.65%, respectively. The cohort rates appear relatively close across these five ledgers, but this is not proof of calibrated equivalence: assets share the same dates and market environment, and the comparison is based on the existing feature definitions.

## 5. Cross-asset timestamp alignment audit

The five ledgers were compared row-by-row using `available_at_ts_ms`.

| Asset | Rows | Duplicate availability timestamps | Non-4-hour adjacent steps | Identical timestamp sequence to BTC |
|---|---:|---:|---:|---|
| BTC | 2,358 | 0 | 0 | Yes |
| ETH | 2,358 | 0 | 0 | Yes |
| SOL | 2,358 | 0 | 0 | Yes |
| DOGE | 2,358 | 0 | 0 | Yes |
| AVAX | 2,358 | 0 | 0 | Yes |

All five availability timestamp sequences match exactly, with no duplicates or non-4-hour steps in the audited ledgers. Common availability range is 2025-10-22 16:00 UTC through 2026-11-19 12:00 UTC.

**Boundary of this finding:** this proves row-level alignment of the five committed feature ledgers, not independent correctness of their upstream 1-minute/15-minute source candles, OHLCV completeness, candle-close semantics, or VPS-to-canonical provenance. Those source audits remain separate Gate 0 work.

## 6. Interpretation and decision

1. Rolling-180 has larger tail movements in its thresholds but lower observed label turnover than Expanding-prior in this sample.
2. Expanding-prior thresholds move less at the 95th percentile, but its descriptive labels change more frequently. This can arise because small threshold movements near the current width can flip a label.
3. Neither method dominates on all stability dimensions. The results do not justify choosing one.
4. The five feature ledgers are exactly timestamp-aligned at their availability timestamps, which supports synchronized cross-asset descriptive analysis on these ledgers.
5. No method is selected or approved. Do not replace historical full-sample classifications or promote either candidate to production.
6. G0-04 causal event availability and G0-05 three-family candidate generation remain OPEN / CRITICAL. Gate 0 remains CONDITIONAL HOLD. Gate 2 and strategy/backtest work remain closed.

## 7. Next required work

Before any threshold policy selection, define a written, predeclared comparison protocol covering threshold stability, label turnover, warm-up coverage, cross-asset behavior and event eligibility, with no forward-return, MFE/MAE, PnL or strategy outcome inputs. Then audit upstream source provenance and candle availability semantics independently. Keep rejection, breakout continuation and failed-breakout reversal as separate event families when the candidate-availability audit is eventually performed.

No source ledgers or archived outputs were modified. No VPS operation, workflow dispatch, candidate generation or trading simulation was performed.
