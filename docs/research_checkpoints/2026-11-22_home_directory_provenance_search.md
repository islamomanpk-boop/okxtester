# Home Directory Provenance Search — 2026-11-22

## Purpose
Record a read-only inspection of the home-directory locations and shell history for clues about the five candle CSVs.

## Findings
- Relevant project directories present:
  - `~/okx_adaptive_bot`
  - `~/okx_scalp`
  - `~/okx_scalping_data`
  - `~/okx_scalping_reports`
  - `~/okxtester`
- The top level of `~/okx_scalping_data` contained no non-CSV files in the inspected listing. No adjacent metadata or downloader file was identified there.
- The inspected `~/.bash_history` had no matching lines for download, candle API endpoints, the data directory, or the BTC CSV filename.
- No `~/.zsh_history` result was shown.

## Interpretation and limits
The shell history and data-directory listing did not establish the candle source. Shell history may be incomplete, and the downloader may live in another project directory or may have been run from a different environment.

## Next safe step
Inspect filenames, source references, and Git history in `~/okx_scalp` and `~/okx_adaptive_bot` without running scripts. Do not inspect or expose credentials or API secrets if present.

## Safety state
No scripts, downloads, API calls, or data transformations were run. No files were modified. Backtests remain paused.
