# Phase 3 G0-05 — Owner-Authorized Canonical Candidate Ledger Build

**Date:** 2026-11-28  
**Repository:** `islamomanpk-boop/okxtester`  
**Branch:** `price-action-v1`  
**Authorization:** Explicit project-owner approval in the conversation on 2026-11-28.  
**Status:** Real canonical ledger generated; full 60-field row validation and cross-row linkage validation passed. G0-05 evidence artifact remains subject to review; this does not pass Gate 0 or authorize execution/PnL work.

## 1. Workflow and artifact

- Workflow: [46149804561](https://github.com/islamomanpk-boop/okxtester/actions/runs/46149804561) — SUCCESS.
- Workflow commit: `26ac706767d3f9b490cfa2b8250c13417f46b356`.
- Artifact: `phase3-g0-05-canonical-candidate-ledger-46149804561`.
- Artifact ID: `15265550848`.
- Artifact ZIP SHA-256: `e66ea4b16811d158a9b86dfb90113be13cc5fccfc89f1c42b5330fba294456da`.
- Artifact size: 2,587,810 bytes; not expired at time of verification.
- Artifact contains the source audit outputs, source manifest, independent source verification, canonical build report and canonical ledger exports.

The workflow re-downloaded the exact pinned G0-04 artifact (ID `15087542445`, source run `45756061179`), verified its frozen SHA-256 before extraction, re-ran the primary source provenance/disposition audit, re-ran the independent source identity/lifecycle verifier, and only then invoked the owner-authorized canonical builder. No manual workflow dispatch was used.

## 2. Real canonical ledger result

<badge>G0_05_REAL_CANONICAL_CANDIDATE_LEDGER_BUILD_AND_VALIDATION_PASS</badge>

- Canonical records: **4,947**.
- Required fields per record: **60 exactly**.
- Candidate rule version: `G0_05_CANDIDATE_RULE_V1`.
- Deterministic candidate IDs: unique and recomputed.
- Family/source-event identity uniqueness: passed.
- Full canonical record validator: passed on all 4,947 real records.
- Full ledger validator: passed.
- Failed-breakout source candidate links: **932 / 932** resolved to the exact linked breakout candidate.
- Canonical disposition counts exactly match source-only disposition counts.

### Family counts

| Family | Canonical records |
|---|---:|
| SUPPORT_REJECTION | 558 |
| RESISTANCE_REJECTION | 596 |
| BREAKOUT_CONTINUATION | 2,861 |
| FAILED_BREAKOUT_REVERSAL | 932 |
| **Total** | **4,947** |

### Reconciled dispositions

| Family group | Eligible | Rejected | Expired | Censored |
|---|---:|---:|---:|---:|
| Rejection (support + resistance) | 1,083 | 31 | 40 | 0 |
| Breakout continuation | 1,038 | 1,823 | 0 | 0 |
| Failed-breakout reversal | 735 | 30 | 167 | 0 |
| **Total** | **2,856** | **1,884** | **207** | **0** |

The single return-inside observation exactly at +12 hours remains excluded from canonical confirmation under the strict half-open horizon. It is not counted as an eligible failed-breakout event.

## 3. Canonical output integrity

- `g0_05_canonical_candidate_ledger.jsonl` SHA-256:
  `202c44f456af021b9ec8cc642e82c349f4858baadb04bcdb2342973cb752db14`
- `g0_05_canonical_candidate_ledger.csv` SHA-256:
  `eca9f326bc44a74ba9631bc6b5d4a6c7b5691fea6b59c7031976f7fd7f5ff1a5`

The builder checks source-audit pass status, source-manifest identity, all three source-only input row counts, each row's manifest ID, frozen family disposition totals, exact 60-field shape, canonical record validation, candidate ID uniqueness, source-event uniqueness, exact-once reconciliation and failed-breakout cross-row inheritance/linkage before writing outputs.

## 4. Real-data issue found and corrected

The first authorized real-row attempt stopped at the canonical validator because the source audit encoded absent historical cohort membership as the string `NONE`. The canonical contract models membership as a list of zero or more actual cohort labels; `NONE` is not a membership label. The source mapper was corrected to serialize absence as an empty membership list. The corrected workflow re-ran the source audit and independent verifier from the frozen inputs and then passed the complete real canonical build.

The first failed attempt did not produce a canonical ledger. The successful artifact above is from the corrected workflow.

## 5. Gate and scope boundary

**Real G0-05 canonical candidate/disposition ledger: GENERATED AND VALIDATED.**

This closes the specific previously missing real-row generation/validation step. It does **not by itself** declare Gate 0 passed. Remaining independent Gate 0 requirements include funding-engine/settlement-mark acceptance, fee/instrument assumptions, standalone sizing, contract rounding, stop-gap risk and execution-engine readiness.

No orders, fills, execution simulations, PnL, strategy comparisons, strategy selection or live trading were run or authorized. Gate 2 and later remain closed. Phase 3 strategy PnL backtesting is not authorized.

**Next safe action:** inspect the canonical evidence artifact and conduct a read-only post-build reconciliation/review against the accepted G0-05 field mapping, source manifest and family counts. Only after that review should the G0-05 gate status be formally updated. Gate 0 blockers remain separate.
