# G0-05 Disposition Contract and Audit-Coverage Follow-up — V1

**Date:** 2026-11-26  
**Parent records:**  
- `2026-11-26_g0_05_independent_row_level_reconciliation_v1.md`
- `2026-11-26_g0_05_independent_reconciliation_followup_v1.md`

**Gate decision:** No G0-05 gate pass is declared. Canonical candidate generation remains blocked.

## 1. F-03 — Snapshot expiry reason/status mismatch resolved

The frozen schema previously listed `SNAPSHOT_EXPIRED_BEFORE_CONFIRMATION` under `REJECTED`, while the source-disposition implementation correctly classified the 40 snapshot-validity-endpoint cases as `EXPIRED`.

The schema now classifies `SNAPSHOT_EXPIRED_BEFORE_CONFIRMATION` under `EXPIRED`, with the meaning that the source snapshot's predeclared validity interval ended before rejection confirmation. This aligns the schema with the existing source disposition and preserves the 40-event count. No historical output was rewritten.

## 2. Additional contract and audit-coverage safeguards

The G0-05 contract now includes:
- controlled REJECTED, EXPIRED and CENSORED reason-code sets;
- validation that eligible rows use `exclusion_reason=NONE`;
- validation that CENSORED rows carry matching non-empty censoring and exclusion reasons;
- exact asset + snapshot + policy + population threshold lookup, with no nearest-snapshot fallback;
- fail-closed validation that threshold calibration ends strictly before the classified snapshot and contains at least 180 prior contexts;
- exact source-key equality or explicit subset reconciliation, with duplicate-key rejection.

The source-audit implementation now uses the exact threshold lookup and source-key reconciliation helpers. Before writing its three ledgers, it also verifies:
- expected physical source population size;
- nonblank and unique physical source identity per output row;
- only the four permitted disposition statuses; and
- disposition counts sum exactly to the expected source population.

The synthetic suite now covers the full controlled reason-code sets, exact threshold lookup/missing-neighbor behavior, prior-context constraints, exact and subset source-key joins, duplicate/missing/extra keys, and disposition ledger population/identity/status accounting.

## 3. Workflow verification

### Candidate contract and expanded synthetic tests

- Run: [45799630705](https://github.com/islamomanpk-boop/okxtester/actions/runs/45799630705) — SUCCESS.
- Commit: `28f08bb392edec38ec408c20324591e777e32343`.
- The test file contains 76 synthetic test methods; the workflow's compile and test steps both succeeded.

### Final integrated read-only source audit

- Run: [45799690941](https://github.com/islamomanpk-boop/okxtester/actions/runs/45799690941) — SUCCESS.
- Job: `139839356439`.
- Checked-out commit: `db189ea2fd23a9edaf2e8d08f6b1486a1cab4a06`.
- Artifact ID: `15106213659`.
- Artifact ZIP SHA-256: `544a8b90f34be3931b2a91963d5d692a949fc3afd19ad0f8ce78322152c39a72` (independently recomputed after download).
- Report status: `G0_05_SOURCE_PROVENANCE_AND_IDENTITY_AUDIT_PASS`.

An intermediate source-audit run at commit `2f50850bcf142017708efd1ab71a8bbc3a0bdaf8` failed during module import after the new shared contract helpers were introduced. The import path was corrected in commit `db189ea2fd23a9edaf2e8d08f6b1486a1cab4a06`; the subsequent integrated source-audit run completed successfully.

## 4. Final verified disposition totals

The integrated audit preserves the same mutually exclusive source accounting:

| Family | Source rows | Eligible | Rejected | Expired | Censored |
|---|---:|---:|---:|---:|---:|
| Rejection | 1,154 | 1,083 | 31 | 40 | 0 |
| Breakout continuation | 2,861 | 1,038 | 1,823 | 0 | 0 |
| Failed-breakout reversal | 932 | 736 | 30 | 166 | 0 |
| **Total** | **4,947** | **2,857** | **1,884** | **206** | **0** |

The Module B horizon reconciliation remains 1,592 events to 6,368 horizon rows, exactly four distinct horizon types per event. The failed-breakout first-eligible timestamp semantics remain corrected: all 736 eligible rows have a first-eligible timestamp; all 30 rejected rows have that field blank, while 20 observed confirmations remain preserved separately.

## 5. Remaining limitations and authorization boundary

- The five raw 1-minute files were hash-checked and timestamp-indexed by the workflow, but were not separately downloaded and re-hashed by the independent artifact reviewer.
- The 76 tests are synthetic contract tests; they do not replace a full candidate-generation dry-run or independent review of canonical candidate records.
- No canonical candidate rows, orders, fills, PnL, execution simulation or strategy conclusions have been generated.
- This workflow's PASS status is a source-audit result only, not a G0-05 gate approval.
- Phase 3 remains active. No phase transition is authorized.
