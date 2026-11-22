# Expanded Price-Action Behaviour Research Plan — Impulses, Retracements, Sideways Markets and Weekly Movement

**Project:** Price Action V1  
**Branch:** `price-action-v1`  
**Date:** 2026-11-22  
**Status:** Research plan only. No backtests, strategy experiments, data transformations, or changes to local files are authorized.

## Purpose

Expand the five-asset research programme (BTC, ETH, SOL, DOGE, AVAX) beyond general volatility. Study how price expands, retraces, consolidates, reverses, and distributes movement across daily, weekly, 4H, 15M and (where needed for execution context) 1M observations.

The objective is to understand market behaviour and build evidence for later market-regime and risk-management design. Descriptive movement is not automatically executable opportunity or strategy profitability.

## A. Impulse, pump/dump and post-move recovery

### Questions

- After a strong upward or downward move, how much does price retrace?
- Does price continue in the original direction, consolidate, or reverse?
- How long until the first 1%, 2%, 3%, 5% retracement from the extreme?
- How much of the original impulse is given back?
- How often does price fully erase the impulse or cross its starting level?
- Do outcomes differ by coin, impulse size, direction, volatility state, weekday, and time of day?

### Event definitions to keep separate

1. **Close-to-close impulse:** percentage change between consecutive daily closes, or between closes separated by a defined multi-day horizon.
2. **Intraperiod excursion:** movement from a pre-event reference close to a subsequent high (pump) or low (dump). This captures path extremes but is not equivalent to a close-to-close return.
3. **Multi-day impulse:** cumulative close-to-close move over fixed horizons (e.g. 2, 3, 5 and 7 days), plus a separate rolling-extreme measure if useful.

Do not mix these event types in one statistic. Define the event start, reference price, threshold crossing and event extreme explicitly.

### Candidate thresholds and follow-up horizons

- Daily close-to-close absolute thresholds: 2%, 3%, 5%, 7%, 10%.
- Multi-day absolute thresholds: 3%, 5%, 7%, 10%, 15% over separately reported 2-, 3-, 5- and 7-day horizons.
- Follow-up observations after event confirmation: 4H, 12H, 24H, 48H, 72H and 7 days.

### Required outcome metrics

For bullish events, measure peak-to-subsequent-trough retracement; for bearish events, trough-to-subsequent-peak rebound. Report both:
- percentage move from the extreme (e.g. pullback from the peak);
- fraction of the original impulse surrendered or recovered.

Also measure continuation beyond the original extreme, time to each retracement/rebound threshold, full reversal, maximum favourable/adverse excursion after event confirmation, and whether the event reaches a new extreme before retracing.

Report median, mean, P10/P25/P75/P90, event counts, and sample dates. Avoid relying on averages alone.

### Event-overlap and selection safeguards

- State whether events are overlapping or non-overlapping.
- For the primary event study, use a reproducible event-clustering rule so one long move does not create many nearly identical observations.
- A threshold crossing is only known after the candle closes; do not pretend it was known at the candle's start.
- Follow-up windows must begin after the event is confirmed. Do not include pre-confirmation movement.
- Include events that continue without a meaningful retracement; do not select only events that pull back.
- Separate full-sample descriptive results from any later causal, train/validation/OOS analysis.

## B. Sideways/ranging behaviour on 4H and 15M

### Questions

- How often does each asset spend time in objectively defined ranges?
- How long do ranges last?
- What is the typical range height in percentage and volatility-normalized units?
- Within a range, how far do price excursions travel from the range midpoint, upper boundary and lower boundary?
- How often do boundary tests hold, break and fail?
- How much movement occurs inside a range on 4H versus 15M?
- Are 15M swings mostly noise inside a 4H range, or do they provide meaningful internal structure?

### Multi-timeframe structure

- **4H:** primary research timeframe for classifying broader local trend/range structure.
- **15M:** measure internal oscillations, boundary tests, pullbacks and failed breaks inside the 4H context.
- Keep the 15M measurements nested inside the 4H classification that was available at that time when later developing causal rules.
- Use 1M only where needed to study intrabar ordering/fill feasibility, not to redefine the 4H/15M market regime.

### Range definitions to compare

