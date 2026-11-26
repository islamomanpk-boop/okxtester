# G0-04 Independent AI Review Prompt — V1

You are acting as an independent technical reviewer. You have not participated in designing, implementing, debugging, or previously reviewing this project. Do not assume the implementation is correct because GitHub Actions passed or because the project notes say it passed.

## Review target — freeze these exact versions

- Repository: https://github.com/islamomanpk-boop/okxtester
- Branch: `price-action-v1`
- Exact implementation commit: `8326c1edea66c11391ab614b9ce4afa9be5bc1fd`
- Source file: https://github.com/islamomanpk-boop/okxtester/blob/8326c1edea66c11391ab614b9ce4afa9be5bc1fd/research/phase3_g0_04_causal_breakout_reconstruction_v1.py
- Workflow run: https://github.com/islamomanpk-boop/okxtester/actions/runs/45752717022
- Artifact: https://github.com/islamomanpk-boop/okxtester/actions/runs/45752717022/artifacts/15085744573
- Artifact ZIP SHA-256: `11f6908b191d3b66bd4d17ef5a3e5d05f7f37050f9565ceeea05f4abc4571bfe`
- Review checklist and disposition form: https://github.com/islamomanpk-boop/okxtester/blob/price-action-v1/docs/research_checkpoints/2026-11-26_g0_04_independent_review_packet_v1.md
- Implementation checkpoint: https://github.com/islamomanpk-boop/okxtester/blob/price-action-v1/docs/research_checkpoints/2026-11-26_g0_04_implementation_checkpoint_v1.md

If you cannot access or download any required item, say so explicitly. Do not infer its contents from summaries. If possible, request that the user attach the artifact ZIP and source file. Verify the exact commit and artifact hash before reviewing.

## Your task

Perform a skeptical, independent, read-only audit of G0-04 causal breakout reconstruction. Do not modify files, run workflows, create candidates, or authorize later project phases. Do not merely restate the checkpoint. Inspect the actual source and artifact evidence available to you, and independently recompute important checks where technically possible.

Focus on finding defects, not validating the previous assistant. In particular, investigate:

1. **Provenance:** exact source revision, workflow checkout SHA, artifact identity/hash, source input hashes, output hashes and reproducibility.
2. **Input integrity:** schemas, row counts, UTC millisecond timestamps, monotonicity, uniqueness, OHLCV validity, one-minute cadence and the 569,125-row exact five-asset common index.
3. **Bar construction:** right-labelled / left-closed completed 15-minute and 4-hour bars; partial bars; timestamp semantics.
4. **Causality:** detector context versus the separately lagged historical breakout context; backward-only as-of joins; any future leakage; availability time versus signal time.
5. **Historical baseline:** independently recompute all 20 asset × definition × direction baseline counts and verify exact matches.
6. **Threshold calibration:** FIXED_180, EXPANDING_PRIOR and ROLLING_180 semantics; prior completed contexts only; warm-up; UNIQUE_4H_FEATURE_ROWS versus JOINED_15M_ROWS; 16 joined 15-minute rows per prior 4-hour context; strictly earlier calibration endpoint; P25/P40 ordering.
7. **Historical classification ledger:** verify the complete uniqueness grain includes identity + definition + zone level; ensure legitimate repeated signal identities across STRICT_P25/BROAD_P40 and 5/10/15% zones are not misdiagnosed; invalid/null timestamps must be rejected before integer conversion; verify the resulting 932 distinct identities.
8. **Raw events and reconciliation:** verify 2,861 unique raw crossing identities, all expected strict/broad variants, strict/broad nesting, 932 selected historical identities, all 120 reconciliation dimensions and zero raw-source mismatches. Distinguish eligibility differences from raw-source mismatches.
9. **Output integrity:** independently recompute all seven output hashes and check schemas, row counts, key uniqueness and manifest correctness.
10. **Research interpretation:** determine whether the output supports only descriptive causal-eligibility reconstruction or makes any unsupported claim about selected policies, execution, profitability, or strategy performance.

## Required response format

Start with a short statement of what materials you actually accessed and what you could not access.

Then provide a table with columns:
- Review area
- PASS / FAIL / NOT VERIFIED
- Evidence actually inspected or recomputed
- Findings / severity

For every claimed PASS, identify the evidence and method. Do not mark something PASS solely because a workflow succeeded or a checkpoint says so.

List all defects, possible defects, missing evidence, and questions. Classify each as:
- BLOCKER — must be fixed before G0-04 acceptance
- MAJOR — materially weakens confidence; resolve before acceptance
- MINOR — does not block acceptance, but document it
- NONE — no issue found in the inspected scope

Conclude with exactly one disposition:
- **ACCEPT** — all required checks are independently verified and no material issue remains.
- **REJECT** — one or more required checks fail.
- **INCONCLUSIVE** — essential evidence could not be accessed or independently verified.

Do not be agreeable. Do not invent evidence, outputs, test results, or file contents. Clearly disclose your limitations, model identity, and whether you independently inspected the raw artifact or only reviewed text summaries. A clean report is not proof of correctness if you could not inspect the data.

Even if you conclude ACCEPT, state that this is an independent AI technical review, not a human review or formal authorization for G0-05. The project owner must record the disposition and decide whether AI review satisfies their governance standard. G0-05 candidate generation, execution simulation, backtesting and PnL remain unauthorized unless separately approved through the project's gates.
