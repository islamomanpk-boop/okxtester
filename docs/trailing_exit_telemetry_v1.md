# Trailing Exit Telemetry V1

## Purpose

Record causal, trade-level evidence about trailing stop-loss and trailing take-profit behaviour. This is reporting instrumentation only: it does not change signal generation, entry timing, sizing, stop/target calculation, or exit-fill priority.

## Timestamp convention

All telemetry timestamps are Unix epoch milliseconds, matching the existing `entry_time` and `exit_time` fields in trade CSV files. An activation/update timestamp stores that candle's opening-time timestamp (Unix milliseconds), but the condition is evaluated only after the full 1-minute candle has completed. The resulting trailing level is eligible beginning with the next 1-minute candle, preserving the existing causal execution rule.

## Trade CSV fields

- `initial_stop_price`: stop price assigned when the position is opened.
- `stop_price`: final protective stop price at trade close.
- `trailing_mode`: `none`, `trailing_stop_loss`, or `trailing_take_profit`.
- `trailing_sl_active`: whether trailing stop-loss activated during the trade.
- `trailing_sl_activation_time`: completed 1-minute candle timestamp of first activation.
- `trailing_sl_activation_price`: best favourable high/low observed on the activation candle.
- `trailing_sl_activation_level`: price threshold required for activation.
- `trailing_sl_activation_r`: favourable movement in R observed at activation.
- `trailing_sl_update_count`: number of actual protective-stop improvements after activation.
- `trailing_sl_last_update_time`: timestamp of the last protective-stop improvement.
- `trailing_tp_active`: whether trailing take-profit activated during the trade.
- `trailing_tp_activation_time`: completed 1-minute candle timestamp of first activation.
- `trailing_tp_activation_price`: best favourable high/low observed on the activation candle.
- `trailing_tp_activation_level`: original target price that triggered activation.
- `trailing_tp_activation_r`: favourable movement in R observed at activation.
- `trailing_tp_price`: final trailing take-profit level at trade close.
- `trailing_tp_update_count`: number of trailing take-profit level initializations/improvements.
- `trailing_tp_last_update_time`: timestamp of the last trailing take-profit level improvement.
- `max_favorable_price`: best favourable price observed during the trade.
- `max_favorable_time`: timestamp when the best favourable price was first observed.
- `max_favorable_excursion_r`: maximum favourable price movement divided by the initial risk distance.

For non-trailing trades, activation fields remain empty/false and update counts remain zero. Maximum favourable excursion is still tracked so baseline and trailing experiments can be compared.

## Interpretation limits

Telemetry records the best favourable extreme visible in each completed 1-minute candle. It does not infer the intrabar path between high and low. Activation is processed after exit checks for the current candle, and any newly calculated trailing level is first usable on the next candle. This avoids retroactively applying a stop to the candle that activated it.

The final stop price alone is not a substitute for the activation fields: a stop may remain unchanged even when activation occurred if the proposed trailing level did not improve the existing stop.

## Validation

Unit tests cover long and short trailing-stop activation, long and short trailing-take-profit activation, activation timestamps, level-update counts, and the existing protective-stop priority on a trailing-take-profit activation candle.
