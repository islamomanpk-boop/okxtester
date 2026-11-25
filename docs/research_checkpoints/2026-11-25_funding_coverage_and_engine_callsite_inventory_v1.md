# Funding coverage and engine call-site inventory V1

**Recorded:** 2026-11-25  
**Branch:** `price-action-v1`  
**Purpose:** Preserve reusable funding-data and engine-integration evidence for Phase 3 and later market-regime phases.

## 1. Shared funding-data evidence

The actual local processed OKX `realizedRate` funding files for BTC, ETH, SOL, DOGE, and AVAX USDT swaps were audited on 2026-11-25.

- 1,188 rows per asset; 5,940 rows total.
- Identical timestamp coverage: 2025-10-20 00:00 UTC through 2026-11-19 16:00 UTC.
- Observed cadence: 8 hours; 1,187 intervals per asset.
- Zero missing settlements, gaps, irregular intervals, duplicates, instrument mismatches, invalid rates, or cross-asset timestamp differences.
- Source SHA-256 hashes and local source paths are recorded in `reports/sideways_phase3_research_archive_v1/funding_coverage_audit_v1/funding_coverage_manifest.json` and the accompanying `funding_coverage_audit.md`.

The CSVs remain in the user's local Termux data directory and are intentionally not committed. This evidence can be reused in later phases only while the source hashes, coverage window, instrument identity, and audit assumptions remain applicable. Re-run the audit if the files change or a later phase requires a different date range or instrument set.

**Important limitation:** This audit validates realized funding-rate history and timestamp coverage. It does not establish exact OKX settlement mark-price provenance, nor does it prove that either execution engine applies funding correctly. The engines' candle-close fallback is a proxy and must be explicitly labelled; exact-mark mode must fail closed when an exact mark is unavailable.

## 2. Funding-related Python call-site inventory

The following inventory was captured from the user's repository-root command on 2026-11-25:

```bash
grep -RIn --include='*.py' -E 'simulate_trade\(|run_portfolio_backtest\(|funding_events|funding_by_asset' src research tests
```

### Engine definitions and funding handling

- `src/execution_engine.py:93` — `simulate_trade(...)` definition.
- `src/execution_engine.py:101` — `funding_events: Iterable = ()` default; omission can therefore silently represent no funding events.
- `src/execution_engine.py:204` — funding-event iteration/application.
- `src/portfolio_backtester.py:126` — `_validate_funding(bars_by_asset, funding_by_asset)`.
- `src/portfolio_backtester.py:127-135` — mapping and per-asset presence checks.
- `src/portfolio_backtester.py:284` — `run_portfolio_backtest(...)` definition.
- `src/portfolio_backtester.py:287` — `funding_by_asset` argument.
- `src/portfolio_backtester.py:302` — funding validation call.
- `src/portfolio_backtester.py:316` — per-asset funding-event iteration.

### Direct test coverage and fixtures

- `src/test_execution_engine.py:47,61,72,83,93,105-107,123-125,136-138,146,155` — standalone engine calls and funding-event test cases.
- `src/test_portfolio_backtester.py:65,82,94,120,143,167,188,204,221,230,241,253,270,273,310,313,395` — portfolio backtest calls; line 230 includes an empty mapping case.
- `src/test_experiment_portfolio.py:72,103,134,184` — portfolio calls with `funding_by_asset={"BTC": []}` at lines 75, 106, 137, and 187.
- `src/test_trailing_portfolio.py:56` — wrapper call into the portfolio backtester.

### Research/runner integrations

- `src/run_exit_experiments.py:118-121` — builds `funding_by_asset` and loads funding for each asset.
- `src/run_exit_experiments.py:152,190,211,214` — passes funding data through experiment/backtest paths.
- `src/run_cost_sensitivity.py:65,68` — invokes the portfolio backtester with funding data.

The grep command covered Python files under `src`, `research`, and `tests`. This is a text-match inventory, not proof that every dynamic/imported call path has been found. Re-run after future refactors and before changing public engine signatures.

## 3. Reusable engineering requirements

1. Funding input must be explicit; omission must not silently mean zero funding.
2. Every traded asset must have verified coverage metadata and source identity.
3. Validate each trade's actual holding interval against verified coverage and the expected settlement schedule.
4. Empty events are valid only when the schedule proves no settlement falls in the charged interval.
5. Do not hard-code an 8-hour schedule as a universal rule; use an explicit, versioned schedule or expected settlement timestamps.
6. Exact-mark mode must reject missing exact settlement marks. Any candle-close proxy mode must be explicit and visible in result/report metadata.
7. Preserve and test the current event-boundary convention: `entry_time < funding_timestamp <= exit_time`.
8. Test standalone/portfolio funding arithmetic parity, long/short signs, notional basis, coverage boundaries, missing settlements, duplicates, ordering, and invalid rates.
9. Update all test fixtures and runner integrations deliberately if the funding contract or function signatures change.

## 4. Gate status

This inventory is supporting evidence for the shared execution-engine readiness work (G0-03). It does not close G0-03. Gate 0 remains CONDITIONAL HOLD until coverage-aware, fail-closed behaviour is implemented and tested in both engines. Phase 3 strategy PnL backtesting remains unauthorized until all Gate 0 blockers are resolved.

Because the engine and funding contract are shared infrastructure, retain this evidence for later phases; do not assume later phases are exempt from the same safeguards.


## 5. Post-migration call-site disposition — 2026-11-25

Section 2 is the **pre-migration snapshot** supplied by the user's grep output. The relevant call paths have since been migrated:

- `src/execution_engine.py`: public `simulate_trade` now requires `funding_contract`; the optional empty `funding_events` default has been removed.
- `src/test_execution_engine.py`: legacy event-list fixtures are converted to explicit contracts for arithmetic tests; dedicated tests call the engine directly to verify omitted contracts and out-of-coverage trades fail.
- `src/portfolio_backtester.py`: `run_portfolio_backtest` now validates per-asset contracts and returns normalized coverage metadata for accounting.
- `src/test_portfolio_backtester.py`, `src/test_experiment_portfolio.py`, and `src/test_trailing_portfolio.py`: fixtures are migrated to explicit contracts. Direct integration tests cover missing expected settlements and holding intervals beyond coverage.
- `src/run_exit_experiments.py`: the local funding loader now reads the archived manifest, verifies CSV SHA-256, instrument, row count, endpoints, ordering and rates, and builds the contract from the manifest's explicit schedule.
- `src/run_cost_sensitivity.py`: consumes the migrated contracts and includes manifest hash and proxy-mode provenance in output metadata.
- `src/run_exit_experiment_batch.py`: continues to reuse the shared input tuple and now passes the migrated funding contracts through the single-experiment runner.

The dedicated workflow compiles the engines, loader, cost-sensitivity runner, batch runner, and focused test files. Exact-commit workflow run: https://github.com/islamomanpk-boop/okxtester/actions/runs/45545547488 — **PASS, 75 tests**.

This migration checklist is based on the captured grep inventory plus the focused workflow. A fresh repository-wide text-match audit should still be run before any future public API change. The local CSVs are not in GitHub, so CI's synthetic loader tests do not replace verification against the user's actual local source files.
