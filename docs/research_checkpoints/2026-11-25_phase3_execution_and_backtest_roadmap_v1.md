# Phase 3 Execution and Strategy Research Roadmap V1

**Date:** 2026-11-25  
**Status:** Proposed and approved direction for research sequencing; no strategy parameters selected and no Phase 3 strategy backtest run by this document.  
**Priority:** Phase 3 remains active; Phase 1 handoff paused.

## Objective

Determine whether any of the observed sideways/range behaviours can be converted into a causal, executable, cost-aware trading process. The objective is not to force profitability or to optimize until a favourable result appears. A valid negative result is acceptable.

## Known starting evidence

The Phase 3 descriptive archive includes:
- Reconstructed sideways contexts and frozen boundary interaction labels.
- Selected rejection event anatomy and early-path sequence measurements.
- Breakout prior-test classifications and forward-path outcomes.
- Five-asset 1M OHLCV sources (BTC, ETH, SOL, DOGE, AVAX) with prior quality/alignment audits.
- A matched-control branch rejected because covariate balance and joint common support were inadequate.

These findings can generate candidate hypotheses, but cannot be directly treated as trade signals or fills.

## Research questions

1. Which precisely timestamped sideways rejection or breakout/failure events are available to a live process?
2. How does execution delay and entry resolution affect attainable entry prices and missed opportunities?
3. Which entry order rules can be defined without look-ahead and with realistic fill assumptions?
4. Where can structural invalidation stops be placed, and how does stop distance affect position sizing?
5. Which exit/management hypotheses are justified enough to test: fixed R, structural target, partial exit, trailing exit, or time/invalidation exit?
6. Do any candidate rules retain positive net expectancy and acceptable drawdown on untouched chronological data after fees, slippage, spread and funding?

## Ordered work gates

### Gate 0 — Archive and source audit

- Read the Phase 3 scope completeness audit.
- Inventory the exact signal/event ledgers and source hashes to be used.
- Audit funding history, settlement timestamps, mark-price coverage, fee assumptions, and instrument provenance.
- Confirm all signal timestamps are availability timestamps, not candle-open timestamps.
- Freeze complete-bar and gap/censoring rules.

### Gate 1 — Complete descriptive lifecycle work

- Rejection: continuation, pullback-first, signal-level retests, retest depth, hold/failure, repeated crosses, and signal-candle anatomy.
- Breakout: continuation, return-inside, failed breakout, reclaim, reversal, retest timing/depth, hold/failure, and post-retest continuation.
- De-cluster event episodes and preserve ambiguous OHLC ordering rather than inventing intrabar paths.
- Report asset, side, context, time period, event count, and dependence.

### Gate 2 — Execution-resolution comparison

Use the same completed 15M signal cohort for all execution resolutions:
- 1M reference execution.
- Causally resampled 3M, 5M and 15M execution views.
- First eligible bar must begin at or after signal availability.
- Measure entry delay, entry price versus signal close and frozen structure, favourable/adverse movement while waiting, retest opportunity, fill/miss/expiry rates under declared order rules, and post-fill adverse selection.
- Do not assume faster or slower execution is better.

### Gate 3 — Candidate entry definitions

Compare a small, predeclared set only:
1. Next-eligible-1M market-style entry.
2. Pullback/limit entry at a frozen signal reference level.
3. Boundary/signal-level retest entry.
4. Lower-timeframe confirmation entry after a completed bar.

For every method define order activation, price, expiry, cancellation/invalidation, touch/fill rules, partial fills, missed fills, adverse selection, and fees. Do not treat OHLC touch as a guaranteed fill.

### Gate 4 — Stop, target and trade-management hypotheses

Do not choose the best levels from the full dataset. Derive a small set from structural and descriptive evidence, then freeze:
- Structural invalidation stop (signal/retest/zone extreme plus a justified buffer).
- Volatility-normalized buffer as a separate hypothesis.
- Fixed-R target (e.g. a small predeclared set of R multiples).
- Structural opposing-boundary or measured-move target where logically applicable.
- Partial-exit and trailing rules as separate hypotheses, not bundled optimization.
- Time stop and setup invalidation.

