# G0-05 Candidate Field-Value Decisions — V1

**Date:** 2026-11-26  
**Scope:** Freeze version identifiers and controlled field values required to implement the already-frozen G0-05 candidate/disposition schema.  
**Status:** Contract decisions for future implementation; no candidate rows generated.

## 1. Version identifiers

| Field | Frozen value |
|---|---|
| `regime_definition_version` | `SIDEWAYS_DETECTOR_ORIGINAL_V1` |
| `candidate_rule_version` | `G0_05_CANDIDATE_RULE_V1` |
| `source_pipeline_version` | `G0_04_CAUSAL_RECONSTRUCTION_V1+MODULE_A_V1_1+MODULE_B_V1_1` |
| `decluster_policy_id` | `G0_05_INTERVAL_GRAPH_METADATA_V1` |

The source-pipeline value is a provenance label, not a claim that all three modules contribute to every family. Family-specific paths remain explicit.

## 2. Instrument IDs

Use the exact OKX USDT-swap instrument ID:

`{ASSET}-USDT-SWAP`

for BTC, ETH, SOL, DOGE and AVAX.

Evidence: the static semantic review of the original VPS downloader records that instrument IDs are constructed as `{asset}-USDT-SWAP`; the read-only VPS SQLite/CSV reconciliation independently lists the same five instrument IDs. The G0-05 canonical Git CSVs are a separately versioned snapshot, so this mapping identifies the market instrument, not the acquisition snapshot or source-file provenance.

## 3. Confirmation rule identifiers

All confirmation bars are 15 minutes (900,000 ms). The signal candle open, close and availability timestamps remain distinct.

| Family | `confirmation_rule_id` | Confirmation / availability |
|---|---|---|
| SUPPORT_REJECTION / RESISTANCE_REJECTION | `STRONG_REJECTION_15M_CLOSE_V1` | First strong rejection candle close = source rejection candle open + 900,000 ms. |
| BREAKOUT_CONTINUATION | `BOUNDARY_CROSSING_15M_CLOSE_V1` | Completed 15m crossing candle close timestamp. |
| FAILED_BREAKOUT_REVERSAL | `RETURN_INSIDE_15M_CLOSE_V1` | First completed 15m close back inside the original source breakout boundary, requiring all 15 component 1m bars. |

`confirmation_status` has exactly:
- `CONFIRMED` — the family-specific confirmation/availability timestamp is observed, even if a separate source, snapshot or causal condition makes the disposition REJECTED or EXPIRED.
- `NOT_CONFIRMED` — the predeclared confirmation did not occur before a complete expiry horizon.
- `CENSORED` — confirmation could not be determined because required source data is incomplete, gapped or ends before resolution.
- `NOT_APPLICABLE` — no confirmation rule applies to the row; this should not be used for the three G0-05 families when a source event exists.

The disposition status remains the controlling eligibility/expiry/censoring field. A confirmed signal can still be REJECTED because its source breakout is not causally eligible.

## 4. Source reconciliation values

`source_reconciliation_status` has exactly:
- `EXACT_SOURCE_MATCH`
- `EXACT_PHYSICAL_EVENT_COLLAPSE` — one physical rejection/reversal identity reconciled to its one or two immutable definition-specific rows.
- `DECLARED_SUBSET_MATCH` — Module B's 932 physical source events are an exact subset of the G0-04 raw crossing population.
- `EXACT_LINKED_SOURCE_BREAKOUT` — failed-breakout disposition links to exactly one G0-04 raw crossing identity.

`source_join_cardinality` has exactly:
- `ONE_RAW_CROSSING_TO_ONE_DISPOSITION`
- `ONE_PHYSICAL_EVENT_TO_ONE_OR_TWO_COHORT_ROWS`
- `ONE_FAILED_BREAKOUT_TO_ONE_SOURCE_BREAKOUT`

Do not use generic PASS labels where the cardinality is materially different.

## 5. Candidate and source-event identity

Use the existing pure helper `candidate_id(source_identity, family, rule_version)`, which returns SHA-256 of its canonical payload. Before generation, add collision detection across all four families and deterministic serialization tests.

- Rejection `source_event_id`: existing physical identity `asset|direction|snapshot_index|segment_id|test_rank|test_start_ts_ms`.
- Breakout `source_event_id`: `asset|direction|signal_time_ms|context_snapshot_ms`.
- Failed-breakout `source_event_id`: `source_breakout_source_event_id|confirmation_ts_ms`; if no completed return-inside confirmation exists, use the literal sentinel `NO_CONFIRMATION` in place of the timestamp. Such a row is an EXPIRED/CENSORED/REJECTED disposition record, not a confirmed reversal candidate.

`source_breakout_candidate_id` is derived at the final canonical build from the exact source breakout `source_event_id` using the deterministic candidate-ID helper and `G0_05_CANDIDATE_RULE_V1`, regardless of whether that source breakout's own disposition is eligible or rejected. The source-only disposition ledger preserves `source_breakout_source_event_id` but does not emit candidate IDs. This preserves an auditable link for failed-breakout rows rejected due to an invalid source breakout.

