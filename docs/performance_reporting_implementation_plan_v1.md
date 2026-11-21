# Performance Reporting Implementation Plan V1

Status: Stage 4 validated; Stage 5 real-output validation remains
Project: OKX Multi-Regime Price Action Strategy V1
Branch: price-action-v1

## 1. Current verified project state

The performance reporting requirements are documented in:

- docs/performance_reporting_standard_v1.md

That standard was pushed and independently verified on GitHub.

The project includes:

- src/portfolio_backtester.py
- src/run_exit_experiments.py
- src/run_cost_sensitivity.py
- src/performance_metrics.py
- src/performance_reporting.py
- Their corresponding unit and integration tests.

The experiment runners use summary-only equity-curve storage. The backtester
collects the daily, drawdown, and exposure statistics required by the shared
report generator without retaining the full minute-by-minute equity curve.

The reporting implementation preserves the existing backtester behavior
and writes reports separately for each experiment or cost scenario.

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

Status: Complete and validated.

Created:
- src/performance_metrics.py
- src/test_performance_metrics.py

Implemented trade statistics, portfolio metrics, daily returns, monthly
returns, grouped trade statistics, and exit-reason summaries.

Empty trade sets, zero denominators, unavailable ratios, breakeven trades,
and insufficient daily observations are handled explicitly.

### Stage 2 - Backtester integration

Status: Complete and validated on 2026-11-21.

The backtester collects UTC daily equity marks, intraday drawdown in amount
and percent, concurrent-position counts, and exposure/utilization statistics
in both full and summary-only modes. The final daily mark is replaced with
realized final equity after end-of-data closures.

The integration test verifies matching daily, drawdown, and exposure
statistics between full and summary-only modes.

### Stage 3 - Breakdown reporting

Status: Complete and validated on 2026-11-21.

Created:
- src/performance_reporting.py
- src/test_performance_reporting.py

The report generator builds overall portfolio and trade metrics, per-asset,
per-direction, and asset-and-direction breakdowns, daily returns, monthly
UTC returns, and exit-reason summaries. It writes seven machine-readable
CSV tables plus a human-readable Markdown report. The report includes run
metadata and explicit end-of-data and exchange-liquidation limitations.

The complete project test suite passed 183 tests in 3.829 seconds at the
Stage 3 validation checkpoint.

### Stage 4 - Experiment runner integration

Status: Complete and validated on 2026-11-21.

Both experiment runners call the shared reporting generator after each
backtest:

- Exit experiments produce the seven detailed CSV tables and Markdown
  performance report alongside the existing summary and trade CSVs.
- Each cost-sensitivity scenario produces the same detailed report set.
- Metadata records experiment/scenario identifiers, UTC execution window,
  1-minute timeframe, per-side fee and slippage assumptions, funding
  treatment, summary-only storage, risk fraction, leverage, and forced
  end-of-data closure policy.
- Cost-sensitivity reports disclose that cost-aware sizing means fills,
  accepted entries, and outcomes may change across scenarios.

Integration tests verify that both runners invoke the shared reporter and
preserve their respective cost assumptions.

Validation on 2026-11-21: the user pulled commit 174681c and ran the complete
test suite successfully: 185 tests passed in 5.157 seconds. This includes
both runner/reporting integration tests and all reporting-generator tests.

The runner integration tests use synthetic fixtures and verify invocation;
their printed 1970 timestamps and zero-trade summaries are test data, not
real market-run results.

### Stage 5 - Real-output validation and release

Status: Pending.

The automated implementation and full-suite test gate is passed. Before
calling the reporting work fully released or starting the 66-experiment
batch, perform controlled real-data smoke tests:

1. Run one baseline exit experiment using the existing local market,
   signal, and funding datasets.
2. Confirm that its report directory contains the expected summary,
   closed-trades, seven detailed CSV tables, and Markdown report.
3. Inspect the generated report for plausible metadata, totals, date
   boundaries, trade counts, and consistency with the runner summary.
4. Run one cost-sensitivity scenario (or the complete small scenario set
   if runtime is acceptable) and verify separate scenario reports and
   preserved fee/slippage assumptions.
5. Check that the pre-existing baseline report is not overwritten.
6. Run git diff --check and confirm no raw market/funding data, secrets,
   or temporary backups are staged.
7. Record smoke-test outcomes and any corrections in this plan.
8. Commit and push any approved fixes; independently verify the remote
   branch and changed files.

Do not start the full 66-experiment batch until Stage 5 real-output
validation is complete and the reporting release is committed and verified.

## 4. Required output files

For each experiment or cost scenario, generate:

- Main summary CSV.
- Closed-trades CSV.
- Overall metrics CSV.
- Per-asset metrics CSV.
- Per-direction metrics CSV.
- Asset-and-direction metrics CSV.
- Daily returns CSV.
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
- Real-output smoke tests are reviewed.
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
