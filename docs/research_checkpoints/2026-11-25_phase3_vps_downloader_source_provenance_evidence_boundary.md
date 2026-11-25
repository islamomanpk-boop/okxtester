# Phase 3 VPS Downloader Source and Instrument/Volume Provenance — Evidence Boundary

**Date:** 2026-11-25  
**Status:** PARTIAL INVENTORY ONLY — SOURCE IMPLEMENTATION NOT REVIEWED  
**Gate:** Gate 0 source provenance remains OPEN; Gate 0 remains CONDITIONAL HOLD.

## Purpose

Follow up the historical 1M identity finding by determining whether the current VPS downloader's actual source code and instrument/volume mapping can be independently reviewed from the connected GitHub evidence surface.

## Evidence available from the latest read-only VPS inventory

Workflow: `okxtester_private` run `45648774228`  
Job: `139327152757`  
Result: completed successfully.

The job log reports:

- VPS project root: `$HOME/okx_market_data_v1`.
- SQLite database: `$HOME/okx_market_data_v1/raw/okx_swap_1m.sqlite3`.
- Candidate project file: `download_okx.py`, 7,421 bytes.
- Five project CSV candidates: BTC, ETH, DOGE, AVAX and SOL 1-minute files, each approximately 37–45 MB.
- SQLite table `candles` with 2,890,411 rows and columns:
  `inst_id, ts, open, high, low, close, vol, vol_ccy, vol_ccy_quote, confirm`.
- SQLite `quick_check`: `ok`.
- The audit reported no candidate evidence in its six searched Gate 0 categories, including source provenance and execution engine. This is an inventory classification, not proof that the downloader source contains no relevant logic.

The private repository's tracked workflow definitions also reveal the configured operational paths and conventions:

- The monitor checks for process name `download_okx.py` and reads `$HOME/okx_market_data_v1/reports/download.log`.
- The aligned-dataset workflow reads the SQLite database in read-only mode, selects confirmed candles (`confirm=1)), and retrieves `inst_id, ts, open, high, low, close, vol`.
- The final audit also uses `inst_id` and `confirm=1` to assess five-coin timestamp coverage.
- The workflows do not contain the downloader's acquisition implementation.

## What is not established

The connected evidence currently provides the downloader's filename and size, but not its source contents. The downloader implementation is not tracked in the inspected private repository tree, and no source-code copy or immutable hash of `download_okx.py` was available in the reviewed GitHub records.

Therefore the following remain unverified:

1. Exact OKX REST endpoint(s), request parameters, pagination and retry behavior.
2. Whether `inst_id` is populated directly from the requested OKX swap instrument IDs and whether any aliases or symbol transformations occur.
3. Meaning and conversion of `vol`, `vol_ccy` and `vol_ccy_quote`; in particular, which field is the intended base/contract/quote volume for each instrument.
4. Whether only confirmed candles are persisted, how unconfirmed candles are updated, and how duplicates or corrections are handled.
5. UTC timestamp unit and candle-open versus candle-close timestamp semantics in the downloader's write path.
6. Acquisition time, original response provenance, and whether the five project CSV files are byte-identical to the canonical Git 1M files.
7. A source hash tying the inspected VPS downloader to a reviewed, version-controlled implementation.

The database schema and downstream query usage do not prove how values were acquired or populated. No volume-unit interpretation should be inferred from column names alone.

## Safe next verification

A future read-only VPS inspection should retrieve and report only:

- SHA-256 and file metadata for `download_okx.py`;
- source text or a separately secured review copy, without printing credentials or API secrets;
- exact endpoint, instrument ID, timestamp, confirmation and volume-field mapping;
- schema and write/upsert logic;
- downloader version/commit or an immutable source snapshot hash.

Any inspection must avoid modifying the downloader, database, raw CSVs, service state or VPS configuration. Do not expose API keys, tokens, credentials or private notification topics in the report.

## Gate disposition

- VPS downloader file existence and size: **OBSERVED** in read-only inventory.
- Database table schema and row count: **OBSERVED** in read-only inventory.
- Operational path and downstream confirmed-candle selection: **OBSERVED** in tracked workflow definitions.
- Downloader source implementation and instrument/volume semantics: **NOT REVIEWED / UNVERIFIED**.
- Canonical Git 1M to historical Termux 1M byte identity: **UNVERIFIABLE** on current evidence.
- Gate 0: **CONDITIONAL HOLD**.
- Candidate generation, Gate 2 execution-resolution comparison and strategy PnL backtests remain unauthorized.

No VPS files, database rows, raw CSVs or services were modified by this review.


## Follow-up — downloader and volume semantics now reviewed (2026-11-25)

This section supersedes the earlier statements above that the downloader implementation and volume-unit semantics had not been reviewed.

The VPS downloader source was fingerprinted and statically inspected; its exact instrument construction is `{asset}-USDT-SWAP` for BTC, ETH, SOL, DOGE, and AVAX. It maps OKX candle response positions 5, 6, and 7 to database fields `vol`, `vol_ccy`, and `vol_ccy_quote`, respectively. The exact SQLite conflict/update clause and confirmed-only CSV export projection/filter were subsequently established in [the SQL/export semantics checkpoint](2026-11-25_phase3_vps_downloader_sql_export_update_semantics_v1.md).

The official OKX V5 schema defines derivative `vol` as contract quantity, `volCcy` as base-currency quantity, and `volCcyQuote` as quote-currency quantity. Exact Decimal comparison of all overlapping rows established that canonical Git `vol` equals VPS `volCcy` across all five assets. See [canonical/VPS OHLCV reconciliation](2026-11-25_phase3_vps_canonical_ohlcv_reconciliation_v1.md) and the updated `docs/execution_data_audit_v1.md`.

Still unverified: original Termux 1M input byte identity because no contemporaneous hashes were recorded; complete historical acquisition/refresh lineage; and why OKX currently labels the old SOL 2026-08-28 08:30 UTC candle `confirm=0`. The VPS SQLite database is mutable, not an immutable acquisition ledger. These findings do not close all Gate 0 source provenance or authorize backtesting.
