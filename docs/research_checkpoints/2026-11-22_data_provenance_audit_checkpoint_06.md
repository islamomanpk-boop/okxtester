# Data Provenance and Reliability Audit — Checkpoint 06

Date: 2026-11-22
Project: OKX Price Action Research V1
Branch: price-action-v1
Status: audit plan agreed; local evidence not yet re-verified in this checkpoint.

## Purpose

Before computing descriptive BTC, ETH, SOL, DOGE and AVAX behaviour statistics, establish that the local files are the intended OKX perpetual instruments and that their timestamps, OHLCV fields, coverage and preparation history are understood.

This is a read-only audit. It does not authorize backtests, signal generation, data transformation, report regeneration, or restarting the paused 66-experiment telemetry batch.

## Known local file inventory (reported in prior session; not re-verified here)

Directory: `~/okx_scalping_data/`

- `BTC_USDT_USDT_1m.csv`
- `ETH_USDT_USDT_1m.csv`
- `SOL_USDT_USDT_1m.csv`
- `DOGE_USDT_USDT_1m.csv`
- `AVAX_USDT_USDT_1m.csv`

Previously reported columns: `ts,open,high,low,close,vol`.
Previously reported first timestamp: `1760950200000` for all five.
Previously reported last timestamps:
- BTC and ETH: `1795097640000`
- SOL and DOGE: `1795097700000`
- AVAX: `1795097760000`

These values are inventory clues only. They do not establish the exchange, market type, contract identity, timezone semantics, volume units, or whether the files are the exact intended inputs for this research project.

Prior individual one-minute quality audits were reported as passing duplicate, missing-interval, OHLCV validity and timestamp checks. Cross-coin alignment was also previously checked. Preserve those results as historical audit claims until the scripts, outputs and source lineage are reviewed.

## Audit questions

### 1. Instrument identity
- Confirm exchange is OKX.
- Confirm each market is the intended USDT-margined perpetual swap, not spot or a different contract.
- Record exact OKX instrument identifiers, such as the exchange's instrument ID, where available.
- Confirm whether contract specifications or symbol conventions changed during the sample.

### 2. Source and lineage
- Identify downloader/API endpoint or export source.
- Record retrieval date, pagination method, and any retry/backfill process.
- Identify scripts and repository revisions that produced or modified the CSVs.
- Determine whether the files came from another project directory and whether that affects their suitability for this project.
- Do not infer provenance from filenames alone.

### 3. Time semantics and coverage
- Confirm `ts` unit (expected milliseconds only if verified) and whether it represents candle open time.
- Confirm UTC interpretation and exact 1-minute candle boundaries.
- Record first/last candle, row count, expected interval count, and common complete sample across all five assets.
- Identify partial first/last days and weeks; exclude incomplete calendar periods from daily/weekly comparisons where required.
- Confirm alignment using timestamp keys, not row positions.

### 4. OHLCV schema and units
- Verify OHLC price units and numeric parsing.
- Verify whether `vol` means base-asset volume, quote volume, contracts, or another unit.
- Confirm candle aggregation conventions and OHLC invariants.
- Confirm treatment of zero-volume candles and any exchange-specific missing-candle behaviour.

### 5. Related data dependencies
- Identify funding-rate source, instrument mapping, timestamps, units and coverage before using funding in any future execution-cost analysis.
- Identify provenance and generation code for 15-minute signals under `~/okx_adaptive_bot/reports/price_action_signals/`; do not assume they were generated from these exact five files.
- Keep funding and signal lineage separate from the 1-minute OHLCV audit.

## Evidence classification

Every finding must be labelled:
- **Verified:** supported by source metadata, code, API/export records or reproducible read-only checks.
- **Reported, not re-verified:** stated in prior project notes but evidence has not yet been inspected.
- **Unknown:** no adequate evidence yet.

Do not silently upgrade a reported claim to verified.

## Safe audit sequence

1. Inspect file names, sizes, headers and a few sample rows only.
2. Inspect existing downloader/audit scripts and their Git history.
3. Inspect existing audit outputs without regenerating them.
4. Verify instrument IDs and API source using recorded metadata or existing downloader configuration.
5. Reconcile timestamps, coverage and common sample.
6. Record unresolved questions and only then decide whether the data is fit for descriptive analysis.

No files are to be deleted, overwritten, moved, normalized, or re-exported during this audit. Preserve untracked reports and telemetry outputs. Do not use `git clean`, `git reset --hard`, or broad ignore rules as part of this work.

## Gate before empirical descriptive analysis

Daily/weekly movement calculations and other five-coin descriptive statistics may begin only after:
- instrument identity and market type are verified;
- timestamp unit and candle-time semantics are verified;
- OHLCV schema and volume units are documented;
- common coverage and alignment are reconciled;
- data limitations are written down.

This gate applies to descriptive calculations as well as strategy testing. No backtest is authorized by completion of this audit.

## Next user-assisted action

When ready, perform a read-only inventory in Termux: list the five CSV file sizes, print their headers and first/last two rows, and inspect the existing downloader/audit script names. Do not launch any Python research or backtest runner yet.