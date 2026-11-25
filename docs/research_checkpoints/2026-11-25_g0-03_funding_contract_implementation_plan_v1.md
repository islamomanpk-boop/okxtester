# G0-03 Funding Contract Implementation Plan V1

**Date:** 2026-11-25  
**Branch:** `price-action-v1`  
**Status:** Design checkpoint; implementation not yet accepted.

## 1. Baseline verification

A dedicated push-triggered workflow was added at `.github/workflows/funding-engine-contract-tests.yml`.

Baseline run: https://github.com/islamomanpk-boop/okxtester/actions/runs/45544206451

Result: **PASS**. The workflow compiled the engines and ran 55 existing tests:
- Standalone execution engine: 12
- Portfolio backtester: 15
- Portfolio experiment integration: 4
- Trailing portfolio integration: 5
- Portfolio allocator: 15
- Portfolio safety: 4

This is a pre-change baseline, not evidence that funding coverage is already safe.

## 2. Source findings confirmed

- `src/execution_engine.py`: `simulate_trade` currently defaults `funding_events` to an empty iterable. A caller can omit funding and silently receive zero funding PnL.
- `src/portfolio_backtester.py`: `_validate_funding` validates mapping keys, event fields, rates, chronological order, and optional mark-price values. It does not require coverage metadata or compare events with an expected settlement schedule; an empty list is accepted.
- Both engines apply the convention `entry_time < funding_time <= exit_time`.
- Both engines may use the settlement-minute candle close if an explicit mark price is absent.
- `src/run_exit_experiments.py` loads the funding CSVs and passes rate events into the portfolio engine. Its reports currently describe candle-close fallback as a proxy.
- The audited funding manifest contains per-asset instrument identity, SHA-256, coverage endpoints, expected interval, row count, and PASS status. The current audit is 8-hour cadence for the audited historical scope; this must not become a universal hard-coded assumption.

## 3. Contract to implement

Introduce one shared funding contract/validator used by both execution engines.

Each traded asset must have:
- A non-empty instrument identity (for example, `BTC-USDT-SWAP`).
- Verified coverage start and end timestamps in milliseconds.
- A source identifier and 64-character SHA-256 hash.
- An explicit schedule identifier/version and an explicit ordered list of expected settlement timestamps. The schedule list must be derived from verified source metadata, not inferred from the observed events alone.
- An explicit mark-price mode: `exact` or `candle_close_proxy`.

The actual event list must:
- Be explicitly supplied, including when it is empty.
- Have strictly increasing, unique timestamps.
- Contain finite rates in the accepted range.
- Match the expected settlement timestamp set for the verified source coverage. Missing and extra settlements fail closed.
- Carry a positive finite `mark_price` for every event in `exact` mode.
- Permit a missing mark only in `candle_close_proxy` mode, with proxy mode visible in trade and report metadata.

Every completed trade must have its full holding interval inside verified funding coverage. For the trade interval `entry_time < settlement_time <= exit_time`, every expected settlement must be applied exactly once. Empty events are valid only when the expected schedule contains no settlement in the charged interval.

## 4. Event timing and execution semantics

Preserve and explicitly test:
- A settlement at the entry timestamp is not charged.
- A settlement at the exit timestamp is charged.
- Positive funding rates make longs pay and shorts receive.
- Negative rates reverse those signs.
- Funding notional is quantity multiplied by the settlement mark price.
- Portfolio funding must be applied before processing exits at a timestamp, matching the existing boundary convention.

The portfolio engine currently processes funding on its one-minute execution timeline. The implementation must explicitly reject a settlement schedule/event that cannot be represented on that timeline rather than silently skipping it. Exact marks remove the need to infer settlement price from candle close, but do not remove the need to process the settlement event at the correct timestamp.

## 5. Runner and report integration

