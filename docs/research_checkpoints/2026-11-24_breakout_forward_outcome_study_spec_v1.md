# Breakout Forward-Outcome Study V1 — Frozen Specification

Date: 2026-11-24
Branch: price-action-v1
Status: Frozen research specification; implementation not yet authorized until this file is committed and synchronized.

## 1. Research question

After a historically detected sideways-channel breakout is confirmed, how far does price move in the breakout direction, how far does it move adversely, how quickly does it move, and how often does it close back through the broken boundary?

Do these outcomes differ according to the number and type of boundary tests and confirmed rejections before the breakout?

This is a descriptive historical forward-outcome study. It is not a trading strategy, profitability test, causal study, or recommendation to trade.

## 2. Immutable source and event definitions

Use the recovered original source without modification:

- Source: `research/archive/final_timing_corrected_breakout_and_retest_recovered_original_2026-11-22.py`
- Expected Git blob SHA: `95d2975947c449f3813d80ee7b12008db14f071f`

Do not change the original detector, its thresholds, its event timestamps, or its broad/strict definitions.

Required reproduction gate:

- Reproduce all 20 original asset/definition/direction event counts.
- Reproduce all 10 original P25/P40 channel-width quantiles.
- Fail closed if any count or quantile does not match the frozen original study.

Use the completed prior-test classification study as the source of pre-breakout group labels:

- `reports/breakout_prior_test_count_v1/breakout_prior_test_classifications_v1.csv`
- `reports/breakout_prior_test_count_v1/breakout_prior_test_links_v1.csv`
- `reports/breakout_prior_test_count_v1/original_event_reproduction_v1.csv`
- `reports/breakout_prior_test_count_v1/reconstruction_audit_v1.csv`
- `reports/breakout_prior_test_count_v1/run_metadata.json`

The prior-test study's source and definitions remain unchanged.

## 3. Assets and data

Primary assets:

- BTC
- ETH
- SOL
- DOGE
- AVAX

Use the existing 1-minute source files under `$HOME/okx_scalping_data`.

Required data checks:

- Verify timestamp ordering and uniqueness.
- Verify 1-minute continuity for every evaluated event window.
- Verify valid OHLC values and high/low consistency.
- Record each source file's SHA256.
- Record the common timestamp intersection and any exclusions.
- Do not silently fill, interpolate, or fabricate missing candles.
- Exclude volume from analysis because its source units remain unverified.

Use UTC for all event and candle timestamps.

## 4. Event identity and pre-breakout groups

Preserve separate results for:

- Original definition: BROAD_P40 and STRICT_P25.
- Direction: UPPER and LOWER.
- Touch zone: 5%, 10%, and 15% of frozen channel width.

The 10% zone is primary. The 5% and 15% zones are sensitivity analyses and must not be pooled with the primary zone.

Use the prior-test classification at the matching asset, definition, direction, signal timestamp, and zone.

Create mutually exclusive descriptive groups:

1. DIRECT: zero prior touch tests.
2. CONTACT_ONLY: one or more prior touch tests and zero confirmed rejections.
3. ONE_REJECTION: exactly one prior confirmed rejection.
4. TWO_REJECTIONS: exactly two prior confirmed rejections.
5. THREE_PLUS_REJECTIONS: three or more prior confirmed rejections.

Do not call every zero-rejection event a direct breakout. Contact-only events are a separate group.

Retain the original touch-test, confirmed-rejection, and contact-only counts in event-level outputs. Do not discard the underlying counts when assigning groups.

## 5. Signal and entry timing

The original breakout signal is confirmed at the close-labelled 15-minute signal timestamp.

The original timing convention must be preserved:

- The final 1-minute candle belonging to the signal's 15-minute interval is timestamped `signal_time - 1 minute`.
- The first eligible entry candle is the next 1-minute candle.
- Entry price is that next candle's OPEN.
- Entry timestamp is the next 1-minute candle's timestamp.

Never use the breakout signal candle's open, high, or low as post-entry movement.

Never enter at the 15-minute close if that would use a price unavailable under the specified next-1-minute-open execution convention.

If the next 1-minute entry candle is missing, invalid, or unavailable, record an explicit exclusion reason. Do not substitute another price.

## 6. Forward horizons

Measure four fixed horizons from the entry timestamp:

- 15 minutes: 15 complete 1-minute candles.
- 1 hour: 60 complete 1-minute candles.
- 4 hours: 240 complete 1-minute candles.
- 12 hours: 720 complete 1-minute candles.

For a horizon of N minutes, evaluate the N consecutive 1-minute candles beginning with the entry candle. The final close is the close of the Nth candle.

Each horizon must be independently marked complete or incomplete.

Do not treat a shorter available window as a complete longer horizon. Do not silently drop incomplete observations from audit denominators.

## 7. Forward outcome measurements

Calculate outcomes from the entry OPEN.

For an UPPER breakout:

- Favourable extreme is the maximum HIGH after entry.
- Adverse extreme is the minimum LOW after entry.

For a LOWER breakout:

- Favourable extreme is the minimum LOW after entry.
- Adverse extreme is the maximum HIGH after entry.

For each complete horizon, calculate:

1. Signed directional close return percentage.
   - UPPER: `(horizon_close / entry_price - 1) * 100`
   - LOWER: `(entry_price / horizon_close - 1) * 100`

