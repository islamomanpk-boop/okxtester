# Performance Reporting Implementation Plan V1

Status: Stages 1-5 complete; reporting release validated on 2026-11-21
Project: OKX Multi-Regime Price Action Strategy V1
Branch: price-action-v1

## 1. Current verified project state

The authoritative reporting requirements are documented in
docs/performance_reporting_standard_v1.md.

The project includes the portfolio backtester, exit-experiment runner,
cost-sensitivity runner, reusable performance metrics/reporting modules,
and their unit and integration tests.

The runners use summary-only equity-curve storage. Required daily,
drawdown, and exposure statistics are collected without retaining the full
minute-by-minute equity curve. Real-data reports are generated locally;
raw market/funding data and generated trade/report outputs are not
committed.

## 2. Implementation objectives

The reporting system provides trade-level and portfolio metrics,
intraday maximum drawdown, daily UTC equity/returns, Sharpe, Sortino,
CAGR, Calmar, recovery factor, concurrent positions, capital utilization,
gross exposure, per-asset and per-direction breakdowns, asset-direction
breakdowns, monthly UTC returns, exit-reason breakdowns, CSV outputs,
and human-readable Markdown reports.

Summary-only and full equity-curve modes are tested for consistent
portfolio metrics.

## 3. Implementation stages

### Stage 1 - Reusable performance metrics

Status: Complete and validated.

Created performance metrics and tests covering trade statistics,
portfolio metrics, daily/monthly returns, grouped statistics, and
exit-reason summaries. Empty trade sets, zero denominators, unavailable
ratios, breakeven trades, and insufficient daily observations are handled.

### Stage 2 - Backtester integration

Status: Complete and validated on 2026-11-21.

The backtester collects UTC daily equity marks, intraday drawdown,
concurrent-position counts, and exposure/utilization statistics in both
full and summary-only modes. Integration tests verify consistency.

### Stage 3 - Breakdown reporting

Status: Complete and validated on 2026-11-21.

The shared report generator produces overall metrics, per-asset,
per-direction, asset-direction, daily, monthly, and exit-reason reports.
It writes seven detailed CSV tables and a Markdown report, including
run metadata and end-of-data/exchange-liquidation limitations.
The Stage 3 complete suite checkpoint passed 183 tests.

### Stage 4 - Experiment runner integration

Status: Complete and validated on 2026-11-21.

Both exit experiments and cost-sensitivity scenarios invoke the shared
report generator. Outputs include summary/trade CSVs, seven detailed
CSV tables, and Markdown reports. Metadata records experiment/scenario,
UTC window, execution timeframe, per-side fees/slippage, funding,
summary-only mode, risk fraction, leverage, and end-of-data closure.
Cost-sensitivity reports disclose that cost-aware sizing can change
fills, accepted entries, and outcomes.

The complete suite passed 185 tests at an earlier Stage 4 checkpoint.
The four-scenario implementation subsequently passed 188 tests.

### Stage 5 - Real-output validation and release

Status: Complete and validated on 2026-11-21.

#### Real-data exit smoke test

Experiment: fixed_stop_0_50pct__fixed_target_1_00pct

- Assets: BTC, ETH, SOL, DOGE, AVAX; execution: 1 minute.
- Window: 2025-10-20T08:50:00+00:00 to 2026-11-19T14:14:00+00:00.
- Candidates: 17,943; accepted entries/trades: 5,026.
- Initial equity: $1,000; final equity: $40.850131.
- Net PnL: -$959.149869; return: -95.914987%.
- Maximum drawdown: 96.048263%.
- Gross PnL: -$74.127200; fees: $886.391482; funding: +$1.368814.
- Costs: 0.05% taker fee per side and 2 bps slippage per side.
- Exit reasons: 3,299 stop, 9 stop-gap, 1,715 target, 2 target-gap,
  and 1 end-of-data; total 5,026, matching trade count.
- Summary, trades, seven detailed CSV tables, and Markdown reports
  were generated; totals reconciled.

Maximum marked gross exposure/equity was 1.018688x. This is a post-mark
measurement and can exceed 1.0x as prices/equity move after allocation.
It is not, by itself, proof of an entry-time allocation-cap breach.

#### Four-scenario real-data cost sensitivity

All scenarios used 17,943 candidates, five assets, 1-minute execution,
0.5% risk fraction, shared 1x gross-exposure allocation limit, and
historical funding. Cost-aware sizing can change trade counts/outcomes.

| Scenario | Fee per side | Slippage per side | Trades | Final equity | Net PnL | Return | Max drawdown |
|---|---:|---:|---:|---:|---:|---:|---:|
| Baseline | 0.05% | 2 bps | 5,976 | $24.241370 | -$975.758630 | -97.575863% | 97.626744% |
| Zero fees | 0% | 2 bps | 5,982 | $604.414866 | -$395.585134 | -39.558513% | 55.495925% |
| Zero slippage | 0.05% | 0 bps | 5,896 | $85.043505 | -$914.956495 | -91.495650% | 92.035546% |
| Higher slippage | 0.05% | 5 bps | 6,035 | $3.009207 | -$996.990793 | -99.699079% | 99.704633% |

