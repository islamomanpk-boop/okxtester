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

The source-only disposition artifact now emits family, side, historical/causal cohort, overlap cluster and repeated-signal group fields. Canonical `candidate_id`, final `source_event_id`, `instrument_id` and version labels remain to be materialized.

## 3. Snapshot and threshold provenance

### 3.1 Exact join keys

- Rejection source row → detector feature row: `asset + snapshot_index`; confirm that the feature row's `available_at_ts_ms` matches the boundary ledger's frozen snapshot timestamp.
- Breakout raw crossing → historical detector channel cross-check: `asset + (context_snapshot_ms - 14,400,000) == available_at_ts_ms` for upper/lower/channel-width only. G0-04 raw context is authoritative for efficiency/overlap and for the snapshot's own availability timestamp; do not compare those two metrics to same-time detector features.
- Failed breakout → inherit the source breakout's snapshot and frozen boundaries. A later 4-hour snapshot must not replace the source breakout context.
- All families → G0-04 threshold row: `asset + exact snapshot_ms + EXPANDING_PRIOR + UNIQUE_4H_FEATURE_ROWS`.

### 3.2 Canonical field population

| Canonical field | Source / transform |
|---|---|
| `snapshot_id` | Stable asset + exact snapshot availability timestamp; rejection may also retain original snapshot index. |
| `snapshot_available_at_ts_ms` | Exact detector feature `available_at_ts_ms`. |
| `snapshot_valid_from_ts_ms` | Same as snapshot availability. |
| `snapshot_valid_until_ts_ms` | Rejection: next detector feature snapshot availability. Breakout/failed: next 4H historical context snapshot = context snapshot + 14,400,000 ms. |
| `frozen_upper_boundary`, `frozen_lower_boundary` | Rejection: exact detector feature row at snapshot. Breakout: G0-04 historical raw context; verify channel values against detector feature one 4H bar earlier. Failed breakout inherits original source breakout values. |
| `channel_width_pct` | Rejection: exact detector feature value. Breakout/failed: G0-04 historical raw context value, cross-checked to detector feature one 4H bar earlier. |
| `threshold_policy_id` | `EXPANDING_PRIOR`. |
| `threshold_population_id` | `UNIQUE_4H_FEATURE_ROWS`. |
| `threshold_value` | Exact G0-04 p25 for causal strict; exact p40 for causal broad-only or broad-threshold rejection. Blank only when no exact threshold exists due warm-up. |
| `threshold_percentile` | 25 for strict; 40 for broad-only / broad outer-threshold evaluation; blank for warm-up. |
| `threshold_calibration_start_ts_ms` | G0-04 `first_prior_context_ms`. |
| `threshold_calibration_end_ts_ms` | G0-04 `last_prior_context_ms`; must be strictly before the classified snapshot. |
| `threshold_prior_observation_count` | G0-04 `prior_context_count`; require at least 180. |
| `efficiency_value` | Rejection: exact feature `directional_efficiency`. Breakout/failed: G0-04 historical raw context `efficiency`; it is not expected to equal the original detector feature at the same timestamp. |
| `efficiency_limit` | Frozen constant 0.30. |
| `overlap_value` | Rejection: exact feature `mean_overlap`. Breakout/failed: G0-04 historical raw context `overlap`; it is not expected to equal the original detector feature at the same timestamp. |
| `overlap_minimum` | Frozen constant 0.70. |

Do not recompute thresholds in the candidate builder. The source audit already proves exact snapshot-key lookup, prior-only calibration and minimum prior count.

## 4. Source-file lineage and manifest

