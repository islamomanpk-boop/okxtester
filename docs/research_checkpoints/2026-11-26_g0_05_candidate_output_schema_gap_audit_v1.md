# G0-05 Canonical Candidate Output Schema Gap Audit — V1

**Date:** 2026-11-26  
**Scope:** Read-only comparison of the frozen candidate/disposition schema against the current source-only disposition artifact.  
**Disposition:** Source-only dispositions are reconciled; canonical candidate schema/output is not yet implemented. No candidate generation was run.

## 1. Controlling inputs

- Frozen field contract: `2026-11-26_g0_05_candidate_disposition_schema_v1.md`.
- Frozen family timing decisions: `2026-11-26_g0_05_family_timing_contract_decisions_v1.md`.
- Source-only disposition artifact: run [45802145534](https://github.com/islamomanpk-boop/okxtester/actions/runs/45802145534), artifact ID `15106714247`, ZIP SHA-256 `ef08831a8ad5bbb6326d4847b842b2e229cee4cdd174e4292cddbc45c96aa5bb`.
- Contract synthetic suite: run [45802241180](https://github.com/islamomanpk-boop/okxtester/actions/runs/45802241180), **80/80 PASS**.
- Independent raw 1-minute membership: run [45802348522](https://github.com/islamomanpk-boop/okxtester/actions/runs/45802348522), **PASS**.

The current artifact is explicitly a source-only disposition dry-run. Its rows must not be mistaken for canonical candidate records.

## 2. Existing source-only fields

| Field or property | Rejection | Breakout continuation | Failed-breakout reversal |
|---|---|---|---|
| Asset | Present | Present | Present |
| Family / subfamily | Support/resistance family present | Continuation family present | Reversal family present |
| Direction / LONG-SHORT mapping | Present | Present | Present |
| Physical/source identity | Source row IDs and source collapse identity represented | Exact raw source key present | Exact source key and Module B row IDs present |
| Historical cohort memberships | Present | Not yet preserved as a distinct historical membership field | Present |
| Causal strict/broad cohort | Present after reason-contract correction | Present | Present |
| Signal/confirmation timestamp | Confirmation present | Signal availability present | Signal and confirmation present |
| First eligible 1-minute timestamp | Eligible-only; independently verified | Eligible-only; independently verified | Eligible-only; independently verified |
| Disposition status | Present | Present | Present |
| Frozen reason code | Present and validated | Present and validated | Present and validated |
| Censoring reason | Present, blank for current uncensored rows | Present, blank for current uncensored rows | Present, blank for current uncensored rows |

## 3. Required canonical fields not yet materialized

The following items are not present as complete fields in the current three source-only ledgers. Some can be populated from frozen source joins; others require a versioned decision before generation.

### 3.1 Deterministic identity and version provenance

- `candidate_id`: deterministic candidate ID helper exists in the pure contract module, but no canonical candidate rows have been generated or collision-checked.
- `source_event_id`: physical source identity needs to be emitted in the canonical form for each family. The current rejection ledger retains contributing row IDs; breakout and failed-breakout retain source keys.
- `instrument_id`: map asset to exact OKX instrument identity using frozen instrument metadata, not a guessed string.
- `regime_definition_version`, `candidate_rule_version`, `source_pipeline_version`: version identifiers need to be frozen and emitted.
- `source_sha256_manifest_id`, source paths and blob IDs: current manifest pins the files globally, but candidate rows do not yet reference the manifest identifier and source-specific lineage.

### 3.2 Snapshot and threshold provenance

- Snapshot ID and validity start/end timestamps are not fully emitted in the source-only rows.
- Frozen upper/lower boundary values are not emitted in the three disposition CSVs.
- Exact threshold value, percentile, calibration start/end, and prior observation count are not emitted per row.
- Channel width, directional efficiency and overlap values are not emitted per row.
- The exact selected policy/population is known and used by the source audit, but the complete per-row provenance must be joined from the frozen G0-04 artifact and detector-feature sources.

### 3.3 Signal and confirmation anatomy

- Signal candle open, close, and availability are not all separately represented in each source-only row.
- Rejection source candle open and completed-close confirmation must remain separate fields in the canonical output.
- Failed-breakout confirmation rule ID, complete 15-minute component-bar proof, OHLC-path ambiguity flags, and source breakout candidate linkage are not fully materialized.
- The 12-hour failed-breakout observation endpoint/rule ID is not emitted as an explicit lifecycle field in the source-only row.
- The source breakout link can be constructed from the exact G0-04 raw crossing identity, but a canonical `source_breakout_candidate_id` cannot be populated until candidate IDs are generated deterministically in the same controlled build.

### 3.4 Dependence and event metadata

- `overlap_cluster_id` and `repeated_signal_group_id` are not currently emitted.
- The frozen decisions prohibit deleting or collapsing overlapping events, but the exact metadata-only cluster construction and reporting convention has not yet been specified. Do not invent a cluster window or use future outcomes to define one.
- Rejection test-rank/source repeated-test identity is preserved in source IDs, but a canonical repeated-signal group field is not yet materialized.
- `ambiguity_flags` are not emitted in the current source-only artifact.

### 3.5 Lifecycle fields

- For rejection and breakout continuation point events, invalidation and active-order expiry are NOT_APPLICABLE at G0-05; do not invent order lifecycle values.
- Failed-breakout reversal must carry its source breakout link, 12-hour observation rule, and endpoint. These are not yet fully represented as explicit canonical lifecycle columns.
- Canonical output must preserve `candidate_status`, `exclusion_reason`, `censoring_reason`, and ambiguity separately. The source-only artifact now validates status/reason/censoring semantics, but is not yet the final canonical schema.

## 4. Reporting gaps

The current source-audit report reconciles totals by family, but the final acceptance package still needs explicit structured summaries by:
- asset;
- family/subfamily;
- LONG/SHORT and upper/lower boundary;
- historical strict/broad membership;
- causal strict/broad/warm-up/not-eligible cohort;
- disposition and reason code;
- overlap cluster and cluster size, once the metadata-only cluster convention is frozen.

These summaries must reconcile exactly to the 4,947 source physical rows and the 2,857/1,884/206/0 disposition totals. They must not treat strict and broad labels as independent physical events.

## 5. Safe next work

Before canonical candidate generation, continue with contract-only and source-only work:
1. Freeze a field-level mapping from each family source to every canonical output field.
2. Specify the metadata-only overlap/repeated-signal grouping convention without deleting or de-duplicating events.
3. Specify exact source joins for boundaries, snapshots, thresholds, feature values, confirmation bars and Module B ambiguity fields.
4. Add deterministic synthetic tests for the complete canonical row schema, family-specific required/null fields, source-breakout links, and cluster metadata.
5. Add structured per-asset/family/side/cohort/reason disposition summaries to the source-only audit artifact.
6. Independently inspect the final field mapping, joins, row schema and deterministic serialization before any candidate generator is authorized.

## 6. Authorization boundary

This audit is descriptive and read-only. It does not authorize canonical candidate generation. No candidate rows, orders, fills, positions, execution simulation, PnL, strategy backtests, or phase transition were produced or authorized.


## 7. Structured disposition summaries added — 2026-11-26

The source-only audit now emits deterministic grouped counts for each family ledger:
- asset × disposition;
- family × LONG/SHORT × disposition × reason;
- source direction × disposition;
- causal cohort × disposition;
- reason code.

Implementation commit: `a1ef8721f3f770fb46079c09ea039da75a7e920e`.

Evidence:
- Source-audit workflow [45802587303](https://github.com/islamomanpk-boop/okxtester/actions/runs/45802587303) — SUCCESS; artifact ID `15108166636`; ZIP SHA-256 `456c683375d20ebef8a852421d235e745d2c79f62be29d2eea18045d59b455cc`, independently recomputed after download.
- Synthetic workflow [45802605906](https://github.com/islamomanpk-boop/okxtester/actions/runs/45802605906) — SUCCESS; **81/81 tests passed**. Added a deterministic grouped-count test confirming row totals reconcile regardless of input order.

This closes the previously noted absence of asset/family/side/causal-cohort/reason grouped disposition summaries in the source-audit report. The summary is descriptive and does not alter or collapse source rows.

Remaining reporting gaps include historical strict/broad membership detail for the raw breakout family, overlap-cluster/repeated-signal metadata and cluster-size reporting. Their construction convention must be frozen without removing overlapping events or using future outcomes. The canonical candidate fields listed in Sections 2–3 above remain unmaterialized.
