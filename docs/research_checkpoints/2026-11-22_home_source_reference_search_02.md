# 2026-11-22 Home Source Reference Search — 1m Candle Provenance

## Status
Read-only source search completed. The original source of the five 1-minute candle CSV files remains unverified. No scripts were executed and no data files were changed.

## Search performed
A recursive grep searched Python, shell, Markdown, and JSON files under:
- `~/okx_adaptive_bot`
- `~/okxtester`
- `~/okx_scalp`

The first search looked for:
- `okx_scalping_data`
- The five exact 1-minute CSV filenames (BTC, ETH, SOL, DOGE, AVAX)

The second search looked for OKX candle endpoint patterns:
- `history-candles`
- `market/candles`
- `api/v5/market`

Both searches excluded Git metadata and Python cache directories and displayed up to 180 matches.

## Findings

### References to the five-file data directory
Matches under `~/okxtester` were:
- `src/audit_cross_asset_alignment.py`
- `src/execution_data_audit.py`
- `src/backtest_input_preflight.py`
- `src/run_exit_experiments.py`
- Funding archive/merge scripts referencing only the funding subdirectory
- Existing reports/docs describing the files and synchronized dataset

These are consumer, audit, preflight, experiment, or documentation references. The search did not find a candle downloader that writes the five 1-minute CSVs.

### OKX candle endpoint references
The only match was:
- `~/okx_scalp/1_fetch.py` at its `/api/v5/market/history-candles` endpoint.

Prior read-only inspection established that this script requests `BAR = "15m"`, checks OKX SWAP instruments, and writes compressed files under `~/okx_scalp/data/`. It is therefore evidence for a separate 15-minute workflow, not evidence that it created the five 1-minute files under `~/okx_scalping_data/`.

### Direct conclusion
The five 1-minute files are consumed by the Price Action research tooling, but their original downloader, exact OKX instrument identifiers, API response provenance, and volume units are not established by the searched source files.

Absence of a match in these three directories does not prove that no downloader exists elsewhere. It only means this search did not locate one.

## Research controls
- No backtest, experiment, downloader, audit script, or data transformation was run.
- No dataset or report was modified locally.
- The experiment pause remains in force.
- Do not label the five files as verified OKX USDT-SWAP data until a source-to-file link or equivalent independent provenance evidence is found.

## Next read-only investigation
If provenance work continues, inspect `~/okx_scalping_reports` and any remaining source/configuration/log files outside the three searched trees for references to the five-file directory, exact filenames, 1-minute bars, and OKX candle endpoints. Do not execute discovered scripts.
