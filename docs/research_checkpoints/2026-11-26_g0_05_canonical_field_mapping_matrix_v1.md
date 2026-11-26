# G0-05 Canonical Candidate Field-Mapping Matrix — V1

**Date:** 2026-11-26  
**Scope:** Field-level mapping from the frozen G0-05 schema to accepted source records and exact join keys.  
**Status:** Mapping design; not a candidate generator and not canonical candidate output.  
**Authorization:** No canonical candidate generation is authorized by this document.

## 1. Frozen implementation identifiers proposed

These identifiers should be used consistently in the eventual candidate build. They do not change the source populations or decision thresholds.

| Field | Proposed value | Notes |
|---|---|---|
| `regime_definition_version` | `SIDEWAYS_DETECTOR_ORIGINAL_V1` | Original feature-definition implementation. |
| `candidate_rule_version` | `G0_05_CANDIDATE_RULE_V1` | Deterministic identity input; freeze before generation. |
| `source_pipeline_version` | `G0_04_CAUSAL_RECONSTRUCTION_V1+MODULE_A_V1_1+MODULE_B_V1_1` | Records the source pipeline family; family-specific components may be NOT_APPLICABLE. |
| `decluster_policy_id` | `G0_05_INTERVAL_GRAPH_METADATA_V1` | Metadata only; family-specific 24H/12H windows documented in the cluster amendment records. |
| Rejection `confirmation_rule_id` | `STRONG_REJECTION_15M_CLOSE_V1` | Source 15m candle open is not availability; close is confirmation. |
| Breakout `confirmation_rule_id` | `BOUNDARY_CROSSING_15M_CLOSE_V1` | Completed 15m signal close is availability. |
| Failed-breakout `confirmation_rule_id` | `RETURN_INSIDE_15M_CLOSE_V1` | First completed 15m close back inside original source boundary. |
| Failed-breakout `expiry_rule_id` | `SOURCE_BREAKOUT_12H_RETURN_INSIDE_V1` | Endpoint = source breakout signal time + 43,200,000 ms. |

The final version identifiers must be reviewed with the full schema before the candidate implementation is authorized.

## 2. Identity and classification fields

| Canonical field | Rejection mapping | Breakout continuation mapping | Failed-breakout reversal mapping |
|---|---|---|---|
| `candidate_id` | SHA-256 helper over rejection physical identity + family + candidate rule version | SHA-256 helper over exact raw crossing key + family + rule version | SHA-256 helper over source breakout identity + completed confirmation timestamp + reversal rule version |
| `source_event_id` | Existing physical identity: asset, direction, snapshot index, segment ID, test rank, test start | `asset|direction|signal_time_ms|context_snapshot_ms` | Source breakout identity + completed return-inside confirmation timestamp |
| `source_event_row_ids` | Both BROAD_P40 and STRICT_P25 source event IDs as present | G0-04 raw crossing identity; add Module B definition-specific IDs only as historical membership evidence | Module B event IDs for BROAD_P40 and STRICT_P25 as present |
| `family` | SUPPORT_REJECTION for lower; RESISTANCE_REJECTION for upper | BREAKOUT_CONTINUATION | FAILED_BREAKOUT_REVERSAL |
| `instrument_id` | **Decision required:** resolve exact OKX instrument ID from the frozen data-download metadata; do not infer from asset text alone | Same | Inherit source breakout instrument ID |
| `asset` | Boundary-test source row | G0-04 raw crossing | Module B event/source breakout |
| `side` | Lower LONG; upper SHORT | Upper LONG; lower SHORT | Upper-breakout failure SHORT; lower-breakout failure LONG |
| `boundary_side` | Original lower/upper boundary | Original crossed lower/upper boundary | Source breakout boundary side |
| `historical_cohort_memberships` | Existing source definition labels | Exact-key Module B join now supplies NONE, BROAD_P40, or BROAD_P40;STRICT_P25 | Module B source definition labels |
| `causal_cohort_label` | Source-only `causal_cohort` | Source-only `causal_cohort` | Source-only `causal_source_cohort` |
| `overlap_cluster_id` | Accepted Module A 24H interval-graph ID | G0-05 raw crossing 12H interval-graph ID | Inherit exact source breakout cluster |
| `repeated_signal_group_id` | Frozen asset/direction/snapshot-index/segment group | Frozen asset/direction/context-snapshot group | Inherit exact source breakout group |