For each, specify same-bar stop/target collision, gaps, order activation, and whether levels are static or updated using only information available at the time.

### Gate 5 — Execution engine acceptance

Audit and test the existing single-trade and portfolio engines before trusting outputs. Existing documentation identifies limitations: limit orders/expiry are not implemented in the portfolio engine; cost inputs are not yet fully reflected in initial risk sizing; funding mark-price fallback can be approximate; actual signal candidate generation is not integrated.

Required:
- Fees by actual intended order type and verified fee assumptions.
- Spread and adverse slippage.
- Historical funding and verified settlement/mark price; missing data must not be treated as zero.
- Risk sizing that accounts for costs and stop distance.
- Gaps, stop/target collisions, partial/missed fills, expiry, concurrent assets, shared equity and exposure.
- Deterministic reproducible tests for all event ordering.

### Gate 6 — Frozen Phase 3 strategy backtest

Only after Gates 0–5:
- Test each candidate signal family separately before combinations.
- Starting equity: $1,000.
- Risk budget: 0.5% of current equity per trade, with portfolio exposure caps and one-position-per-asset constraints explicitly frozen.
- Use 1M source candles for the primary execution simulation.
- Report gross and net returns and cost decomposition.
- Report trade count, win rate, average win/loss, expectancy in currency and R, profit factor, max drawdown, time under water, exposure, turnover, holding time, fees, slippage, funding, missed/partial fills and asset/side/regime breakdown.
- Include no-trade periods and all valid signals, not only filled/winning examples.

### Gate 7 — Chronological validation

- Use chronological development, validation, and untouched out-of-sample periods.
- Existing strategy specification suggests 60% / 20% / 20%; confirm that split against event counts and data coverage before freezing.
- No shuffling, no threshold selection on the final test set, no repeated peeking at OOS results.
- Include walk-forward or rolling-origin checks only when predeclared.
- Report uncertainty and sensitivity; no broad combinatorial sweep.

## Important boundaries

- The V6 matched-control branch remains closed; do not use those pairs for future outcome comparisons.
- Do not infer causality from Phase 3 observational contrasts.
- Do not treat MFE/MAE or target-touch rates as executable PnL.
- No live deployment recommendation follows from a backtest alone.
- Preserve all prior scripts, data, protocols, failures, and outputs.
- A failed strategy is a valid result if it is evaluated fairly.

## Current status after Gate 0 inspection — 2026-11-25

The initial source/engine readiness report is recorded at [GATE0_SOURCE_ENGINE_READINESS_AUDIT_V1.md](../../reports/sideways_phase3_research_archive_v1/GATE0_SOURCE_ENGINE_READINESS_AUDIT_V1.md).

**Gate 0 decision: CONDITIONAL HOLD — not passed.** The audit found usable five-asset 1M candles, Phase 3 descriptive rejection/breakout ledgers, a funding reconciliation report, and existing execution foundations. Critical blockers remain: reconcile the stale funding audit with the later funding report and verify the five processed funding files in the actual runtime; freeze source hashes/provenance; prove causal Phase 3 event availability and build the three-family range candidate generator; make missing funding fail closed; and include fees/slippage in initial risk sizing. The audit also records the distinction between the trend-only candidate engine and Phase 3 range trading.

Next action: resolve the Gate 0 blocker register in order and reissue a documented Gate 0 pass/hold decision. Do not run Phase 3 strategy PnL backtests until critical blockers are closed.

## Completion standard

Phase 3 is not complete as a trading-system research phase until its scope audit's open items are resolved or explicitly rejected, a candidate strategy is specified and fairly tested, and the final evidence/decision is documented under the project research-governance rules.


