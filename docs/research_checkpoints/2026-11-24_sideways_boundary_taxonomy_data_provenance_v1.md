# Sideways Boundary Interaction Taxonomy V1 — Data Provenance Checkpoint

Date: 2026-11-24
Branch: price-action-v1

## Selected source

Directory:

`~/okx_adaptive_bot/data/`

Files:

- BTC_USDT_15m.csv
- ETH_USDT_15m.csv
- SOL_USDT_15m.csv
- DOGE_USDT_15m.csv
- AVAX_USDT_15m.csv

This is also the default `--data-dir` in the accepted historical boundary reconstruction script.

## Source file integrity

SHA-256 hashes observed during the read-only inspection:

| Asset | SHA-256 | Data rows |
|---|---|---:|
| BTC | 0721a4a25a61f1917be4f9952514096c641fbec64e7ae0d50c7cf1c3ebfe9658 | 37941 |
| ETH | 7195e45315c360e9f1fdd37746125968359bce8632a0bfe51628f104792fdc04 | 37941 |
| SOL | 5b34cbb006497ecd7ebe0cfa67b25b4230cb769d6362d278991171a8f6da2d33 | 37941 |
| DOGE | 3418c81fa16b531eee5de90d8b0ff6a5543db54357cb5572358ff31ab6627b5f | 37941 |
| AVAX | 75ef1a545686217a6d4ca55385690095c6e2a494438b7f4e38352d5ca35de493 | 37941 |

Each CSV contains one header row plus 37,941 data rows.

## Backup comparison

Compared against:

`~/okx_adaptive_bot/backups/pre_boundary_fix_20261120_063657/`

Results:

- BTC: all shared rows identical; current source contains one additional final candle.
- ETH: all shared rows identical; current source contains one additional final candle.
- SOL: all rows identical; SHA-256 hashes match.
- DOGE: all rows identical; SHA-256 hashes match.
- AVAX: all rows identical; SHA-256 hashes match.

The additional BTC and ETH candle has timestamp:

`1795096800000`

No differences were found in any shared CSV rows.

## Historical reconstruction consistency

The accepted historical boundary reconstruction integrity checkpoint dated 2026-11-23 records:

- 37,941 source 15-minute rows per asset.
- 2,358 detector feature rows per asset.
- Zero global 15-minute timestamp gaps.
- Zero 15-minute gaps inside processed snapshot intervals.

The current source files match the recorded 15-minute row count.

The reconstruction script's default data directory is the selected source directory.

## GitHub availability

The raw 15-minute candle CSVs are not stored in the inspected GitHub repository branch.

The detector feature files, reconstruction code, historical reports, and research documentation are stored in the repository.

## Provenance limitations

This checkpoint establishes:

- The exact local source-file hashes observed during inspection.
- Agreement between current and backup files across all shared rows.
- Consistency of current source row counts with the accepted reconstruction audit.
- The reason for selecting the current data directory rather than the older backup.

It does not independently establish the original exchange download method, API endpoint, or complete upstream data lineage.

The hashes must be rechecked immediately before the new study is run. This checkpoint records observed values, not a guarantee that the files cannot change later.

## Research handling

- Do not modify the original 15-minute source files.
- Do not overwrite the historical reconstruction script or reports.
- The new boundary interaction taxonomy must use a separate implementation and output directory.
- Any changed source hash or unexpected row-count difference must stop the run pending investigation.