The source-only disposition artifact now emits all fields in this section except canonical `candidate_id`, `source_event_id` in the final schema form, `instrument_id`, and final version labels.

## 3. Snapshot and threshold provenance

### 3.1 Exact join keys

- Rejection source row → detector feature row: `asset + snapshot_index`; confirm that the feature row's `available_at_ts_ms` matches the boundary ledger's frozen snapshot timestamp.
- Breakout raw crossing → detector feature row: `asset + context_snapshot_ms == available_at_ts_ms`; do not use nearest timestamp.
- Failed breakout → inherit the source breakout's snapshot and frozen boundaries. A later 4-hour snapshot must not replace the source breakout context.
- All families → G0-04 threshold row: `asset + exact snapshot_ms + EXPANDING_PRIOR + UNIQUE_4H_FEATURE_ROWS`.

### 3.2 Canonical field population

| Canonical field | Source / transform |
|---|---|
| `snapshot_id` | Stable asset + exact snapshot availability timestamp; rejection may also retain original snapshot index. |
| `snapshot_available_at_ts_ms` | Exact detector feature `available_at_ts_ms`. |
| `snapshot_valid_from_ts_ms` | Same as snapshot availability. |
| `snapshot_valid_until_ts_ms` | Next detector feature snapshot availability for that asset; half-open interval endpoint. Rejection source ledger already carries the next-available timestamp. |
| `frozen_upper_boundary`, `frozen_lower_boundary` | Exact detector feature row or G0-04 raw crossing row; failed breakout inherits the original source breakout values. |
| `channel_width_pct` | Exact detector feature / G0-04 raw crossing value. |
| `threshold_policy_id` | `EXPANDING_PRIOR`. |
| `threshold_population_id` | `UNIQUE_4H_FEATURE_ROWS`. |
| `threshold_value` | Exact G0-04 p25 for causal strict; exact p40 for causal broad-only or broad-threshold rejection. Blank only when no exact threshold exists due warm-up. |
| `threshold_percentile` | 25 for strict; 40 for broad-only / broad outer-threshold evaluation; blank for warm-up. |
| `threshold_calibration_start_ts_ms` | G0-04 `first_prior_context_ms`. |
| `threshold_calibration_end_ts_ms` | G0-04 `last_prior_context_ms`; must be strictly before the classified snapshot. |
| `threshold_prior_observation_count` | G0-04 `prior_context_count`; require at least 180. |
| `efficiency_value` | Exact feature `directional_efficiency` / G0-04 raw crossing `efficiency`. |
| `efficiency_limit` | Frozen constant 0.30. |
| `overlap_value` | Exact feature `mean_overlap` / G0-04 raw crossing `overlap`. |
| `overlap_minimum` | Frozen constant 0.70. |

Do not recompute thresholds in the candidate builder. The source audit already proves exact snapshot-key lookup, prior-only calibration and minimum prior count.

## 4. Source-file lineage and manifest

