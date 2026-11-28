# Phase 3 G0-05 — Independent Source Verification Closeout

**Date:** 2026-11-28  
**Repository:** `islamomanpk-boop/okxtester`  
**Branch:** `price-action-v1`  
**Status:** Step 22 complete; G0-05 remains open and canonical candidate generation remains unauthorized.  
**Mode:** Read-only verification of frozen source populations and source-only disposition outputs. No candidate rows or real candidate IDs generated.

## 1. Evidence and reproducibility

- Independent verifier: `research/phase3_g0_05_independent_source_verification_v1.py`.
- Final code/branch commit: `8744a1981237f3aabfe73bacf3cc8bdfa5bb295f`.
- Workflow: [46148537294](https://github.com/islamomanpk-boop/okxtester/actions/runs/46148537294) — SUCCESS.
- Evidence artifact: `phase3-g0-05-source-audit-46148537294`, artifact ID `15264717673`.
- Artifact ZIP SHA-256: `865c8a1a5cf0fc2e0ce9a85df14200d64054738c063275f7ce675d471af48974`.
- The workflow independently verified the pinned G0-04 artifact ZIP before extraction, ran the primary read-only source audit, compiled the independent verifier, ran it, and uploaded the six-file evidence package.
- The independent verifier uses only the Python standard library and imports neither the canonical candidate contract nor the primary source-audit implementation.

## 2. Independent results

### Rejection family

- 1,154 physical rejection identities reconstructed from 1,992 immutable cohort memberships.
- Exact source identity and broad/strict source-row membership reconciled.
- Independently recomputed disposition totals:
  - 1,083 eligible: 942 causal strict + 141 causal broad-only.
  - 31 rejected: 29 warm-up + 2 causal regime not eligible.
  - 40 expired before confirmation.
- Total: 1,154 physical events.

The independent check validates rejection physical identity, membership and causal disposition. It does not independently rebuild the accepted Module A 24-hour interval-graph cluster assignment; the primary source audit continues to reconcile those accepted cluster IDs.

### Breakout continuation

- All 2,861 G0-04 raw crossing identities reconcile exactly once to the source-only disposition ledger.
- P25/P40 flags and causal disposition labels independently recomputed from the frozen threshold artifact and raw event context.
- Independently rebuilt 12-hour half-open overlap components from raw one-minute timestamp grids: 1,037 clusters.
- Cluster counts by asset: BTC 220, ETH 201, SOL 212, DOGE 193, AVAX 211.
- Disposition totals:
  - 1,038 eligible: 794 causal strict + 244 causal broad-only.
  - 1,823 rejected: 1,561 causal regime not eligible + 262 warm-up.
- Total: 2,861 raw crossing identities.

### Failed-breakout reversal

- 1,592 Module B cohort rows collapse to 932 physical source breakout identities.
- Every failed-breakout identity maps to exactly one source breakout identity; source cohort, event identity and causal-source-cohort inheritance are checked.
- All 932 lifecycle records checked against the strict half-open 12-hour window.
- One observed return-inside event occurs exactly at the 12-hour right endpoint. It is retained as an observation but excluded from canonical confirmation, as required.
- Disposition totals:
  - 735 eligible.
  - 30 rejected because the source breakout is not causally eligible.
  - 167 expired without a qualifying return-inside confirmation.
- Total: 932 physical failed-breakout source events.

## 3. Reconciled source-ledger totals

| Family | Source-only rows / physical identities | Eligible | Rejected | Expired |
|---|---:|---:|---:|---:|
| Rejection | 1,154 physical events (1,992 cohort memberships) | 1,083 | 31 | 40 |
| Breakout continuation | 2,861 raw crossing identities | 1,038 | 1,823 | 0 |
| Failed-breakout reversal | 932 physical events (1,592 cohort memberships) | 735 | 30 | 167 |
| **Total source-only disposition rows** | **4,947** | **2,856** | **1,884** | **207** |

The 4,947 rows are not 4,947 independent physical events: failed-breakout rows link back to breakout identities, and rejection/Module B cohort memberships include nested historical definitions. Overlap clusters describe dependent event windows, not independent observations.

## 4. Scope and limitations

This verification independently covers source identities, source membership, causal cohort/disposition recomputation, breakout overlap components, failed-breakout source linkage, causal-cohort inheritance, and half-open lifecycle semantics.

It does not:
- independently rebuild Module A's accepted rejection interval-graph clustering;
- independently reconstruct every Module B 15-minute OHLC confirmation candle from the 15 component one-minute bars (that reconstruction remains in the primary source audit);
- apply the 60-field canonical candidate validator to real rows;
- generate real candidate IDs or `source_breakout_candidate_id` values;
- create a canonical candidate ledger, orders, fills, execution simulations, PnL, or strategy conclusions.

The separate synthetic contract suite's latest known result remains 190/190 passed (run 46140552809). The current source-audit workflow does not replace that synthetic suite.

## 5. Gate disposition

**Step 22: COMPLETE.** Independent source identity and lifecycle verification is green.

**G0-05: OPEN — not closed. Canonical candidate generation: NOT AUTHORIZED.** The source-only disposition ledgers are not canonical candidate records. The final candidate IDs and linked failed-breakout source candidate IDs remain intentionally unmaterialized. The full 60-field validator has synthetic coverage, but no real canonical ledger has been produced or reviewed.

**Gate 0: CONDITIONAL HOLD — not passed.** This G0-05 source verification does not close the separate funding-engine/settlement-mark acceptance, fee/instrument assumptions, standalone sizing, contract rounding, stop-gap risk, or execution-engine readiness blockers. Gate 2 and all later gates remain closed; no Phase 3 strategy PnL backtest is authorized.

## 6. Smallest safe next step

Complete a read-only pre-generation gate review that reconciles the canonical field-mapping matrix with the later frozen field-value decisions, verifies the family-specific nullability and identity rules against the current 60-field validator, and records a final G0-05 authorization decision. Any real canonical candidate build must remain a separately approved action after that review; it must not be inferred from this successful source-only audit.


## 7. Pre-generation contract review — 2026-11-28

A static comparison of the canonical contract, serializer and field-mapping matrix found:
- `CANONICAL_REQUIRED_FIELDS` contains exactly 60 fields.
- The canonical serializer emits exactly 60 keys: no missing required keys and no extra keys.
- The field-mapping matrix now names all 60 required fields explicitly, including overlap-cluster size/bounds and the three NOT_APPLICABLE invalidation-reference fields.

The review also found a validator gap: the row validator accepted any globally allowed `source_reconciliation_status` / `source_join_cardinality` combination regardless of family. It now enforces the exact family mapping:
- Rejection: `EXACT_PHYSICAL_EVENT_COLLAPSE` + `ONE_PHYSICAL_EVENT_TO_ONE_OR_TWO_COHORT_ROWS`; BROAD_P40 membership required; one or two source cohort IDs.
- Breakout continuation: `EXACT_SOURCE_MATCH` + `ONE_RAW_CROSSING_TO_ONE_DISPOSITION`; exactly one raw source row ID.
- Failed-breakout reversal: `EXACT_LINKED_SOURCE_BREAKOUT` + `ONE_FAILED_BREAKOUT_TO_ONE_SOURCE_BREAKOUT`; one or two source cohort IDs, with exact source-breakout link and inherited source metadata checked by the ledger validator.

Implementation and synthetic evidence:
- Contract change: commit `e1affcb1ed585546e181fb4ab7332f0c844f4d45`.
- Three new fail-closed tests: commit `a2479ed6496f7e698c0f43d940573f7f77cc152f`.
- Normal push-triggered synthetic workflow [46149074209](https://github.com/islamomanpk-boop/okxtester/actions/runs/46149074209) — SUCCESS; **193/193 tests passed**.

### Pre-generation review disposition

**Technical pre-generation review: PASS for the inspected contract/serializer/mapping checks.** The 60-field serializer mapping is exact, the field matrix covers all 60 fields, and family-specific source reconciliation semantics now fail closed under synthetic tests.

**Canonical candidate build: HOLD — not authorized.** This review did not generate real candidate IDs, `source_breakout_candidate_id` values or canonical candidate rows. The independent source verifier has the explicit scope limitations in Section 4; in particular, it does not independently rebuild Module A's 24-hour cluster graph or independently repeat the full 15-component OHLC aggregation. Those remain covered by the primary source audit and its existing checks, not by the new independent verifier.

**G0-05 remains OPEN; Gate 0 remains CONDITIONAL HOLD.** The next action requiring owner authorization is a separately scoped real canonical candidate/disposition build, followed by a real-row validator run and artifact review. This must not be interpreted as authorization for execution simulation, strategy PnL backtesting, Gate 2+, or live trading.


## 8. Owner-authorized real canonical candidate ledger build — 2026-11-28

The project owner explicitly authorized the real G0-05 canonical candidate/disposition build. The normal push-triggered workflow [46149804561](https://github.com/islamomanpk-boop/okxtester/actions/runs/46149804561) completed successfully on commit `26ac706767d3f9b490cfa2b8250c13417f46b356`.

- Artifact: `phase3-g0-05-canonical-candidate-ledger-46149804561`, ID `15265550848`, ZIP SHA-256 `e66ea4b16811d158a9b86dfb90113be13cc5fccfc89f1c42b5330fba294456da`, 2,587,810 bytes.
- Generated and validated 4,947 real canonical records with exactly 60 required fields each.
- Family counts: support rejection 558; resistance rejection 596; breakout continuation 2,861; failed-breakout reversal 932.
- Dispositions: rejection 1,083 eligible / 31 rejected / 40 expired; breakout 1,038 eligible / 1,823 rejected; failed breakout 735 eligible / 30 rejected / 167 expired; aggregate 2,856 eligible / 1,884 rejected / 207 expired / 0 censored.
- Deterministic candidate IDs and family/source identity uniqueness passed.
- Full canonical record and ledger validation passed.
- All 932 failed-breakout source-candidate links resolved and inherited source metadata passed.
- Canonical JSONL SHA-256: `202c44f456af021b9ec8cc642e82c349f4858baadb04bcdb2342973cb752db14`.
- Canonical CSV SHA-256: `eca9f326bc44a74ba9631bc6b5d4a6c7b5691fea6b59c7031976f7fd7f5ff1a5`.

The first real-data attempt correctly stopped because the source mapper used the sentinel `NONE` for an absent historical cohort membership, while the canonical contract expects an empty list. The mapper was corrected to emit an empty membership list, and the full corrected workflow reran the frozen source audit, independent source verification and canonical build before passing. The failed attempt did not produce a canonical ledger.

Detailed build evidence is in `docs/research_checkpoints/2026-11-28_g0_05_canonical_candidate_ledger_build_v1.md`.

**Status update:** the previously missing real canonical candidate/disposition generation and real-row validation step is now complete. The evidence artifact still requires read-only post-build review before formally closing G0-05. This result does not pass Gate 0: funding/settlement-mark acceptance, fee/instrument assumptions, sizing, contract rounding, stop-gap risk and execution-engine readiness remain separate blockers. No orders, fills, execution simulation, PnL, strategy comparison or live trading was performed or authorized.


## 9. Superseding final build with independent post-build evidence review — 2026-11-28

The canonical build workflow now includes a second, separately implemented read-only post-build reviewer. Final workflow [46150045661](https://github.com/islamomanpk-boop/okxtester/actions/runs/46150045661) completed **SUCCESS** on commit `19a6325780693696890f9f3493a713702e8a8f7f`. This is the authoritative final evidence package and supersedes the earlier build-only artifact in Section 8.

- Artifact: `phase3-g0-05-canonical-candidate-ledger-46150045661`.
- Artifact ID: `15265023491`.
- Artifact ZIP SHA-256: `0b9464cbeda0a513cea915aae78a1c43aab2b5563448a0e19b247c02b4081935`.
- Artifact size: 2,588,629 bytes; not expired at time of verification.
- Canonical JSONL SHA-256: `387d376bc269587de6fb48686641cd27e885a2d3bd6c6a8ae96a9a9dd61333d8`.
- Canonical CSV SHA-256: `325c714e5923612a711d18a855d1540e1f59b27d26d65636ebabd7578c81bb43`.
- Complete source manifest ID: `8458ca73f07db7d3ff4517123dd0d6b33acb39e99174ecd39056b585a9988c82`.

The independent post-build reviewer returned `G0_05_POST_BUILD_EVIDENCE_REVIEW_PASS` and verified:
- 4,947 JSONL records and exactly 60 canonical fields on every row.
- Exact family totals: 558 support rejection, 596 resistance rejection, 2,861 breakout continuation, 932 failed-breakout reversal.
- Aggregate dispositions: 2,856 eligible, 1,884 rejected, 207 expired, 0 censored.
- Candidate IDs recomputed independently and deterministic order/uniqueness confirmed.
- Canonical CSV and JSONL semantically equivalent row by row.
- Canonical file hashes and complete source-manifest identity reverified.
- Exact-once source-to-canonical identity reconciliation across all 4,947 source rows.
- All 932 failed-breakout links resolve to the correct breakout candidate and preserve inherited provenance, cluster and expiry fields.

This final run reran the frozen G0-04 artifact digest check, primary source audit, independent source identity/lifecycle verifier, canonical generation/full 60-field ledger validator and the separate post-build reviewer. All steps succeeded.

**Technical disposition:** G0-04 remains ACCEPTED. G0-05 implementation, real candidate generation, full validation and independent post-build evidence review are now technically complete and ready for formal G0-05 closeout. The project owner has authorized generation, but a distinct formal gate-acceptance decision has not yet been recorded; until that decision is made, keep G0-05 marked READY FOR FORMAL CLOSEOUT rather than silently changing its gate state.

**Gate 0 remains CONDITIONAL HOLD — not passed.** G0-03 real-input funding integration/exact settlement-mark policy, G0-07 standalone sizing/contract rounding/gap risk, G0-08 fee/instrument assumptions and G0-09 settlement-mark fidelity/execution-engine acceptance remain separate blockers. No orders, fills, execution simulation, PnL, strategy comparison, Gate 2+ or live trading was performed or authorized.
