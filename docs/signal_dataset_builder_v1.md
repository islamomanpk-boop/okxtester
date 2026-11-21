# Price Action V1 — Multi-Timeframe Signal Dataset Builder

## Purpose

Build local 15-minute price-action datasets for BTC, ETH, SOL, DOGE,
and AVAX. Attach causal daily and 4-hour price structure for Model A,
while retaining the indicator-assisted regime separately for Model B.

## Inputs

- `~/okx_adaptive_bot/data/indicators/{SYMBOL}_USDT_15m_indicators.csv`
- `~/okx_adaptive_bot/data/indicators/{SYMBOL}_USDT_4h_indicators.csv`
- `~/okx_adaptive_bot/data/indicators/{SYMBOL}_USDT_1d_indicators.csv`
- `~/okx_adaptive_bot/reports/{SYMBOL}_regimes.csv`
- `src/price_action_signals.py`
- `src/price_action_structure.py`

## Model A — Pure price action

Daily and 4-hour structure are calculated independently using OHLC only.
Extra EMA, RSI, ADX, and other indicator columns are not passed to the
structure detector.

The structure detector uses three candles to the left and three to the
right to confirm swing highs and lows. A pivot is available only after
the third right-side candle closes.

Structure availability:
- Daily: candle open timestamp + 24 hours.
- 4-hour: candle open timestamp + 4 hours.
- 15-minute signal: candle open timestamp + 15 minutes.

Both higher-timeframe structures are attached using backward as-of
matching. Exact availability-time matches are allowed. Future matches
are forbidden.

`pa_direction_permission`:
- `LONG_ONLY`: daily and 4-hour structures are both BULLISH.
- `SHORT_ONLY`: daily and 4-hour structures are both BEARISH.
- `NO_TREND`: structures conflict, are neutral, or are not yet available.

Daily and 4-hour BOS events are retained separately. BOS is an event,
not an entry signal.

## Model B — Indicator-assisted regime

The existing regime report is retained. Its output is available as
`indicator_regime`. The legacy `regime` column remains as a compatibility
alias. Model B labels do not determine Model A structure or permission.

## ATR14

The 15-minute indicator CSV does not currently contain ATR14. The builder
calculates it from 15-minute OHLC using the existing Wilder-style formula:

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