The current G0-05 source manifest is `source_manifest.json` from source-audit run [45804274324](https://github.com/islamomanpk-boop/okxtester/actions/runs/45804274324), artifact ID `15107399743`. Its SHA-256 is:

`abd869c9c11a31f42ae916bc56492977dce79dd18f5e2c9c9b1f23584629a440`

Use this value as the current `source_sha256_manifest_id` only for that exact manifest version. A later source manifest must receive a new ID.

Family source paths:
- Rejection: `reports/sideways_boundary_events_historical_v1/boundary_tests_historical_v1.csv`; `reports/sideways_phase3_research_archive_v1/episode_retest_anatomy_v1/event_anatomy_v1.csv`; per-asset `reports/sideways_detector_original_v1/{ASSET}_features_original_v1.csv`; `data/market_1m/{ASSET}_USDT_USDT_1m.csv`; G0-04 causal threshold artifact.
- Breakout continuation: G0-04 artifact `unique_raw_crossing_events_with_six_variants.csv`; per-asset detector feature file; G0-04 threshold artifact; exact raw 1-minute file. Module B `breakout_lifecycle_events_v1_1.csv` supplies historical cohort membership only, not the primary breakout source population.
- Failed breakout: Module B `breakout_lifecycle_events_v1_1.csv` and `breakout_lifecycle_horizons_v1_1.csv`; exact G0-04 source breakout key; raw 1-minute source; inherited detector snapshot and threshold provenance.

The canonical row should retain the family-relevant paths and Git blob IDs from the manifest, not a hand-written list of guessed hashes.

## 5. Signal, confirmation and availability

| Field | Rejection | Breakout continuation | Failed-breakout reversal |
|---|---|---|---|
| `signal_candle_open_ts_ms` | `first_strong_rejection_ts_ms` | `signal_time_ms - 900000` | `confirmation_ts_ms - 900000` |
| `signal_candle_close_ts_ms` | `confirmation_ts_ms` | `signal_time_ms` | `confirmation_ts_ms` |
| `signal_available_at_ts_ms` | `confirmation_ts_ms = rejection open + 900000` | `signal_time_ms` | Completed 15m return-inside close timestamp |
| `confirmation_bar_interval_ms` | 900000 | 900000 | 900000 |
| `first_eligible_execution_bar_open_ts_ms` | Existing eligible-only first-minute field | Existing eligible-only first-minute field | Existing eligible-only first-minute field |
| `event_observed_at_ts_ms` | Confirmation/availability timestamp | Signal close/availability timestamp | Completed return-inside confirmation timestamp |

The first eligible 1-minute open is a timestamp only. It is not an order, fill or assumed execution price.

## 6. Disposition, lifecycle and ambiguity

| Canonical field | Mapping / rule |
|---|---|
| `candidate_status` | Exact source-only `disposition`. |
| `exclusion_reason` | Exact `reason_code`; eligible rows must be `NONE`. |
| `censoring_reason` | Exact validated source-only `censoring_reason`; non-empty only for CENSORED. |
| `ambiguity_flags` | **Join/implementation still required:** preserve signal/confirmation-candle OHLC-path ambiguity using all 15 component 1m bars. Do not use later retest ambiguity fields as a substitute for confirmation-bar ambiguity. |
| `decluster_policy_id` | `G0_05_INTERVAL_GRAPH_METADATA_V1`; retain the family-specific 24H rejection and 12H raw-breakout algorithm/version in metadata. |
| `invalidation_reference_type/value/ts_ms` | NOT_APPLICABLE for G0-05 point-event availability; do not invent a stop or trade invalidation. |
| `expiry_rule_id` | NOT_APPLICABLE for rejection/continuation; `SOURCE_BREAKOUT_12H_RETURN_INSIDE_V1` for failed breakout. |
| `expiry_ts_ms` | NOT_APPLICABLE for rejection/continuation; source breakout signal + 43,200,000 ms for failed breakout. |
| `source_breakout_candidate_id` | **Derived at canonical build:** deterministic candidate ID for the exact source breakout identity, using the same frozen rule version. |
| `source_reconciliation_status` | Map the exact source audit join result; allowed successful values should distinguish exact one-to-one from declared one-to-many cohort lineage. |
| `source_join_cardinality` | Rejection physical event → one or two definition rows; breakout raw source key → one raw row; failed breakout physical event → one or two Module B definition rows and one exact source breakout key. |

## 7. Remaining decisions / implementation gates

1. Verify and freeze exact OKX `instrument_id` mapping from original downloader metadata.
2. Freeze the proposed version/rule identifier strings in the full schema review.
3. Implement the exact 15-component-minute confirmation-candle OHLC ambiguity extraction, including failed-breakout reversal.
4. Freeze allowed `confirmation_status` values and `source_reconciliation_status` values; the schema currently names the fields but does not enumerate their values.
5. Materialize the complete canonical row schema with family-specific NOT_APPLICABLE/null rules and exact source lineage.
6. Add tests for deterministic candidate IDs, collision checks, source-breakout candidate linkage, full family schema, confirmation ambiguity, source paths/blob references, and deterministic serialization.
7. Independently review the field mapping and full candidate output before any canonical generation is authorized.

## 8. Boundary

This matrix is a mapping and gap analysis only. It does not create candidate rows, orders, fills, execution simulation, PnL, strategy backtests or phase transitions.
