# Sideways-Market Behaviour Research — Chapter 2

**Date:** 2026-11-22  
**Project:** OKX Price Action Research V1  
**Status:** Desk-research framework; no local empirical results yet  
**Branch:** `price-action-v1`

## 1. Purpose

Before designing a range-trading rule or a sideways-market filter, distinguish different market conditions that are often grouped together as “sideways”. A flat net return does not imply a quiet or safe market: price can travel a large distance in both directions and finish near its starting point.

This chapter defines candidate categories, measurable observations, research questions, and safeguards. It does **not** select thresholds, claim an edge, or authorize a backtest.

## 2. Working taxonomy (hypotheses to test)

1. **Quiet / compressed range** — relatively small realized movement and a narrow high-low envelope; repeated rotation may occur, but trading costs can consume small moves.
2. **Wide / orderly range** — clear upper and lower boundaries with repeated rotations; the range is wider, but boundary reactions may be less predictable than they look in hindsight.
3. **Volatile / choppy sideways** — large intraperiod movement but little net directional progress; frequent overlap, reversals, and stop-distance expansion can make it especially costly.
4. **Range-to-trend transition** — compression or repeated boundary tests followed by expansion and directional structure change.
5. **Trend pause / consolidation** — a pause inside a larger directional structure; it should not automatically be treated as a fully independent range.
6. **Shock / disorderly market** — abrupt displacement, gaps or fast continuation, possibly with unstable liquidity; candidate no-trade condition until conditions normalize.

These labels describe observable behaviour, not hidden certainty about what price will do next. A market can move between categories; classification should allow an “uncertain / transition” state.

## 3. Why a single sideways label is inadequate

A close-to-close return near zero can coexist with a large high-low range. Therefore measure at least three separate dimensions:

- **Directional progress:** absolute net return over a fixed window, and signed return.
- **Total movement / volatility:** realized volatility from intrabar returns and high-low range.
- **Path efficiency:** net displacement divided by the sum of absolute price changes over the same window. Low efficiency indicates substantial back-and-forth movement relative to net progress.

Use consistent windows and calculate all features using only information available at the decision time. Do not interpret low efficiency alone as a trade signal.

## 4. Candidate observable features

For each asset, on 15M and 4H bars (with 1M data retained for execution/path analysis):

- Rolling high-low envelope width, expressed as a percentage and normalized by prior ATR.
- Realized volatility and its percentile relative to a trailing historical window.
- Absolute net return over the same window.
- Path efficiency / directional efficiency.
- Confirmed swing highs and lows; whether structure is making higher highs/lows, lower highs/lows, or overlapping swings.
- Number of distinct tests near candidate range boundaries, with a pre-defined tolerance.
- Close location within the rolling range; wick penetration versus candle close beyond a boundary.
- Boundary rejection distance and time spent near the boundary.
- Breakout follow-through, maximum favourable excursion, adverse excursion, and return back inside the range.
- Range duration, width stability, and volatility expansion/contraction.

These are candidate measurements, not a final indicator stack. The primary Model A remains pure OHLC price action. ATR-normalized quantities may be used as scale descriptors where already specified; they must not silently introduce directional indicator filters.

## 5. Range boundaries and false-breakout research

A boundary must be defined without looking forward. Candidate methods to compare separately:

- A rolling high/low from a fixed, completed-bar lookback.
- A structure boundary from confirmed swing points.
- A consolidation envelope defined by a fixed set of completed bars.

For each boundary interaction, record:

- Whether price only wicks through, or a completed candle closes outside.
- Penetration size relative to prior ATR / range width.
- Whether the next bars continue outside, stall, or close back inside.
- Time to continuation or re-entry.
- Maximum favourable and adverse excursion after the first boundary break.
- Whether the move reaches a pre-defined objective before invalidation.
- Whether the same event occurs across BTC, ETH, SOL, DOGE, and AVAX.

A **false breakout** must be operationally defined before measurement. For example, one candidate definition is a completed close outside a previously known boundary followed by a close back inside within a fixed number of bars, without reaching a pre-defined continuation threshold. The look-forward window and continuation threshold are research parameters, not facts; compare a small number of pre-registered definitions and report sensitivity.

Avoid hindsight bias: do not draw the range using bars that occur after the alleged breakout.

## 6. Candidate behaviour matrix (not yet validated)

| Observed condition | Candidate interpretation | Research treatment |
|---|---|---|
| Narrow range + low realized volatility + low net return | Quiet compression | Measure duration and later expansion; do not assume a breakout is imminent |
| Wide envelope + repeated reactions + low net progress | Wide range | Measure boundary rotation and net-after-cost opportunity |
| High realized movement + low net progress + low path efficiency | Choppy sideways | Test as a potential no-trade condition |
| Range contraction followed by expansion and confirmed structure break | Possible transition | Measure continuation and failure rates |
| Pullback / pause while higher-timeframe structure remains directional | Trend consolidation | Keep distinct from a standalone range |
| Extreme volatility / abrupt displacement | Shock state | Measure recovery time and execution risk; consider temporary no-trade |

## 7. Research questions for the five OKX instruments

