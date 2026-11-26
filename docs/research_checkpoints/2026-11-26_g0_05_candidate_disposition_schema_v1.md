# G0-05 Candidate / Disposition Ledger Schema — V1

**Date:** 2026-11-26  
**Project:** OKX Price Action V1 — Phase 3 Sideways / Range  
**Dependencies:** G0-04 acceptance; G0-05 threshold, family timing, source manifest and synthetic contract decisions.  
**Status:** Schema frozen for implementation and source-only reconciliation. This document does not authorize canonical candidate generation.

## 1. Ledger purpose

G0-05 produces a point-in-time event-availability and disposition ledger. It does not represent open orders, positions, fills, or trades. Every source event considered by a family must receive exactly one disposition. Eligible means only that the event is causally available for later Gate 2 research; it does not mean executable or profitable.

Keep these families separate:
- `SUPPORT_REJECTION` — lower boundary, LONG.
- `RESISTANCE_REJECTION` — upper boundary, SHORT.
- `BREAKOUT_CONTINUATION` — upper boundary LONG; lower boundary SHORT.
- `FAILED_BREAKOUT_REVERSAL` — upper-breakout failure SHORT; lower-breakout failure LONG.

Strict and broad remain nested labels. Asset, boundary side, direction, family and source identity must never be pooled away.

## 2. Candidate/disposition status enum

The field `candidate_status` has exactly these allowed values:

| Value | Meaning |
|---|---|
| `ELIGIBLE_FOR_FURTHER_VALIDATION` | All G0-05 source, timing, snapshot and causal-regime conditions pass. This is candidate availability only. |
| `REJECTED` | A hard source, schema, identity, feature, direction, join or causal eligibility condition fails. |
| `EXPIRED` | A predeclared event horizon elapsed without the required confirmation. |
| `CENSORED` | The event cannot be resolved because required source data is missing, incomplete, gapped or ends before the observation rule resolves. |

OHLC-path ambiguity is carried in `ambiguity_flags`; it is not silently promoted to a separate status and does not imply an inferred intrabar ordering. If ambiguity makes a specific confirmation unobservable under the frozen rule, use CENSORED with a specific censoring reason.

For every row:
- `exclusion_reason = NONE` if status is `ELIGIBLE_FOR_FURTHER_VALIDATION`;
- `exclusion_reason` is a non-empty enum value for REJECTED, EXPIRED or CENSORED;
- `censoring_reason` is non-empty only for CENSORED;
- `expiry_rule_id` and `expiry_ts_ms` are NOT_APPLICABLE for point-event rejection and continuation families; do not invent an active-order expiry at G0-05;
- failed-breakout reversal uses the source breakout's 12-hour observation horizon.

## 3. Controlled reason codes

### REJECTED
- `CAUSAL_THRESHOLD_WARMUP`
- `CAUSAL_REGIME_NOT_ELIGIBLE`
- `SNAPSHOT_EXPIRED_BEFORE_CONFIRMATION`
- `SNAPSHOT_NOT_AVAILABLE_AT_SIGNAL`
- `SOURCE_HASH_MISMATCH`
- `MISSING_SOURCE_IDENTITY`
- `SOURCE_JOIN_UNMATCHED`
- `DUPLICATE_SOURCE_IDENTITY`
- `DUPLICATE_CANDIDATE_ID`
- `INVALID_SOURCE_SCHEMA`
- `INVALID_FEATURE_VALUES`
- `FUTURE_CONTEXT_ASSIGNED`
- `DIRECTION_MAPPING_MISMATCH`
- `NO_VALID_SOURCE_BREAKOUT`
- `INCOMPLETE_CONFIRMATION_BAR`

### EXPIRED
- `EXPIRED_NO_RETURN_INSIDE_WITHIN_12H`

### CENSORED
- `MISSING_OR_GAPPED_MINUTES`
- `INCOMPLETE_15M_CONFIRMATION`
- `SOURCE_END_BEFORE_RESOLUTION`
- `AMBIGUOUS_CONFIRMATION_UNRESOLVED`

No other reason string may be emitted without a versioned schema amendment.

## 4. Required columns

### 4.1 Identity and classification
- `candidate_id` — deterministic SHA-256 of canonical source identity + family + rule version; collision checked.
- `source_event_id` — canonical underlying physical event identity; immutable and independent of duplicated historical cohort labels.
- `source_event_row_ids` — all immutable accepted source-row identities contributing to this physical event, preserving the original strict/broad definition rows.
- `family`, `instrument_id`, `asset`, `side`, `boundary_side`.
- `regime_definition_version`, `candidate_rule_version`, `source_pipeline_version`.
- `historical_cohort_memberships` — list containing BROAD_P40, STRICT_P25 or both as present in the accepted source; `causal_cohort_label` is STRICT_P25 / BROAD_ONLY / NOT_ELIGIBLE / WARMUP / NOT_APPLICABLE.
- `overlap_cluster_id`, `repeated_signal_group_id` (metadata only; no source event deletion).

