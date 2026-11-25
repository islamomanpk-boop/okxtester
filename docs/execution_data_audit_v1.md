# Execution Data Audit V1

## Purpose

Validate the local one-minute OHLCV data used by the price-action
backtester and document whether historical funding data is available.

## Inputs

Five local files under `~/okx_scalping_data/`:

- BTC_USDT_USDT_1m.csv
- ETH_USDT_USDT_1m.csv
- SOL_USDT_USDT_1m.csv
- DOGE_USDT_USDT_1m.csv
- AVAX_USDT_USDT_1m.csv

Expected columns: ts, open, high, low, close, vol.

## Checks

- Required columns and nonempty datasets.
- Valid integer millisecond timestamps.
- Duplicate and chronological timestamp checks.
- One-minute interval continuity.
- Numeric and positive OHLC prices.
- Valid OHLC candle structure.
- Non-negative volume.

## Funding limitation

Funding data is audited separately. Missing funding history must not be
silently interpreted as zero funding. A fully cost-adjusted perpetual
swap backtest requires validated historical funding records.

## Output

`reports/execution_data_audit.md`

Raw market data remains local and is not committed to Git.


## Repository provenance correction — 2026-11-25

The original input section above describes the earlier local execution-data audit snapshot. It is not an accurate description of the current canonical repository storage. The current `price-action-v1` tree tracks five 1-minute CSV source files under `data/market_1m/`; they are not merely local-only files. This correction supersedes the final sentence above for the current repository snapshot.

The five tracked source files are pinned in the Module B V1.1 run metadata at `reports/phase3_breakout_lifecycle_v1_1/run_metadata_v1_1.json`. At canonical branch head `d7502306e89b0b78980eb9e3c8a39570b3b05966`, the paths, byte sizes, Git blob IDs and SHA-256 values are:

| Instrument | Tracked path | Bytes | Git blob SHA-1 | File SHA-256 |
|---|---|---:|---|---|
| BTC-USDT-SWAP | `data/market_1m/BTC_USDT_USDT_1m.csv` | 30,787,707 | `639f7b8a6d54747dd3eb3370dc133d53f6382bfd` | `3afab3d60387c87fc4b96f54911538fea6bbb7682b2e18001537bc4359da6633` |
| ETH-USDT-SWAP | `data/market_1m/ETH_USDT_USDT_1m.csv` | 30,568,239 | `3017d870fe1cb764e1acb8fdec04138592749d69` | `8a2924bcb23bd5963cd1c46b8871475ff7ff4a3c8d8bed6325dbd406ec0552d2` |
| SOL-USDT-SWAP | `data/market_1m/SOL_USDT_USDT_1m.csv` | 26,848,394 | `a850c2dc4a2c14b34b59737ccfbb2e4c59d97bf3` | `8ed0a2efade22a11aa50f4511cdab3d32f438759f7acd7819ccbe41ab92ac0b3` |
| DOGE-USDT-SWAP | `data/market_1m/DOGE_USDT_USDT_1m.csv` | 31,378,267 | `2162df0f277bef6c04bd191b459a35d735c68f2d` | `eabf087b1a782d316fa1560b10fc4ee7adfc0adb426ef3d1158dc18c248c40f4` |
| AVAX-USDT-SWAP | `data/market_1m/AVAX_USDT_USDT_1m.csv` | 25,858,552 | `6e0cb0c55aa2aafb4118d62522826bcf1a2aeb62` | `44ac7db951247a374aecba845336517b82b2655489920d62ec70f9b02fccdfd5` |

These SHA-256 values are the source hashes recorded by the deterministic Module B run metadata and are linked to the exact Git blob IDs above. The Module B run reports 569,125 common one-minute timestamps and zero gaps in the common aligned timeline. This provenance record does not assert that the VPS SQLite database is byte-identical to the canonical Git CSVs, nor that the downloader currently produces those exact files. Runtime/VPS lineage still requires a direct manifest comparison.

**Retention and canonical-source rule:** the tracked `data/market_1m/` files are the canonical repository snapshot for the cited Module B run. Do not silently replace them, rewrite history, or delete them. Any refreshed market data must be introduced as a separately versioned source snapshot with its own immutable manifest (instrument IDs, acquisition/source metadata, byte size, row count, timestamp bounds, Git blob ID and SHA-256), and downstream studies must pin that snapshot explicitly. Raw/private funding CSVs remain outside Git; their separate Termux manifest is not evidence of VPS runtime presence.

**G0-10 disposition:** the documentation contradiction is corrected for the current canonical repository snapshot. The remaining source-provenance issue is the VPS-to-canonical lineage and refresh/retention process, not whether the five cited CSVs are tracked.
