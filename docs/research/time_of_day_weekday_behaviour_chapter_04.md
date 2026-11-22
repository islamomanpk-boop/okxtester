# Time-of-Day and Day-of-Week Behaviour — Chapter 4

**Date:** 2026-11-22  
**Project:** OKX Price Action Research V1  
**Status:** Desk-research framework; no local empirical results yet  
**Branch:** `price-action-v1`

## 1. Purpose

Study whether BTC, ETH, SOL, DOGE, and AVAX exhibit repeatable differences in movement, volatility, trading activity, and extreme-event frequency across UTC hours and weekdays.

This is not a search for a calendar rule to trade blindly. The key question is whether time-of-week adds stable descriptive or predictive information after controlling for volatility regime, asset, and market-wide conditions.

## 2. What published research reports

### 2.1 Broad cross-exchange intraday patterns

Brauneis, Mestel, and Theissen (2025; published online in 2024), “The crypto world trades at tea time: intraday evidence from centralized exchanges across the globe,” examine 1,940 currency pairs across 38 exchanges. They report pronounced time-of-day patterns in trading activity, volatility, and illiquidity, with these measures generally peaking around 16:00–17:00 UTC. Their sample suggests commonality across exchanges and pairs, while also identifying local factors.  
DOI: https://doi.org/10.1007/s11156-024-01304-1

**Interpretation:** 16:00–17:00 UTC is a reasonable hypothesis window to inspect in our data, not a pre-approved trading window. The study's pairs, exchanges, and sample do not prove that our five OKX perpetual instruments have the same pattern.

### 2.2 BTC and ETH periodicity

Hansen, Kim, and Kimbrough (2024), “Periodicity in Cryptocurrency Volatility and Liquidity,” *Journal of Financial Econometrics*, 22(1), 224–251, study BTC and ETH using Coinbase Pro, Binance, and Uniswap V2 data. They report systematic patterns in volatility and volume by weekday, hour, and within-hour interval.  
DOI: https://doi.org/10.1093/jjfinec/nbac034

**Interpretation:** Analyze more than daily candles. Hourly and intrahour variation can be hidden by daily aggregation. The study does not establish a profitable hour-of-day effect.

### 2.3 Day-of-week effects may be localized

Aalipour, Mehdian, and Rezvanian (2026), “Are day-of-the-week effects in cryptocurrencies real? Intraday evidence from active and less active cryptocurrencies,” *Finance Research Letters*, 110634, use hourly data for four active and eight less-active cryptocurrencies. They report that apparent weekday effects are driven by a limited number of intraday intervals, are asset-specific and short-lived, and are not persistent broad daily effects.  
DOI: https://doi.org/10.1016/j.frl.2026.110634

**Interpretation:** Do not assume a whole weekday is bullish, bearish, quiet, or volatile based on a daily average. A weekday difference may be driven by a few hours and may not persist.

### 2.4 Jump timing

Saef et al. (2024), “Understanding temporal dynamics of jumps in cryptocurrency markets,” report hourly seasonality in detected jumps in their tick-data sample, with more jumps around 13:00–17:00 UTC and fewer during 01:00–07:00 UTC. The authors' sample and jump-detection method are specific; 1-minute OHLCV cannot reproduce tick-level jump identification exactly.  
DOI: https://doi.org/10.1007/s42521-024-00116-1

## 3. What we should measure locally

Use UTC as the canonical time standard. Derive hour and weekday from the candle timestamp only after confirming whether the stored timestamp is the candle open time and that it represents UTC.

For every asset, calculate separately:

### By UTC hour (00 through 23)
- Number of observations and valid trading days.
- Mean and median absolute 1-minute, 15-minute, and hourly returns.
- Mean and median high-low range.
- Realized volatility from 1-minute log returns.
- 90th, 95th, and 99th percentiles of absolute returns and range.
- Frequency of large positive and negative moves using both fixed and trailing-volatility-normalized thresholds.
- Volume distribution only after confirming its unit and meaning.
- Share of hours classified as quiet, trending, choppy, or shock, once those labels are defined causally.

### By weekday (Monday through Sunday, UTC)
- Mean and median daily range.
- Mean, median, and standard deviation of close-to-close return.
- Absolute return and realized volatility.
- Positive/negative day frequency.
- Extreme-move counts and jump-like event counts.
- Weekly high-low range and close-to-close return.
- Sample counts and uncertainty intervals.

### Hour × weekday interaction
- Build a 7-by-24 matrix for volatility, range, absolute return, and event frequency.
- Report counts in each cell.
- Use this to discover whether a weekday pattern is concentrated in particular hours.
- Do not overinterpret thin cells or noisy extremes.

## 4. Separating activity from direction

Time-of-day may help forecast *how much* price moves without forecasting *which direction* it moves.

