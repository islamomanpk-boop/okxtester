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
| Historical cohort memberships | Present | Now joined from Module B by exact raw-crossing identity and preserved | Present |
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

- `overlap_cluster_id`, `overlap_cluster_size`, and cluster start/end bounds are now emitted in all three source-only ledgers. Rejection uses the accepted Module A 24H interval-graph clusters with physical size recounted after strict/broad collapse; breakout continuation uses the same frozen Module B 12H interval-graph method applied to all 2,861 unique raw crossings; failed-breakout reversal inherits its linked source breakout cluster.
- Clusters are metadata only. No overlapping event is removed, merged or re-labelled.
- A separate `repeated_signal_group_id` rule remains unfrozen. Existing rejection test-rank/segment identity and distinct raw breakout crossing keys preserve repeated events without adding a new grouping rule.
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

The overlap-cluster metadata and cluster-size reporting gap has been closed as recorded below. A separate repeated-signal group identifier remains undefined; existing source identities continue to preserve repeated events. The canonical candidate fields listed in Sections 2–3 above remain unmaterialized.


## 8. Raw breakout historical cohort membership reconciled — 2026-11-26

The G0-04 raw crossing ledger contains a `was_historical_selected` boolean but does not itself expose per-event strict/broad cohort labels. The source-only audit now reconciles that flag to Module B's event rows by exact (asset, direction, signal timestamp, snapshot timestamp) identity and preserves the resulting `BROAD_P40` / `STRICT_P25` memberships in each breakout disposition row.

Implementation commit: `3f906768028ff686a526e43182dd8a3d2a672c13`.

Evidence:
- Source audit [45802913642](https://github.com/islamomanpk-boop/okxtester/actions/runs/45802913642) — SUCCESS; artifact ID `15108411917`; ZIP SHA-256 `181b395393c9f7d012c282b64d862f10f83639f974543acf3b139a20e7d7f6e5`, independently recomputed after download.
- Synthetic tests [45802929770](https://github.com/islamomanpk-boop/okxtester/actions/runs/45802929770) — SUCCESS; **86/86 tests passed**.
- The 2,861 raw crossing rows reconcile to 1,929 with no historical selected cohort, 272 broad-only, and 660 with both BROAD_P40 and STRICT_P25. No strict-only row exists.
- The raw selected flag must agree with the exact-key Module B membership; unknown labels and strict-without-broad fail closed.

Historical cohort membership is separate from causal eligibility. The 932 historically selected events are not treated as the only causally eligible events, and causal strict/broad classifications are not overwritten by historical cohort labels.


## 9. Frozen overlap-cluster metadata added — 2026-11-26

The source-only disposition audit now attaches deterministic overlap-cluster metadata without deleting or deduplicating any source event.

- Rejection: reuses the accepted Module A 24H interval-graph cluster IDs and start/end bounds. Cluster sizes are recalculated at the 1,154 physical-event grain after strict/broad cohort collapse, preventing nested cohort rows from inflating physical cluster size.
- Breakout continuation: applies the frozen Module B 12H per-asset interval-graph algorithm to all 2,861 unique G0-04 raw crossings. Each window begins at signal availability and ends after the observed 1-minute bars, capped at 720; exact source-minute continuity is required. The 932 Module B source events are cross-checked against their recorded `observed_bars_12h`.
- Failed-breakout reversal: inherits the overlap cluster of its linked source breakout and is not counted as a new source event cluster.

Evidence:
- Source audit [45803856975](https://github.com/islamomanpk-boop/okxtester/actions/runs/45803856975) — SUCCESS; artifact ID `15108946054`; ZIP SHA-256 `a3c5ca3bc224ea457134253506b5222248cc409563a2bfdeaa14a34ffecc62f9`, independently recomputed after download.
- Synthetic suite [45803874401](https://github.com/islamomanpk-boop/okxtester/actions/runs/45803874401) — SUCCESS; **93/93 tests passed**. Tests cover transitive overlap, half-open endpoint separation, deterministic ordering, multiple assets, non-positive windows, duplicate IDs, exact observed-window starts and cohort-cluster consistency.

Cluster summary:
- Rejection physical events: **380 clusters** across five assets; largest physical cluster size **16** (the accepted Module A cohort-row cluster maximum was 32 before strict/broad collapse).
- Breakout raw crossings: **1,037 clusters** across five assets; largest cluster size **14**.
- Failed-breakout rows inherit source breakout clusters; they are a subset and do not create additional cluster counts.

The original accepted Module A and Module B outputs remain unchanged. The G0-05 breakout cluster IDs are versioned separately as `g0_05_raw_overlap` because the cluster population now includes all 2,861 raw crossings, not only Module B's historical selected subset.
