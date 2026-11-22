# 2026-11-22 Source Data Integrity Verification — Rebuild Preparation

Status: **PASS for per-file timestamp and schema integrity; cross-timeframe OHLC aggregation not yet verified.**

## Scope
Read-only verification performed in the user's Termux environment for BTC, ETH, SOL, DOGE, and AVAX:
- 1M: `~/okx_scalping_data/{ASSET}_USDT_USDT_1m.csv`
- 15M: `~/okx_adaptive_bot/data/{ASSET}_USDT_15m.csv`
- 4H: `~/okx_adaptive_bot/data/{ASSET}_USDT_4h.csv`

All 15 files contain columns `ts, open, high, low, close, vol`.

## Results

| Asset | 1M rows | 1M first UTC | 1M last UTC | 15M rows | 15M first UTC | 15M last UTC | 4H rows | 4H first UTC | 4H last UTC |
|---|---:|---|---|---:|---|---|---:|---|---|
| BTC | 569,125 | 2025-10-20 08:50 | 2026-11-19 14:14 | 37,941 | 2025-10-20 09:00 | 2026-11-19 14:00 | 2,370 | 2025-10-20 12:00 | 2026-11-19 08:00 |
| ETH | 569,125 | 2025-10-20 08:50 | 2026-11-19 14:14 | 37,941 | 2025-10-20 09:00 | 2026-11-19 14:00 | 2,370 | 2025-10-20 12:00 | 2026-11-19 08:00 |
| SOL | 569,126 | 2025-10-20 08:50 | 2026-11-19 14:15 | 37,941 | 2025-10-20 09:00 | 2026-11-19 14:00 | 2,370 | 2025-10-20 12:00 | 2026-11-19 08:00 |
| DOGE | 569,126 | 2025-10-20 08:50 | 2026-11-19 14:15 | 37,941 | 2025-10-20 09:00 | 2026-11-19 14:00 | 2,370 | 2025-10-20 12:00 | 2026-11-19 08:00 |
| AVAX | 569,127 | 2025-10-20 08:50 | 2026-11-19 14:16 | 37,941 | 2025-10-20 09:00 | 2026-11-19 14:00 | 2,370 | 2025-10-20 12:00 | 2026-11-19 08:00 |

For every one of the 15 files:
- Duplicate timestamps: 0
- Out-of-order timestamps: 0
- Unexpected timestamp intervals: 0
- Epoch-aligned timestamps: all rows
- Required OHLC columns: present

Expected intervals checked: 60,000 ms (1M), 900,000 ms (15M), and 14,400,000 ms (4H).

## Interpretation and limits
1. Per-file time series are strictly increasing and regularly spaced over their reported coverage.
2. The five 1M files have slightly different row counts/end timestamps. Do not assume identical tails or force alignment by row number; align by timestamp.
3. The 15M coverage starts at 09:00 UTC, after the 1M start at 08:50 UTC. The 4H coverage starts at 12:00 UTC. Initial higher-timeframe coverage must be treated cautiously.
4. This check does **not** establish that 15M and 4H OHLCV candles equal aggregation of the 1M candles. Nor does it establish complete initial/final aggregation buckets or cross-asset timestamp alignment.
5. Next required audit: independently aggregate 1M candles into epoch-anchored 15M and 4H buckets using the repository's documented left-labeled/left-closed convention; compare timestamps and OHLCV values against supplied higher-timeframe files, while explicitly excluding incomplete buckets. Investigate any mismatches before reconstructing boundary events.

## Research status
This is a source-data integrity checkpoint only. It does not validate the repeated-boundary detector, event reconstruction, outcome formulas, or the provisional November 22 outcome results. No strategy or profitability conclusion follows.
