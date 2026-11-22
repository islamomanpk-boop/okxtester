# Data Provenance Audit — Script and Lineage Findings

Date: 2026-11-22
Project: OKX Price Action Research V1
Branch: price-action-v1
Evidence: user-provided output from existing reports and source files; no scripts executed.

## 1. Historical 1-minute quality report

The report `reports/1m_data_quality_audit_2026-11-20.md` records:

| Asset | Rows | Duplicates | Missing | Invalid OHLCV |
|---|---:|---:|---:|---:|
| BTC | 569125 | 0 | 0 | 0 |
| ETH | 569125 | 0 | 0 | 0 |
| SOL | 569126 | 0 | 0 | 0 |
| DOGE | 569126 | 0 | 0 | 0 |
| AVAX | 569127 | 0 | 0 | 0 |

It reports start 2025-10-20 08:50 UTC and end times BTC/ETH 2026-11-19 14:14 UTC, SOL/DOGE 14:15 UTC, AVAX 14:16 UTC. It states no duplicate, missing, invalid, or out-of-order candles and explicitly says cross-asset synchronization still needs verification.

These are reported historical results. The report states its source was Termux audit output; it does not identify the candle downloader, API endpoint, OKX instrument IDs, candle timestamp convention, or volume unit.

## 2. Important path mismatch in audit script

The user-inspected `src/audit_price_action_v1_data.py` defines:

`BASE = Path.home() / "okx_adaptive_bot" / "data"`

It checks 1m, 15m, 4h, 1d files and indicator files under that directory. The five local 1m files actually inspected in the inventory are under:

`~/okx_scalping_data/`

Therefore this script does not directly audit the five inventory files unless an additional copy/path mapping is established. Do not cite its PASS output as validation of the files in `~/okx_scalping_data/`.

The script performs structural checks (columns, timestamp monotonicity/duplicates/interval, numeric OHLCV, positive prices, OHLC invariants, nonnegative volume). These checks do not establish exchange provenance or volume units.

## 3. Cross-asset alignment script has write side effects

The inspected `src/audit_cross_asset_alignment.py` reads the five `~/okx_scalping_data/*_USDT_USDT_1m.csv` files and calculates timestamp intersections, but it also writes:
- `~/okx_scalping_data/synchronized_5asset_1m.csv`
- `reports/cross_asset_timestamp_alignment.csv`
- `reports/cross_asset_timestamp_exceptions.csv`
- `reports/cross_asset_timestamp_alignment.md`

It creates the reports directory if absent and overwrites outputs with standard write calls. It is therefore not a read-only inspection script. Do not execute it during this preservation-first audit without explicit user approval and a safe output plan.

The script's logic uses exact timestamp intersection and no forward filling. It also flags unmatched timestamps inside the common range and gaps in the common timeline. Its status logic should be reviewed carefully before relying on its output.

## 4. What the exchange references show

The grep output found explicit OKX references in:
- `src/download_funding_archives.py`: constructs instruments as `{asset}-USDT-SWAP` and uses an OKX static historical funding archive URL.
- `src/merge_funding_history.py`: uses the OKX public funding-rate-history endpoint and checks `instId`.

These establish intended OKX identity for the funding workflow, not the 1m candle CSVs. The grep output did not reveal a candle downloader or OKX candle API endpoint in the inspected source/docs/reports.

The search output was truncated by `head` and ended with a broken-pipe message; absence of a candle downloader in that output is not proof that none exists elsewhere.

## 5. Git history limitation

The displayed history for the two audit scripts contains generic commit messages:
- `c68fa92 Update research code and reports`
- `e8e761c Update research code and reports`
- `b71f7e8 Update research code and reports`
- `95b95eb Update research code and reports`

These messages do not identify the candle source or downloader.

## 6. Current evidence classification

### Verified from displayed files/output
- Five local files exist at `~/okx_scalping_data/` with the displayed CSV header and sample rows.
- Historical report records the stated row counts and structural quality results.
- Price-action audit script uses a different base path (`~/okx_adaptive_bot/data`).
- Cross-asset script has output-writing side effects.
- Funding scripts explicitly refer to OKX USDT swap instruments and OKX funding sources.

### Reported, not independently re-verified
- All five candle datasets passed the historical individual quality audit.
- Previous cross-asset alignment was checked in an earlier project phase (but the displayed 2026-11-20 report says synchronization still needed verification, so the chronology/evidence must be reconciled).

### Unknown
- Exact candle data source and downloader/API endpoint.
- Exact exchange instrument IDs for candle files.
- Whether candles are OKX USDT swaps versus spot or another source.
- Timestamp semantics (candle open vs close) and API timezone convention.
- `vol` unit.
- Whether a prior alignment audit was subsequently completed and what its result was.

## 7. Next read-only inspection

Inspect:
- `reports/execution_data_audit.md`
- `reports/cross_asset_timestamp_alignment.md` if it exists
- `reports/cross_asset_timestamp_alignment.csv` if it exists
- `reports/cross_asset_timestamp_exceptions.csv` if it exists
- repository history for `src/audit_cross_asset_alignment.py` and the five-file path.

Do not execute `src/audit_cross_asset_alignment.py`. Do not run any backtest, data builder, downloader, signal generator, or other process. Preserve all existing outputs and the paused telemetry batch.
