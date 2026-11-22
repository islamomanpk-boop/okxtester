# Shell History Provenance Checkpoint — 2026-11-22

## Scope
Read-only inspection of the Termux user's standard shell history files for traces of the downloader or source of the five 1-minute CSV datasets.

## Command and result
Inspected the existence and sizes of:
- ~/.bash_history
- ~/.zsh_history
- ~/.history

Only ~/.bash_history existed (17 KB; listed modification time Nov 21, 2026 17:29 local).

Searched the existing history for these patterns:
- history-candles
- market/candles
- okx.com
- okx.*download
- download.*okx
- USDT_USDT_1m

Result: zero matching lines in ~/.bash_history.

## Interpretation
This search provides no additional evidence identifying the downloader or original data source. It does not establish that no download occurred: shell history can be incomplete, disabled, cleared, or recorded in another location/session.

## Current provenance assessment
- Confirmed: the adaptive-bot ZIP archive contains all five 1-minute CSV files (BTC, ETH, SOL, DOGE, AVAX) alongside the preparation script and derived timeframe data.
- Strongly supported: these five files were included in the adaptive-bot research workflow.
- Not confirmed: original exchange, API endpoint, exact instrument IDs, and volume units.
- Project configuration naming OKX USDT perpetuals is evidence of intended market, not independent proof of candle provenance.

## Safety and research status
No archive extraction, scripts, backtests, downloads, transformations, or data modifications were performed. Experiments remain paused. Continue provenance research read-only until explicitly authorized otherwise.