### 4.2 Snapshot and threshold provenance
- `snapshot_id`, `snapshot_available_at_ts_ms`, `snapshot_valid_from_ts_ms`, `snapshot_valid_until_ts_ms`.
- `frozen_upper_boundary`, `frozen_lower_boundary`, `channel_width_pct`.
- `threshold_policy_id = EXPANDING_PRIOR`.
- `threshold_population_id = UNIQUE_4H_FEATURE_ROWS`.
- `threshold_value`, `threshold_percentile` (25 or 40), `threshold_calibration_start_ts_ms`, `threshold_calibration_end_ts_ms`, `threshold_prior_observation_count`.
- `efficiency_value`, `efficiency_limit = 0.30`, `overlap_value`, `overlap_minimum = 0.70`.
- `source_file_paths`, `source_git_blob_ids`, `source_sha256_manifest_id`.

The exact threshold value must be looked up from the frozen G0-04 threshold artifact using asset + exact snapshot + policy + population. Do not recompute or substitute thresholds inside the candidate generator. Calibration must end strictly before the classified snapshot; minimum prior count is 180.

### 4.3 Signal and availability
- `signal_candle_open_ts_ms`, `signal_candle_close_ts_ms`, `signal_available_at_ts_ms`.
- `confirmation_rule_id`, `confirmation_bar_interval_ms`, `confirmation_status`.
- `first_eligible_execution_bar_open_ts_ms` — timestamp only, not an order or fill.
- `source_breakout_candidate_id` — required for failed-breakout reversal; otherwise NOT_APPLICABLE.
- `event_observed_at_ts_ms`.

All timestamps are UTC epoch milliseconds. Signal candle open, close, availability, confirmation and first eligible minute remain distinct fields. For all accepted events, the first eligible 1-minute bar opens exactly at signal availability; a missing exact bar is not shifted to a nearby minute.

### 4.4 Disposition and lifecycle
- `candidate_status`, `exclusion_reason`, `censoring_reason`, `ambiguity_flags`.
- `decluster_policy_id`, `invalidation_reference_type`, `invalidation_reference_value`, `invalidation_reference_ts_ms`.
- `expiry_rule_id`, `expiry_ts_ms`.
- `source_reconciliation_status`, `source_join_cardinality`.

For rejection and continuation point events, invalidation/expiry fields are NOT_APPLICABLE. For failed-breakout reversal, preserve source breakout ID and 12-hour horizon. Never simulate an entry, stop, target, fill or trade PnL.

## 5. Canonical source identity

- Rejection underlying physical identity: `asset|direction|snapshot_index|segment_id|test_rank|test_start_ts_ms`. The source `definition` field is historical cohort membership, not a second physical event. Preserve both original definition-specific source row IDs in `source_event_row_ids`; one physical event receives one causal disposition and one candidate identity.
- Breakout continuation: `asset|direction|signal_time_ms|context_snapshot_ms`, using the G0-04 raw crossing ledger. Each unique raw crossing remains separate, including overlaps.
- Failed-breakout reversal: source breakout candidate ID + completed 15-minute return-inside confirmation timestamp + rule version. Exactly one first qualifying completed return-inside confirmation per source breakout under the frozen lifecycle rule.

Strict/broad duplicate cohort rows are represented as historical cohort-membership metadata on one underlying physical event. Do not double-count a strict event as a second independent event within broad.

## 6. Mandatory disposition accounting

For each family and asset, report:
- raw source rows;
- unique source identities;
- eligible-for-further-validation;
- rejected by reason;
- expired by reason;
- censored by reason;
- duplicate identities and collisions;
- overlap-cluster counts and sizes;
- unexplained unmatched source rows.

Every source row must be accounted for. The sum of mutually exclusive dispositions must equal the source population after explicitly declared source-row collapsing. Unexplained missing identities must equal zero. Strict must remain nested within broad.

## 7. Current implementation boundary

The current 31-test synthetic suite covers core timestamp, snapshot, regime-threshold, nesting, family-direction, 15-minute completeness, source-linkage, horizon and determinism primitives. The read-only source audit separately verifies pinned sources and identity joins.

Before canonical candidate generation, add tests for the exact source-key joins, missing/duplicate rows, threshold lookup at exact snapshot availability, all disposition reason codes, family-specific warm-up and snapshot-expiry cases, and full reconciliation totals. Then run the source-only dry-run and inspect its artifact. Candidate generation remains blocked until that evidence is accepted.

No orders, fills, execution simulation, PnL, strategy backtests or Gate 2+ work are authorized.
