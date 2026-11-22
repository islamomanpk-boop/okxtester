# Research Checkpoint — 2026-11-22

## User's standing project rule

**Permanent working rule:** Whenever we perform research, run a test, make a meaningful discovery, change an assumption, or make an important project decision, record the work in GitHub. Prefer a concise dated research note or an update to the relevant project document. Include purpose, method, inputs, assumptions, result, limitations, and next action. Do not rely on chat history as the only record.

Do not claim a test or research task is complete until its outputs have been checked. Keep raw evidence and reproducible scripts where practical; summarize key findings in Markdown.

## Environment check

The user ran a Termux inventory from `~/okxtester`.

- No `run_exit_experiment_batch` process was running at the time of the check.
- Five 1-minute OHLCV CSVs were found under `~/okx_scalping_data/`:
  - `BTC_USDT_USDT_1m.csv` (~30 MB)
  - `ETH_USDT_USDT_1m.csv` (~30 MB)
  - `SOL_USDT_USDT_1m.csv` (~26 MB)
  - `DOGE_USDT_USDT_1m.csv` (~30 MB)
  - `AVAX_USDT_USDT_1m.csv` (~25 MB)
- The displayed files use columns `ts,open,high,low,close,vol`.
- Their displayed first timestamps begin at `1760950200000`. Their last displayed timestamps differ by a few minutes:
  - BTC: `1795097640000`
  - ETH: `1795097640000`
  - SOL: `1795097700000`
  - DOGE: `1795097700000`
  - AVAX: `1795097760000`
- Five processed funding-rate files were found under `~/okx_scalping_data/funding_rates/processed/`, one per asset, approximately 54–56 KB each.
- Five 15-minute signal CSVs were found under `~/okx_adaptive_bot/reports/price_action_signals/`, one per asset, approximately 21–22 MB each.

**Important provenance warning:** The market-data and signal files are in directories named for other local projects (`okx_scalping_data`, `okx_adaptive_bot`). Their existence does not prove they are the exact, current inputs used by `okxtester`. Before analysis, verify signal-generation code/version, columns, timestamp ranges, asset mapping, data lineage, and that all files correspond to the same intended dataset and research specification. Do not move or delete these source files as part of repository cleanup.

## Repository report inventory — partial

The user's `find reports -maxdepth 3 -type f | sort | head -100` output showed:
- Data quality and input-preflight reports.
- Cross-asset timestamp alignment reports and exceptions.
- Cost-sensitivity outputs, including per-scenario metrics, trade exports, monthly/daily returns, and performance reports.
- A large original `reports/exit_experiments/` collection with batch logs/manifests/comparison and per-experiment summaries, trade exports, and breakdowns.
- EMA-pullback diagnostic and holding-period experiment outputs.
- Execution-data audit report.

The displayed listing was intentionally limited to the first 100 sorted paths and ended with a broken-pipe message from `head`; it is **not a complete inventory**. Do not delete or classify files based only on this partial listing.

## Telemetry rerun state

At inventory time no batch process was running. The telemetry-enabled batch was previously interrupted after two experiments completed. Those first two outputs were saved in `reports/exit_experiments_telemetry_v1/`. The remainder must be treated as unrun/unknown until its checkpoint and files are inspected. Do not resume the entire 66-experiment matrix automatically.

## Next audit steps

1. Inspect the telemetry directory: list all files, read the checkpoint and log, and identify exactly which experiments completed.
2. Generate a complete tracked-file inventory for branch `price-action-v1` using Git, including `git ls-files`, file sizes, and directory totals. Separately list untracked and ignored files.
3. Verify the actual source files and signal files with headers, row counts, timestamp ranges, duplicates, missing intervals, and per-asset alignment. Confirm lineage before treating them as project inputs.
4. Inspect funding file schemas, coverage, timestamp conventions, and missing intervals.
5. Inspect the signal-generation project/code and document exactly how the 15M signals were produced.
6. Only after dependency/reference checks, propose a keep/archive/delete classification. No deletion is approved by this checkpoint.

## Interpretation limits

This checkpoint records only what was visible in the user's terminal output. It does not certify full data integrity, signal correctness, repository completeness, or the correctness of past backtest results.
