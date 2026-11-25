# Phase 3 Breakout Causal Reconstruction Preflight Contract V1

**Date:** 2026-11-25  
**Project:** OKX Price Action V1 — Phase 3 Sideways / Range  
**Branch:** `price-action-v1`  
**Status:** IMPLEMENTATION PREFLIGHT ONLY — no causal event reconstruction has been run by this checkpoint; no candidates or outcomes authorized.

## 1. Purpose

Freeze the implementation preflight and hard acceptance checks for the full completed-15M breakout-population reconstruction required by G0-04. This contract supplements, and does not replace, Sections 10–11 of:

`docs/research_protocols/2026-11-25_phase3_past_only_regime_threshold_selection_protocol_v1.md`

The reconstruction must discover the full raw boundary-crossing universe first, then apply each of the six predeclared causal calibration variants. It must not start from the retrospective 932-signal selected ledger.

## 2. Immutable 1M inputs

Use only the five canonical files pinned in the accepted Module B V1.1 metadata. Verify SHA-256 before parsing; fail closed on any mismatch.

| Asset | File | Expected SHA-256 |
|---|---|---|
| BTC | `data/market_1m/BTC_USDT_USDT_1m.csv` | `3afab3d60387c87fc4b96f54911538fea6bbb7682b2e18001537bc4359da6633` |
| ETH | `data/market_1m/ETH_USDT_USDT_1m.csv` | `8a2924bcb23bd5963cd1c46b8871475ff7ff4a3c8d8bed6325dbd406ec0552d2` |
| SOL | `data/market_1m/SOL_USDT_USDT_1m.csv` | `8ed0a2efade22a11aa50f4511cdab3d32f438759f7acd7819ccbe41ab92ac0b3` |
| DOGE | `data/market_1m/DOGE_USDT_USDT_1m.csv` | `eabf087b1a782d316fa1560b10fc4ee7adfc0adb426ef3d1158dc18c248c40f4` |
| AVAX | `data/market_1m/AVAX_USDT_USDT_1m.csv` | `44ac7db951247a374aecba845336517b82b2655489920d62ec70f9b02fccdfd5` |

Required input preflight:
- exact required columns: `ts, open, high, low, close, vol`;
- no duplicate timestamps within any asset;
- finite, valid OHLCV values;
- use the intersection of all five timestamp indices, matching the recovered original source;
- common index must contain exactly 569,125 timestamps, strictly increasing at exactly 60,000 ms cadence, with zero gaps;
- report each asset's source-row count and rows excluded from the common index; do not silently discard or rewrite source files.

## 3. Rebuild and validate bars/context

Rebuild 15M and 4H bars from the common 1M index using the recovered source convention:
- `resample(label="right", closed="left")`;
- retain only intervals with exactly 15 or 240 constituent 1M candles, respectively;
- OHLCV aggregation: first open, maximum high, minimum low, last close, summed volume;
- 15M and 4H labels are right-edge close/availability timestamps.

Reproduce the recovered source context formula exactly:
- prior 12 completed 4H candles for upper/lower channel, using rolling extrema shifted by one 4H row;
- channel width `(upper / lower - 1) * 100`;
- the exact historical efficiency and overlap formulas from the archived Python source;
- backward as-of join from completed 15M close labels to the latest available 4H context snapshot.

Hard checks:
1. No joined 15M close may precede its assigned context snapshot.
2. Every joined row must have a finite context and valid upper/lower boundary.
3. A complete, aligned 4H context interval is expected to own 16 complete right-labelled 15M rows in `[T, T + 4 hours)`. Verify this from actual data; report every exception and stop if any context used in calibration has partial/missing coverage.
4. Reconcile context timestamps, upper/lower boundaries and width formula against the detector feature ledger using the documented one-4H offset. Report mismatches; never force a join.

## 4. Mandatory historical baseline reproduction gate

Before producing any past-only event counts, reproduce the accepted original full-sample baseline from the same canonical 1M hashes. This is a code/input integrity gate, not a live calibration method.

The expected event counts are:

