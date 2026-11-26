# G0-04 Independent Review Packet — V1

**Date:** 2026-11-26  
**Project:** OKX Price Action V1 — Phase 3 Sideways / Range  
**Review target:** G0-04 corrected canonical reconstruction  
**Status:** READY FOR INDEPENDENT REVIEW — NOT ACCEPTED  
**Required reviewer:** A person other than the author/implementer and other than the assistant workflow that prepared this packet.

## 1. Frozen review target

- Branch: `price-action-v1`
- Exact implementation commit: `8326c1edea66c11391ab614b9ce4afa9be5bc1fd`
- Workflow: [Run 45752717022](https://github.com/islamomanpk-boop/okxtester/actions/runs/45752717022)
- Job: `139684635786` — SUCCESS
- Artifact: [phase3-g0-04-causal-reconstruction-45752717022](https://github.com/islamomanpk-boop/okxtester/actions/runs/45752717022/artifacts/15085744573)
- Artifact ID: `15085744573`
- Artifact ZIP SHA-256: `11f6908b191d3b66bd4d17ef5a3e5d05f7f37050f9565ceeea05f4abc4571bfe`
- Source: `research/phase3_g0_04_causal_breakout_reconstruction_v1.py`
- Implementation checkpoint: `2026-11-26_g0_04_implementation_checkpoint_v1.md`

The reviewer must verify that the downloaded artifact and source correspond to these exact identifiers. A newer branch HEAD must not silently replace this frozen target.

## 2. Required independent checks

Record PASS / FAIL / NOT VERIFIED and evidence for every item.

1. **Provenance and immutability**
   - Confirm exact source commit and workflow checkout SHA.
   - Confirm artifact ID, ZIP SHA-256, metadata code revision, input hashes and output hashes.
   - Confirm five canonical 1-minute input files match the frozen hashes and schemas.

2. **Input integrity and common index**
   - Confirm expected columns, row counts, UTC millisecond timestamps, monotonicity, uniqueness, valid OHLCV and exact 60-second cadence.
   - Confirm the five-asset common index is exactly 569,125 timestamps.
   - Review the per-asset excluded-from-common-index counts recorded in the manifest.

3. **Bar and context construction**
   - Verify complete right-labelled/left-closed 15-minute and 4-hour aggregation.
   - Verify detector context is unshifted and historical breakout context uses the documented one-completed-4H-candle lag.
   - Verify backward-only as-of joins and absence of future context leakage.
   - Verify documented partial final 15-minute contexts are excluded from completed-context calibration rather than silently treated as complete.

4. **Historical baseline gate**
   - Independently recompute all 20 asset × definition × direction historical counts.
   - Confirm all 20 match the frozen baseline exactly before causal outputs are accepted.

5. **Threshold calibration**
   - Independently verify the 180-prior-completed-context warm-up and policy semantics for FIXED_180, EXPANDING_PRIOR and ROLLING_180.
   - Verify UNIQUE_4H_FEATURE_ROWS and JOINED_15M_ROWS populations.
   - Verify each calibration endpoint is strictly earlier than its classified snapshot.
   - Verify the 15-minute joined population uses exactly 16 rows per prior 4-hour context.
   - Verify P25 <= P40 for every corresponding threshold record.

6. **Historical classification matrix correction**
   - Verify the source ledger is a classification matrix with intentional repeats across STRICT_P25/BROAD_P40 and 5/10/15% zone levels.
   - Verify uniqueness is checked at the complete classification-row grain (identity + definition + zone), not prematurely at signal-identity grain.
   - Verify null/invalid timestamps are rejected before integer conversion.
   - Verify the collapse to 932 distinct historical signal identities is correct and reproducible.

7. **Raw events and reconciliation**
   - Verify 2,861 unique raw crossing identities and all expected strict/broad variants.
   - Verify strict eligibility is nested within broad eligibility.
   - Verify exactly 932 raw events are marked as historical selected identities.
   - Verify all 120 reconciliation dimensions are present and raw-source mismatch count is zero; distinguish eligibility differences from raw-source mismatches.

8. **Output integrity and scope**
   - Recompute all seven output-file hashes against run metadata.
   - Confirm output schemas, row counts, uniqueness constraints and manifest completeness.
   - Confirm outputs remain descriptive eligibility evidence only: no selected policy, orders, fills, execution simulation, strategy backtest or PnL conclusions.

## 3. Known boundaries / do not misclassify

- The workflow success is an execution result, not independent review or formal acceptance.
- The assistant-side second-pass audit is not an independent human/reviewer sign-off.
- Historical classification repetitions across two definitions and three zone levels are expected at the classification-matrix grain; genuine duplicate full classification rows must still fail closed.
- The final partial 15-minute context per asset is a documented coverage exception, not a complete prior calibration context.
- The 932 historical identity list is a reconciliation reference, not a candidate-generation source.
- G0-05 implementation/candidate generation remains blocked until this review is accepted and the decision is recorded.
- Gate 0 remains CONDITIONAL HOLD. No strategy backtesting or PnL work is authorized.

## 4. Reviewer disposition template

**Reviewer name / GitHub identity:**  
**Relevant independence / qualifications:**  
**Review date (UTC):**  
**Exact source commit reviewed:**  
**Exact workflow run / job:**  
**Exact artifact ID and ZIP SHA-256:**  

| Review area | PASS / FAIL / NOT VERIFIED | Evidence / notes |
|---|---|---|
| Provenance and immutability | | |
| Input integrity and common index | | |
| Bar and context construction | | |
| 20/20 historical baseline | | |
| Threshold calibration | | |
| Classification matrix and 932 identities | | |
| 2,861 raw events and 120-dimension reconciliation | | |
| Output hashes and descriptive-only scope | | |

**Unresolved findings / required repairs:**  

**Final disposition (choose one):**
- ACCEPT — all required checks passed; no unresolved material discrepancy.
- REJECT — one or more required checks failed.
- INCONCLUSIVE — evidence unavailable or insufficient.

**Reviewer explanation and evidence links:**  

A reviewer must not select ACCEPT if any required item is FAIL or NOT VERIFIED. If rejected or inconclusive, G0-04 stays open and G0-05 stays blocked. The reviewer must submit their own signed review/comment or commit; this packet must not be self-approved by its preparer.


## Review addendum — corrected validator revision and raw-data audit — 2026-11-26

The original frozen review target above remains preserved for audit history. A subsequent defensive validation repair produced a new canonical execution target:

- Corrected source commit: `86b49598d676b6ab00649bf31d4490ffbb1e608f`
- Workflow run: [45756061179](https://github.com/islamomanpk-boop/okxtester/actions/runs/45756061179)
- Job: `139694830125`, SUCCESS
- Artifact ID: `15087542445`
- Artifact ZIP SHA-256: `ef6204b546b49880675514ff76b4f6cb86e2821ba2b0d1d5412549927388f0a1`

The new run's seven output files are byte-identical to the prior corrected artifact, and all seven output hashes match the new metadata. The only code change between those runs is defensive rejection of null/non-numeric zone levels; the actual source classification ledger contains no such values.

A separate direct raw-input audit is recorded in `2026-11-26_g0_04_implementation_checkpoint_v1.md`. It independently verified all five input SHA-256 values, 569,125 identical common timestamps, timestamp cadence and OHLCV validity, reproduced all 20 historical baseline counts and 10 P25/P40 quantiles from raw market data, and matched all 2,358 detector feature-ledger rows per asset within (10^{-9}). It also checked the 4,776-row historical classification ledger: 932 identities, expected definitions and zone levels, no null zones and no duplicate full-grain rows.

The separate AI review by Kimi remains recorded as INCONCLUSIVE because that reviewer did not personally inspect the raw input files. The additional checks above are an assistant-side audit, not a human sign-off and not a retroactive change to Kimi's disposition. The project owner must decide whether the combined evidence satisfies the review standard and record ACCEPT / REJECT / CONDITIONAL HOLD. Until that decision is recorded, G0-04 is not formally accepted and G0-05 remains blocked.