Do not assume one definition is correct. Compare several transparent, price-based definitions:
1. Rolling high-low channel over fixed 4H bar counts.
2. Swing-high/swing-low bounded structure with a documented pivot confirmation delay.
3. Low directional efficiency / high candle overlap over a fixed window, combined with bounded range expansion.

A pivot must not be treated as known before its confirmation bars have completed. Avoid using future pivots to create a live signal in retrospective labels.

### Range metrics

For each range episode, report:
- duration in 4H bars and 15M bars;
- total height as a percentage of range start or midpoint;
- median and percentile 4H and 15M candle ranges;
- average and median absolute close-to-close movement;
- upper/lower boundary test counts;
- maximum penetration beyond each boundary;
- time spent near upper, middle and lower thirds;
- maximum adverse/favourable excursion from range boundaries;
- breakout frequency, failed-breakout frequency and post-breakout follow-through;
- range expansion/contraction before resolution.

Report distributions and sample sizes by coin. A high-low range alone is not a tradable profit estimate.

## C. Weekly movement and movement distribution

### Questions

- How much does each coin typically travel from weekly open to weekly high and low?
- When during the week do the high and low tend to occur?
- How much of the eventual weekly range has already occurred by each day?
- How large are pullbacks during a weekly directional move?
- Does a large weekly move tend to continue, stall, or retrace?
- Are weekly moves concentrated in a few large 4H/15M impulses or spread across many smaller swings?

### Weekly metrics

For complete UTC weeks (Monday through Sunday), calculate separately:
- weekly high-low range percentage;
- weekly close-to-close return;
- maximum upside excursion from weekly open;
- maximum downside excursion from weekly open;
- order and timing of weekly high and low;
- maximum retracement from the weekly high and rebound from the weekly low;
- daily and 4H contributions to the final weekly range;
- proportion of final weekly high-low range observed by the end of each day;
- weekly path efficiency (absolute net close movement divided by total absolute close-to-close path), clearly defined;
- number and size of meaningful 4H directional legs and pullbacks.

Do not infer that the full weekly range could have been captured by a single trade. Report path and timing.

## D. Cross-cutting comparisons

For all studies:
- Compare BTC, ETH, SOL, DOGE and AVAX individually and side by side.
- Segment outcomes by bullish/bearish direction and event/range size.
- Where sample size permits, compare low/normal/high volatility contexts, with thresholds calculated only from information available before the observation if making causal claims.
- Compare chronological subperiods; do not let full-sample averages hide changing behaviour.
- Report event/episode counts and uncertainty; flag thin samples.
- Keep UTC timestamps consistent and preserve complete-bar requirements.
- Retain the source-provenance caveat: intended OKX market configuration does not independently prove the source/instrument of the 1M candles.

## E. How this informs later system design

The existing architecture remains:
- 1D: broad market environment.
- 4H: regime (trend, range, no-trade).
- 15M: signal generation.
- 1M: entry/stop/target execution simulation after signal completion.

Potential later hypotheses (not decisions):
- Use market structure to define trade invalidation.
- Use volatility as a buffer or risk-distance context, not as a substitute for structure.
- Compare structure-only, volatility-only and hybrid stops.
- Compare fixed-R, structure-based, partial-exit and trailing target management.
- Keep a shared portfolio dollar-risk budget. Wider stops require smaller position sizes.
- Include fees, slippage, funding, fill assumptions, partial/missed fills, and intrabar stop/target collision rules in any future authorized testing.

## Research order

1. Impulse and post-impulse retracement/recovery study.
2. 4H range identification and duration study.
3. 15M movement and oscillation inside 4H ranges.
4. Breakout, failed-breakout and post-breakout follow-through study.
5. Weekly path and movement-distribution study.
6. Integrate findings into a market-structure research chapter.
7. Only after research review, propose candidate stop/target hypotheses. No backtesting until the user explicitly authorizes it.

## Non-negotiable interpretation limits

- A pump/dump threshold event is not evidence of manipulation.
- A retracement is not necessarily a reversal.
- Range movement is not automatically capturable profit.
- Weekly high-low range is not a weekly trade return.
- A 15M candle's high-low movement does not prove an order could have entered and exited at those prices.
- Retrospective regime labels must not be reused as live signals without causal redesign.
- Descriptive statistics do not establish strategy profitability.

**Decision:** Expand the research agenda to include impulse recovery, 4H/15M range behaviour, breakout quality, and weekly movement distribution. Continue read-only research only.