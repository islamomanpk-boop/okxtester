# Breakout Prior-Test Count Research — V1 Plan

**Date:** 2026-11-24
**Branch:** price-action-v1
**Status:** Approved research direction; specification must be frozen before implementation.
**Assets:** BTC, ETH, SOL, DOGE, AVAX.

## 1. Research question

Does the number of distinct prior tests and rejections at a resistance or support boundary affect the subsequent breakout or breakdown?

Compare:
- Direct breakout: zero prior confirmed rejection episodes.
- One prior rejection episode.
- Two prior rejection episodes.
- Three or more prior rejection episodes.

Run the mirrored analysis for upper resistance breakouts and lower support breakdowns.

This question has not been answered by the original breakout study or matched-control V2.

## 2. Preserve the original signal definition

Use the recovered timing-corrected original breakout event engine as the immutable reference.

- Preserve the accepted 15M signal and frozen 4H channel methodology.
- Preserve all five assets and strict P25 / broad P40 definitions.
- Preserve the accepted event counts and thresholds.
- Do not add a previous-sideways gate, cooldown, or de-clustering to the reproduction gate.
- Signal is confirmed at the completed 15M close.
- Follow-up begins at the next eligible 1M candle.
- Never modify the recovered original script.

## 3. Define prior tests without candle-count inflation

A test is a distinct price interaction with the same frozen boundary, not an individual candle touching it.

Track two quantities separately:
1. Boundary-contact episodes.
2. Confirmed rejection episodes.

For upper resistance, identify contact near the frozen upper boundary followed by a completed 15M close back inside the channel. Mirror the rule for lower support.

A new episode cannot begin until price has first moved sufficiently away from the boundary. Freeze the primary separation rule and sensitivity alternatives in the implementation specification before calculation.

Do not count consecutive candles in one continuous touch as separate tests.

For the first version, keep the boundary fixed to the same 4H snapshot. Do not silently combine tests against different refreshed boundaries.

Record the exact timestamps, prices, rejection depth, and separation between episodes so the classification can be audited.

## 4. Cohorts

Classify each accepted breakout event by the number of distinct prior confirmed rejection episodes at its relevant frozen boundary:

- 0
- 1
- 2
- 3+

Also retain contact-only counts and rejection characteristics. Do not merge contact-only events with confirmed rejections.

## 5. Outcomes

From the next eligible 1M open, measure at 15M, 1H, 4H and 12H:

- Directional MFE and non-positive MAE.
- Net directional close-to-close movement.
- Mean, median, P75 and P90.
- Return-inside and ending-inside-channel frequencies.
- Continuation thresholds: 0.25%, 0.50%, 1.00%, 1.50%, 2.00%.
- Time to each threshold.
- Time to first adverse move and first meaningful continuation.
- Breakout candle range, body, wick proportions and close location.
- Prior rejection count, rejection depth and time since last rejection.

Report sample sizes and incomplete-follow-up exclusions for every group.

## 6. Comparability and robustness

Compare groups within asset, direction and strict/broad definition. Report pooled results only alongside asset-level results.

Inspect differences in volatility, channel width, boundary distance, breakout candle size and calendar period. Do not interpret raw group differences as causal effects.

Use time-block or event-cluster uncertainty intervals. Account for overlapping events and overlapping follow-up windows.

Run sensitivity checks for the touch-zone and episode-separation definitions. Freeze primary definitions before viewing outcomes.

## 7. Separate post-breakout retest experiment

After the prior-test-count study, run a separate study of what happens after the breakout:

- No retest before continuation.
- Retest of the broken boundary that holds.
- Retest that penetrates and recovers.
- Retest that fails and returns inside the old channel.
- Multiple post-breakout retests.

Measure time to retest, depth, duration near the level, hold/failure, subsequent MFE/MAE and net movement.

Do not mix post-breakout retests with pre-breakout resistance/support tests.

## 8. Safeguards

- No lookahead: all prior tests must be known by the breakout confirmation close.
- Freeze levels and event timestamps.
- Require exact timestamp continuity; do not bridge missing candles.
- Preserve all original scripts and previous research outputs.
- New versioned scripts and unique output names only.
- No strategy simulation, profitability claims or strategy selection from descriptive results alone.
- Volume analysis remains excluded until source volume units are verified.
- No local market-data modification.

## 9. Sequence

1. Freeze the operational definitions and sensitivity rules.
2. Build a read-only event-classification diagnostic.
3. Audit sample counts and manually inspect representative event sequences.
4. Run the full descriptive outcome comparison only after classification passes.
5. Then conduct the separate post-breakout retest study.
6. Only after these findings decide which entry behaviours merit a trading backtest.

**No empirical results are claimed by this plan.**
