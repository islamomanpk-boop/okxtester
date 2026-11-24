# Breakout Forward-Outcome Study V1 — Measurement Clarification

Date: 2026-11-24
Applies to: `2026-11-24_breakout_forward_outcome_study_spec_v1.md`
Status: Frozen clarification; does not alter original event detection or classification.

## 1. Purpose

Clarify directional return and excursion formulas so upper and lower breakout measurements use the same entry-price denominator and are mathematically comparable.

The original frozen specification remains unchanged. This document supplements its measurement definitions.

## 2. Directional close return

Let `s = +1` for UPPER and `s = -1` for LOWER.

For each horizon:

`directional_close_return_pct = s * (horizon_close / entry_price - 1) * 100`

Positive values mean the close moved in the breakout direction. Negative values mean the close moved against the breakout direction.

Use the same entry-price denominator for both directions. Do not use reciprocal price ratios for lower breakouts.

## 3. Maximum favourable excursion (MFE)

MFE is a non-negative price movement in the breakout direction, expressed as a percentage of entry price.

For UPPER:

`MFE_pct = (maximum_high_after_entry / entry_price - 1) * 100`

For LOWER:

`MFE_pct = (entry_price - minimum_low_after_entry) / entry_price * 100`

## 4. Maximum adverse excursion (MAE)

MAE is a non-negative price movement against the breakout direction, expressed as a percentage of entry price.

For UPPER:

`MAE_pct = (entry_price - minimum_low_after_entry) / entry_price * 100`

For LOWER:

`MAE_pct = (maximum_high_after_entry - entry_price) / entry_price * 100`

## 5. Channel-width normalization

Let `W = original_upper_boundary - original_lower_boundary`.

For UPPER:

- Favourable price excursion = `maximum_high_after_entry - entry_price`.
- Adverse price excursion = `entry_price - minimum_low_after_entry`.

For LOWER:

- Favourable price excursion = `entry_price - minimum_low_after_entry`.
- Adverse price excursion = `maximum_high_after_entry - entry_price`.

Normalize each excursion:

`excursion_as_pct_of_channel = price_excursion / W * 100`

This is a percentage of the original channel width, not a return percentage.

## 6. Timing of extremes

The first 1-minute candle in the horizon has elapsed-minute index zero at its OPEN timestamp.

Record the timestamp of the candle containing the first occurrence of each maximum favourable and adverse extreme. OHLC data does not reveal the exact intraminute time of an extreme; do not imply greater timing precision.

If an extreme is repeated, retain its earliest candle.

## 7. Horizon row structure

The event-level output uses one row per:

`asset + definition + direction + signal_time + zone_pct_of_channel + horizon`

Each event/zone therefore has four horizon rows, including explicit incomplete or excluded statuses. Grouped summaries must reconcile to these rows and preserve denominators.

## 8. Entry and immediate boundary condition

The entry candle is the first 1-minute candle opening at the 15-minute signal close timestamp.

Record whether its OPEN is already at or back through the original boundary:

- UPPER immediate adverse entry condition: `entry_open <= original_upper_boundary`.
- LOWER immediate adverse entry condition: `entry_open >= original_lower_boundary`.

This flag is separate from the first post-entry candle CLOSE boundary-failure measurement. Do not silently classify an immediate adverse entry as a later close failure.

## 9. Scope

These clarifications change no original breakout event, timestamp, boundary, pre-breakout group, or source dataset.

No fee, slippage, funding, execution, or profitability claim is introduced.