Update the historical runner to:
- Load and verify the archived funding manifest.
- Recompute each local CSV SHA-256 and compare it with the archived hash.
- Validate instrument identity and coverage metadata.
- Supply the complete verified funding event history plus the expected schedule to the engine; do not construct the schedule solely from the events found in the file.
- Keep the current candle-close proxy explicit until exact OKX settlement mark data is obtained and verified.

Record the mark-price mode and source/coverage identity in per-trade outputs, experiment summaries, and performance-report metadata. Do not label proxy pricing as exact.

## 6. Required tests

- Omitted funding input fails in the standalone engine.
- Missing per-asset coverage metadata fails in both engines.
- Empty events plus an expected settlement fails.
- Empty events plus no expected settlement passes.
- A missing interior expected settlement fails.
- Duplicate, out-of-order, invalid, and non-finite rates fail.
- A trade before coverage start or after coverage end fails closed.
- Entry-time settlement is excluded; exit-time settlement is included.
- Positive/negative rates for long and short positions have correct signs and notional.
- Exact mode rejects a missing mark price.
- Proxy mode works only when explicitly selected and is labelled in outputs.
- Standalone and portfolio funding arithmetic agree for equivalent trades.
- Portfolio rejects expected settlement timestamps that do not align with its execution timeline.

## 7. Migration scope

The signature/contract migration must update:
- `src/execution_engine.py` and `src/test_execution_engine.py`
- `src/portfolio_backtester.py` and `src/test_portfolio_backtester.py`
- `src/test_experiment_portfolio.py`
- `src/test_trailing_portfolio.py`
- `src/run_exit_experiments.py`
- `src/run_cost_sensitivity.py`
- All focused workflow paths and test commands as needed.

The grep inventory in `2026-11-25_funding_coverage_and_engine_callsite_inventory_v1.md` is the migration checklist. Re-run it after changes to detect missed integrations.

## 8. Gate decision

The baseline workflow is now available and passing. G0-03 remains OPEN. No strategy PnL backtest is authorized until the shared contract, runner integration, and required tests are implemented and pass. Exact settlement mark-price availability remains a separate evidence requirement; the current verified funding-rate files do not provide it.


## 9. Validator implementation checkpoint — 2026-11-25

Implemented and committed:
- `src/funding_coverage.py`
- `src/test_funding_coverage.py`
- Updated `.github/workflows/funding-engine-contract-tests.yml` to compile and run the new validator tests.

The shared validator currently enforces:
- Explicit per-asset `events` and `coverage` objects.
- Instrument identity and SHA-256 format.
- Coverage and event-window bounds.
- Explicit schedule ID, start, interval, and end (no universal 8-hour constant).
- Exact equality between expected and supplied settlement timestamps in the event window.
- Strictly increasing unique timestamps, finite bounded rates, and mark-price mode validation.
- Exact mode requires a positive finite mark price.
- A trade-window helper checks source coverage and the expected settlements in `entry_time < funding_time <= exit_time`.

GitHub Actions run: https://github.com/islamomanpk-boop/okxtester/actions/runs/45544624998

Result: **PASS** — 68 tests across the new funding contract suite (13) and the existing standalone engine (12), portfolio backtester (15), experiment integration (4), trailing portfolio (5), allocator (15), and safety (4).

One earlier test run failed because the test expected the wrong missing-settlement count (one instead of three). The assertion was corrected; the passing run above includes the correction.

**Important boundary:** This is a validated standalone contract module, not yet integrated into `execution_engine.py`, `portfolio_backtester.py`, or the historical data loader. Existing engine APIs still have their old behaviour. G0-03 remains OPEN and strategy PnL backtesting remains unauthorized.

## 10. Next implementation slice

Integrate the shared contract into the standalone engine first, then the portfolio engine:
1. Require explicit funding events and coverage metadata; omission must fail.
2. Validate the actual completed trade's holding interval after its exit time is known.
3. Ensure event timestamp ordering and mark-price mode are consistent with the contract.
4. Add per-trade funding provenance fields.
5. Migrate the portfolio runner and all fixtures/call sites to the same contract shape.
6. Verify the local CSV SHA-256 values against the archived manifest in `run_exit_experiments.py`.
7. Re-run the dedicated workflow and only then consider G0-03 closure.