## 6. Event-observed timestamp

- Rejection: completed rejection confirmation timestamp.
- Breakout continuation: completed crossing close / signal availability timestamp.
- Failed-breakout reversal: completed return-inside confirmation timestamp; if no confirmation, the row's event-observed timestamp is the source breakout's 12-hour expiry endpoint and `confirmation_status=NOT_CONFIRMED` or `CENSORED` as appropriate.

The event-observed timestamp is not a fill or execution timestamp.

## 7. Ambiguity flags

Use a semicolon-delimited, sorted list of controlled flags; use `NONE` when no flag applies.

The mandatory failed-breakout confirmation flags distinguish:
- `CONFIRMATION_CANDLE_OPEN_OUTSIDE_CLOSE_INSIDE` — the completed 15m confirmation candle opens beyond the original breakout boundary and closes back inside.
- `CONFIRMATION_CANDLE_WICK_OUTSIDE_CLOSE_INSIDE` — the candle opens at/inside the boundary, but its high/low extends beyond the boundary before the close returns inside.

The close-based rule still confirms the event; the flag records that the 15m OHLC does not reveal the intrabar path. The flags are mutually exclusive for a single boundary-side confirmation candle.

This flag must be computed from the exact 15 component 1m bars. If any component is missing, do not infer OHLC; disposition the event under the frozen incomplete/gap rule. Do not substitute later Module B retest ambiguity fields for confirmation-candle ambiguity.

Additional flags require a versioned contract amendment before emission.

## 8. Lifecycle fields

- `invalidation_reference_type`, `invalidation_reference_value`, and `invalidation_reference_ts_ms` are `NOT_APPLICABLE` for all G0-05 point-event availability rows. No stop, trade invalidation or order lifecycle is represented.
- Rejection and breakout continuation `expiry_rule_id` and `expiry_ts_ms` are `NOT_APPLICABLE`.
- Failed-breakout reversal `expiry_rule_id = SOURCE_BREAKOUT_12H_RETURN_INSIDE_V1`; `expiry_ts_ms = source_breakout_signal_time_ms + 43200000`.
- Failed-breakout source breakout boundary and snapshot remain immutable throughout the 12-hour observation lifecycle.

## 9. Source manifest identifier

`source_sha256_manifest_id` is the SHA-256 of the exact `source_manifest.json` bytes included in the source-audit artifact. For the complete source-audit manifest V2 in run 45806239609 / artifact 15109506588, the value is:

`82bce2b7549efb959a2805641cfda46c1ea6a158e8e6c7d24cd8f3795ca80bbb`

This is the SHA-256 of the exact `source_manifest.json` bytes. The earlier 7-file-only manifest ID is superseded. Every later source-audit run must use its own computed hash; never reuse this ID after the manifest or source-audit revision changes.

## 10. Remaining implementation checks

Before candidate generation:
1. Add these controlled values to the full schema validator.
2. Implement the exact 15-component 1m confirmation-candle OHLC aggregation and failed-breakout ambiguity flag.
3. Verify each instrument ID against the acquisition source metadata and all five source file identities.
4. Implement deterministic candidate IDs, including the failed-breakout no-confirmation sentinel, and collision checks.
5. Implement exact family-specific source path/blob lineage and manifest ID.
6. Add synthetic tests for every controlled enum, family-specific NOT_APPLICABLE fields, no-confirmation identity, source-breakout linkage, and ambiguity.
7. Independently review the full candidate field mapping and output serializer before candidate generation.

## 11. Authorization boundary

This document freezes field values and identity semantics only. It does not authorize canonical candidate generation, execution simulation, strategy backtests, PnL or a phase transition.


## 12. Confirmation OHLC ambiguity implementation evidence

The source-only audit now independently aggregates every observed failed-breakout confirmation 15m candle from its exact 15 component 1m OHLC bars and emits `confirmation_status`, `confirmation_rule_id`, `confirmation_bar_interval_ms`, and `ambiguity_flags`.

