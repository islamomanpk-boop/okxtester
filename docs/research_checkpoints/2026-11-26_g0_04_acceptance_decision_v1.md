# G0-04 Acceptance Decision — V1

**Date:** 2026-11-26  
**Project:** OKX Price Action V1 — Phase 3 Sideways / Range  
**Decision authority:** Project owner delegated routine technical disposition authority to the assistant in the conversation dated 2026-11-26.  
**Disposition:** **ACCEPTED — TECHNICAL G0-04 CLOSEOUT**  
**Scope:** G0-04 causal breakout reconstruction and past-only threshold comparison only.

## 1. Decision

G0-04 is accepted on the combined evidence available in the repository and the separately documented raw-data/artifact audit. This is a delegated project-owner decision. It is not a human reviewer sign-off, and it does not change the separate AI reviewer Kimi's original **INCONCLUSIVE** disposition.

The evidence is sufficient to close the G0-04 technical reconstruction task because the specific evidence gap behind Kimi's inconclusive result—direct access to raw 1-minute inputs and independent reproduction of the historical baseline—was subsequently addressed in the project-side audit below.

## 2. Frozen canonical evidence

- Branch: `price-action-v1`
- Corrected validator source commit: `86b49598d676b6ab00649bf31d4490ffbb1e608f`
- Workflow run: [45756061179](https://github.com/islamomanpk-boop/okxtester/actions/runs/45756061179)
- Job: `139694830125` — SUCCESS; all workflow steps passed.
- Artifact: [phase3-g0-04-causal-reconstruction-45756061179](https://github.com/islamomanpk-boop/okxtester/actions/runs/45756061179/artifacts/15087542445)
- Artifact ID: `15087542445`
- Artifact ZIP SHA-256: `ef6204b546b49880675514bf76b4f6cb86e2821ba2b0d1d5412549927388f0a1`
- Latest documentation/evidence checkpoint at decision time: `cf4c45558ef893ffe817c80edd57c85ebb760f3b`

## 3. Acceptance evidence

The corrected workflow compiled the reconstruction source, passed synthetic contract tests, completed the fail-closed descriptive reconstruction, and uploaded the artifact successfully.

The recorded second-pass and raw-input audits establish:
- All five canonical 1-minute CSV SHA-256 hashes match the run metadata.
- Source row counts: BTC 569,125; ETH 569,125; SOL 569,126; DOGE 569,126; AVAX 569,127.
- The common index is exactly 569,125 identical timestamps; timestamp cadence, ordering, uniqueness, and OHLCV checks reported no defects.
- A separate implementation rebuilt completed 15-minute/4-hour bars, historical lagged contexts, joined 15-minute observations, P25/P40 quantiles and breakout crossing counts directly from raw data.
- All 20 historical baseline counts and all 10 historical quantiles reproduced.
- All five detector feature ledgers matched 2,358 rebuilt contexts per asset within 1e-9 (maximum absolute difference recorded as 3.33e-16).
- Historical classification ledger: 4,776 rows, 932 distinct identities, expected STRICT_P25/BROAD_P40 definitions and 5/10/15 zone levels, zero null/invalid zones and zero duplicate full-grain rows.
- Corrected artifact: 65,310 threshold rows and 2,861 unique raw crossing rows. The seven output-file hashes match the manifest; the 120 reconciliation dimensions show zero raw-source mismatches.
- Threshold calibration endpoints precede their classified snapshots; fixed/rolling windows use 180 prior completed contexts; joined-15M prior counts equal 16 rows per prior context; P25 does not exceed P40.
- Edge-population checks confirmed 262 warm-up events, two SOL events with undefined efficiency/overlap, and 12 legacy ratio-efficiency values above 1. These are retained as explicit descriptive limitations/exclusions, not silently altered or reinterpreted.

Full run metadata, source hashes, row-level outputs, and method details remain in `2026-11-26_g0_04_implementation_checkpoint_v1.md`.

## 4. Review limitations preserved

- Kimi's separate AI review remains **INCONCLUSIVE** because Kimi did not inspect the raw 1-minute CSVs or independently regenerate the baseline. Its verdict is not overwritten.
- The direct raw-input, baseline, detector-ledger and artifact recomputations were performed as a separate project-side assistant audit. They are not a human sign-off and must not be represented as such.
- No human reviewer was available. The project owner explicitly delegated this disposition decision to the assistant.
- The 262 warm-up events, two SOL undefined-feature events, and 12 legacy ratio-efficiency values above 1 remain documented. The historical ratio formula is preserved; values above 1 are not automatically treated as detector-efficiency defects.
- The accepted outputs remain descriptive eligibility evidence. No threshold policy is selected by this acceptance, and no orders, fills, execution simulation, strategy backtest, or PnL conclusions are authorized.

## 5. What this decision unlocks

G0-04 is closed. The next numbered task, **G0-05**, may proceed to contract finalization, source inventory, explicit decision-making on the threshold policy/population and snapshot semantics, and synthetic-test implementation.

This decision does **not** authorize canonical candidate generation yet. Before generating candidates, G0-05 must freeze in a dated decision record:
1. Selected past-only threshold policy and weighting population, with sensitivity variants retained.
2. Warm-up and eligibility rules, including the 262-event warm-up and two undefined-feature exclusions.
3. Snapshot availability, refresh and validity semantics.
4. Support/resistance rejection confirmation, de-clustering, invalidation and expiry rules.
5. Breakout continuation event/de-clustering rules.
6. Failed-breakout return-inside confirmation and source-breakout linkage.
7. Exact input paths, Git blob IDs, SHA-256 hashes, schemas and source versions.

Gate 0 remains **CONDITIONAL HOLD** because other source/engine blockers, including funding/mark-price, fees/slippage and execution-engine readiness, have their own numbered acceptance requirements. Phase 3 sequencing remains unchanged. No Gate 2+, execution simulation, strategy backtesting, or PnL work is authorized by this G0-04 decision.
