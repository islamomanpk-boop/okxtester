# Archive provenance inventory review

Date: 2026-11-22
Branch: `price-action-v1`

## Inspection performed

Read-only listing of `~/okx_adaptive_bot/okx_research_project.zip` using `unzip -l`, filtered for likely downloader, API, source, provenance, manifest, metadata, README, log, history, instrument, exchange, and market filenames, plus source/config/documentation extensions.

No extraction or script execution occurred.

## Findings

The archive contains 211 entries, with 206,969,357 bytes of uncompressed content.

The filtered listing shows configuration files and project processing scripts, including `src/prepare_data.py`, indicator/regime scripts, validation and backtest scripts. It does not show an identifiable downloader/fetch script, API log, source manifest, provenance note, instrument metadata file, or README documenting the original 1-minute candle source.

This is a filename-based inventory conclusion only. A downloader or source reference could be embedded in an unfiltered file or shell history outside the archive; this inspection does not prove none ever existed.

## Current provenance assessment

The archive strongly links the five 1-minute CSVs to the adaptive-bot data-preparation workflow. The archive inventory does not independently establish where those candles were originally downloaded from or which exchange instrument identifiers they represent.

## Next step

Inspect existing shell-history files read-only for commands that may show how the five 1-minute CSVs were acquired or copied. Do not execute any historical command. Do not extract the archive. Experiments remain paused.
