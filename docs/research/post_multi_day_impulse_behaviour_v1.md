# Post-Multi-Day Impulse Behaviour — Five Assets (V1)

**Status:** Descriptive research only. No backtest, trade simulation, or local file changes.  
**Assets:** BTC, ETH, SOL, DOGE, AVAX  
**Data:** 394 complete UTC daily candles per asset; 569,125 common 1-minute timestamps.  
**Triggers:** 3-day and 5-day close-to-close pumps/dumps of at least 5% or 10%.  
**Follow-up:** 1, 3 and 7 complete days after the trigger close.

## Method

A trigger is confirmed at day t close when close[t] / close[t-N] - 1 reaches the specified threshold. Follow-up measurements begin after that close.

For each event and horizon:
- Forward close return = close[t+h] / close[t] - 1.
- Pump continuation = maximum future high above the trigger close.
- Pump pullback = maximum future low below the trigger close.
- Dump continuation = maximum future low below the trigger close.
- Dump rebound = maximum future high above the trigger close.
- Full close reversal means a future daily close crosses the close from immediately before the N-day impulse. For a pump, a future close at or below close[t-N]; for a dump, a future close at or above close[t-N].

The printed `close` statistic is the median **signed** forward close return. Thus a negative number after a dump means the price continued lower on a close-to-close basis.

Raw events include overlapping triggers. Non-overlapping events are selected chronologically, greedily excluding another event until the previous event's impulse window plus the follow-up horizon has elapsed. This is a sensitivity analysis, not a unique or universally optimal event-clustering method.

Only events with a complete 7-day follow-up were retained for all horizons, keeping the candidate set consistent across 1D, 3D and 7D summaries.

## Main comparison: 3-day impulse >=5%, next 7 days

### After pumps

| Asset | Non-overlap n | Median forward close | Median continuation | Median pullback | Full close reversal |
|---|---:|---:|---:|---:|---:|
| BTC | 10 | -0.83% | 2.69% | 4.45% | 20.0% |
| ETH | 19 | -1.18% | 3.90% | 7.93% | 42.1% |
| SOL | 17 | -0.60% | 5.93% | 6.74% | 41.2% |
| DOGE | 19 | -3.54% | 3.33% | 8.03% | 47.4% |
| AVAX | 23 | -2.53% | 5.43% | 10.59% | 52.2% |

### After dumps

| Asset | Non-overlap n | Median forward close | Median downside continuation | Median rebound | Full close reversal |
|---|---:|---:|---:|---:|---:|
| BTC | 12 | -3.28% | 5.73% | 3.09% | 16.7% |
| ETH | 17 | -1.44% | 5.36% | 3.08% | 23.5% |
| SOL | 19 | -2.88% | 8.18% | 4.70% | 15.8% |
| DOGE | 24 | -3.02% | 6.98% | 4.41% | 20.8% |
| AVAX | 21 | -1.30% | 7.17% | 5.59% | 23.8% |

## Additional 5-day impulse >=5%, next 7 days

### After pumps

| Asset | Non-overlap n | Median forward close | Median continuation | Median pullback | Full close reversal |
|---|---:|---:|---:|---:|---:|
| BTC | 11 | +2.35% | 3.48% | 4.85% | 0.0% |
| ETH | 18 | +0.24% | 5.73% | 4.91% | 27.8% |
| SOL | 14 | +2.07% | 10.15% | 3.82% | 28.6% |
| DOGE | 16 | -4.81% | 2.93% | 9.75% | 43.8% |
| AVAX | 17 | -1.82% | 4.63% | 7.18% | 35.3% |

### After dumps

| Asset | Non-overlap n | Median forward close | Median downside continuation | Median rebound | Full close reversal |
|---|---:|---:|---:|---:|---:|
| BTC | 11 | -1.17% | 3.39% | 4.05% | 9.1% |
| ETH | 16 | -2.53% | 7.72% | 3.48% | 18.8% |
| SOL | 18 | -4.62% | 8.33% | 2.81% | 22.2% |
| DOGE | 21 | -1.84% | 7.74% | 4.39% | 9.5% |
| AVAX | 20 | -3.71% | 7.75% | 5.41% | 20.0% |

## Findings and interpretation

1. In the 3D >=5% pump cohort, median post-trigger pullbacks were largest for AVAX (10.59%) and DOGE (8.03%) in the non-overlapping sample. Their full close-reversal proportions were 52.2% and 47.4%.
2. In the same cohort after dumps, SOL had the largest median downside continuation (8.18%). The median signed forward close return was negative for all five assets.
3. The 5D >=5% results show that post-pump behaviour is not uniform across impulse lengths: SOL's median forward close was positive (+2.07%) while DOGE's was negative (-4.81%). This is a reason to keep impulse duration as a separate dimension rather than combine all events.
4. DOGE and AVAX showed large post-pump pullbacks in several comparisons, but this does not establish a profitable short setup. The reported pullback is an extreme intraperiod excursion, not an executable trade result.
5. A full close reversal is deliberately strict and close-based. Intraday highs/lows can cross the pre-impulse reference without a daily close doing so.

## Important limitations and audit notes

- Samples are modest. 10% trigger cohorts often have very few non-overlapping events; their percentages and medians are highly unstable. Do not infer that 0% reversal means reversal cannot happen.
- The non-overlap filter is greedy and chronological. A different event-clustering rule can produce a different sample.
- Trigger thresholds are nested; 10% events are also included in 5% events.
- Continuation and pullback are maximum excursions over the follow-up interval. They can occur in either order; daily OHLC does not reveal the exact intraday sequence.
- The maximum favourable/adverse excursion is not an entry/exit simulation. It ignores fills, fees, slippage, funding, liquidity and stop/target collisions.
- Results are conditional descriptive statistics, not causal proof or forecasts.
- The underlying 1-minute CSV source exchange/API and exact instrument provenance remain unverified.

## Research decision

Do not choose coin-specific SL/TP values from these statistics. They motivate further study of post-impulse path, range regimes and execution feasibility. Next planned topic: objectively defined sideways/ranging conditions on 4H, with 15M internal movement and boundary behaviour. Continue read-only; no backtests without explicit authorization.
