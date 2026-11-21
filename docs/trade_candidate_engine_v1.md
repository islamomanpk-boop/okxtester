# Trade Candidate Engine V1

## Scope

The first version generates Model A trend candidates only.
SIDEWAYS and other NO_TREND rows do not generate trend candidates.
Range trading will be researched as a separate strategy family.

## Direction permission

- LONG_ONLY permits bullish setups only.
- SHORT_ONLY permits bearish setups only.
- NO_TREND permits no trend candidate.

The permission is already produced by the causal daily and 4H
OHLC-only structure agreement in the signal dataset builder.

## Priority

Priority 3:
- Support rejection for long candidates.
- Bullish order-block first retest for long candidates.
- Resistance rejection for short candidates.
- Bearish order-block first retest for short candidates.

Priority 2:
- Bullish engulfing or pin bar with a support-zone touch.
- Bearish engulfing or pin bar with a resistance-zone touch.

Priority 1:
- Standalone bullish or bearish engulfing and pin-bar signals.

A zone touch alone is never a candidate.

Only one candidate is emitted per asset and signal candle.
The highest priority wins. Ties are resolved by signal-type name.

## Stop reference and execution separation

The candidate records a structural stop reference:
- Long: signal candle low minus 0.10 x ATR14.
- Short: signal candle high plus 0.10 x ATR14.

This is a reference for the signal-candle-extreme stop experiment.
It is not an execution fill or a final stop for every experiment.

The candidate engine does not invent an entry price or target.
The next eligible 1-minute candle determines market entry.
Fixed-percentage stop models and take-profit variants require the
execution layer to calculate prices from the actual entry.

## Causality

- A 15-minute signal becomes available at its candle close.
- `signal_available_at` must equal `ts + 15 minutes`.
- Output timestamps are Unix milliseconds.
- Candidate ranking uses only signal-time information.
- No future execution candles or returns are read.

## Output

Each candidate includes asset, side, signal timestamps, priority,
signal type, Model A label, stop reference, ATR-normalized distance,
and completed signal-candle OHLC/ATR values.

The output is a setup description, not a backtester-ready order.
