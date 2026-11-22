# Telemetry Batch Checkpoint — 2026-11-22

## Observed state

The local telemetry manifest at `reports/exit_experiments_telemetry_v1/exit_experiment_batch_manifest.csv` contains 66 experiment rows.

- 2 experiments are marked `completed`:
  - `fixed_stop_0_50pct__fixed_target_0_75pct`
  - `fixed_stop_0_50pct__fixed_target_1_00pct`
- 1 experiment is marked `running`:
  - `fixed_stop_0_50pct__fixed_target_1_50pct`
- The remaining 63 rows are marked `pending`.
- The batch log ends immediately after the batch 3 heading. This is consistent with an interrupted run, but the manifest status alone does not prove a process is currently running.
- The two completed experiments each have trade, summary, metrics, daily/monthly return, exit-reason, and performance-report outputs. The trade CSVs are approximately 2.18 MB and 1.82 MB respectively.
- The telemetry comparison CSV is non-empty (999 bytes); it should be inspected before relying on its contents.
- No restart or cleanup is authorized by this checkpoint.

## Git working-tree state observed

- 97 tracked files were reported in the repository.
- `git status --short` summary: 2 modified tracked entries, 729 untracked entries, 0 deleted entries.
- `git diff --stat` showed changes to:
  - `reports/exit_experiments/fixed_stop_0_50pct__fixed_target_0_75pct_summary.csv`
  - `reports/exit_experiments/fixed_stop_0_50pct__fixed_target_0_75pct_trades.csv`
- The tracked trade CSV diff is large (11,954 changed lines; 5,979 insertions and 5,979 deletions). The cause has not yet been established.
- Untracked content includes generated experiment reports, cost-sensitivity outputs, telemetry outputs, and `src/portfolio_backtester.py.backup`.
- No files were deleted. No files were staged or committed as part of this checkpoint.

## Next safe actions

1. Verify whether a batch process is running with `pgrep -af run_exit_experiment_batch`.
2. Count manifest statuses and inspect the third experiment's output presence.
3. Inspect telemetry CSV headers and the comparison CSV.
4. Inspect the two tracked report diffs to determine why they changed.
5. Classify untracked files into source, concise research evidence, reproducible generated outputs, temporary files, and backups before deciding what to commit or ignore.
6. Do not run `git clean`, `git reset --hard`, mass deletion, or restart all 66 experiments without an explicit decision.

## Research integrity note

The telemetry rerun was introduced because the original trade records did not preserve sufficient trailing-exit activation/path telemetry. The partial rerun must remain isolated under `reports/exit_experiments_telemetry_v1/`; original reports under `reports/exit_experiments/` must be preserved and any changes to tracked originals investigated before further execution.
