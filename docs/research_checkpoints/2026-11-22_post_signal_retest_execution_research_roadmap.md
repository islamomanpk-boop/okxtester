# Expanded Price-Action Research Roadmap — 2026-11-22

**Repository:** `islamomanpk-boop/okxtester`  
**Branch:** `price-action-v1`  
**Status:** Research plan only. No strategy backtests or local data modifications are authorized by this plan.

## Purpose

Extend the five-asset (BTC, ETH, SOL, DOGE, AVAX) price-action research so that strategy design is based not only on market regimes and signal occurrence, but also on the price path after a signal, retests, and realistic entry execution.

The research remains descriptive until the user explicitly authorizes strategy testing. Do not select final stop-loss, take-profit, or execution settings from descriptive statistics alone.

## Agreed research sequence

### 1. Finish sideways boundary-rejection movement study

For the existing exploratory 4H sideways classifications (STRICT_P25 and BROAD_P40), study strong upper- and lower-boundary rejection events.

Measure after the completed rejection candle:
- Maximum favourable excursion (MFE) and maximum adverse excursion (MAE).
- Median, P75 and P90 favourable/adverse movement.
- Time to reach 0.25%, 0.50%, 1.00% and other justified movement levels.
- Whether price moves toward the channel middle or opposite boundary.
- Compare with non-touch sideways candles, matched as closely as practical by asset, regime snapshot and signal-candle range.

Event rules:
- Use the 10% boundary zone as the primary definition; treat 5% and 15% as sensitivity checks where useful.
- A strong upper rejection touches the upper zone, then closes below its inner edge while remaining inside the channel. A strong lower rejection is the mirror image.
- Count only the first strong rejection in a continuous touch episode.
- Require actual 15M timestamp continuity and split episodes when the confirmed 4H snapshot changes.
- Signal is available only at the rejection candle close; follow-up begins on the next eligible minute.
- Freeze the channel boundary known at confirmation for event measurements.
- Report sample sizes and incomplete-horizon exclusions.

### 2. Breakout continuation and breakout retests

For confirmed upper and lower breakouts, separately measure:
- Maximum continuation beyond the frozen channel boundary.
- MFE and MAE from the breakout candle close.
- Median, mean, P75 and P90 continuation.
- Time to reach directional movement levels such as 0.25%, 0.50%, 1.00%, 1.50% and 2.00%.
- Return-inside frequency and time outside the channel.
- Retest frequency, time to retest, retest depth, boundary hold/failure, and continuation after a successful retest.
- Breakout candle range, body and wick characteristics.

Avoid false crossings caused solely by a refreshed 4H channel boundary. A breakout crossing should be evaluated against one frozen boundary, with the prior close compared against that same boundary. De-cluster consecutive outside closes into breakout episodes. Follow-up begins after the breakout close.

### 3. Post-signal price-path research

Use a common, precisely defined set of confirmed 15M signals. Separate bullish and bearish signals and preserve the original signal timestamp.

Study:
- Direct continuation versus pullback-first paths.
- MFE, MAE, net movement and time to meaningful movement.
- Frequency and depth of pullbacks and retests.
- Time to retest, retest candle sizes, and whether retests hold or fail.
- 1M, 3M, 5M and 15M candle range, body and wick behaviour around the signal and retest.
- Signal outcomes across trend, range, volatility and post-impulse environments.

Only use information available at the signal close. Future observations must begin after confirmation. Report overlapping-event effects and sample sizes.

### 4. Entry execution timeframe comparison

Compare 1M, 3M, 5M and 15M execution using the **same completed 15M signals**, not separate signal sets.

For each execution timeframe, investigate:
- Earliest eligible entry time and delay from signal confirmation.
- Entry price relative to signal close and subsequent market prices.
- Movement while waiting: favourable and adverse excursion.
- Entry opportunity/missed-entry frequency under explicit entry rules.
- Retest/confirmation availability and fill assumptions.
- Candle-size and wick behaviour at execution.
- Fee, spread, slippage, funding and order-type implications when later modelling execution.

The 1M series is the execution reference for path measurement. Resampled 3M, 5M and 15M execution candles must be aligned causally and must not use candles that began before signal confirmation. Compare like-for-like signals and identical follow-up horizons. Do not assume faster execution is better.

### 5. Entry method comparison

After the post-signal and retest evidence is available, define and compare candidate entry methods:
- Immediate next-eligible-candle entry.
- Pullback/limit entry.
- Retest entry at the relevant signal or breakout level.
- Confirmation entry after a completed lower-timeframe candle.

Specify expiry, fill conditions, missed fills, partial fills and adverse selection. Keep signal generation separate from entry execution.

### 6. Market-environment conditioning

Compare signal and entry behaviour across:
- 1D broad environment.
- 4H trend, range and no-trade regimes.
- Volatility states, with causal thresholds reserved for any future live classifier.
- Post-pump/dump conditions.
- Upper/lower range boundary versus channel middle.

Check whether behaviour is consistent across all five assets or whether evidence supports asset-specific treatment.

### 7. Risk, exit and portfolio research

Only after the preceding evidence:
- Form hypotheses for structure-based, volatility-based and hybrid stops.
- Compare fixed-R, structure-based, partial and trailing exits.
- Maintain consistent portfolio dollar risk; wider stops imply smaller position sizes.
- Include fees, spread, slippage, funding, fill uncertainty and intrabar stop/target ordering.
- Evaluate net expectancy, drawdown, exposure, robustness and chronological out-of-sample performance, not just gross return or trade count.

## Methodology safeguards

1. Keep Price Action V1 separate from older OKX Scalping and Adaptive Bot projects unless evidence establishes a connection.
2. Preserve the existing data-provenance caveat: the five 1M datasets have passed prior quality/alignment checks, but their original exchange/API and instrument identity are not independently verified.
3. Use common timestamps and complete bars; do not forward-fill or fabricate candles.
4. Distinguish event confirmation time from the earlier intrabar high/low that may have contributed to the signal.
5. No lookahead: a signal is usable only after its candle closes; all follow-up begins afterward.
6. Freeze event boundaries/levels when required so later channel updates cannot rewrite the historical trigger.
7. De-cluster repeated events and report both raw and appropriately non-overlapping counts where informative.
8. Treat overlapping follow-up windows as dependent observations.
9. Report sample sizes, missing/incomplete horizons, thresholds and all event definitions.
10. Descriptive movement, MFE/MAE and target-touch frequencies are not proof of executable profitability.
11. Full-sample quantiles are exploratory and retrospective, not live thresholds.
12. Do not run backtests or modify local data/files without explicit user authorization.

## Current next action

Continue with the read-only sideways boundary-rejection movement study. Review its methodology and output before proceeding to breakout continuation/retests, then post-signal price paths and execution timeframe comparison.

## Research status

This document records the agreed roadmap and methodology intentions. It does not claim that the planned studies have been completed or that any entry timeframe, entry method, stop or target has been selected.
