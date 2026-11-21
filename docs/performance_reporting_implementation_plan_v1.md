# Performance Reporting Implementation Plan V1

Status: In progress - Stage 1 complete; Stage 2 next
Project: OKX Multi-Regime Price Action Strategy V1
Branch: price-action-v1

## 1. Current verified project state

The performance reporting requirements are documented in:

- docs/performance_reporting_standard_v1.md

That standard was pushed and independently verified on GitHub.

Verified commit:
- 4d390af
- Document performance reporting and validation standard

The existing project includes:

- src/portfolio_backtester.py
- src/run_exit_experiments.py
- src/run_cost_sensitivity.py
- src/test_portfolio_backtester.py
- Existing exit experiment configuration and trailing-exit modules.
- A previously completed and committed baseline experiment.

The experiment runners currently use summary-only equity-curve storage.
The backtester returns closed trades, decisions, total gross PnL,
fees, funding PnL, final equity, return, and maximum drawdown percentage.

The reporting implementation must preserve existing backtester behavior
and existing experiment results unless a tested correction is necessary.

## 2. Implementation objectives

Implement a reusable and fully tested reporting system that provides:

- Trade-level performance metrics.
- Portfolio return and risk metrics.
- Intraday maximum drawdown in dollars and percent.
- Daily UTC portfolio equity and returns.
- Sharpe, Sortino, CAGR, Calmar, and recovery factor.
- Maximum concurrent positions.
- Average and maximum capital utilization.
- Maximum gross exposure in quote currency and equity multiples.
- Per-asset and per-direction breakdowns.
- Asset-and-direction breakdowns.
- Monthly UTC returns, including partial months.
- Exit-reason breakdowns.
- Human-readable Markdown reports and machine-readable CSV files.

Summary-only mode must collect the required daily and exposure statistics
without storing the complete minute-by-minute equity curve.

Full equity-curve mode and summary-only mode must produce consistent
portfolio metrics.

## 3. Implementation stages

### Stage 1 - Reusable performance metrics

Create:

- src/performance_metrics.py
- src/test_performance_metrics.py

Implement and test trade statistics, portfolio metrics, daily returns,
monthly returns, grouped trade statistics, and exit-reason summaries.

Handle empty trade sets, zero denominators, unavailable ratios,
breakeven trades, and insufficient daily observations explicitly.

Stage 1 implementation is complete and committed on branch `price-action-v1`.
Validation on 2026-11-21: the complete project test suite passed, 174 tests
in 3.468 seconds. The suite includes the new performance-metrics tests and
all existing project tests. UTC month-end and partial-month boundaries,
summary-only CAGR boundaries, and unavailable drawdown-dependent ratios
are covered by tests.

### Stage 2 - Backtester integration

Modify:

- src/portfolio_backtester.py
- src/test_portfolio_backtester.py

Add lightweight collection of:

- UTC daily equity marks.
- Intraday maximum drawdown amount.
- Maximum simultaneous open positions.
- Average capital utilization.
- Maximum capital utilization.
- Maximum gross exposure.
- Maximum gross exposure as a multiple of positive marked equity.

Preserve the existing full and summary-only modes.

Test that both modes return matching daily, drawdown, and exposure metrics.

### Stage 3 - Breakdown reporting

Generate:

- Overall portfolio metrics.
- Per-asset metrics.
- LONG versus SHORT metrics.
- Asset-and-direction metrics.
- Monthly UTC returns.
- Exit-reason breakdowns.

Include losing assets and directions. Do not omit groups because their
results are unfavorable.

### Stage 4 - Experiment runner integration

Integrate the reporting system into:

- src/run_exit_experiments.py
- src/run_cost_sensitivity.py

Each experiment or scenario must produce the reporting files specified
in docs/performance_reporting_standard_v1.md.

Comparison reports must preserve the cost assumptions and experiment IDs.

### Stage 5 - Validation and release

Before the reporting implementation is considered complete:

1. Add unit tests for all metric definitions and edge cases.
2. Test daily and monthly UTC boundaries.
3. Test empty and breakeven trade groups.
4. Test undefined profit factor, payoff, Sharpe, Sortino, and Calmar.
5. Test long and short breakdowns.
6. Test full versus summary-only consistency.
7. Run the complete unit test suite.
8. Run git diff --check.
9. Review generated reports for correctness and completeness.
10. Commit and push all approved changes to price-action-v1.
11. Independently verify the pushed commit and files on GitHub.

## 4. Required output files

For each experiment or cost scenario, generate:

- Main summary CSV.
- Closed-trades CSV.
- Overall metrics CSV or report.
- Per-asset metrics CSV.
- Per-direction metrics CSV.
- Asset-and-direction metrics CSV.
- Monthly returns CSV.
- Exit-reason breakdown CSV.
- Human-readable Markdown report.

For experiment batches, generate a comparison CSV.

## 5. Project safety and data rules

- Do not commit raw market data or raw funding data.
- Do not commit API keys, credentials, or secrets.
- Do not commit temporary backups.
- Preserve existing reports and losing experiment results.
- Do not overwrite the previously committed baseline report.
- Keep implementation changes tested and documented.

## 6. Experiment execution gate

Do not start the full 66-experiment batch until:

- The reporting implementation is complete.
- All relevant tests pass.
- The complete project test suite passes.
- The reporting changes are committed and pushed.
- The remote branch and files are independently verified.

After that gate, run cost sensitivity and the exit experiment batches
sequentially, recording results and preserving all scenarios.

## 7. Relationship to the reporting standard

This document describes the implementation sequence.

The authoritative metric definitions, calculation conventions,
required breakdowns, output requirements, and interpretation rules
remain in:

docs/performance_reporting_standard_v1.md
