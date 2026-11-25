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

## Current next action

Begin Gate 0: inspect the existing Phase 3 signal/event ledgers, original signal availability timestamps, funding/fee source coverage, and existing execution-engine limitations. Produce a source/engine readiness report before coding a strategy or running any trade simulation.

## Completion standard

Phase 3 is not complete as a trading-system research phase until its scope audit's open items are resolved or explicitly rejected, a candidate strategy is specified and fairly tested, and the final evidence/decision is documented under the project research-governance rules.


## 8. Scope clarification — all three Phase 3 trade families

Phase 3 is not a breakout-only project. The range-trading programme must evaluate both support/resistance rejection opportunities and moves through those boundaries. The candidate families are:

1. **Support/resistance rejection (range-boundary trades):** long after a causally confirmed rejection at support; short after a causally confirmed rejection at resistance. Support and resistance are evaluated separately as well as directionally pooled; do not assume they behave symmetrically. Candidate exits may include the range interior/opposing boundary, a predeclared R target, or a time/invalidation exit.
2. **Breakout continuation:** long after a confirmed resistance break or short after a confirmed support break, with continuation and retest-entry variants tested as distinct hypotheses.
3. **Failed-breakout reversal:** after a confirmed break fails and price re-enters/reclaims the prior range, test the reversal direction (short after failed upside break; long after failed downside break), with exact confirmation and invalidation timestamps frozen.

These are research families, not approved strategies. Gate 0–5 apply across all relevant families, with family-specific signal definitions and order rules. At Gate 6, test each family independently first, report support versus resistance and long versus short breakdowns, and only then consider a combined portfolio if the individual results and exposure interactions justify it. Never pool the families in a way that hides a losing side or regime. The original Gate 0–7 sequence remains the single control sequence; this clarification expands the scope, not the number of gates.

For clarity, the shared control sequence is: **0 readiness audit → 1 descriptive lifecycle → 2 execution-resolution comparison → 3 entry rules → 4 stops/targets/management → 5 engine acceptance → 6 family-by-family strategy backtests → 7 chronological validation**. Phase 1 remains paused until the Phase 3 programme is completed or formally rejected.
