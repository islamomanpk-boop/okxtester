# Phase 3 Fixed-180 Past-Only Threshold Diagnostic V1

**Date:** 2026-11-25  
**Project:** OKX Price Action V1 — Phase 3 Sideways / Range  
**Branch:** `price-action-v1`  
**Status:** EXPLORATORY MECHANICAL DIAGNOSTIC — no policy selected; no event/candidate generation, forward outcomes or PnL.

## 1. Purpose

Complete the predeclared three-policy comparison by measuring the fixed-180 calibration alternative alongside the previously recorded expanding-prior and rolling-180 diagnostics. This is a descriptive calibration-mechanics comparison only.

## 2. Frozen inputs and integrity

Read-only inputs are the five existing 4H feature ledgers:

| Asset | Path | Git blob SHA |
|---|---|---|
| BTC | `reports/sideways_detector_original_v1/BTC_features_original_v1.csv` | `e422073b993cf5d9d11050216509165277339710` |
| ETH | `reports/sideways_detector_original_v1/ETH_features_original_v1.csv` | `c38641d3846931afd6e44a7f39318251fe3c5653` |
| SOL | `reports/sideways_detector_original_v1/SOL_features_original_v1.csv` | `5ba90a99a33924f3de6bcbe9cd1d76aa0a9dd207` |
| DOGE | `reports/sideways_detector_original_v1/DOGE_features_original_v1.csv` | `5fb8cb621628e069b1e2500f8047eb908b031909` |
| AVAX | `reports/sideways_detector_original_v1/AVAX_features_original_v1.csv` | `06b6f7ee947ef5e62b8cf2b9cc64fb7caaa523e5` |

Each ledger contained exactly 2,358 rows. All five had 2,358 unique, strictly increasing `available_at_ts_ms` values, with every adjacent step exactly 14,400,000 ms. The five ledgers use the same timestamp sequence.

Common availability range: 2025-10-22 16:00 UTC to 2026-11-19 12:00 UTC. The first 180 snapshots are excluded from evaluation; the first evaluated snapshot is 2025-11-21 16:00 UTC. Each asset therefore has 2,178 evaluated snapshots.

## 3. Method

For each asset, P25 and P40 use linear-interpolated quantiles of `channel_width_pct`.

- **Fixed-180:** calculate each threshold once from the first 180 completed snapshots and hold it constant for all 2,178 evaluated snapshots.
- **Expanding-prior:** at evaluated row i, calculate from all rows strictly before i.
- **Rolling-180:** at evaluated row i, calculate from the immediately preceding 180 rows, excluding i.

The evaluated strict label is width <= causal P25, directional efficiency <= 0.30, and mean overlap >= 0.70. The broad label substitutes causal P40. Strict and broad are nested labels, not independent populations.

The fixed-180 results below were calculated directly from the committed CSV values. The expanding and rolling comparison values are reproduced from the previously archived threshold stability audit; the independent recalculation in the same run also matched those archived values to displayed precision.

## 4. Fixed-180 results by asset

Threshold values are channel-width percentage points. Turnover is label changes per 100 adjacent evaluated snapshots. Mean run length is in 4H snapshots.

| Asset | Fixed P25 | Fixed P40 | Strict eligible % | Broad eligible % | Strict turnover /100 | Broad turnover /100 | Strict mean run | Broad mean run |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | 4.302651 | 4.883065 | 30.58 | 35.12 | 14.06 | 15.99 | 7.09 | 6.24 |
| ETH | 7.132630 | 8.201747 | 37.56 | 41.69 | 16.95 | 18.60 | 5.89 | 5.36 |
| SOL | 7.419062 | 9.322865 | 35.49 | 42.52 | 16.03 | 19.34 | 6.22 | 5.16 |
| DOGE | 7.569115 | 8.514990 | 35.49 | 39.12 | 14.75 | 16.12 | 6.76 | 6.19 |
| AVAX | 8.217496 | 9.067867 | 36.87 | 39.58 | 14.93 | 16.77 | 6.68 | 5.95 |

As expected for a frozen threshold, both threshold series have zero absolute change on every update. That is a mechanical property of the policy, not evidence that the policy is well calibrated or robust.

## 5. Three-policy comparison

Equal-weight means across the five assets:

| Policy | Strict eligible % | Broad eligible % | Strict turnover /100 | Broad turnover /100 |
|---|---:|---:|---:|---:|
| Fixed-180 | 35.20 | 39.61 | 15.34 | 17.36 |
| Expanding-prior | 23.57 | 32.28 | 11.34 | 14.50 |
| Rolling-180 | 19.89 | 28.77 | 9.76 | 13.62 |

Fixed-180 produced materially larger eligible cohorts and higher label turnover than either adaptive alternative in all five assets. Its P25/P40 values reflect only the initial calibration month and do not adapt to later changes in channel-width distributions. Expanding-prior produced intermediate cohort rates and turnover. Rolling-180 produced the smallest cohort rates and lowest turnover in this sample, while the prior audit showed larger P95 threshold movements than expanding-prior.

These are operational trade-offs, not a ranking of predictive quality. Higher eligible-row counts, lower turnover, or static thresholds are not intrinsically better.

## 6. Decision

1. The three predeclared detector-ledger policies are now mechanically compared on the same 180-snapshot warm-up.
2. No policy is selected. The results do not establish a uniquely justified operational winner.
3. Retain fixed-180, expanding-prior and rolling-180 as sensitivity variants pending the source-specific event-eligibility mapping and the other predeclared readiness checks.
4. Do not transfer these detector-ledger threshold values directly into the breakout source. The breakout pipeline requires its own source-specific reconstruction and the common 4H calibration clock defined in Section 11 of the threshold-selection protocol.
5. G0-04 and G0-05 remain OPEN / CRITICAL. Gate 0 remains CONDITIONAL HOLD. No candidate generation, outcome study, Gate 2 or strategy/PnL backtest is authorized.

## 7. Scope exclusions

No source ledger was modified. No candidate IDs, orders, fills, stops, targets, matched controls, forward outcomes, inference or PnL were generated. No VPS operation or workflow dispatch was performed.

**Companion protocol:** `docs/research_protocols/2026-11-25_phase3_past_only_regime_threshold_selection_protocol_v1.md`  
**Prior stability/alignment audit:** `docs/research_checkpoints/2026-11-25_phase3_threshold_stability_alignment_audit_v1.md`
