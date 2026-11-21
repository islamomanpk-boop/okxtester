# Price Action V1 — Signal Quality and Distribution Audit

## Purpose

Describe the frequency and distribution of the ten implemented price-action
event signals across BTC, ETH, SOL, DOGE, and AVAX.

This is a descriptive audit. Signal frequency is not evidence of profitability.

## Inputs

Local files:

`~/okx_adaptive_bot/reports/price_action_signals/{SYMBOL}_15m_price_action_signals.csv`

The builder output contains the 15-minute signal flags and the backward-matched
4-hour regime labels.

## Measurements

- Per-asset event counts for all ten signal columns.
- Confirmed pivot highs and lows, reported separately as structural events.
- Event counts grouped by BULLISH, BEARISH, SIDEWAYS, TRANSITION, WARMUP,
  and NO_REGIME_AVAILABLE.
- Number of candles with zero, one, two, or at least three event signals.
- Number of unique candles with at least one signal and with multiple signals.
- Regime candle coverage for each asset.

A candle with two active signal flags contributes two events but only one
signal-bearing candle. Overlap is not treated as two independent trades.

## Validation

The audit rejects missing required columns, empty datasets, duplicate or
non-chronological timestamps, unknown regime labels, missing boolean values,
and invalid signal flag values.

## Output

`reports/signal_quality_audit.md`

Only the compact report and source code are committed. The large generated
signal CSV datasets remain local.

## Limitations

This audit does not simulate orders, fills, stop-losses, take-profits, fees,
slippage, funding, or portfolio exposure. It does not calculate win rate,
expectancy, profit factor, or drawdown. Those belong to later backtesting
stages.

No signal is selected or described as profitable based on this report.