Therefore keep separate outcomes:
1. Signed return (direction).
2. Absolute return (movement magnitude).
3. High-low range (intraperiod excursion).
4. Realized volatility (path variation).
5. Volume/activity (only if semantics are verified).
6. Net trading opportunity after realistic execution costs (only in a later, separately approved study).

A high-volatility hour is not automatically a good trading hour. It can bring wider adverse excursions, slippage, and false breakouts. A low-volatility hour may have insufficient movement to cover fees.

## 5. Weekends and weekday comparisons

Do not simply compare one pooled weekend average with one weekday average. Report:
- Saturday and Sunday separately.
- Each weekday separately.
- Weekend vs weekday as a secondary aggregate.
- Per-asset results and equal-weighted five-asset summaries.
- Results by year / chronological subperiod where sample size allows.
- Results conditional on volatility and market regime.

Potential confounders include changes in market composition, macro/news shocks, exchange conditions, funding schedules, and major institutional participation. A weekday association is descriptive unless a carefully designed analysis supports a stronger claim.

## 6. Time-zone and daylight-saving safeguards

- Store and analyze timestamps in UTC.
- Do not convert historical bars to a fixed local offset before calculating hour-of-day patterns.
- If interpreting results relative to London or New York market hours, account for daylight-saving transitions. UTC times of local sessions can shift seasonally.
- Keep candle-open timestamp conventions consistent; a 1-minute candle stamped 14:00 may represent the interval beginning at 14:00, not the interval ending then.
- Exclude incomplete boundary intervals when aggregating hourly or daily candles.

## 7. Statistical safeguards

- Normalize hourly volatility by an appropriate asset-specific baseline; otherwise high-volatility coins can dominate.
- Compare both raw and volatility-normalized event frequencies.
- Use confidence intervals or day-block bootstrap methods to reflect serial dependence; do not treat every minute as an independent observation.
- Correct for multiple comparisons when testing 24 hours × 7 weekdays × 5 assets × several outcomes.
- Prefer effect sizes and stability over p-values alone.
- Use a development period to discover hypotheses, validation to assess them, and preserve the final 20% as untouched out-of-sample data.
- Check whether apparent patterns survive subperiod analysis and reasonable alternative definitions.
- Do not use the final out-of-sample period to choose the best hour or weekday.
- Report all tested comparisons to reduce selection bias.

## 8. Questions for our five coins

1. Does each asset have a repeatable UTC intraday volatility profile?
2. Do BTC, ETH, SOL, DOGE, and AVAX peak at the same hours, or are their patterns different?
3. Are large upward and downward moves concentrated in the same hours?
4. Does the 16:00–17:00 UTC activity/volatility peak appear in our OKX data?
5. Are weekends less volatile, more volatile, or simply different in their intraday distribution?
6. Are any weekday differences persistent after conditioning on volatility regime?
7. Are calendar effects driven by a few hours rather than full days?
8. Do time-of-day effects differ between trend, quiet range, choppy range, and shock states?
9. Do extreme events cluster at particular hours, and are those hours also associated with higher adverse excursion?
10. Are observed patterns stable across the chronological development, validation, and untouched out-of-sample periods?

## 9. Implications for the research programme

Time-of-day and weekday should initially be **descriptive context**, not hard-coded trade filters. If local results show a stable difference, it may justify a later hypothesis test such as:
- whether execution costs or slippage differ by hour;
- whether event follow-through differs by hour;
- whether range breakouts fail more often during certain conditions;
- whether the same signal has different MFE/MAE distributions by hour.

Any later strategy test must use causal features, realistic costs, and a pre-defined evaluation protocol. Do not optimize an hour filter against the full history.

## 10. Current conclusions and next step

- Published research finds intraday patterns in crypto volatility, volume, liquidity, and jump frequency.
- A broad cross-exchange study reports activity, volatility, and illiquidity peaks around 16:00–17:00 UTC; this is a hypothesis for our OKX sample, not a guaranteed local pattern.
- Recent weekday research warns that calendar effects may be concentrated in a few hours, asset-specific, and short-lived.
- Direction, movement magnitude, range, realized volatility, and activity must be measured separately.
- No hour or weekday is approved as a trade/no-trade rule by this chapter.

**Next step:** Review cross-asset correlation and conditional co-movement, then audit local data lineage before any empirical calculations. The telemetry exit batch remains paused. No scripts, tests, backtests, or experiments are authorized by this chapter.

## References

1. Brauneis, A., Mestel, R., & Theissen, E. (2025). https://doi.org/10.1007/s11156-024-01304-1
2. Hansen, P. R., Kim, C., & Kimbrough, W. (2024). https://doi.org/10.1093/jjfinec/nbac034
3. Aalipour, N., Mehdian, S., & Rezvanian, R. (2026). https://doi.org/10.1016/j.frl.2026.110634
4. Saef, D., Nagy, O., Sizov, S., & Härdle, W. (2024). https://doi.org/10.1007/s42521-024-00116-1
