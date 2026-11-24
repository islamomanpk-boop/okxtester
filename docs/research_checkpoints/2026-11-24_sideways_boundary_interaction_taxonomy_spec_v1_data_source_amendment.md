# Sideways Boundary Interaction Taxonomy V1 — Data-Source and Tail-Handling Amendment

Date: 2026-11-24  
Applies to: `docs/research_checkpoints/2026-11-24_sideways_boundary_interaction_taxonomy_spec_v1.md`  
Branch: `price-action-v1`  
Status: **AMENDMENT FROZEN — data-source contract clarified before implementation.**

## 1. Purpose and precedence

This amendment resolves the input-series ambiguity between the frozen taxonomy specification and the existing accepted historical boundary reconstruction pipeline.

The original taxonomy specification remains unchanged. This document supplements only its data-source description and tail-handling requirements. All taxonomy definitions, classification priorities, approach bands, output fields, validation rules, and stop conditions in the original specification remain in force.

If the original specification's source-path wording conflicts with this amendment, use the source contract in this amendment. No other part of the original specification is superseded.

## 2. Underlying source and selected observation series

The underlying source is the original 1-minute OHLCV history:

`~/okx_scalping_data/{ASSET}_USDT_USDT_1m.csv`

The selected 15-minute observation series is the existing derived data:

`~/okx_adaptive_bot/data/{ASSET}_USDT_15m.csv`

Assets: BTC, ETH, SOL, DOGE, AVAX.

The taxonomy implementation may consume the existing 15-minute files directly. It must not treat them as an independent raw source: they are derived from the original 1-minute files and their equivalence is supported by the aggregation audits listed below.

The 15-minute schema is `ts,open,high,low,close,vol`. The timestamp is the opening label of a 15-minute bucket.

## 3. Verified aggregation convention and equivalence

The independent aggregation audits dated 2026-11-22 and 2026-11-23 establish the following convention:

- Epoch-aligned 15-minute buckets.
- `closed="left"`, `label="left"`.
- Bucket interval: `[ts, ts + 900000 ms)`.
- Open: first constituent 1-minute open.
- High: maximum constituent 1-minute high.
- Low: minimum constituent 1-minute low.
- Close: last constituent 1-minute close.
- Volume: sum of constituent 1-minute volume.
- Retain only complete buckets with exactly 15 constituent 1-minute observations.

For BTC, ETH, SOL, DOGE, and AVAX, the audits report 37,941 supplied and rebuilt complete 15-minute candles per asset, with matching timestamps and exact matches across all five OHLCV fields. The 2026-11-23 audit reports maximum absolute difference 0.0 for every asset.

Evidence:
- `docs/research_checkpoints/2026-11-22_1m_to_15m_4h_aggregation_audit.md`
- `docs/research_checkpoints/2026-11-23_termux_15m_4h_ohlcv_aggregation_pass.md`

This establishes cross-timeframe aggregation equivalence for the available files. It does not establish original exchange-download lineage, instrument identity independently of prior source records, or volume-unit interpretation.

## 4. Source file identity and change control

The 2026-11-24 provenance checkpoint records the observed SHA-256 hashes and row counts for the selected five 15-minute files:

| Asset | SHA-256 | Data rows |
|---|---|---:|
| BTC | `0721a4a25a61f1917be4f9952514096c641fbec64e7ae0d50c7cf1c3ebfe9658` | 37,941 |
| ETH | `7195e45315c360e9f1fdd37746125968359bce8632a0bfe51628f104792fdc04` | 37,941 |
| SOL | `5b34cbb006497ecd7ebe0cfa67b25b4230cb769d6362d278991171a8f6da2d33` | 37,941 |
| DOGE | `3418c81fa16b531eee5de90d8b0ff6a5543db54357cb5572358ff31ab6627b5f` | 37,941 |
| AVAX | `75ef1a545686217a6d4ca55385690095c6e2a494438b7f4e38352d5ca35de493` | 37,941 |

