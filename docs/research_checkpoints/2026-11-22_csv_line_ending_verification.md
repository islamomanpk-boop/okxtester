# CSV Line-Ending Verification — 2026-11-22

## Files checked

Two locally modified tracked files were compared byte-for-byte against their committed `HEAD` versions after normalizing CRLF (`\r\n`) to LF (`\n`).

| File | Current bytes | Committed bytes | Current CRLF | Committed CRLF | Same after normalization |
|---|---:|---:|---:|---:|---|
| `reports/exit_experiments/fixed_stop_0_50pct__fixed_target_0_75pct_summary.csv` | 655 | 653 | 2 | 0 | Yes |
| `reports/exit_experiments/fixed_stop_0_50pct__fixed_target_0_75pct_trades.csv` | 1,658,985 | 1,653,008 | 5,977 | 0 | Yes |

Both files have the same number of LF characters in current and committed copies. The extra bytes are exactly consistent with CRLF line endings replacing LF line endings. The normalized content comparison returned `True` for both files.

## Conclusion

These two tracked-file modifications are line-ending-only changes. No differences in CSV field values or records were detected by the normalization comparison. The committed versions remain the canonical versions.

## Safe cleanup option

Because the normalized contents were verified identical, the two local formatting-only changes can be discarded with a narrowly scoped restore:

```bash
git restore -- reports/exit_experiments/fixed_stop_0_50pct__fixed_target_0_75pct_summary.csv reports/exit_experiments/fixed_stop_0_50pct__fixed_target_0_75pct_trades.csv
```

This command affects only those two named tracked files. It does not delete untracked reports, telemetry outputs, or the backup file. Do not use a broad reset or clean command.

## Next research priority

Continue investigating the completed telemetry runs, especially position notional, turnover, fee calculation, and trade-level telemetry timing. Keep the original experiment evidence and the separate telemetry output directory isolated.
