# Adaptive-bot archive confirms five 1-minute input files

Date: 2026-11-22
Repository branch: `price-action-v1`

## Scope and safety

This was a read-only inspection. The archive was listed with `unzip -l`; it was not extracted, and no scripts were executed. Backtests and experiments remain paused.

## Evidence observed

Archive:
`~/okx_adaptive_bot/okx_research_project.zip`

Reported size: 62 MB.
Archive listing records these five original 1-minute files:

| Asset | Archive path | Uncompressed bytes |
|---|---|---:|
| BTC | `data/BTC_USDT_USDT_1m.csv` | 30,787,707 |
| ETH | `data/ETH_USDT_USDT_1m.csv` | 30,568,239 |
| SOL | `data/SOL_USDT_USDT_1m.csv` | 26,848,394 |
| DOGE | `data/DOGE_USDT_USDT_1m.csv` | 31,378,267 |
| AVAX | `data/AVAX_USDT_USDT_1m.csv` | 25,858,552 |

The archive also contains:
- `config.json`
- `src/prepare_data.py`
- derived 15m, 4h and 1d CSVs for all five assets
- indicator files and regime reports.

The archived 1-minute file sizes closely match the five files previously inventoried in `~/okx_scalping_data/`. The archive listing gives source-file timestamps on 2026-11-19 around 18:15–18:17, matching the previously recorded local file modification times.

The adaptive-bot preparation script inspected earlier expects the exact five 1-minute filenames in its `data/` directory, validates OHLCV/timestamps and resamples them to 15m, 4h and 1d. The archive contains both those expected inputs and the corresponding derived timeframes.

## Assessment

**Strongly supported:** The adaptive-bot archive contains the five original 1-minute CSV inputs, alongside the preparation script and derived timeframe datasets. This establishes a strong link between these five files and the adaptive-bot data-preparation workflow.

**Strongly supported but not byte-verified:** The archived source-file sizes and recorded timestamps closely match the five files previously inspected in `~/okx_scalping_data/`.

**Not yet established:** The archive does not prove the original exchange/API endpoint, the exact OKX instrument identifiers, contract metadata, volume units, or whether every candle was sourced from OKX. The config's declared exchange/market is intended configuration, not independent source provenance.

## Next read-only investigation

Inspect the archive's remaining file listing for downloader scripts, source notes, logs, manifests, metadata, or API response records. Do not extract or execute archive contents. If no downloader or source metadata is present, continue searching the existing local project files for the process that created the five 1-minute files.

## Operational status

All backtests and experiments remain paused. No files were extracted or modified during this inspection.
