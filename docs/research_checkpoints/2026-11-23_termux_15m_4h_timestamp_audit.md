# Termux 15M/4H Timestamp Cadence Audit — 2026-11-23

**Project:** OKX Price Action V1  
**Branch:** `price-action-v1`  
**Status:** Timestamp cadence audit PASS; OHLCV aggregation equivalence and timestamp-label semantics remain OPEN.  
**Scope:** Read-only Python CSV audit of the five existing 15M and 4H files under `~/okx_adaptive_bot/data/`.

## Results

For each of BTC, ETH, SOL, DOGE, and AVAX:

| Check | 15M | 4H |
|---|---:|---:|
| Data rows | 37,941 | 2,370 |
| Duplicate timestamps | 0 | 0 |
| Timestamps off expected interval grid | 0 | 0 |
| Incorrect adjacent timestamp steps | 0 | 0 |

- All five 15M files share first timestamp `1760950800000` and last timestamp `1795096800000`.
- All five 4H files share first timestamp `1760961600000` and last timestamp `1795075200000`.
- Every 15M adjacent timestamp difference is exactly 900,000 ms.
- Every 4H adjacent timestamp difference is exactly 14,400,000 ms.
- No files were modified.

## Interpretation

The files have internally regular timestamp cadence and no duplicate or missing intervals within their respective observed ranges. This does not establish that the files use the accepted breakout study's timestamp-label convention or that their OHLCV values equal aggregates from the synchronized 1M source.

The 15M and 4H ranges differ at their endpoints. This must be evaluated against complete-bar resampling rules and the source 1M coverage; row counts alone are not proof of aggregation equivalence.

## Next gate

Independently aggregate the synchronized 1M source using the accepted resampling conventions and compare timestamps and OHLCV values against these files. Establish whether the files are open-labelled or close-labelled and identify the exact complete common range. Do not proceed to matched controls or outcomes until the required original breakout event counts can be reproduced exactly.