1. How often does each category occur, and how long do episodes last?
2. Does the distribution differ between BTC, ETH, SOL, DOGE, and AVAX?
3. Are ranges narrower in percentage terms for BTC, or do normalized measures tell a different story?
4. How often are range boundaries tested before a confirmed break?
5. What fraction of boundary breaks fail under each pre-defined false-breakout rule?
6. How do follow-through and re-entry rates vary with volatility, range width, time of day, and asset?
7. Do choppy episodes have higher stop-hit frequency or worse net outcomes after fees and slippage?
8. Does a sideways classification on 4H agree with 15M behaviour, or does the lower timeframe frequently appear choppy during a higher-timeframe trend?
9. Are transitions synchronized across the five assets, or do some assets lead/lag? Any lead/lag observation is descriptive, not causal.
10. How stable are results across chronological development, validation, and untouched out-of-sample periods?

## 8. Method safeguards

- Use completed candles only. A swing point is unavailable until its confirmation rule has elapsed.
- At time t, calculate rolling thresholds only from data available up to t; never use full-sample quantiles to classify historical bars.
- Use a minimum episode duration and hysteresis / persistence rule to reduce rapid label flipping. Choose these only through development data and report sensitivity.
- Keep “uncertain / transition” available rather than forcing every bar into trend or range.
- Report asset-level and pooled results; do not let BTC dominate pooled statistics.
- Use common-date comparisons as well as each asset's full valid sample.
- Separate signal opportunity from tradability: range movement must exceed fees, slippage, funding (where applicable), and execution uncertainty.
- Do not use the final 20% out-of-sample period to select definitions or thresholds.
- Do not treat a hidden-state model, clustering output, or visual chart label as a profitable strategy.
- Avoid optimizing many thresholds. Pre-register a small number of definitions and report all tested variants.

## 9. Literature reviewed

### Pennoni, Bartolucci, Forte & Ametrano (first published 10 November 2021)
“Exploring the dependencies among main cryptocurrency log-returns: A hidden Markov model.” *Economic Notes*, 51(1), e12193. DOI: https://doi.org/10.1111/ecno.12193

The study models daily returns of BTC, ETH, XRP, LTC, and BCH jointly with latent regimes, allowing regime-specific means and covariance matrices. It reports heterogeneous correlation structure and medium-term structural change in BTC correlations with other cryptocurrencies. Relevance: market states and cross-asset dependence can vary; a single fixed correlation or universal range label should not be assumed. Limitation: daily data and a different asset set / sample; it does not validate our 15M/4H range definitions or OKX trading rules.

### Figà-Talamanca, Focardi & Patacca (2021)
“Regime switches and commonalities of the cryptocurrencies asset class.” *The North American Journal of Economics and Finance*, 57, 101425. DOI: https://doi.org/10.1016/j.najef.2021.101425

The article applies hidden Markov models to individual and joint cryptocurrency regimes and reports multiple regimes associated with increasing volatility states. Relevance: volatility regimes and common states across assets are legitimate research dimensions. Limitation: regime identification is not equivalent to actionable range boundaries or profitable range trading.

### Koki, Leonardos & Piliouras (2022)
“Exploring the predictability of cryptocurrencies via Bayesian hidden Markov models.” *Research in International Business and Finance*, 59, 101554. DOI: https://doi.org/10.1016/j.ribaf.2021.101554

The published abstract describes state-dependent return behaviour and distinguishes bull, bear, and calm regimes. Relevance: “calm” or low-volatility conditions should be considered separately from directional bull/bear states. Limitation: model-based state labels do not prove that a rule using them will be tradable after costs.

### Wafi, El-Halaby & Aboul-Dahab (published 26 October 2026)
“Regime-dependent bitcoin volatility forecasting under alternative information sets: evidence from econometric, deep learning, and hybrid models.” *Digital Finance*. DOI: https://doi.org/10.1007/s42521-026-00229-9

Using daily BTC data from 1 February 2018 to 19 July 2025, the study reports that forecasting performance differs between normal and crisis regimes and that no model dominates in every condition. Relevance: regime-specific evaluation and strict rolling out-of-sample comparison matter. Limitation: it forecasts volatility, not range-trading returns, and concerns BTC rather than our five OKX perpetual instruments.

## 10. Current conclusions

- “Sideways” should be decomposed into at least quiet compression, wide/orderly range, volatile/choppy sideways, trend consolidation, transition, and shock.
- Net return alone is insufficient to describe a range. Combine directional progress, total movement, and path efficiency.
- Range boundaries and false breakouts must be defined causally before measuring them.
- The literature supports time-varying regimes and heterogeneous cross-asset dependence, but does not tell us which thresholds work for these five instruments.
- No range strategy, filter threshold, or trade rule is approved by this chapter.

## 11. Next step (no execution authorized)

Continue desk research on pump/dump and jump behaviour, then review data lineage and provenance before any local descriptive calculations. The previously paused 66-experiment telemetry batch remains paused. Do not launch scripts, tests, backtests, or new experiments without explicit user approval.

## References

- https://doi.org/10.1111/ecno.12193
- https://doi.org/10.1016/j.najef.2021.101425
- https://doi.org/10.1016/j.ribaf.2021.101554
- https://doi.org/10.1007/s42521-026-00229-9
