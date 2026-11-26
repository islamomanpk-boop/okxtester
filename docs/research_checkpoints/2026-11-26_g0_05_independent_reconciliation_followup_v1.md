# G0-05 Independent Reconciliation Follow-up — V1

**Date:** 2026-11-26  
**Parent review:** `2026-11-26_g0_05_independent_row_level_reconciliation_v1.md`  
**Scope:** Resolution of findings F-01 and F-02.  
**Gate decision:** No G0-05 gate pass is declared. Canonical candidate generation remains blocked.

## 1. Changes

Two narrow changes were committed to `price-action-v1`:

- Source audit implementation: commit `21f9532074fc7ba6e9be5c13d80a5c1988e04103`.
- Synthetic regression tests: commit `302d54eb6bcbb3bd3b1a134c445f81aec8d2eee9`.

### F-01 — Module B horizon reconciliation

The source audit now:
- requires the event and horizon fields needed for reconciliation;
- requires exactly one each of 15M, 1H, 4H and 12H for every event ID;
- rejects missing, extra, unknown or duplicate event/horizon pairs;
- compares 12H completion flags to `complete_12h` in the event ledger;
- compares 12H first return-inside confirmation timestamps to the event ledger; and
- rejects confirmations at/before the breakout signal or after the 12-hour boundary.

The synthetic suite now tests valid four-horizon coverage, missing and duplicate horizon rows, unknown event IDs, completion mismatch, confirmation mismatch, the exact 12-hour boundary and a confirmation after 12 hours.

### F-02 — First-eligible timestamp semantics

The failed-breakout ledger now populates `first_eligible_1m_open_ts_ms` only when the final disposition is `ELIGIBLE_FOR_FURTHER_VALIDATION`. The observed `confirmation_ts_ms` remains preserved for rejected events when a confirmation exists.

Synthetic tests cover eligible, rejected, expired and censored dispositions, plus an eligible row missing its confirmation timestamp.

## 2. Workflow verification

### Updated source audit

- Run: [45799176659](https://github.com/islamomanpk-boop/okxtester/actions/runs/45799176659) — SUCCESS.
- Job: `139837582503`.
- Checked-out commit: `21f9532074fc7ba6e9be5c13d80a5c1988e04103`.
- Artifact ID: `15106107761`.
- Artifact ZIP SHA-256: `f2c0319a451299fb5cab17cadb0f32c3f45576b6f83052fb631be9e06e181dca` (independently recomputed after download).
- Report status: `G0_05_SOURCE_PROVENANCE_AND_IDENTITY_AUDIT_PASS`.

The new report records:
- 1,592 Module B events reconciled to 6,368 horizon rows;
- exactly four horizon rows per event: 15M, 1H, 4H and 12H;
- 1,289 event-ledger rows with a 12H confirmation;
- 12H completion and confirmation fields match the event ledger.

The source-disposition counts remain unchanged:

| Family | Source rows | Eligible | Rejected | Expired | Censored |
|---|---:|---:|---:|---:|---:|
| Rejection | 1,154 | 1,083 | 31 | 40 | 0 |
| Breakout continuation | 2,861 | 1,038 | 1,823 | 0 | 0 |
| Failed-breakout reversal | 932 | 736 | 30 | 166 | 0 |
| **Total** | **4,947** | **2,857** | **1,884** | **206** | **0** |

For the 30 rejected failed-breakout rows, the new artifact has zero non-null `first_eligible_1m_open_ts_ms` values; 20 observed confirmations remain preserved in `confirmation_ts_ms`.

New output hashes:
- `rejection_source_dispositions.csv`: `797456556a4dd6c55dc5a14dc891860a7235c3d759cac371bb770cd32334eea4`.
- `breakout_source_dispositions.csv`: `71df0aa38be5e90767009dbb71616baf45e99ca3a2e8104a319f50342b2b7ff0`.
- `failed_breakout_source_dispositions.csv`: `119270c33e667e84cbdf44c58d5696affa1da5f8ee9d4703aae4f10794ce10c8`.

### Expanded synthetic tests

- Run: [45799202181](https://github.com/islamomanpk-boop/okxtester/actions/runs/45799202181) — SUCCESS.
- Job: `139837671330`.
- Commit: `302d54eb6bcbb3bd3b1a134c445f81aec8d2eee9`.
- Compile step and synthetic test step both completed successfully.

## 3. Updated disposition of findings

- **F-01:** Resolved in the audit implementation and covered by synthetic tests; current pinned Module B rows pass the new reconciliation.
- **F-02:** Resolved in the source-disposition output and covered by synthetic tests; observed confirmations remain preserved separately from eligible-minute timestamps.

The original review remains unchanged as an immutable record. This follow-up does not remove the independent review's stated limitation that the five raw 1-minute market files were not separately downloaded and re-hashed during that review. The successful source-audit workflow itself verifies their frozen hashes, row counts, timestamp grid and exact first-minute membership.

## 4. Remaining work and boundaries

- Complete any remaining G0-05-specific test requirements in the frozen candidate/disposition schema, including source-key failure cases and full disposition reason coverage.
- Resolve the raw 1-minute source-membership independent-review limitation if a second independent reproduction is required by the gate.
- Do not generate canonical candidate records until the remaining G0-05 review requirements are satisfied and the required authorization is given.
- No orders, fills, positions, PnL, execution simulation, strategy backtests or phase transition are authorized by this follow-up.