## 11. Engine integration and source-loader checkpoint — 2026-11-25

Implemented on `price-action-v1`:

### Standalone engine
- `simulate_trade` now requires an explicit `funding_contract`; the former silent `funding_events=()` default is removed.
- The shared validator checks the contract before simulation and checks the actual entry-to-exit holding interval after the exit is known.
- A missing exact mark fails in exact mode. Candle-close fallback is permitted only in explicit `candle_close_proxy` mode.
- Trade output records mark-price mode, source hash, instrument, schedule ID, and settlements applied.

### Portfolio engine
- `run_portfolio_backtest` now requires per-asset `{events, coverage}` contracts.
- It validates complete source schedule coverage, actual trade holding intervals, and exact/proxy mark rules.
- A settlement inside the execution window must align with the 1-minute timeline. Events outside the current execution window remain part of the verified full source history and are not incorrectly required to appear on the trimmed timeline.
- Portfolio trade output records the same funding provenance fields.

### Historical data loader and reporting
- `run_exit_experiments.py` now reads the archived funding coverage manifest, requires PASS status and the complete five-asset set, verifies each local CSV SHA-256, instrument identity, row count, endpoints, ordering, and rates, then passes the full verified history and manifest-defined schedule into the portfolio engine.
- The loader does not derive its schedule from observed event rows. It uses the archived per-asset first timestamp, interval, and final timestamp.
- `run_cost_sensitivity.py` and the batch experiment runner were migrated to the new six-item shared-input tuple.
- Added `src/verify_local_funding_manifest.py`, a no-backtest CLI that verifies all five real local CSVs against the committed manifest and validates their complete schedules. It is included in CI compilation.
- Experiment and cost-sensitivity summaries/report metadata identify the manifest hash and explicitly state `candle_close_proxy`. Trade rows retain per-asset source identity and schedule provenance.
- Exact OKX settlement marks remain unavailable in the audited source files; no output labels candle-close proxy marks as exact.

### Integration tests and workflow
- Added `src/test_funding_loader.py` for manifest hash mismatch, instrument mismatch, and successful contract construction.
- Added engine-level tests for omitted standalone funding input, out-of-coverage trades, missing portfolio settlements, and portfolio holding intervals beyond coverage.
- The workflow compiles the engines, loaders, batch runner, local verification CLI, and focused tests. It checks out the exact triggering commit (`${{ github.sha }}`), not the moving branch tip.

Latest full focused run after the exact-checkout workflow adjustment:
https://github.com/islamomanpk-boop/okxtester/actions/runs/45545754508

Result: **PASS — 75 tests on the exact triggering commit**, including compilation of the local verification CLI:
- Funding contract: 13
- Funding manifest loader: 3
- Standalone execution engine: 14
- Portfolio backtester: 17
- Experiment integration: 4
- Trailing portfolio integration: 5
- Portfolio allocator: 15
- Portfolio safety: 4


## 12. Remaining G0-03 acceptance work

G0-03 is still **OPEN**. The code-level contract and local-file loader are implemented, but do not close the gate until:

1. The exact-commit workflow run above passes — **complete**.
2. Run `PYTHONPATH=src python src/verify_local_funding_manifest.py` from the repository root on the user's Termux environment. It checks the real five-asset processed CSVs against the archived manifest without running a backtest. Those CSVs are intentionally not in GitHub, so CI's synthetic loader tests cannot replace this local-source verification.
3. The exact-mark versus proxy policy is formally accepted for the research objective. The current implementation explicitly supports proxy mode but does not claim exact settlement marks.
4. All remaining project-wide funding call sites are re-audited after the API migration.

No strategy PnL backtest is authorized until the Gate 0 decision is formally updated. The five-asset audit and contract remain reusable for later phases while the exact source files and scope remain unchanged.
