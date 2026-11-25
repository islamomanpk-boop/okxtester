# Phase 3 Multi-Timeframe Source-Lineage Reconciliation V1

**Date:** 2026-11-25  
**Project:** OKX Price Action V1 — Phase 3 Sideways / Range  
**Scope:** Read-only reconciliation of existing 1M → 15M/4H aggregation evidence, raw 15M provenance notes, and canonical Git source manifests  
**Status:** Cross-timeframe aggregation equivalence is historically reported PASS for the compared local files; exact identity of those 1M inputs with the current canonical Git snapshot and VPS runtime lineage remains UNVERIFIED. No data was downloaded, modified, or regenerated.

## 1. Decision summary

The earlier aggregation work should not be repeated merely to produce another PASS:

- The 2026-11-22 independent aggregation audit reports exact OHLCV equality between five local 1M sources and supplied 15M/4H files, with 37,941 complete 15M bars and 2,370 complete 4H bars per asset.
- The 2026-11-23 Termux audit records the 1M input location as `~/okx_scalping_data/{ASSET}_USDT_USDT_1m.csv` and supplied higher-timeframe files under `~/okx_adaptive_bot/data/`. It reports exact equality for all five OHLCV fields at every compared timestamp, using epoch-anchored left-closed/left-labelled complete buckets.
- The accepted boundary taxonomy provenance note separately records SHA-256 hashes for five raw 15M files under `~/okx_adaptive_bot/data/`; those raw 15M CSVs are not committed to the canonical Git branch.
- The later Module B V1.1 run metadata pins the current canonical `data/market_1m/` Git blob IDs and SHA-256 values and reports 569,125 common 1M timestamps with zero gaps.

These records do **not** form a complete byte-level chain between the 1M files used by the historical aggregation audit, the later canonical Git blobs, the raw 15M source hashes, and the VPS SQLite/downloader runtime. The earlier aggregation result is valid within its documented comparison scope; it must not be upgraded into a claim of acquisition provenance or runtime equivalence.

## 2. Evidence matrix

| Evidence | Inputs / location recorded | What is established | What remains unestablished |
|---|---|---|---|
| 2026-11-22 aggregation audit | Five local 1M files and supplied 15M/4H files | 10/10 asset-timeframe comparisons passed; exact timestamps and OHLCV on complete buckets | Input SHA-256 values and exact byte identity to later canonical Git snapshots; upstream acquisition lineage |
| 2026-11-23 Termux aggregation pass | 1M under `~/okx_scalping_data/`; 15M/4H under `~/okx_adaptive_bot/data/` | 37,941 15M and 2,370 4H bars per asset; left-labelled complete buckets match all five OHLCV fields | Immutable 1M input hashes tied to the later Git snapshot; VPS runtime equivalence |
| 2026-11-24 boundary taxonomy provenance | Five raw 15M files under `~/okx_adaptive_bot/data/` | Observed 15M SHA-256 values and row counts; backup comparison for shared rows | Original OKX downloader/API lineage; corresponding 1M hashes at the time; Git-tracked raw 15M source |
| Module B V1.1 run metadata | Canonical `data/market_1m/` paths, Git blob IDs and SHA-256 values | Exact source snapshot pinned for Module B; per-asset row counts and common aligned 1M timeline | Whether the earlier Termux aggregation used these exact byte-identical 1M files; VPS runtime equivalence |
| 2026-11-25 expanded VPS inventory | Configured VPS/project/repository roots and bounded file scans | No candidate provenance records found in the inspected scope; a downloader and candle database were inventoried | Downloader's full semantics, historical source hashes, data refresh history, and whether runtime files match canonical Git data |

## 3. Raw 15M hashes already recorded

The 2026-11-24 provenance checkpoint records these hashes for the raw local 15M CSVs (37,941 data rows each):

| Asset | Raw 15M SHA-256 |
|---|---|
| BTC | `0721a4a25a61f1917be4f9952514096c641fbec64e7ae0d50c7cf1c3ebfe9658` |
| ETH | `7195e45315c360e9f1fdd37746125968359bce8632a0bfe51628f104792fdc04` |
| SOL | `5b34cbb006497ecd7ebe0cfa67b25b4230cb769d6362d278991171a8f6da2d33` |
| DOGE | `3418c81fa16b531eee5de90d8b0ff6a5543db54357cb5572358ff31ab6627b5f` |
| AVAX | `75ef1a545686217a6d4ca55385690095c6e2a494438b7f4e38352d5ca35de493` |

The same note records that BTC/ETH current files each had one additional final candle relative to their named backup, while all shared rows matched; SOL/DOGE/AVAX matched their backups byte-for-byte. This is local file integrity/backup evidence, not original exchange acquisition provenance.

