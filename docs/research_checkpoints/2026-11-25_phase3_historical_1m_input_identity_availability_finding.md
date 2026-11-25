# Phase 3 Historical 1M Input Identity Check — Availability Finding

**Date:** 2026-11-25  
**Branch:** `price-action-v1`  
**Status:** BLOCKED BY MISSING HISTORICAL INPUT HASHES / SOURCE ACCESS  
**Related checkpoint:** `docs/research_checkpoints/2026-11-25_phase3_multitimeframe_source_lineage_reconciliation_v1.md`

## Question

Can the exact 1M files used in the 2026-11-22/23 local aggregation audits be proven byte-identical to the five canonical 1M CSVs currently tracked under `data/market_1m/`?

## Evidence reviewed

1. The 2026-11-23 Termux aggregation checkpoint explicitly names the historical inputs:
   `~/okx_scalping_data/{ASSET}_USDT_USDT_1m.csv`.
   It reports exact OHLCV aggregation matches against the corresponding local 15M/4H files, but it does not record SHA-256 hashes, Git blob IDs, file sizes, or an immutable manifest for those 1M inputs.
2. The 2026-11-24 raw 15M provenance checkpoint records SHA-256 values for five files in `~/okx_adaptive_bot/data/`, but says the raw 15M CSVs are not stored in the inspected GitHub branch.
3. The canonical GitHub branch tracks five current 1M CSVs under `data/market_1m/`; Module B V1.1 run metadata records their SHA-256 values and Git blob IDs.
4. Repository file search for the historical raw 15M filename convention did not return tracked raw 15M CSVs. The historical Termux 1M source paths are local-device paths, not repository paths. No connector-accessible copy of those exact historical Termux 1M files or their contemporaneous hashes was found in the reviewed canonical repository evidence.

## Finding

**A byte-for-byte comparison cannot be performed from the available repository records.** The historical audit's exact OHLCV aggregation PASS remains valid for the files that were compared at that time. However, without a contemporaneous SHA-256 manifest or access to the original Termux 1M files, the link from those historical inputs to the later canonical Git 1M snapshot is **UNVERIFIABLE from current evidence**.

This is not a mismatch. It is missing evidence. Do not describe the historical and canonical files as identical, and do not infer they differ.

## Required handling

- Preserve the current canonical Git files and historical reports unchanged.
- If the original Termux files still exist, a future read-only local audit can hash them and compare against the five canonical SHA-256 values in the Module B metadata.
- If the original files no longer exist, retain the identity link as UNVERIFIABLE; do not recreate a substitute and call it the historical input.
- Any new source download must be a separate versioned snapshot with its own acquisition metadata and SHA-256 manifest. It cannot retroactively prove the old input identity.

## Gate disposition

- Historical local 1M→15M/4H OHLCV aggregation: **REPORTED PASS**.
- Historical 1M input byte identity to current canonical Git snapshot: **UNVERIFIABLE / NOT PROVEN**.
- No evidence of a byte mismatch was found.
- G0 source provenance remains OPEN; Gate 0 remains CONDITIONAL HOLD.
- No candidate generation, Gate 2 execution-resolution comparison, or strategy PnL backtest is authorized.

No files outside the GitHub documentation were accessed or modified. No VPS command, download, overwrite, or deletion was performed.
