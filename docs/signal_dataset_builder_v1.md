# Price Action V1 — Signal Dataset Builder

## Purpose

Build local 15-minute price-action signal datasets for BTC, ETH, SOL, DOGE,
and AVAX, enriched with the most recently available 4-hour market regime.

## Inputs

- `~/okx_adaptive_bot/data/indicators/{SYMBOL}_USDT_15m_indicators.csv`
- `~/okx_adaptive_bot/reports/{SYMBOL}_regimes.csv`
- `src/price_action_signals.py`

## Causal timing

- 15m `ts` is the candle opening timestamp.
- Price-action signals become available at `ts + 15 minutes`.
- 4h regime reports provide `available_at`, which must equal `ts + 4 hours`.
- Regime attachment uses backward `merge_asof` matching.
- Exact-time matches are valid because both candles have closed at that instant.
- A regime with an availability time later than the signal availability time is forbidden.
- Rows before the first available 4h regime are marked `NO_REGIME_AVAILABLE`.

## ATR14

The 15m indicator CSV does not currently contain ATR14. The builder calculates
it from 15m OHLC using the same Wilder-style exponentially weighted formula as
`src/calculate_indicators.py`:

- alpha = 1/14
- adjust = False
- min_periods = 14

Original indicator files are not modified.

## Outputs

Local per-asset CSV files are written to:

`~/okx_adaptive_bot/reports/price_action_signals/`

The compact audit report is written to:

`reports/signal_dataset_audit.md`

Raw candle data and large generated signal CSVs must not be committed to Git.
