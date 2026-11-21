# Indicator and Regime Inventory Audit

Date: 2026-11-21
Project: OKX Multi-Regime Price Action Strategy V1
Branch: price-action-v1

## 1. Indicator file audit

All 15 indicator files were present.

All five assets had identical row counts and indicator columns.

### Daily (1D)
Rows per asset: 394

Columns:
- OHLCV
- EMA50
- EMA200
- ATR14

Missing values per asset:
- EMA50: 49
- EMA200: 199
- ATR14: 13

### Four-hour (4H)
Rows per asset: 2,370

Columns:
- OHLCV
- EMA50
- EMA200
- ATR14
- ADX14

Missing values per asset:
- EMA50: 49
- EMA200: 199
- ATR14: 13
- ADX14: 26

### Fifteen-minute (15M)
Rows per asset: 37,941

Columns:
- OHLCV
- EMA20
- EMA50
- RSI14
- Bollinger middle, upper and lower
- Volume SMA20

Missing values per asset:
- EMA20: 19
- EMA50: 49
- RSI14: 14
- Bollinger middle: 19
- Bollinger upper: 19
- Bollinger lower: 19
- Volume SMA20: 19

The missing-value counts are consistent across all five assets and are consistent with indicator warm-up periods.

## 2. Regime report audit

All five regime reports were present.
Each report contained 2,370 rows.
All reports ended at 2026-11-19 08:00 UTC.

### BTC
- WARMUP: 1,202
- TRANSITION: 428
- BEARISH: 309
- SIDEWAYS: 245
- BULLISH: 186

### ETH
- WARMUP: 1,202
- TRANSITION: 382
- SIDEWAYS: 381
- BEARISH: 293
- BULLISH: 112

### SOL
- WARMUP: 1,202
- TRANSITION: 466
- BEARISH: 288
- SIDEWAYS: 272
- BULLISH: 142

### DOGE
- WARMUP: 1,202
- BEARISH: 567
- SIDEWAYS: 334
- TRANSITION: 267
- BULLISH: 0

### AVAX
- WARMUP: 1,202
- SIDEWAYS: 525
- TRANSITION: 320
- BEARISH: 260
- BULLISH: 63

## 3. Preliminary assessment

- All 15 indicator files exist.
- Indicator columns and row counts are consistent across assets.
- Indicator missing-value counts are consistent with expected warm-up periods.
- All five regime reports exist and have matching row counts.
- DOGE having no bullish classifications is an observation, not automatically an error.
- WARMUP classifications require further validation against daily and 4H indicator availability.

## 4. Remaining validation

This is an inventory and completeness report, not final proof of regime correctness.

The next audit must independently verify:
1. 4H timestamps match the original candles.
2. Daily data is only used after the daily candle closes.
3. The backward as-of merge does not select future data.
4. Saved regime labels match an independent recalculation.
5. Timestamp ordering and uniqueness.

No strategy backtesting should begin until these checks pass.