2. Maximum favourable excursion (MFE), percentage of entry price.
3. Maximum adverse excursion (MAE), percentage of entry price.
4. MFE divided by the original frozen channel width, expressed as a percentage of channel width.
5. MAE divided by the original frozen channel width, expressed as a percentage of channel width.
6. Timestamp and elapsed minutes of the first occurrence of the maximum favourable extreme.
7. Timestamp and elapsed minutes of the first occurrence of the maximum adverse extreme.

Use the actual high/low price extremes, not candle closes, for MFE and MAE.

MFE and MAE are non-negative excursion magnitudes. Preserve signed directional close return separately.

If an extreme occurs more than once, use the earliest occurrence and document this tie rule.

## 8. Boundary failure measurement

Use the original frozen channel boundary recorded for the breakout event.

For an UPPER breakout, a boundary failure occurs at the first post-entry 1-minute candle whose CLOSE is less than or equal to the original upper boundary.

For a LOWER breakout, a boundary failure occurs at the first post-entry 1-minute candle whose CLOSE is greater than or equal to the original lower boundary.

Record:

- Whether boundary failure occurred within each horizon.
- First failure timestamp.
- Minutes from entry to first failure.
- Whether the entry OPEN was already back through the boundary.

An entry OPEN already back through the boundary must be explicitly flagged as an immediate adverse entry condition. Do not conceal it by waiting for the first candle close.

Boundary failure is a descriptive event label, not proof that a particular stop-loss would have executed.

## 9. Statistical summaries

Produce event-level results and grouped summaries.

At minimum, summarize by:

- Asset.
- Original breakout definition.
- Direction.
- Touch-zone percentage.
- Pre-breakout group.
- Forward horizon.

For each group and horizon report:

- Number of original classified events.
- Number eligible for entry.
- Number with complete horizon data.
- Number and reason for exclusions.
- Median and mean signed close return.
- Median and mean MFE.
- Median and mean MAE.
- Median MFE/channel-width and MAE/channel-width.
- Percentage with positive signed close return.
- Percentage with boundary failure.
- Median time to MFE.
- Distribution percentiles: 10th, 25th, 50th, 75th, and 90th where sample size permits.

Always show denominators. Do not hide small sample sizes.

Do not pool assets, directions, definitions, or zone variants in a way that obscures their separate results. Any combined summary must be explicitly labelled as pooled and secondary.

## 10. Audit and validation requirements

The implementation must fail closed if required checks fail.

Required checks include:

- Original 20/20 event counts reproduced.
- Original 10/10 quantiles reproduced.
- Every event maps to exactly one prior-test classification per zone.
- Every event has one unambiguous entry timestamp and price, or an explicit exclusion.
- Entry is strictly after signal confirmation under the frozen timing convention.
- No post-entry measurement uses a candle before entry.
- Each complete horizon contains exactly its required number of consecutive 1-minute candles.
- No missing or duplicate timestamps occur inside a complete outcome window.
- High/low excursion calculations respect breakout direction.
- Boundary-failure timestamps are not before entry.
- Group counts reconcile to the classification input.
- Event-level rows reconcile to grouped-summary denominators.
- Exclusions are counted and reason-coded.
- Repeated event keys are detected and rejected.
- Input and output file hashes and run metadata are recorded.

Include unit tests for upper and lower direction symmetry, entry timing, exact horizon lengths, MFE/MAE calculations, boundary failure, missing candles, incomplete horizons, and group reconciliation.

## 11. Interpretation limits

This study measures historical price movement after detected breakouts. It does not establish that a trade could be executed profitably.

It does not include:

- Trading fees.
- Slippage.
- Funding costs.
- Spread or order-book depth.
- Position sizing.
- Stop-loss or take-profit rules.
- Liquidation or margin mechanics.
- Portfolio exposure or simultaneous positions.

Do not label any group profitable, tradable, or superior based only on gross forward movement.

Do not infer causality from differences between pre-breakout groups. These groups may differ in market conditions and sample composition.

The original channel thresholds are full-sample retrospective quantiles, not live-calibrated thresholds. This limitation must remain visible in every interpretation.

The 5%, 10%, and 15% touch-zone variants overlap and are not independent samples.

Post-breakout retest behaviour is not the focus of this study and must be kept separate from pre-breakout test classification.

## 12. Outputs

Use a new, unique output directory:

`reports/breakout_forward_outcome_v1/`

Do not overwrite existing reports or source files.

Expected outputs:

- Event-level forward outcomes CSV.
- Grouped forward-outcome summaries CSV.
- Event exclusion audit CSV.
- Original event reproduction CSV.
- Reconstruction and validation audit CSV.
- Run metadata JSON, including input hashes and parameters.
- Complete run log.
- Test results.

The run must preserve all intermediate audit evidence needed to reproduce the findings.

## 13. Scope boundary

This specification authorizes implementation of the descriptive forward-outcome study only after this specification is committed and synchronized.

It does not authorize:

- Modifying the original breakout detector.
- Modifying the prior-test classifier.
- Changing frozen event definitions.
- Selecting a trading strategy.
- Running a fee-adjusted trading simulation.
- Claiming profitability or recommending live trading.

A separate specification and approval will be required for any later execution, fee/slippage, or strategy backtest.
