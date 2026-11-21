# Regime Integrity and Look-Ahead Audit

Project: OKX Multi-Regime Price Action Strategy V1
Branch: price-action-v1
Audit date: 2026-11-21
Assets: BTC, ETH, SOL, DOGE, AVAX

## Final result

PASS — all five assets passed the independent audit.

## Checks performed for each asset

1. Regime report row count matches original 4H indicator data.
2. No duplicate report timestamps.
3. Report timestamps are in chronological order.
4. Report timestamps exactly match original 4H candles.
5. 4H availability timestamps equal candle timestamp + 4 hours.
6. OHLCV values match original 4H data.
7. EMA50, EMA200, ATR14 and ADX14 match original 4H indicators.
8. Daily availability timestamps equal daily candle timestamp + 24 hours.
9. Backward as-of merge selects no future daily candle.
10. Daily close, EMA50 and EMA200 match independently reconstructed values.
11. Saved regime labels match independent recalculation.

## Results

| Asset | Result | WARMUP | First ready timestamp (UTC) |
|---|---|---:|---|
| BTC | PASS | 1,202 | 2026-05-08 20:00 |
| ETH | PASS | 1,202 | 2026-05-08 20:00 |
| SOL | PASS | 1,202 | 2026-05-08 20:00 |
| DOGE | PASS | 1,202 | 2026-05-08 20:00 |
| AVAX | PASS | 1,202 | 2026-05-08 20:00 |

## Regime distributions

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

## Interpretation

The saved regime reports are consistent with the source indicator data and the classification rules.

The independently reconstructed daily merge confirms that no future daily candle was selected for any 4H decision timestamp.

The WARMUP period is consistent across all assets. The first ready timestamp is 2026-05-08 20:00 UTC.

DOGE having no bullish classifications in this sample is an observed result, not an audit failure.

## Important limitation

This audit verifies timestamp alignment, source-value integrity,
backward daily merging and regime-label reproducibility.

It does not prove that the strategy is profitable or that every
possible execution-time look-ahead issue has been eliminated.

## Next stage

Proceed to price-action signal specification and execution design.
Do not claim strategy performance until realistic backtesting
and out-of-sample validation have been completed.
