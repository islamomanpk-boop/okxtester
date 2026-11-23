# Breakout event reproduction source audit — 4H input provenance lead

**Date:** 2026-11-23  
**Branch:** `price-action-v1`  
**Status:** New source-audit lead; not yet tested and not a root-cause finding.

## Why this audit was opened

V3 tested both the archived 11-change percentage ER and the historical 12-change absolute-price ER. Both returned 0/20 event-count matches. A direct source comparison identified a material input-path distinction that the ER formula diagnostics do not test.

## Source-grounded observations

### Archived breakout/retest research script

File: `research/archive/final_timing_corrected_breakout_and_retest_research_original_v1.sh`

- Loads 1m files from `~/okx_scalping_data/{ASSET}_USDT_USDT_1m.csv`.
- Constructs 4h bars directly from those 1m files using pandas resampling:
  - `rule="4h"`
  - `origin="epoch"`
  - `label="left"`
  - `closed="left"`
  - retains bins with exactly 240 1m closes.
- Computes 12-bar channel and the archived 11-change percentage ER.
- Makes the 4h feature snapshot available at the 4h bar-start label plus four hours.
- Maps snapshots backward-as-of to 15m bar-start labels.
- Uses an archived event mask that additionally requires the prior 15m row to be selected as sideways.

### Historical sideways detector

File: `research/sideways_detector_original_v1.py`

- Defaults to loading separate 4h files from `~/okx_adaptive_bot/data/{ASSET}_USDT_4h.csv`.
- Validates the 4h timestamps are epoch-aligned and every adjacent row is exactly four hours apart.
- Computes the historical 12-change absolute-price ER from 13 closes.
- Builds channel/overlap from the current and prior 11 4h bars.
- Records the snapshot availability time as the final channel candle's start timestamp plus four hours.
- Produces 2,358 feature rows from a 2,370-row 4h source.

These are distinct source-data pathways: one is 4h bars resampled from the 1m research files; the other is a standalone 4h CSV set from a different directory. The inspected code does not establish that their OHLC values are identical.

## Why this matters

The V3 reconstruction uses 4h bars resampled from the 1m research data. Matching the historical ER formula does not prove that this 4h OHLC series is the same series used by the historical sideways detector or by the run that generated the accepted event-count table.

A difference in 4h source candles can alter channel highs/lows, efficiency, overlap, sideways selection, snapshot rows, and ultimately event counts—even if thresholds printed to six or nine decimals happen to agree.

## What is not established

- This source-path distinction is **not yet proven to explain** the 20 count mismatches.
- It is not known from the inspected code alone which 4h source was used for the historical accepted 20/20 event run.
- No claim is made that either 4h dataset is more correct.
- No event counts are accepted or changed by this audit.

## Next controlled diagnostic

Before another event-engine variant, compare the two 4h sources asset by asset, if both local datasets are available:

1. Load standalone `~/okx_adaptive_bot/data/{ASSET}_USDT_4h.csv`.
2. Independently resample `~/okx_scalping_data/{ASSET}_USDT_USDT_1m.csv` with the archived script's exact 4h resampling rules and 240-minute completeness requirement.
3. Align on 4h bar-start timestamps.
4. Report row counts, timestamp intersection, rows missing on either side, and exact/tolerance-based differences for open/high/low/close.
5. Identify the first and largest differences per asset; report whether the standalone source is a direct aggregation of the same 1m input.
6. Do not tune formulas or target counts. Do not run controls or forward outcomes.

If standalone 4h files are unavailable, stop and report that the source comparison cannot yet be completed. Ask for only the missing files or a simple local directory listing; do not silently substitute another source.

## Gate

**Event reproduction remains on HOLD.** No matched controls, forward outcomes, or profitability analysis until the historical input source and full event engine are independently reconciled.

This checkpoint records a testable source-provenance lead only, not an accepted empirical finding.