## 8. Scope clarification — all three Phase 3 trade families

Phase 3 is not a breakout-only project. The range-trading programme must evaluate both support/resistance rejection opportunities and moves through those boundaries. The candidate families are:

1. **Support/resistance rejection (range-boundary trades):** long after a causally confirmed rejection at support; short after a causally confirmed rejection at resistance. Support and resistance are evaluated separately as well as directionally pooled; do not assume they behave symmetrically. Candidate exits may include the range interior/opposing boundary, a predeclared R target, or a time/invalidation exit.
2. **Breakout continuation:** long after a confirmed resistance break or short after a confirmed support break, with continuation and retest-entry variants tested as distinct hypotheses.
3. **Failed-breakout reversal:** after a confirmed break fails and price re-enters/reclaims the prior range, test the reversal direction (short after failed upside break; long after failed downside break), with exact confirmation and invalidation timestamps frozen.

These are research families, not approved strategies. Gate 0–5 apply across all relevant families, with family-specific signal definitions and order rules. At Gate 6, test each family independently first, report support versus resistance and long versus short breakdowns, and only then consider a combined portfolio if the individual results and exposure interactions justify it. Never pool the families in a way that hides a losing side or regime. The original Gate 0–7 sequence remains the single control sequence; this clarification expands the scope, not the number of gates.

For clarity, the shared control sequence is: **0 readiness audit → 1 descriptive lifecycle → 2 execution-resolution comparison → 3 entry rules → 4 stops/targets/management → 5 engine acceptance → 6 family-by-family strategy backtests → 7 chronological validation**. Phase 1 remains paused until the Phase 3 programme is completed or formally rejected.


## Funding verification implementation update — 2026-11-25

The fail-closed funding coverage audit code and deterministic unit tests have been added. See `src/funding_coverage_audit.py`, `src/test_funding_coverage_audit.py`, and `docs/funding_coverage_audit_v1.md`. The audit uses explicit expected window/cadence defaults from the prior reconciliation report, hashes each input, checks missing/irregular settlements and cross-asset timestamp equality, and produces a JSON manifest plus Markdown report.

The automated GitHub workflow tests synthetic fixtures only. It does not have the local processed funding files and cannot certify them. Gate 0 remains on hold until the actual local audit passes and the real manifest is archived.


## Actual funding-data verification — 2026-11-25

The real local audit has now been executed successfully against the five processed OKX realized-rate CSVs in the user's Termux environment. It found 1,188 rows per asset (5,940 total), identical timestamps across assets, coverage from 2025-10-20 00:00 UTC through 2026-11-19 16:00 UTC, 1,187 expected 8-hour intervals per asset, zero missing settlements, and no gaps or irregular intervals. Per-file SHA-256 hashes are permanently recorded in `reports/sideways_phase3_research_archive_v1/funding_coverage_audit_v1/funding_coverage_manifest.json`, alongside the human-readable report.

This closes the funding-file availability/hash/coverage evidence items G0-01 and G0-02 for the audited Termux environment. It does **not** close engine-side funding validation/application, exact mark-price provenance, fee/instrument assumptions, or the Phase 3 candidate-generation blockers. **Gate 0 remains CONDITIONAL HOLD; Gate 6 backtesting is still not authorized.** Raw funding CSVs remain local and are not committed.


## Funding contract implementation and focused workflow update — 2026-11-25

The earlier funding blocker description is a historical snapshot and has been materially updated:
- Both execution paths now require explicit funding contracts; the single-trade engine no longer defaults to an empty event list.
- The shared validator checks declared source/coverage/schedule metadata against the exact expected settlement timestamps. An empty list is valid only when the declared schedule proves no settlement is due.
- The portfolio engine validates per-asset contracts and settlement alignment against its synchronized 1M timeline.
- The experiment input loader verifies the local CSV hashes and metadata against the archived manifest and explicitly labels its current funding mark mode as `candle_close_proxy`.
- Focused CI run **45624704814** passed compilation and all seven focused test groups: https://github.com/islamomanpk-boop/okxtester/actions/runs/45624704814.