- Source audit [45805545548](https://github.com/islamomanpk-boop/okxtester/actions/runs/45805545548) — SUCCESS; artifact ID `15109271179`; ZIP SHA-256 `d4bde5c29d32ad1a2ccab7c9d1c35a26eec3e7f9e642dc01b0178d9b6e4c9d25`, independently recomputed after download.
- Synthetic suite [45805565739](https://github.com/islamomanpk-boop/okxtester/actions/runs/45805565739) — SUCCESS; **102/102 tests passed**.
- Rejection: 1,154/1,154 confirmation timestamps classified CONFIRMED.
- Breakout continuation: 2,861/2,861 completed 15m crossing signals classified CONFIRMED.
- Failed breakout: 756 observed return-inside confirmations were rebuilt from 15 exact 1m component bars and classified CONFIRMED; 176 rows had no return-inside confirmation and were classified NOT_CONFIRMED.
- The 756 confirmation bars all had an OPEN_OUTSIDE_CLOSE_INSIDE ambiguity flag in this source population; no wick-only flag was observed. The flag is preserved and does not suppress or alter a close-confirmed event.
- Family disposition totals did not change: 2,857 eligible, 1,884 rejected, 206 expired, 0 censored.

The source audit checks the confirmation component bars and OHLC validity. The independent raw minute verifier separately checks the five full timestamp grids and eligible timestamp membership; its rerun against this artifact is tracked separately.


## 13. Complete source manifest V2 and per-row lineage

The source audit now emits a complete `G0_05_COMPLETE_SOURCE_MANIFEST_V2` containing:
- all seven pinned repository input files;
- the frozen G0-04 artifact identity, ZIP hash, code revision and all eight artifact member hashes (including run metadata);
- accepted Module A event output and run metadata;
- Module B event, horizon and run-metadata files;
- all five raw 1-minute market files with row counts, SHA-256 and Git blob SHA-1;
- the source-audit code revision and Actions run identity.

Each source-only disposition row now carries:
- `source_sha256_manifest_id` equal to the SHA-256 of the exact manifest bytes;
- family- and asset-specific `source_file_paths`;
- the corresponding repository `source_git_blob_ids`. G0-04 artifact members are linked by path and SHA-256 in the complete manifest rather than Git blob IDs.

Evidence:
- Source audit [45806239609](https://github.com/islamomanpk-boop/okxtester/actions/runs/45806239609) — SUCCESS; job `139862147342`; artifact ID `15109506588`.
- Artifact ZIP SHA-256: `c87808aaac2be5d7013d42d3f93fcbb0ed44d1602470c030642fcf6ffc75efcb`, independently recomputed after download.
- Exact `source_manifest.json` SHA-256 / row manifest ID: `82bce2b7549efb959a2805641cfda46c1ea6a158e8e6c7d24cd8f3795ca80bbb`; independently recomputed and matched the report and every row.
- The manifest includes 7 repository inputs, 8 G0-04 artifact files, 2 Module A files, 3 Module B files, and 5 raw market inputs.
- All 4,947 disposition rows have exactly one identical manifest ID; per-row source paths correctly select the matching asset's feature and 1m market file.

This supersedes the earlier incomplete source manifest. The independent minute verifier is being rerun against this complete-manifest artifact.


## 14. Independent minute verification against complete manifest V2

The independent verifier consumed the source-only disposition artifact produced with the complete manifest V2:

- Workflow [45806451121](https://github.com/islamomanpk-boop/okxtester/actions/runs/45806451121) — SUCCESS; job `139862911450`.
- Artifact ID `15110066577`.
- ZIP SHA-256 `fdbd4121aa14d047b4b0a83239860bf6ef3f097b0626ba7de63eedc8812f630c`, independently recomputed after download.
- Result: `INDEPENDENT_EXACT_MINUTE_MEMBERSHIP_PASS`; all five raw market files re-hashed and checked for strict ordering, minute alignment and continuity; 2,857/2,857 eligible timestamps present; 2,090 non-eligible rows have blank first-eligible timestamps.

The manifest ID in the source audit rows remains `82bce2b7549efb959a2805641cfda46c1ea6a158e8e6c7d24cd8f3795ca80bbb`, and the independent minute check did not alter source populations.


## 15. One-4H-lagged breakout context mapping correction

The first canonical field-mapping attempt incorrectly tried to join G0-04 raw breakout `efficiency` and `overlap` to the original detector feature row at the same context timestamp. The source audit correctly failed closed on a BTC mismatch.

Inspection of the accepted G0-04 reconstruction code showed the raw crossing ledger uses `historical_breakout_context`, whose channel is intentionally one completed 4H candle lagged. Its channel boundaries and width cross-check to the original detector feature row at:

`reference_feature_snapshot_ts_ms = context_snapshot_ms - 14,400,000`

The raw G0-04 row remains authoritative for its `efficiency` and `overlap` values; those are computed from the historical breakout context and are not required to equal the original detector feature row's directional efficiency/mean overlap.

Correct family mapping:
- Rejection: exact original detector feature row at `snapshot_ms`; `regime_definition_version=SIDEWAYS_DETECTOR_ORIGINAL_V1`.
- Breakout / failed breakout: exact G0-04 raw context at `context_snapshot_ms`; verify `upper`, `lower` and `channel_width_pct` against the detector feature row one 4H bar earlier; use raw context `efficiency` and `overlap`; `regime_definition_version=HISTORICAL_BREAKOUT_CONTEXT_V1`.
- Breakout/failed-breakout context validity ends at the next 4H context snapshot (`context_snapshot_ms + 14,400,000`), subject to the source's complete 4H grid.

The source audit now performs this lagged channel cross-check and preserves `reference_feature_snapshot_ts_ms` plus `reference_feature_match_status` (`MATCHED_ONE_4H_LAG` or `EXPECTED_LEADING_LEGACY_BOUNDARY`). At most one distinct leading context per asset is permitted. It no longer incorrectly compares historical-context efficiency/overlap to same-time detector values.