## 4. Canonical 1M snapshot pinned by Module B

The accepted Module B metadata pins the five current canonical files by Git blob SHA-1 and file SHA-256. These are the exact hashes in `reports/phase3_breakout_lifecycle_v1_1/run_metadata_v1_1.json`:

| Asset | Git blob SHA-1 | File SHA-256 |
|---|---|---|
| BTC | `639f7b8a6d54747dd3eb3370dc133d53f6382bfd` | `3afab3d60387c87fc4b96f54911538fea6bbb7682b2e18001537bc4359da6633` |
| ETH | `3017d870fe1cb764e1acb8fdec04138592749d69` | `8a2924bcb23bd5963cd1c46b8871475ff7ff4a3c8d8bed6325dbd406ec0552d2` |
| SOL | `a850c2dc4a2c14b34b59737ccfbb2e4c59d97bf3` | `8ed0a2efade22a11aa50f4511cdab3d32f438759f7acd7819ccbe41ab92ac0b3` |
| DOGE | `2162df0f277bef6c04bd191b459a35d735c68f2d` | `eabf087b1a782d316fa1560b10fc4ee7adfc0adb426ef3d1158dc18c248c40f4` |
| AVAX | `6e0cb0c55aa2aafb4118d62522826bcf1a2aeb62` | `44ac7db951247a374aecba845336517b82b2655489920d62ec70f9b02fccdfd5` |

Module B source rows are BTC 569,125; ETH 569,125; SOL 569,126; DOGE 569,126; AVAX 569,127. The common aligned timeline is 569,125 timestamps with zero gaps. This is a pinned canonical source snapshot for that study.

## 5. Remaining reconciliation questions

1. Are the five 1M inputs used by the 2026-11-23 Termux aggregation audit byte-identical to the five canonical Git files pinned in Module B metadata? The historical audit notes do not record the input SHA-256 values, so the existing documents alone cannot answer this.
2. Can the raw 15M SHA-256 files from the 2026-11-24 note be rechecked against a fresh aggregation from the exact canonical 1M blobs? The historical equality result strongly supports the aggregation convention, but the source snapshot identity needs to be proven.
3. Are the raw 4H source files still available with immutable hashes? The cited notes report their OHLCV equivalence but do not provide a corresponding five-file 4H SHA-256 manifest.
4. Does the VPS `download_okx.py` produce the canonical 1M file schema, instrument IDs, timestamp convention, volume field and exact source snapshot? The expanded VPS inventory found no source-provenance record in its inspected roots; this must be resolved by read-only code/config inspection and runtime manifest evidence.
5. Are OKX instrument identity and volume semantics supported by downloader/API response fields or other authoritative acquisition records? Filenames and matching OHLCV are not enough.

## 6. Safe next verification

When the original Termux source files remain available, perform a read-only manifest comparison only:

- Recompute SHA-256 for each original 1M input and compare with the canonical Module B SHA-256 values above.
- Recompute SHA-256 for each raw 15M and 4H file and compare with the historical manifests where available.
- If the exact 1M inputs match canonical hashes, independently rebuild 15M and 4H complete buckets from those exact canonical files and compare timestamp sets plus all OHLCV fields against the raw higher-timeframe files.
- Record missing/extra timestamps, partial first/last buckets, and every mismatch; do not silently drop mismatches.
- Preserve raw files and outputs. Do not overwrite, rename, delete, or refresh source data as part of the audit.
- For VPS lineage, inspect downloader/config and runtime manifests read-only; do not run a downloader or modify the VPS.

If the original local files are no longer available, mark that historical byte-level link UNVERIFIABLE rather than reconstructing or assuming it.

## 7. Gate disposition

- Cross-timeframe OHLCV aggregation equivalence for the files compared in the earlier audits: **HISTORICALLY REPORTED PASS**.
- Exact identity between those historical 1M inputs and the current canonical Git 1M snapshot: **UNVERIFIED**.
- Raw 15M local source hashes: **RECORDED**, but upstream acquisition lineage remains **UNVERIFIED**.
- Raw 4H immutable file hashes: **NOT RECORDED in the cited checkpoints**.
- VPS downloader/runtime equivalence to canonical Git sources: **UNVERIFIED**.
- G0 source provenance remains **OPEN**; Gate 0 remains **CONDITIONAL HOLD**.
- No candidate generation, Gate 2 execution-resolution comparison, strategy PnL backtest, or Phase 1 handoff is authorized by this checkpoint.

No source data, VPS state, or historical report was modified by this audit.
