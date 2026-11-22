# Data Provenance Audit — Inventory Findings

Date: 2026-11-22
Project: OKX Price Action Research V1
Branch: price-action-v1
Evidence status: user-provided read-only Termux inventory output.

## Observed local files

All five expected CSV files exist under `~/okx_scalping_data/`:

- `BTC_USDT_USDT_1m.csv` — reported size 30M; filesystem modification Nov 19 18:15.
- `ETH_USDT_USDT_1m.csv` — reported size 30M; filesystem modification Nov 19 18:16.
- `SOL_USDT_USDT_1m.csv` — reported size 26M; filesystem modification Nov 19 18:16.
- `DOGE_USDT_USDT_1m.csv` — reported size 30M; filesystem modification Nov 19 18:17.
- `AVAX_USDT_USDT_1m.csv` — reported size 25M; filesystem modification Nov 19 18:17.

All headers are identical: `ts,open,high,low,close,vol`.

The first two displayed rows for each file show timestamps separated by 60,000 milliseconds. All five displayed first timestamps are `1760950200000`.

Displayed final timestamps:
- BTC: `1795097640000`
- ETH: `1795097640000`
- SOL: `1795097700000`
- DOGE: `1795097700000`
- AVAX: `1795097760000`

Thus the displayed final timestamps differ by at most 120,000 milliseconds (two minutes). This is not by itself proof of missing data; exact row counts, interval checks and common coverage need to be reconciled from existing audit evidence.

## What this inventory supports

- All five expected local files exist.
- Their CSV headers match.
- The sample timestamps appear to use millisecond-scale epoch values and the displayed adjacent rows are one minute apart.
- Their displayed start timestamps match.
- Their displayed end timestamps are not identical.
- File modification times are Nov 19 (year inferred from current project date; filesystem output did not print year).

## What it does not prove

- Exchange or instrument identity (OKX vs another source; swap vs spot).
- Exact instrument IDs or contract specifications.
- Whether timestamps are candle-open times and UTC.
- Meaning or unit of `vol`.
- Downloader/API provenance, pagination, backfill or data transformation history.
- Full row counts, exact coverage, completeness, or common sample.

Do not infer the market type from the filename pattern `*_USDT_USDT_1m.csv`.

## Existing audit and source files located

The read-only `find` inventory located:
- `src/audit_cross_asset_alignment.py`
- `src/audit_price_action_v1_data.py`
- `src/execution_data_audit.py`
- `src/signal_quality_audit.py`
- `src/download_funding_archives.py`
- `reports/1m_data_quality_audit_2026-11-20.md`
- `reports/execution_data_audit.md`
- `reports/funding_data_audit.md`
- `reports/signal_dataset_audit.md`
- `reports/signal_quality_audit.md`
- `docs/execution_data_audit_v1.md`
- `docs/signal_quality_audit_v1.md`

The `find` command did not locate an obvious price-candle downloader by filename. This does not prove no downloader exists; it may have a different name or reside outside the searched depth/directories.

## Next read-only step

Inspect the existing data-quality report, execution-data documentation, audit scripts and repository history to find source assumptions and prior evidence. Do not execute these scripts yet. Do not modify, move, delete, or regenerate any data or reports. The telemetry batch remains paused.