All scenarios had profit factor below 1 and negative expectancy:

- Baseline: PF 0.718956; expectancy -$0.163280/trade; win rate 40.56%.
- Zero fees: PF 0.959038; expectancy -$0.066129/trade; win rate 40.47%.
- Zero slippage: PF 0.803495; expectancy -$0.155183/trade; win rate 42.32%.
- Higher slippage: PF 0.586007; expectancy -$0.165201/trade; win rate 37.96%.

All four scenarios had negative net PnL, including zero fees. Costs
materially worsened results, but costs alone do not explain the negative
performance. These are research results, not evidence of a profitable
or deployable strategy.

All ten expected files were verified for each scenario: summary, trades,
overall metrics, per-asset metrics, per-direction metrics,
per-asset-direction metrics, daily returns, monthly returns,
exit-reason breakdown, and Markdown report. A scenario comparison
output was generated.

Validation confirmed that exit-reason counts equal trade counts,
trade-level net PnL reconciles with portfolio net PnL to rounding
precision, and gross PnL minus fees plus funding reconciles with net
PnL to rounding precision. Baseline per-asset and per-direction groups
were negative.

Maximum marked gross exposure/equity across the four scenarios was
approximately 1.015x-1.020x. These post-mark measurements do not alone
establish an entry-time allocation-cap breach.

#### Test, repository, and output-safety gate

The complete project test suite passed 188 tests on the four-scenario
implementation. The user verified all 40 expected cost-sensitivity
files and confirmed that the earlier 1.00% target exit smoke-test report
remained present.

Generated real-data reports and the temporary backtester backup remain
local and untracked. Do not commit raw market/funding data, generated
trade reports, or temporary backups without a separate explicit decision.

Stage 5 reporting validation is complete. The full 66-experiment batch
has not been run and is a separate next-stage decision.

## 4. Required output files

For each experiment or cost scenario:

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

Experiment batches also generate a comparison CSV.

## 5. Project safety and data rules

- Do not commit raw market or raw funding data.
- Do not commit API keys, credentials, or secrets.
- Do not commit temporary backups.
- Preserve existing reports and losing experiment results.
- Do not overwrite previously generated baseline reports.
- Keep implementation changes tested and documented.
- Generated local real-data reports are not automatically part of
  the source-code release.

## 6. Experiment execution gate

The reporting implementation, tests, real-output smoke tests, and
documentation release gate are complete and validated.

The full 66-experiment batch is not included in this release. Before
starting it, agree the execution order, resource/runtime constraints,
output-retention approach, and review checkpoints. Run batches
sequentially and preserve all scenarios. Backtest results are not a
guarantee of future performance or authorization to deploy live trading.

## 7. Relationship to the reporting standard

This document records the implementation sequence and validation.
Authoritative metric definitions, calculation conventions, required
breakdowns, output requirements, and interpretation rules remain in
docs/performance_reporting_standard_v1.md.


## 8. Stage 6 - Resumable 66-experiment batch runner

Status: Implemented on 2026-11-21; local Termux test validation pending.
The full real-data batch has not been started.

Added `src/run_exit_experiment_batch.py` and its unit tests.
The existing single-experiment runner now exposes
`run_one_experiment_with_inputs`, allowing the batch runner to reuse
one preloaded set of synchronized candles, funding events, and signal
candidates across all experiments.

### Batch design

- Validates the exact 66-variant matrix: 22 baseline, 22 trailing-stop,
  and 22 trailing-take-profit experiments.
- Runs experiments sequentially; it does not launch parallel workers.
- Loads shared market, funding, and candidate inputs once per batch run.
- Writes each experiment's reports before moving to the next experiment.
- Verifies all eleven expected artifacts and the matching one-row
  summary before marking an experiment complete.
- Writes an atomic batch manifest and comparison CSV after each
  successful experiment.
- Calls garbage collection between experiments to reduce retained
  Python objects on memory-constrained Android devices.
- Stops on the first experiment error while preserving completed outputs.
- Resumes by skipping only experiments whose complete artifact set and
  summary are verified. Partial or invalid outputs are rerun.
- `--rerun-completed` explicitly forces completed experiments to run again.
- `--dry-run` and `--list-experiments` inspect the matrix without
  loading the real datasets.

### Termux commands

Inspect the matrix without running it:

```bash
cd ~/okxtester
git pull origin price-action-v1
PYTHONPATH=src python -m run_exit_experiment_batch --dry-run
```

Run or resume the full batch:

```bash
cd ~/okxtester
PYTHONPATH=src python -m run_exit_experiment_batch
```

The runner writes local-only files under
`~/okxtester/reports/exit_experiments/`:

- `exit_experiment_batch_manifest.csv`
- `exit_experiment_batch_comparison.csv`
- Eleven artifacts per experiment, including the summary, trades,
  seven detailed metric CSVs, and two Markdown reports.

The batch runner implementation and tests are committed to the project
branch. The user must run the local test suite after pulling these
changes. No 66-experiment real-data run is authorized by this
implementation commit; the real-data batch starts only after local
tests and a dry-run are reviewed.
