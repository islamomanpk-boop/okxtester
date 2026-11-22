# Literature review 01 — crypto market behavior and research implications
Date: 2026-11-22
Branch: price-action-v1

## Scope and caution
This is a desk-research chapter, not an empirical result from the project's local OKX candles. Published samples, exchanges, instruments, time periods, and sampling frequencies differ from our BTC/ETH/SOL/DOGE/AVAX USDT perpetual data. Use the findings to form hypotheses only. No strategy or time filter is approved by this review.

## 1. Intraday seasonality
Brauneis, Mestel and Theissen, *The crypto world trades at tea time: intraday evidence from centralized exchanges across the globe*, Review of Quantitative Finance and Accounting (2025; published online 2024), DOI: https://doi.org/10.1007/s11156-024-01304-1.
- Sample: 1,940 pairs across 38 centralized exchanges.
- Reports recurring intraday patterns in activity, volatility and illiquidity, with broad peaks around 16:00–17:00 UTC.
- Research implication: measure hourly returns, realized range/volatility, volume (if trustworthy), and liquidity proxies separately for each of our five instruments. Compare UTC hours and weekdays. This is not evidence that 16:00–17:00 UTC is a profitable trading window on OKX.

Hansen, Kim and Kimbrough, *Periodicity in Cryptocurrency Volatility and Liquidity*, Journal of Financial Econometrics 22(1), 224–251 (2024), DOI: https://doi.org/10.1093/jjfinec/nbac034.
- Finds systematic hour-of-day, day-of-week and within-hour patterns in BTC and ETH volatility and volume across CEX/DEX data.
- Research implication: avoid assuming intraday conditions are stationary; estimate patterns by asset and subperiod, and test whether they persist out of sample.

## 2. Jumps and shock behavior
Saef, Nagy, Sizov and Härdle, *Understanding temporal dynamics of jumps in cryptocurrency markets: evidence from tick-by-tick data*, Digital Finance 6, 605–638 (2024), DOI: https://doi.org/10.1007/s42521-024-00116-1. A correction was published in 2025; consult the corrected version before reproducing detailed numerical claims.
- The study reports temporally clustered jumps, negative jumps dominating in its sample, and BTC jumps often preceding jumps in other assets. It also reports intraday concentration of detected jumps.
- Its data are tick-by-tick observations from seven exchanges over 2019–2021 and do not directly establish behavior in our later OKX 1-minute sample.
- Research implication: measure positive and negative impulse events separately; compare jump frequency, magnitude, clustering, co-occurrence and post-event paths. Avoid treating every large candle as a statistically identified jump.

## 3. Momentum versus reversal
Zaremba et al., *Up or down? Short-term reversal, momentum, and liquidity effects in cryptocurrency markets*, International Review of Financial Analysis 78 (2021), DOI: https://doi.org/10.1016/j.irfa.2021.101908.
- The study reports that short-term reversal/momentum patterns vary with liquidity and that the most liquid large assets can behave differently from the broad universe.
- Research implication: measure continuation and reversal separately by asset, horizon and volatility/liquidity proxy. Do not assume a universal momentum or mean-reversion rule.

## 4. Regime changes
Figà-Talamanca, Focardi and Patacca, *Regime switches and commonalities of the cryptocurrencies asset class*, North American Journal of Economics and Finance 57 (2021), DOI: https://doi.org/10.1016/j.najef.2021.101425.
- Applies Hidden Markov Models and reports multiple volatility-related regimes and commonalities across cryptoassets.
- Research implication: market behavior can change state; compare simple transparent causal regime descriptors before considering more complex latent-state models. Regime labels must use only information available at the time.

## 5. Research hypotheses for our five instruments
These are questions to test, not established coin-specific facts:
1. BTC jump/volatility events may be followed by elevated volatility or jumps in ETH/SOL/DOGE/AVAX.
2. Cross-asset dependence may rise during market shocks and fall in quieter periods.
3. Intraday volatility and activity may vary by UTC hour and weekday for each instrument.
4. Large positive and negative impulses may have different continuation and retracement distributions.
5. Continuation versus reversal may depend on asset, horizon, market state and liquidity/cost conditions.
6. Quiet range, volatile sideways, transition and shock conditions should be analyzed separately.

## 6. Empirical measurement plan (no execution authorized by this literature review)
For BTC, ETH, SOL, DOGE, AVAX, using aligned 1m OHLCV:
- Returns: log returns at 1m, 15m, 1h, 4h and 1d.
- Volatility: realized volatility, rolling range, ATR-normalized movement, tail quantiles and volatility clustering.
- Intraday: UTC hour and weekday distributions, with sample counts and subperiod stability.
- Impulses: causal threshold based on prior rolling volatility; direction, size, duration, speed, MFE/MAE and forward returns at 15m/1h/4h/12h/24h.
- Trend/chop: directional efficiency, net displacement versus total path, swing persistence and retracement depth.
- Cross-asset: rolling return correlations, conditional correlations during shocks, co-jump timing, and lead/lag tests with multiple-testing caution.
- Sideways: range width/duration, boundary tests, false breaks, breakout continuation/failure and mean-reversion distance/time.
- Costs: evaluate net outcomes only after applying the documented fee, slippage and funding assumptions.

## 7. Safeguards
- Verify exact data provenance, instrument type, timestamps, missingness and funding coverage before empirical analysis.
- Do not infer liquidity from OHLCV volume alone; it is not order-book depth or spread.
- Do not call correlation or temporal precedence proof of causal leadership.
- Use chronological 60/20/20 development/validation/OOS partitions; do not tune on the final OOS segment.
- Keep Model A pure price action separate from any indicator-assisted benchmark.
- The paused 66-experiment batch remains paused. This document does not authorize running or resuming it.

## Bibliography
- Brauneis et al. (2025): https://doi.org/10.1007/s11156-024-01304-1
- Hansen et al. (2024): https://doi.org/10.1093/jjfinec/nbac034
- Saef et al. (2024), corrected 2025: https://doi.org/10.1007/s42521-024-00116-1
- Zaremba et al. (2021): https://doi.org/10.1016/j.irfa.2021.101908
- Figà-Talamanca et al. (2021): https://doi.org/10.1016/j.najef.2021.101425
