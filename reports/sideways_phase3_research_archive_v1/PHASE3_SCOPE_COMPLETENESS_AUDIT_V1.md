# Phase 3 Scope Completeness Audit V1

**Review date:** 2026-11-25  
**Decision:** Phase 3 is NOT fully complete as a trading-system research phase. Its core descriptive studies are complete, but execution, failed-breakout, entry, exit, and strategy validation work remains open. Phase 1 is paused pending the Phase 3 scope decision.

## 1. Why this audit exists

The earlier Phase 3 closeout correctly described the completed descriptive archive, but its handoff could be read too broadly as saying the entire sideways-market research phase was finished. Earlier project roadmaps explicitly included failed-breakout/reversal anatomy, post-signal retest execution, execution-timeframe comparisons, entry methods, stop/target research, and realistic backtesting. Those items have not all been completed.

This document reconciles the original scope with the actual archived evidence. It does not erase or overwrite earlier closeout records; it narrows their meaning to **core descriptive research complete**.

## 2. Completed work — evidence present in the repository

| Workstream | Status | Evidence / boundary |
|---|---|---|
| Historical sideways detector and regime snapshots | Completed descriptive foundation | `reports/sideways_detector_v1/`, original detector archive, methodology and historical reconstruction checkpoints |
| Boundary reconstruction and test counts | Completed descriptive foundation | `reports/sideways_boundary_events_historical_v1/` |
| Boundary interaction / penetration taxonomy | Completed | `reports/sideways_boundary_interaction_taxonomy_v1/`; 153,540 candle-level observations under frozen cadence and snapshot rules |
| Rejection episode / retest anatomy | Completed for the archived selected cohort | `episode_retest_anatomy_v1/`; 1,992 eligible events, four horizons; not full entry-execution validation |
| Early-path sequence and follow-through | Completed descriptive study | `early_path_followthrough_v1/` |
| Calendar moving-block bootstrap | Completed exploratory uncertainty analysis | `sequence_block_bootstrap_v1/`; does not establish causality or profitability |
| Per-asset / leave-one-asset-out robustness | Completed with small pair counts and caveats | `asset_robustness_v1/`; broad 71 and strict 45 matched pairs |
| Breakout prior-test classification | Completed descriptive study | `reports/breakout_prior_test_count_v1/` |
| Breakout forward-path outcomes | Completed descriptive study | `reports/breakout_forward_outcome_v1/`; no executable trade simulation |
| V6 matched-control branch diagnostics | Completed and rejected for this cohort | V6–V10.11 archives; inadequate balance and joint common support; no future outcomes should be compared using these pairs |
| Five-asset 1M source quality and timestamp alignment | Completed preflight | Separate source audit and Phase 1 preflight archives; source/instrument provenance caveat remains |

## 3. Incomplete or not yet demonstrated by archived outputs

| Workstream | Status | What remains |
|---|---|---|
| Comprehensive failed-breakout taxonomy | **Open** | Define failed break, re-entry, reclaim, reversal, continuation, and event de-clustering using frozen boundaries and confirmation timestamps; quantify outcomes by side/asset/context |
| Comprehensive rejection lifecycle | **Partially complete** | Existing anatomy is useful, but the earlier roadmap's complete continuation/pullback, signal-level retests, retest depth/hold/failure, repeated crosses, and signal-candle-size analysis have not all been shown as completed |
| Breakout retest and failure lifecycle | **Partially complete** | Descriptive forward outcomes exist; a complete retest timing/depth/hold/failure and post-retest continuation study remains to be audited/completed |
| Post-signal execution-resolution comparison | **Open** | Same completed 15M signals compared on 1M, 3M, 5M, and 15M execution; causal bar alignment and earliest eligible execution |
| Entry method research | **Open** | Next-eligible market entry, pullback/limit, signal-level retest, and lower-timeframe confirmation; expiry, fill, missed/partial fill and adverse selection rules |
| Stop-loss research | **Open** | Structure-based, volatility-based, and hybrid invalidation hypotheses; stop distance and position-size consequences |
| Take-profit and trade management | **Open** | Fixed-R, structural targets, partial exits, trailing exits, time exits, invalidation, and exit ordering |
| Full execution-cost validation | **Open** | Applicable fee schedule, spread/slippage assumptions, funding source/coverage and mark-price provenance; do not silently set missing funding to zero |
| Phase 3 strategy/backtest | **Not completed** | Causal signal-to-order-to-fill simulation with portfolio accounting, realistic costs, risk sizing, drawdown and chronological out-of-sample evaluation |
| Phase 3 decision-grade synthesis | **Partially complete** | Current synthesis explains descriptive findings; it must be extended after execution and backtest studies with tested and rejected strategy hypotheses |

## 4. Important prior commitments recovered from the project roadmap

The 2026-11-22 post-signal execution roadmap explicitly calls for:

1. Finish sideways boundary-rejection movement research.
2. Study breakout continuation and breakout retests, including return-inside, retest depth, hold/failure, and continuation.
3. Study post-signal continuation versus pullback-first paths, retests of signal levels, and MFE/MAE.
4. Compare 1M, 3M, 5M, and 15M execution using the same completed 15M signal cohort.
5. Compare entry methods only after the post-signal evidence exists.
6. Condition results on the known 1D/4H environment where valid.
7. Research risk, exits, and portfolio behaviour only after the preceding evidence.

The 2026-11-22 addendum explicitly says the execution-resolution and post-signal retest workstreams were added because the original roadmap had not enumerated them. They must not be mistaken as completed.

## 5. Existing execution/backtest infrastructure — not proof of Phase 3 strategy completion

The repository already contains:
- `docs/execution_engine_v1.md`: single-trade 1M market-entry engine with stop/target, fee, slippage, and funding hooks; important limitations remain.
- `docs/portfolio_backtester_v1.md`: synchronized multi-asset portfolio engine using prepared candidate signals; it does not generate the actual Phase 3 signals.
- `docs/price_action_strategy_spec_v1.md`: broad strategy specification with entry, stop, target and validation hypotheses. It is an initial specification, not evidence that these experiments were implemented, audited, or run for Phase 3.
- `docs/execution_data_audit_v1.md` and `reports/execution_data_audit.md`: execution data and funding-data audit references. Funding availability and exact mark-price coverage must be checked before claiming fully cost-adjusted results.

Existing engine assumptions and limitations must be independently audited before reuse. In particular, the portfolio engine documents that costs are not yet included in initial risk sizing, limit orders and expiries are not implemented, and funding mark-price fallback is approximate.

## 6. Recommended Phase 3 continuation sequence

Do not jump straight into a broad parameter sweep. Proceed in gates:

### Gate A — Close the remaining descriptive execution questions
1. Audit the exact archived status of the rejection and breakout retest/failure work.
2. Complete a frozen failed-breakout / reclaim / reversal taxonomy if absent.
3. Compare execution resolution 1M/3M/5M/15M on the same completed 15M signal set.
4. Measure entry delay, pullback/retest opportunity, fill/miss rates under explicitly stated assumptions, and adverse movement while waiting.

### Gate B — Freeze a small number of candidate trading hypotheses
Only after Gate A:
- Specify exact long/short signal rules and when each becomes knowable.
- Define entry order type, activation time, price, expiry, fill and cancellation rules.
- Define structural stop/invalidation and a small, justified set of target/management hypotheses.
- Define position sizing, portfolio concurrency, and exposure constraints.
- State what evidence would reject each candidate.

Do not select rules by inspecting the final test period.

### Gate C — Validate the execution engine and inputs
Before any strategy result:
- Unit-test order activation, next-eligible-minute timing, gaps, stop/target same-bar collision, partial/missed fills, expiry, fees, slippage, funding, position sizing and portfolio accounting.
- Verify funding coverage, settlement timestamps, mark-price source, instrument identity and fee assumptions.
- Keep 1M as the execution reference; aggregated 3M/5M/15M bars must be causally aligned.
- Include realistic adverse fills and conservative ambiguity handling.

### Gate D — Phase 3 strategy backtest
Once signal and execution rules are frozen:
- Begin with a transparent baseline, not a huge parameter sweep.
- Use the agreed starting capital of $1,000 and risk budget of 0.5% of current equity per trade, subject to the documented exposure and portfolio rules.
- Include fees, spread/slippage and actual funding where verified; explicitly label any unavoidable proxy.
- Report gross and net expectancy, trade count, win/loss distribution, profit factor, drawdown, exposure, turnover, holding time, cost decomposition, missed trades and asset/side breakdowns.
- Use chronological development/validation/untouched test periods; never shuffle.
- Preserve all candidate definitions and rejected results. A positive backtest is not live readiness.

## 7. Research order and Phase 1 handoff

**Phase 1 is paused.** Continue Phase 3 only through the above decision gates. The original five-phase descriptive order remains preserved for the other regimes, but the project now has an explicit user-requested Phase 3 execution/backtest workstream before the handoff.

This is not permission to run arbitrary stop/target optimizations. It is a decision to finish the missing Phase 3 research needed to assess whether any sideways-market behaviour can be executed as a realistic trading system. Each gate requires its own protocol, tests, interpretation, and closeout under `docs/RESEARCH_GOVERNANCE_RULES_V1.md`.

## 8. Final scope statement

- **Phase 3 descriptive research:** core scope complete, with open descriptive sub-studies listed above.
- **Phase 3 execution research:** incomplete.
- **Phase 3 entry/stop/target/trade-management research:** incomplete.
- **Phase 3 realistic strategy backtest and out-of-sample validation:** not completed.
- **Phase 3 overall trading-system readiness:** not established.

No Phase 3 strategy is currently approved as profitable or ready for live use.
