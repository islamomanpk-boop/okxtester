# G0-05 Disposition Reason-Code Contract Follow-up — V1

**Date:** 2026-11-26  
**Scope:** Enforce the frozen status/reason/censoring contract in every source-only disposition row.  
**Disposition:** Source-audit implementation and synthetic regression suite pass. This is not G0-05 acceptance and does not authorize candidate generation.

## 1. Finding

The earlier source-only ledgers contained reason labels that did not conform to the frozen contract:
- eligible broad-only rows used `CAUSAL_BROAD_ONLY` as a reason, although eligible rows require `reason_code=NONE`;
- failed-breakout source-ineligible rows used `SOURCE_BREAKOUT_NOT_CAUSALLY_ELIGIBLE`, while the frozen rejection enum defines `NO_VALID_SOURCE_BREAKOUT`;
- the source audit checked disposition statuses and row totals but did not invoke the shared reason-code validator on every output row.

This was a contract/reporting mismatch, not a change to the previously reconciled source population.

## 2. Corrections

Source audit commit: `253f187b0da75f76c585fed6f4ec416cd28c5ddc`.

The source audit now:
- imports and invokes `validate_disposition_reason` for every output row;
- requires `NONE` for every eligible row;
- uses the frozen reason enums for rejected, expired and censored rows;
- emits a separate `censoring_reason` field, required to match the censor reason for CENSORED rows;
- preserves causal cohort labels separately from exclusion reasons;
- labels failed-breakout events whose source breakout is not causally eligible with `NO_VALID_SOURCE_BREAKOUT`, while preserving source-cohort metadata separately.

The rejection ledger now has a distinct `causal_cohort` field, so strict and broad-only eligibility are not encoded as exclusion reasons.

## 3. Source-audit evidence

- Workflow [45802145534](https://github.com/islamomanpk-boop/okxtester/actions/runs/45802145534) — SUCCESS.
- Job: `139847841449`.
- Checked-out commit: `253f187b0da75f76c585fed6f4ec416cd28c5ddc`.
- Artifact ID: `15106714247`.
- Artifact ZIP SHA-256: `ef08831a8ad5bbb6326d4847b842b2e229cee4cdd174e4292cddbc45c96aa5bb` (downloaded and independently recomputed).

Output hashes:
- `rejection_source_dispositions.csv`: `3b920badb4501235df9087232d0dacbb41214f874d32ad72dcba143a7096e218`.
- `breakout_source_dispositions.csv`: `c330f4803cd196b1950f02dd22689f8e543383d225966fcc1c4606286809080f`.
- `failed_breakout_source_dispositions.csv`: `78291a9256293c2512ae69e81b54fa687bf4f0090e0b9668ea5f840f9c79a8c7`.

The output rows satisfy the frozen reason contract:
- Rejection: 1,083 eligible/NONE; 29 warm-up rejected; 2 causal-regime rejected; 40 snapshot-expired.
- Breakout continuation: 1,038 eligible/NONE; 262 warm-up rejected; 1,561 causal-regime rejected.
- Failed-breakout reversal: 736 eligible/NONE; 30 rejected/NO_VALID_SOURCE_BREAKOUT; 166 expired/EXPIRED_NO_RETURN_INSIDE_WITHIN_12H.
- No censored rows were present in this source population. The censoring field is nevertheless emitted and enforced for future censored rows.

Total dispositions remain 4,947: 2,857 eligible, 1,884 rejected, 206 expired and 0 censored.

## 4. Synthetic regression tests

Four tests were added for:
- valid rows across all four statuses and frozen reason codes;
- rejection of `CAUSAL_BROAD_ONLY` as an eligible-row reason;
- rejection of the unfrozen failed-breakout reason string;
- rejection of a censoring-reason mismatch.

The first CI attempt [45802163583](https://github.com/islamomanpk-boop/okxtester/actions/runs/45802163583) found an outdated test fixture that lacked the now-required reason fields. The fixture was corrected in commit `260bf19c927c9de7bf55b8ec25cc62dca9a58b1a`.

The corrected test workflow [45802241180](https://github.com/islamomanpk-boop/okxtester/actions/runs/45802241180) — SUCCESS; job `139848178216`; **80/80 tests passed**.

## 5. Independent minute-verification pin update

The independent exact-minute workflow has been updated to consume the reason-contract-validated source audit at commit `253f187b0da75f76c585fed6f4ec416cd28c5ddc`, rather than the earlier pre-reason-contract audit. The rerun is tracked separately; this document does not claim that rerun until its workflow and artifact are confirmed.

## 6. Authorization boundary

This closes the reason-code mismatch for the source-only disposition audit. It does not complete the canonical candidate schema, overlap-cluster reporting, all family/asset/side summary requirements, or the full G0-05 acceptance review. No canonical candidate rows, orders, fills, execution simulation, PnL, strategy backtests, or phase transition are authorized by this follow-up.


## 7. Independent minute verification rerun against the reason-validated artifact

- Workflow [45802348522](https://github.com/islamomanpk-boop/okxtester/actions/runs/45802348522) — SUCCESS.
- Job: `139848550215`.
- Checked-out workflow commit: `64bdadc618b4654a7a94164183d0c0a05512158e`.
- The workflow selected the successful source-audit run at exact commit `253f187b0da75f76c585fed6f4ec416cd28c5ddc`.
- Artifact ID: `15107686762`.
- Artifact ZIP SHA-256: `cf5d687ec36d0a6d906cb81f26becbca01e68553297ff422ab59ca69f9004c62`, independently recomputed after download.
- Extracted JSON SHA-256: `b2ab8bf00572c54a60cb3548c3131dcd986ed020639a6b762ce9328187b1e679`.
- Report status: `INDEPENDENT_EXACT_MINUTE_MEMBERSHIP_PASS`.
- All five raw 1-minute source hashes/row counts and all 2,857 eligible timestamp memberships passed again. All 2,090 non-eligible rows had blank first-eligible timestamps.

This rerun confirms the exact-minute result against the newer artifact that also enforces the corrected reason-code contract.
