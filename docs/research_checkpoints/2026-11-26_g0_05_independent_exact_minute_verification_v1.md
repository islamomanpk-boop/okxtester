# G0-05 Independent Exact-Minute Membership Verification — V1

**Date:** 2026-11-26  
**Branch:** `price-action-v1`  
**Scope:** Independent verification of frozen five-asset 1-minute source files and first-eligible timestamp membership in the source-only disposition ledgers.  
**Disposition:** PASS for this narrow verification only. This is not a G0-05 gate approval and does not authorize canonical candidate generation.

## 1. Independent method

A separate verifier was added at `research/phase3_g0_05_independent_minute_verification_v1.py`. It uses only Python standard-library CSV, hashing and JSON operations and does not import the G0-05 source-audit or candidate-contract modules.

It independently:
- re-hashes the five checked-out raw 1-minute CSV files against the frozen G0-04 SHA-256 values;
- parses every timestamp, requiring minute alignment, strict monotonicity, no duplicates, and an uninterrupted 60-second grid;
- verifies the expected row count for each asset;
- reads the three source-disposition ledgers from the corrected source-audit artifact;
- checks every eligible row's first-eligible timestamp is an integer, minute-aligned, exactly equal to its family signal/confirmation timestamp, and present in the relevant asset's raw timestamp index;
- requires every non-eligible row's first-eligible timestamp field to be blank; and
- reconciles family and aggregate eligible counts.

This is a separate implementation and a separate workflow from the source audit. It verifies raw timestamp membership, not the complete candidate schema or every source-identity claim.

## 2. Corrected source-audit evidence used

- Source-audit run: [45800976161](https://github.com/islamomanpk-boop/okxtester/actions/runs/45800976161) — SUCCESS.
- Job: `139843792711`.
- Checked-out commit: `7406bd52d93d10128bc8ea18416366917223b5dc`.
- Artifact ID: `15106648767`.
- Artifact name: `phase3-g0-05-source-audit-45800976161`.
- Artifact ZIP SHA-256: `f8e7f802606ac4b6a977f79e3103b21fa44733cedae833d724a3c6260c2ea517`.

The audit implementation was corrected in commit `7406bd52d93d10128bc8ea18416366917223b5dc` so rejection and breakout rows, like failed-breakout rows, expose `first_eligible_1m_open_ts_ms` only when their final disposition is `ELIGIBLE_FOR_FURTHER_VALIDATION`. Observed confirmation/signal timestamps remain in their separate fields.

## 3. Independent verification run

- Workflow: [45801631819](https://github.com/islamomanpk-boop/okxtester/actions/runs/45801631819) — SUCCESS.
- Job: `139846060250`.
- Workflow commit: `ae9a87f74e252efcf1862cf91be7efa5d1fa7703`.
- Artifact ID: `15107586311`.
- Artifact name: `phase3-g0-05-independent-minute-verification-45801631819`.
- Artifact ZIP SHA-256: `d40b1a565e47d65222836a20c625765b75d47108cb5b33c82c3b115c9b5f22fe`.
- Extracted `independent_minute_verification.json` SHA-256: `b2ab8bf00572c54a60cb3548c3131dcd986ed020639a6b762ce9328187b1e679`.
- Report status: `INDEPENDENT_EXACT_MINUTE_MEMBERSHIP_PASS`.

## 4. Raw 1-minute source results

| Asset | Rows | SHA-256 verified | Strictly increasing | Continuous 1-minute grid |
|---|---:|---|---|---|
| BTC | 569,125 | PASS | PASS | PASS |
| ETH | 569,125 | PASS | PASS | PASS |
| SOL | 569,126 | PASS | PASS | PASS |
| DOGE | 569,126 | PASS | PASS | PASS |
| AVAX | 569,127 | PASS | PASS | PASS |

All five independently recomputed SHA-256 values exactly match the frozen source values. No duplicate, off-minute, non-increasing or missing/gapped timestamp was found.

## 5. Eligible timestamp membership and disposition accounting

| Family | Source rows | Eligible checked | Rejected | Expired | Censored |
|---|---:|---:|---:|---:|---:|
| Rejection | 1,154 | 1,083 | 31 | 40 | 0 |
| Breakout continuation | 2,861 | 1,038 | 1,823 | 0 | 0 |
| Failed-breakout reversal | 932 | 736 | 30 | 166 | 0 |
| **Total** | **4,947** | **2,857** | **1,884** | **206** | **0** |

All 2,857 eligible first-minute timestamps were found exactly in their corresponding raw asset timestamp indexes. For rejection, the timestamp equals the completed 15-minute rejection confirmation; for breakout continuation, it equals the 15-minute signal availability; for failed-breakout reversal, it equals the completed return-inside confirmation.

All 2,090 non-eligible rows have blank first-eligible timestamp fields. The report separately confirms this invariant for all three family ledgers.

## 6. Initial failed attempt and sequencing correction

The first independent run, [45801067586](https://github.com/islamomanpk-boop/okxtester/actions/runs/45801067586), failed closed because the workflow downloaded the prior source-audit artifact, which predated the eligible-only timestamp correction. The verifier correctly detected a non-eligible rejection row with a populated first-eligible timestamp.

The workflow was then amended to select only the successful source-audit run whose checked-out commit is the exact correction commit `7406bd52d93d10128bc8ea18416366917223b5dc`. The successful run [45801631819](https://github.com/islamomanpk-boop/okxtester/actions/runs/45801631819) downloaded that corrected artifact and passed all checks. The initial failure is retained here rather than hidden.

## 7. Remaining G0-05 boundary

This closes the previously identified independent raw 1-minute hash/grid/membership reproduction limitation. It does **not** independently review the complete G0-05 candidate contract, every family source identity, overlap-cluster reporting, or every remaining gate condition. The independent row-level review remains INCONCLUSIVE unless and until all of its findings and the complete gate checklist are resolved.

No canonical candidate rows were generated. No orders, fills, positions, execution simulation, PnL, strategy backtests, profitability claims, or phase transition are authorized by this verification.
