# Telemetry Findings Checkpoint — 2026-11-22

## Batch process and manifest

A read-only inspection confirmed:

- No `run_exit_experiment_batch` process was running.
- The telemetry manifest has 66 rows: 2 `completed`, 1 `running`, and 63 `pending`.
- The row marked `running` is `fixed_stop_0_50pct__fixed_target_1_50pct`, but no output files exist for that experiment and the batch log ends at its batch heading. Treat this as a stale manifest state, not evidence of an active run.
- Do not restart the batch or edit the manifest until the next diagnostic decision is made.

## Completed telemetry experiments

Both completed runs used the fixed 0.50% stop, no trailing mode, five assets, initial portfolio equity $1,000, taker fee 0.05% per side, and slippage 2 bps per side. Their comparison rows report the same candidate count (17,943) and execution window (2025-10-20 08:50 UTC to 2026-11-19 14:14 UTC).

| Metric | 0.75% target | 1.00% target |
|---|---:|---:|
| Trades | 5,976 | 5,026 |
| Accepted entries | 5,976 | 5,026 |
| Rejected entries | 11,967 | 12,917 |
| Final equity | $24.2414 | $40.8501 |
| Net P&L | -$975.7586 | -$959.1499 |
| Return | -97.5759% | -95.9150% |
| Maximum drawdown | 97.6267% | 96.0483% |
| Gross P&L | -$20.99997 | -$74.1272 |
| Fees | $955.9003 | $886.3915 |
| Funding P&L | +$1.1417 | +$1.3688 |

## Interpretation and limits

- Both configurations performed extremely poorly under the tested execution and cost assumptions.
- Fees account for most of the reported net loss in these two runs. This makes trade frequency, turnover, position sizing/notional, and fee/slippage accounting high-priority audit topics.
- The two results do not establish that all strategy configurations fail; only two of 66 telemetry experiments completed.
- Do not infer that telemetry instrumentation itself is validated by these portfolio outcomes. Its event fields and causal timing still need targeted tests and trade-level audits.
- Do not select a strategy or make live-trading decisions from these partial results.

## Tracked CSV line-ending observation

The diff of the tracked baseline summary CSV shows identical visible field values but `^M` characters at the new line endings. This is consistent with a CRLF-versus-LF line-ending conversion. The tracked trades CSV also appears modified, but its diff and line-ending characteristics have not yet been inspected. Do not restore or overwrite either tracked file until that is verified.

## Next actions

1. Verify line-ending counts for both modified tracked CSVs and compare their content with the committed versions.
2. If the only change is line endings, preserve the committed originals and avoid committing a formatting-only diff.
3. Audit trade sizing/notional and calculate actual fee burden per trade and per unit of traded notional for these two completed runs.
4. Inspect telemetry fields in a sample of trade rows and verify activation/update timestamps obey the next-1-minute-candle execution rule.
5. Decide whether a targeted subset of further telemetry runs is needed. Do not automatically resume all 66 experiments.