The current complete G0-05 source manifest V2 is `source_manifest.json` from source-audit run [45806239609](https://github.com/islamomanpk-boop/okxtester/actions/runs/45806239609), artifact ID `15109506588`. Its SHA-256 is:

`82bce2b7549efb959a2805641cfda46c1ea6a158e8e6c7d24cd8f3795ca80bbb`

This manifest includes repository inputs, G0-04 artifact members, Module A/Module B source outputs and metadata, all five raw 1-minute inputs, and the source-audit revision/run identity. Each source-only disposition row carries this exact manifest ID, family/asset-specific source paths, and the corresponding Git blob IDs. G0-04 artifact members are identified by artifact path and SHA-256 in the manifest.

The earlier seven-file-only manifest is superseded. Every later source-audit run must use its own computed manifest ID.

Family source paths:
- Rejection: `reports/sideways_boundary_events_historical_v1/boundary_tests_historical_v1.csv`; `reports/sideways_phase3_research_archive_v1/episode_retest_anatomy_v1/event_anatomy_v1.csv`; per-asset `reports/sideways_detector_original_v1/{ASSET}_features_original_v1.csv`; `data/market_1m/{ASSET}_USDT_USDT_1m.csv`; G0-04 causal threshold artifact.
- Breakout continuation: G0-04 artifact `unique_raw_crossing_events_with_six_variants.csv`; per-asset detector feature file; G0-04 threshold artifact; exact raw 1-minute file. Module B `breakout_lifecycle_events_v1_1.csv` supplies historical cohort membership only, not the primary breakout source population.
- Failed breakout: Module B `breakout_lifecycle_events_v1_1.csv` and `breakout_lifecycle_horizons_v1_1.csv`; exact G0-04 source breakout key; raw 1-minute source; inherited detector snapshot and threshold provenance.

The canonical row should retain the family-relevant paths and Git blob IDs from the manifest, not a hand-written list of guessed hashes. The manifest hash itself is frozen in the field-value decision document.

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
| `ambiguity_flags` | Source-only ledger now emits NONE for rejection/breakout and exact OPEN_OUTSIDE_CLOSE_INSIDE or WICK_OUTSIDE_CLOSE_INSIDE flags for failed-breakout confirmation candles, rebuilt from 15 component 1m OHLC bars. |
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


## 11. Source-only timing and ambiguity fields now emitted — 2026-11-26

The source-only ledgers now carry:
- signal candle open, close and availability timestamps;
- family-specific confirmation rule ID, 900,000 ms bar interval and confirmation status;
- event-observed timestamp;
- ambiguity flags;
- expiry rule/endpoint for failed-breakout reversal;
- NOT_APPLICABLE invalidation reference type;
- source reconciliation status and join cardinality.

Failed-breakout confirmation candles are rebuilt from 15 exact component 1m OHLC records. The current audit found 756 confirmed return-inside events, all with OPEN_OUTSIDE_CLOSE_INSIDE; 176 events had no return-inside confirmation. See source audit [45805545548](https://github.com/islamomanpk-boop/okxtester/actions/runs/45805545548), artifact ID `15109271179`, and tests [45805565739](https://github.com/islamomanpk-boop/okxtester/actions/runs/45805565739), 102/102 passed.

Still to materialize: canonical candidate IDs/source-event IDs, instrument/version labels, per-row snapshot/threshold/feature provenance, manifest/path/blob lineage, source breakout candidate IDs, and all invalidation reference columns (type/value/timestamp) in the final canonical output.


## 12. Complete source lineage now emitted per source-only row

The complete-manifest audit now emits `source_sha256_manifest_id`, `source_file_paths`, and `source_git_blob_ids` on all three source-only disposition ledgers. It covers all five raw 1m files and the G0-04 artifact hashes in addition to the repository and lifecycle inputs.

- Source audit [45806239609](https://github.com/islamomanpk-boop/okxtester/actions/runs/45806239609) — SUCCESS; artifact ID `15109506588`; ZIP SHA-256 `c87808aaac2be5d7013d42d3f93fcbb0ed44d1602470c030642fcf6ffc75efcb`.
- Manifest SHA-256 / row ID: `82bce2b7549efb959a2805641cfda46c1ea6a158e8e6c7d24cd8f3795ca80bbb`; recomputed from the exact manifest bytes and matched every row.
- 4,947 rows carry exactly one manifest ID; each row's paths point to the correct asset-specific feature and market file.

Remaining canonical materialization includes candidate/source-event IDs, version labels, snapshot/threshold/feature values, and failed-breakout source-breakout candidate IDs. The independent minute verifier is being rerun against this latest manifest artifact.


## 13. One-4H-lagged breakout context correction

The source audit initially rejected an incorrect same-timestamp join between G0-04 raw crossing `efficiency` and the original detector feature's `directional_efficiency`. Inspection of the accepted G0-04 code established that breakout raw events use the historical breakout context, whose channel is one 4H candle lagged.

The corrected mapping:
- Rejection uses the original detector feature at the exact rejection snapshot.
- Breakout and failed-breakout use the exact G0-04 raw context at `context_snapshot_ms`; `upper`, `lower` and `channel_width_pct` are cross-checked against the original detector feature at `context_snapshot_ms - 14,400,000`.
- Breakout/failed-breakout `efficiency_value` and `overlap_value` are sourced from the G0-04 raw context, not same-time detector features.
- Breakout/failed-breakout `snapshot_valid_until_ts_ms` is the next 4H context snapshot.

The source audit preserves `reference_feature_snapshot_ts_ms` and uses `HISTORICAL_BREAKOUT_CONTEXT_V1` for breakout/failed-breakout rows. This is a source-timing correction, not a change to G0-04 thresholds or eligibility decisions.