Immediately before implementation, recompute and compare these hashes and row counts. Any mismatch is a stop condition pending investigation. Do not modify the source CSVs.

The raw 1-minute and derived 15-minute CSVs are not stored in this GitHub repository; the provenance checkpoint records their local paths and observed hashes. The research code, specifications, audits, and reports remain version-controlled.

Evidence:
- `docs/research_checkpoints/2026-11-24_sideways_boundary_taxonomy_data_provenance_v1.md`

## 5. Snapshot availability and eligible observations

Use the frozen channel feature files from:

`reports/sideways_detector_original_v1/{ASSET}_features_original_v1.csv`

A feature row's `available_at_ts_ms` is the earliest time its frozen channel may be used. Assign 15-minute candles by their opening timestamp to the interval:

`available_at_ts_ms <= 15m_ts < next_snapshot_available_at_ts_ms`

Preserve the historical reconstruction convention: suppress the first observed 15-minute candle at or after each new snapshot's availability. Do not use a feature row before availability, forward-fill missing candles, or bridge timestamp gaps.

The feature files currently contain 2,358 rows per asset. Their final snapshot availability is `1795089600000`; the final snapshot's channel end is `1795075200000`.

## 6. Incomplete final snapshot interval

The existing audit `docs/research_checkpoints/2026-11-23_rejection_confirmation_1m_timing_and_tail_audit.md` establishes that the final feature-snapshot interval is truncated by the end of the available 15-minute history:

- 9 observed 15-minute bars in the final interval per asset.
- 1 first bar suppressed.
- 8 eligible bars per asset.
- Last eligible candle open: `1795096800000`.
- Last eligible candle close: `1795097700000`.
- Expected next snapshot boundary: `1795104000000`.

This is an incomplete 4-hour snapshot interval, not an internal 15-minute timestamp gap.

Rules:
1. Exclude the final truncated snapshot interval from analyses that require a complete snapshot interval.
2. Do not silently classify the observed partial interval as a complete 4-hour interval.
3. If a future taxonomy output intentionally reports partial-tail observations, mark them explicitly as right-truncated and keep them separate from complete-snapshot primary summaries.
4. Do not extend the final interval, synthesize missing candles, or infer an unobserved next snapshot.
5. Continue to enforce each observation's own 15-minute candle completeness and all timestamp-continuity checks.

The 2026-11-23 tail audit also verified the final rejection-event confirmation sequences against the 1-minute source. That event-specific check does not replace the taxonomy implementation's own source hash, row-count, timestamp, and tail audits.

## 7. Scope unchanged

This amendment does not:
- change any interaction class or its priority;
- change the 5%, 10%, or 15% approach-band definitions;
- change signed-distance or penetration formulas;
- change dual-boundary handling;
- change the existing strong-rejection reference definition;
- authorize episode construction, outcome studies, strategy rules, or profitability claims;
- authorize modification of the original historical reconstruction script, its tests, or its reports.

The taxonomy remains a descriptive candle-level study. Consecutive candles are not independent boundary-test episodes. Episode-level summaries remain a separate later task.

## 8. Implementation gate

Before running the new implementation:

1. Verify the five source file hashes and row counts against Section 4.
2. Verify required columns, finite OHLCV values, valid OHLC relationships, unique ordered timestamps, and 15-minute cadence.
3. Verify all included 15-minute buckets are complete according to the already audited aggregation convention.
4. Verify snapshot availability, first-bar suppression, interval assignment, and final-tail exclusion.
5. Preserve all original files and write code, tests, logs, audits, and results to new versioned paths.
6. Stop on any unexplained source mismatch, incomplete included candle, timestamp gap, invalid OHLC, snapshot misassignment, or reconciliation failure.

No implementation or results are authorized by this amendment alone; it freezes the corrected data contract for the separately specified implementation.