This materially closes the code-level missing-funding-default issue, but G0-03 remains partially open pending a reproducible real-input integration check and final mark-price policy acceptance. The historical mark-price candle endpoint is only a candidate proxy; exact OKX settlement valuation remains unverified. The portfolio path includes estimated entry/stop-exit slippage and taker fees in planned risk sizing; standalone single-trade sizing does not, and contract rounding/gap risk remain open. G0-01/G0-02 are closed for the five actual Termux files audited and hashed on 2026-11-25.

## Historical exit experiment archive disposition — 2026-11-25

The existing 66-configuration exit matrix is a **Model A trend-candidate** study, not Phase 3 range trading. Its source uses the trend-only candidate generator, which suppresses `NO_TREND`, and historical signal files from the separate `okx_adaptive_bot/reports/price_action_signals` input path. All 66 archived configurations completed; all 66 had negative net returns over the shared five-asset sample (approximately −99.89% to −34.34%), with no untouched chronological OOS validation evidenced. Preserve this negative historical result as trend-pipeline/shared-engine evidence; do not select its least-bad exit parameters or transfer them to Phase 3. The separate telemetry rerun archive is incomplete (2 completed, 1 running, 63 pending) and must remain clearly distinguished. Full details are in `docs/PROJECT_RESEARCH_REGISTER_V1.md`, Section 10.


## Latest Gate 0 / Gate 1 status — 2026-11-25

This is the current status snapshot and supersedes earlier provisional Gate 0 and Gate 1 wording in this roadmap and its first audit sections.

### Gate 0

**CONDITIONAL HOLD — not passed.**
- G0-01 / G0-02: **CLOSED** for the five actual processed funding files audited in Termux, with file hashes and coverage manifest archived.
- G0-03: **PARTIALLY CLOSED / ACCEPTANCE OPEN**. Both engines now require explicit funding coverage contracts; fail-closed validation is integrated and focused CI run 45624704814 passed compilation plus seven test groups. A reproducible real-input integration check and exact settlement-mark policy acceptance remain open.
- G0-04 / G0-05: **OPEN / CRITICAL**. Freeze and audit causal Phase 3 event availability/provenance and build/test the separate three-family range candidate generator. The current Model A candidate generator remains trend-only.
- G0-07: portfolio planned-risk sizing includes estimated entry/stop-exit fees and slippage; standalone sizing, exchange lot/tick rounding, and gap-through-stop risk remain open.
- G0-08 / G0-09: historical fee/instrument assumptions and exact settlement mark-price fidelity remain open. The current candle-close funding mode is an explicitly labelled proxy.
- No Gate 6 strategy PnL backtest is authorized.

### Gate 1

**PARTIAL / OPEN.**
- Rejection lifecycle Module A: **ACCEPTED — descriptive closeout complete**. The V1.1 overlap-cluster amendment and closeout are archived at `docs/research_checkpoints/2026-11-25_phase3_rejection_lifecycle_v1_1_overlap_cluster_amendment.md` and `reports/phase3_rejection_lifecycle_v1_1/PHASE3_REJECTION_LIFECYCLE_CLOSEOUT_V1_1.md`.
- Evidence: 1,992 accepted event rows (1,154 broad; 838 nested strict), 3,028 retest episodes, 7,968 horizon rows, 380 overlap clusters, zero source 1M gaps, and 12 passing synthetic tests. Workflow run 45627723414 succeeded; output archive commit 2987ca84a4277170beea9ae36ef88133c886d6bb.
- Breakout failure/reclaim lifecycle Module B: **OPEN**. This is the next Gate 1 task under the same frozen lifecycle protocol.
- Gate 2 remains closed until Module B is accepted or formally rejected and the overall Gate 1 closeout is issued.
