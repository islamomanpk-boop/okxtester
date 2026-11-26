# G0-05 Independent Row-Level Source-Disposition Reconciliation — V1

**Date:** 2026-11-26  
**Project:** OKX Price Action V1 — Phase 3 Sideways / Range  
**Review mode:** Independent, read-only artifact and source reconciliation  
**Disposition:** `DATA_RECONCILIATION_MATCHED_WITH_FOLLOW-UP_FINDINGS`  
**Gate decision:** NOT A G0-05 GATE PASS; NOT AUTHORIZATION FOR CANONICAL CANDIDATE GENERATION.

## 1. Scope and pinned evidence

This review independently inspected the generated G0-05 source-disposition artifact and reconciled its row identities and classifications against the G0-04 raw-crossing artifact and the pinned historical source ledgers.

### G0-05 source-disposition run

- Workflow run: [45784746198](https://github.com/islamomanpk-boop/okxtester/actions/runs/45784746198)
- Checked-out code revision: `5aeafd08f063cb4c515fa2b4c000fa526fb95a38`
- Artifact ID: `15100091580`
- ZIP SHA-256: `8616483b6932bdd0e9976ba31e150b2d93882455365e51cad180a1d94e23eda9`
- `source_audit_report.json` SHA-256: `9cdd341a172d1d1ae9ce2eccf1ca4cbd89e05d9c915b54e5d294cbf13c0db9b4`
- `source_manifest.json` SHA-256: `abd869c9c11a31f42ae916bc56492977dce79dd18f5e2c9c9b1f23584629a440`

The downloaded ZIP digest was recomputed and matched. All three output CSV SHA-256 values were independently recomputed and matched the recorded values:

| Output | SHA-256 |
|---|---|
| `rejection_source_dispositions.csv` | `797456556a4dd6c55dc5a14dc891860a7235c3d759cac371bb770cd32334eea4` |
| `breakout_source_dispositions.csv` | `71df0aa38be5e90767009dbb71616baf45e99ca3a2e8104a319f50342b2b7ff0` |
| `failed_breakout_source_dispositions.csv` | `910cf2b54eae40e97fc38e105632dde070a8c4f33371a918a4e10f7c5aebd2ce` |

### G0-04 reference artifact

- Workflow run: [45756061179](https://github.com/islamomanpk-boop/okxtester/actions/runs/45756061179)
- Code revision: `86b49598d676b6ab00649bf31d4490ffbb1e608f`
- Artifact ID: `15087542445`
- ZIP SHA-256: `ef6204b546b49880675514ff76b4f6cb86e2821ba2b0d1d5412549927388f0a1`

The G0-04 ZIP digest was independently recomputed and matched. All seven output-file SHA-256 values matched the artifact's `run_metadata.json`.

## 2. Independent row-level results

### 2.1 Rejection family — matched

Pinned source blobs inspected:
- Boundary ledger: `2af6f85cd60194019f903a17f16216841ae61f8c`
- Event anatomy: `c58de65ec1936607790c2ee40b828897e6f726dc`
- Feature ledgers: BTC `e422073b993cf5d9d11050216509165277339710`; ETH `c38641d3846931afd6e44a7f39318251fe3c5653`; SOL `5ba90a99a33924f3de6bcbe9cd1d76aa0a9dd207`; DOGE `5fb8cb621628e069b1e2500f8047eb908b031909`; AVAX `06b6f7ee947ef5e62b8cf2b9cc64fb7caaa523e5`.

Independent checks:
- 1,992 confirmed boundary-ledger rows produced 1,992 unique definition-specific event identities.
- All 1,992 identities matched the 1,992 anatomy records one-to-one; no missing or extra IDs.
- All 1,992 confirmation timestamps matched rejection-candle open + 900,000 ms.
- Frozen upper/lower boundaries matched the corresponding feature snapshot.
- Current and next snapshot availability timestamps matched the indexed feature rows.
- No source snapshot was later than its rejection candle open.
- The 1,154 collapsed physical events were unique. All 838 strict physical events were nested in broad; 316 were broad-only.
- Snapshot-endpoint confirmations reconciled to 40 broad and 29 strict cohort rows.

The generated rejection ledger contained 1,154 physical events: 1,083 eligible, 31 rejected, and 40 expired. Its membership labels and source-row-ID counts were internally consistent, with no duplicated source IDs across physical rows. Family mapping was lower-boundary LONG / upper-boundary SHORT.

### 2.2 Breakout continuation — matched

- G0-04 raw crossing ledger: 2,861 rows and 2,861 unique full-grain keys.
- All 2,861 generated breakout ledger keys matched the G0-04 raw-crossing key set exactly; no left-only or right-only keys.
- The selected `EXPANDING_PRIOR + UNIQUE_4H_FEATURE_ROWS` threshold join covered 2,599 events; 262 were pre-calibration warm-up events with no threshold row under any of the six policy/population variants.
- Recomputed strict and broad flags matched every stored selected-variant flag: strict 794, broad 1,038.
- Strict remained a subset of broad.
- Every joined threshold's last prior context was strictly earlier than its classified snapshot; each raw context snapshot was no later than its signal timestamp.
- All six stored eligibility flags were false for all 262 warm-up events.
- The generated ledger contained 1,038 eligible rows and 1,823 rejected rows: 262 warm-up and 1,561 regime-ineligible.
- Family mapping was upper breakout LONG / lower breakout SHORT.

### 2.3 Failed-breakout reversal — matched

Pinned Module B source blobs:
- Event ledger: `da00c6682719864eaee3a491330d57f4d6fd2b39`
- Horizon ledger: `068e2b90b9824f7c68818c0eb913608db6b8a568`

Independent source reconciliation:
- 1,592 event rows had 1,592 unique event IDs and 932 unique physical source keys.
- Cohort collapse was 660 physical events with both BROAD_P40 and STRICT_P25 rows, plus 272 broad-only physical events.
- All 6,368 horizon rows were reconciled: every event had exactly four horizon rows (15M, 1H, 4H, 12H); there were no missing or extra event IDs.
- For all 1,592 events, the 12H horizon `complete` flag matched the event ledger's `complete_12h` flag, and the 12H horizon's first 15-minute return-inside confirmation timestamp matched the event ledger.
- Every non-null confirmation was strictly after the source breakout and no later than 12 hours after it.
- The 932 generated physical source keys matched G0-04 raw crossings exactly.
- All 932 generated source-event ID lists were internally unique and had the expected one- or two-row cohort membership structure.

Generated disposition counts were 736 eligible, 166 expired, and 30 rejected because the linked source breakout was not causally eligible. The 166 expired events had complete 12-hour observation and no return-inside confirmation. The 736 eligible events had a completed confirmation. All 756 non-null confirmations in the output were within the 12-hour horizon. Family mapping was upper-breakout failure SHORT / lower-breakout failure LONG.

## 3. Exact-minute and market-data limitation

The G0-05 source-audit code was inspected. It:
- hashes each of the five canonical 1-minute files before timestamp lookup;
- checks the expected CSV schema;
- rejects off-grid and duplicate 1-minute timestamps;
- checks that the exact availability timestamp exists in that asset's 1-minute open-time set; and
- does not substitute a neighboring minute.

The workflow report records all five market-data row counts and SHA-256 values matching the frozen G0-04 values, and reports all 2,857 eligible rows as passing exact timestamp membership.

In this independent review, the raw five market-data CSVs were not separately downloaded and re-hashed. Therefore the exact timestamp-membership result is corroborated by source-code inspection and the pinned workflow artifact, but was not independently recomputed against all five raw market-data files in this review.

The source audit's `minute_check` verifies presence of the first exact minute; it does not test continuity of a subsequent multi-minute sequence. That is appropriate for this first-minute availability check only. Any later calculation requiring a continuous forward 1-minute path must perform its own gap/continuity check.

## 4. Findings and follow-up actions

### F-01 — Horizon rows are not fully reconciled by the source-audit implementation

- **Severity:** Medium (audit coverage; no current source-data mismatch found)
- **Status:** Confirmed implementation gap
- **Evidence:** In `research/phase3_g0_05_source_manifest_audit_v1.py`, `audit_module_b` checks the horizon file's existence, SHA-256 against Module B metadata, and total row count (lines 396–418). It does not group horizon rows by event ID, require exactly four horizon types per event, or compare the 12H completion/confirmation fields against the event ledger. The failed-breakout dry-run derives its disposition from event-ledger fields (lines 560–603).
- **Independent result:** The current pinned source data passed those missing checks: 6,368 rows, exactly four per each of 1,592 events; no missing/extra IDs; 12H completion and confirmation fields matched.
- **Impact:** The current data reconciles, but future audit runs do not automatically enforce the horizon-to-event relationship that this independent review checked.
- **Recommended action:** Add deterministic checks for event-ID coverage, four distinct horizon labels per event, 12H completion parity, 12H confirmation parity, and confirmation timing. Add synthetic tests for missing, duplicate, extra and mismatched horizon rows.
- **Gate impact:** Follow-up required before treating the source-audit implementation as fully self-verifying; not evidence of a current row mismatch.

### F-02 — Rejected failed-breakout rows can carry a field named as an eligible-minute timestamp

- **Severity:** Low (schema clarity / downstream misuse prevention)
- **Status:** Confirmed
- **Evidence:** In `research/phase3_g0_05_source_manifest_audit_v1.py`, failed-breakout output assigns both `confirmation_ts_ms` and `first_eligible_1m_open_ts_ms` from the observed confirmation regardless of the final disposition (lines 586–603). In the generated artifact, 30 rows are REJECTED because their source breakout is not causally eligible; 20 of those rejected rows nevertheless have a non-null `first_eligible_1m_open_ts_ms`.
- **Impact:** The disposition status correctly marks these rows rejected, so this did not change the 736/166/30 accounting. However, the field name can mislead downstream consumers into treating a rejected event as having an eligible minute.
- **Recommended action:** Preserve the observed lifecycle timestamp in a clearly named field such as `observed_confirmation_minute_open_ts_ms`; populate `first_eligible_1m_open_ts_ms` only for `ELIGIBLE_FOR_FURTHER_VALIDATION` rows. Add a regression test for a rejected source event with a valid observed confirmation.
- **Gate impact:** Correct or explicitly resolve before canonical candidate generation; not a current source-identity or disposition-count mismatch.

## 5. Consolidated accounting

| Family | Source physical rows | Eligible | Rejected | Expired | Censored |
|---|---:|---:|---:|---:|---:|
| Rejection | 1,154 | 1,083 | 31 | 40 | 0 |
| Breakout continuation | 2,861 | 1,038 | 1,823 | 0 | 0 |
| Failed-breakout reversal | 932 | 736 | 30 | 166 | 0 |
| **Total** | **4,947** | **2,857** | **1,884** | **206** | **0** |

All three generated ledger populations reconcile to their expected source identities and mutually exclusive disposition totals. No unexplained source-key mismatch was found.

## 6. Boundaries and conclusion

- This review generated no candidates and made no changes to source data.
- No orders, fills, positions, PnL, execution simulation, profitability claims or strategy conclusions were evaluated.
- The source audit's market-data timestamp membership was inspected but not independently recomputed from all five raw 1-minute files in this review.
- The two findings above are follow-up requirements for audit coverage and schema clarity.
- **Independent disposition:** Current row-level source identities, cohort memberships, threshold flags and failed-breakout horizon mappings reconcile. This report is not a G0-05 gate approval. Canonical candidate generation remains blocked pending disposition of the findings, completion of the remaining required tests/review, and separate authorization.