| Asset | Definition | Direction | Expected |
|---|---|---|---:|
| BTC | BROAD_P40 | LOWER | 91 |
| BTC | BROAD_P40 | UPPER | 115 |
| BTC | STRICT_P25 | LOWER | 62 |
| BTC | STRICT_P25 | UPPER | 81 |
| ETH | BROAD_P40 | LOWER | 87 |
| ETH | BROAD_P40 | UPPER | 77 |
| ETH | STRICT_P25 | LOWER | 51 |
| ETH | STRICT_P25 | UPPER | 51 |
| SOL | BROAD_P40 | LOWER | 117 |
| SOL | BROAD_P40 | UPPER | 96 |
| SOL | STRICT_P25 | LOWER | 77 |
| SOL | STRICT_P25 | UPPER | 71 |
| DOGE | BROAD_P40 | LOWER | 81 |
| DOGE | BROAD_P40 | UPPER | 75 |
| DOGE | STRICT_P25 | LOWER | 55 |
| DOGE | STRICT_P25 | UPPER | 65 |
| AVAX | BROAD_P40 | LOWER | 84 |
| AVAX | BROAD_P40 | UPPER | 109 |
| AVAX | STRICT_P25 | LOWER | 64 |
| AVAX | STRICT_P25 | UPPER | 83 |

All 20 counts must match exactly. If any count differs, stop; do not emit or interpret causal population results. Do not tune formulas to force a match.

## 5. Full-universe event identity and six causal variants

After the historical baseline passes:
1. Enumerate every completed-15M upper/lower boundary crossing under the recovered source's crossing definition, before applying any regime-width threshold. This raw crossing universe must not be restricted to the 932 historical selected signals.
2. Give each unique signal the stable identity `asset + direction + signal_time_ms + context_snapshot_ms`. Strict and broad are nested labels on the same event identity, not duplicate event rows.
3. At each current context T, compute P25/P40 from prior completed context snapshots strictly earlier than T. No 15M observation assigned to T may enter its own threshold.
4. Evaluate the two populations over the same prior context timestamp set:
   - `UNIQUE_4H_FEATURE_ROWS`: one width per prior context;
   - `JOINED_15M_ROWS`: all complete 15M rows assigned to those same prior contexts, retaining repeated widths.
5. Evaluate all three policies with the shared 180-prior-context warm-up:
   - `FIXED_180`: first 180 eligible prior contexts, held fixed;
   - `EXPANDING_PRIOR`: all eligible prior contexts strictly before T;
   - `ROLLING_180`: immediately preceding 180 eligible prior contexts.
6. This produces six named sensitivity variants. Preserve strict P25 and broad P40 flags separately and assert strict is a subset of broad for every event/policy/population.
7. Keep failed-breakout reversal out of this independent event scan; it inherits a verified breakout source event and context and is reconciled later as a separate family.

## 6. Required outputs

Produce only descriptive reconstruction artifacts:
- input manifest and per-asset common-index audit;
- 15M/4H bar counts, completeness and context-to-15M coverage audit;
- source context / detector-feature comparison;
- 20-row historical baseline reproduction table;
- per-context threshold table with policy, population, P25/P40, prior-context count, prior-15M-row count, and first/last prior context timestamps;
- unique raw crossing event ledger with all six strict/broad eligibility flags;
- reconciliation against the 932 unique historical selected signals: unchanged eligible, newly eligible, no-longer eligible, and raw-source mismatch, separately by policy/population/strict/broad/asset/direction;
- summary counts by asset, direction, policy and population;
- run metadata with source hashes, code revision, dependency versions and output hashes.

No candidate IDs, orders, fills, stops, targets, matched controls, forward outcomes, inference or PnL are to be produced.

## 7. Hard stop conditions

Stop and report the exact failing check if:
- any input hash or expected common-index property fails;
- any 15M/4H bar is incomplete but treated as complete;
- context availability or as-of timing is future-dated;
- any calibration sample includes current-context rows;
- the unique-4H and joined-15M populations use different prior context timestamp sets;
- any context in the calibration sample has other than 16 complete 15M rows;
- historical baseline reproduction is not exactly 20/20;
- historical 932-signal identity cannot be reconciled exactly;
- strict/broad nesting fails.

No fallback to the historical selected ledger, no formula tuning, and no partial pass.

## 8. Gate disposition

This document freezes implementation preflight only. It does not report a completed run, select a threshold policy, close G0-04/G0-05, authorize candidate generation, or authorize Gate 2 / strategy backtesting. Gate 0 remains CONDITIONAL HOLD until the required source, event-availability, candidate-contract and execution-readiness requirements are independently closed.
