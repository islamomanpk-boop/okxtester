# Telemetry batch checkpoint — 2026-11-22

## Scope
Checkpoint of the local telemetry-instrumented 66-experiment batch in `reports/exit_experiments_telemetry_v1/`. This is separate from the earlier original outputs in `reports/exit_experiments/`.

## Manifest status observed
The local `exit_experiment_batch_manifest.csv` contains 66 experiment rows:
- 2 marked `completed`
- 1 marked `running`
- 63 marked `pending`
- 0 rows with an error recorded

The two completed experiments are:
1. `fixed_stop_0_50pct__fixed_target_0_75pct`
2. `fixed_stop_0_50pct__fixed_target_1_00pct`

Trade CSVs were present for those two experiments (approximately 2.18 MB and 1.82 MB respectively).

The third row, `fixed_stop_0_50pct__fixed_target_1_50pct`, is marked `running` with no completion timestamp. A previous process check reported no `run_exit_experiment_batch` process running. Therefore this manifest status is likely stale after interruption, but its output files and log must be checked before deciding whether to resume or rerun it.

## Git state observed
- `git diff --name-only` returned no modified tracked files at this checkpoint.
- Generated experiment reports, including `reports/exit_experiments_telemetry_v1/`, are untracked locally and are not yet confirmed saved in GitHub.
- `.gitignore` currently excludes Python cache files, zip files, data/backups/logs directories, selected config files, environment files, and key files. It does not exclude generated report directories.
- A local `src/portfolio_backtester.py.backup` was observed; do not commit it as source without a specific reason.

## Handling decision
No files have been deleted, moved, reset, or committed as part of this checkpoint. Do not use destructive cleanup commands. Preserve raw trade-level outputs locally until the experiment state and evidence are audited. Save concise research findings, methodology, and reproducible code/tests in GitHub; decide separately how to archive large raw CSVs.

## Next audit
1. Check whether a batch process is currently running.
2. Inspect the third experiment's output files, sizes, and log tail to determine whether it completed partially or needs rerunning.
3. Reconcile manifest status with actual complete output sets.
4. Only then decide whether to resume the batch; do not automatically rerun all 66 experiments.
5. Review report retention and ignore policy before any Git staging.
