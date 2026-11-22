# Five-Asset Timestamp Alignment Review — 2026-11-22

## Purpose
Record the review of the existing execution-data and cross-asset alignment reports for BTC, ETH, SOL, DOGE, and AVAX. This was a read-only review. No scripts were run and no local data or reports were modified.

## Evidence reviewed
- `reports/execution_data_audit.md`
- `reports/cross_asset_timestamp_alignment.md`
- `reports/cross_asset_timestamp_alignment.csv`
- `reports/cross_asset_timestamp_exceptions.csv`
- Existence and size of `~/okx_scalping_data/synchronized_5asset_1m.csv`
- Git history for `src/audit_cross_asset_alignment.py`

## Reported results
The existing alignment report states `PASS_WITH_TRAILING_DIFFERENCES`:
- Five assets: BTC, ETH, SOL, DOGE, AVAX.
- Union timestamps: 569,127.
- Exact timestamps common to all five: 569,125.
- Synchronized dataset rows: 569,125.
- No duplicates, out-of-order timestamps, or unexpected intervals for any asset.
- Common window: 2025-10-20 08:50 UTC through 2026-11-19 14:14 UTC.
- The report states that only exact common timestamps were retained; no forward filling or fabricated candles were used.
- Existing synchronized file is approximately 109 MB.

Trailing-only exceptions:
- 2026-11-19 14:15 UTC: BTC and ETH absent; SOL and DOGE have this timestamp.
- 2026-11-19 14:16 UTC: BTC, ETH, SOL, and DOGE absent; AVAX has this timestamp.
- Per-asset CSV reports BTC and ETH each have 2 timestamps not common to all five; SOL and DOGE each have 1; AVAX has 0.

The execution audit independently reports the same per-asset row counts and endpoints, with zero unexpected intervals.

## Interpretation
The existing evidence supports timestamp alignment over the exact common five-asset window. The small row-count differences are confined to trailing timestamps and do not create interior gaps according to the reports. For any future five-asset comparison, the 569,125-row common window is the defensible shared sample, provided the synchronized file itself is later validated against the originals before use.

## Important limitations still open
1. Timestamp alignment does not prove candle provenance. The source/API, exchange identity, instrument IDs, and contract type for the five candle files remain unverified.
2. The `vol` column's unit and meaning remain unverified.
3. Funding files were not found in the local data directory. Funding must not be silently treated as zero.
4. Structural and alignment checks do not establish strategy profitability, realistic fills, or data correctness beyond the checks described.
5. The synchronized file's existence and size were observed, but this review did not compare its contents byte-for-byte or row-by-row with the original source CSVs.

## Safety / execution decision
- Backtests and batch experiments remain paused.
- No alignment script was rerun. The inspected script writes output files, so it is not an appropriate read-only verification method.
- No local files were changed, deleted, or overwritten.

## Next research priorities
1. Establish candle provenance and exact instrument identity from downloader/source records, metadata, or exchange API evidence.
2. Determine the volume unit.
3. Locate and validate historical funding data for the exact instruments and dates.
4. If later authorized, design a strictly read-only independent comparison of the synchronized dataset against the five originals, writing no files.
5. Only after provenance and cost data are resolved should the project decide whether the datasets are suitable for the planned backtests.
