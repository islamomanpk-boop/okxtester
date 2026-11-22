# Pump, Dump, Jump and Shock Behaviour — Chapter 3

**Date:** 2026-11-22  
**Project:** OKX Price Action Research V1  
**Status:** Desk-research framework; no local empirical results  
**Branch:** `price-action-v1`

## 1. Purpose and terminology

This chapter studies unusually fast upward and downward price movements across BTC, ETH, SOL, DOGE, and AVAX. It separates three concepts that must not be conflated:

- **Large move / extreme return:** a statistical description of price movement.
- **Price jump / shock:** a rapid discontinuous-looking move relative to normal local variation. With 1-minute OHLCV data, exact jump timing and microstructure cannot be identified as reliably as with tick and order-book data.
- **Pump-and-dump scheme:** a form of coordinated manipulation. A sharp rise followed by a decline is not, by itself, evidence of manipulation.

In this project, “pump” and “dump” are convenient labels for upward and downward price episodes only. We will not label any event as manipulation without independent evidence.

## 2. What the literature suggests

### 2.1 High-frequency jumps cluster and may be asymmetric

Saef, Nagy, Sizov, and Härdle (2024), *Understanding temporal dynamics of jumps in cryptocurrency markets: evidence from tick-by-tick data*, studied tick data for six cryptocurrencies across seven exchanges from April 2019 to September 2021. They report temporal clustering, a predominance of negative jumps in their sample, and evidence that BTC jumps are often followed by jumps in other currencies or further BTC jumps. They also caution that crypto market microstructure noise makes exact jump timing difficult. Their asset set and historical sample do not match our five OKX perpetual instruments.  
DOI: https://doi.org/10.1007/s42521-024-00116-1

### 2.2 Pump-and-dump schemes are not the same as ordinary volatility

Li, Shin, and Wang (published online 4 April 2025), *Cryptocurrency Pump-and-Dump Schemes*, document scheme episodes with sharp price, volume, and volatility increases followed by quick reversals. The paper also discusses price run-ups before schemes begin and liquidity/price effects around exchange policy changes. This is evidence about identified schemes and should not be generalized to every large candle or every major-coin rally.  
DOI: https://doi.org/10.1017/S0022109025000201

Hamrick et al. (2021), *An examination of the cryptocurrency pump-and-dump ecosystem*, study coordinated pump activity announced in online channels, primarily involving a broad set of coins and exchanges. Their findings underscore that manipulated pump events are a distinct phenomenon, not something that can be diagnosed from OHLCV shape alone.  
DOI: https://doi.org/10.1016/j.ipm.2021.102506

### 2.3 BTC-to-altcoin transmission is a hypothesis worth measuring, not assuming

Kurihara and Matsumoto (published 10 March 2026), *Price Transmission from Bitcoin to Altcoins: High-Frequency Evidence and Implications for Trading Strategy*, use Binance 1-minute data and report delayed responses for some lower-liquidity altcoins, with results varying by market regime. Their detailed asset selection includes many small and less-traded coins, not our exact five OKX contracts. Their reported BTC-to-altcoin lead/lag result motivates a local test, but does not establish that SOL, DOGE, or AVAX reliably lag BTC on OKX.  
DOI: https://doi.org/10.1007/s10690-026-09589-z

## 3. Event-study framework

Do not define an event using a fixed percentage alone. A 2% move may be ordinary for one asset and exceptional for another, or ordinary during a high-volatility period and extreme during a quiet period.

Candidate event definitions to compare on development data:

1. **Fixed-return threshold:** absolute return over a pre-defined horizon exceeds a stated percentage. Easy to explain, but not volatility-adjusted.
2. **Trailing-volatility threshold:** absolute return exceeds a multiple of volatility estimated only from observations available before the event.
3. **Range-expansion threshold:** completed candle or short-window high-low range exceeds a trailing percentile or ATR-normalized threshold.
4. **Multi-bar impulse:** cumulative directional return over a fixed window exceeds a trailing threshold, with a separately measured reversal / retracement phase.

Use symmetric upward and downward rules first. If downside and upside behave differently, report that as a measured asymmetry rather than baking it into the detector.

Thresholds and horizons are not selected in this chapter. Pre-register a small set of candidate definitions and compare them without using the final out-of-sample period for selection.

## 4. Measurements for each upward and downward episode

For every detected event, record:

### Size and speed
- Return from pre-event reference price to event peak/trough.
- Maximum one-minute and 15-minute return within the episode.
- Total high-low excursion.
- Time from event start to peak/trough.
- Average and maximum rate of movement per minute.
- Whether movement is one-candle, multi-candle, or a sequence of impulses.

### Volume and activity
- Volume during the event relative to a trailing baseline (for example, rolling median and percentile).
- Number of 1-minute bars with elevated volume.
- Whether price expansion and volume expansion occur together.
- If trade count, order-book depth, spread, liquidations, or funding are unavailable, explicitly mark them as unavailable. Do not infer liquidity from candle volume alone.

### Continuation and retracement
- Return after 5m, 15m, 1h, 4h, 12h, and 24h from the event start, where the horizon is available.
- Maximum favourable excursion and maximum adverse excursion after event detection.
- Fraction of the initial move retraced at fixed horizons.
- Time to retrace 25%, 50%, 75%, or fully return to the pre-event reference.
- Whether price consolidates, continues, or reverses after the impulse.
- Whether a new extreme is made before the event is considered finished.

### Risk and tradability
- Largest adverse movement during the event and immediately after it.
- Gap-through / stop-slippage exposure at the 1-minute bar level (with OHLC-only limitations clearly stated).
- Fee and slippage sensitivity for any later trading study.
- Whether a realistic entry could have occurred after the event became observable, rather than at the event's hindsight-defined start or low/high.

## 5. Cross-asset event propagation

For BTC, ETH, SOL, DOGE, and AVAX, align timestamps in UTC and examine:

- Same-minute and same-15-minute event co-occurrence.
- Probability that another asset experiences an event within 1, 5, 15, 30, and 60 minutes after a BTC event.
- Conditional returns of each asset after BTC upward and downward events.
- Relative lag distributions and whether the apparent lag is stable across periods.
- Whether the relationship differs in trend, sideways, and shock regimes.
- Whether an asset-specific event occurs without a BTC event.
- Whether simultaneous movements are explained by common market-wide shocks rather than BTC leading.

Use shuffled-time or other suitable null comparisons when later designing the statistical study. Correct for multiple comparisons across assets, horizons, and event definitions. A lead/lag correlation or Granger-causality result is not proof of economic causality or an executable edge.

## 6. Important data limitations

The known local market files are 1-minute OHLCV CSVs. Before using them, verify their exact source, instrument type, contract specification, timezone, volume units, and provenance. A file name containing `USDT_USDT` is not sufficient proof of the exact OKX instrument or data endpoint.

OHLCV alone cannot establish:
- Whether a move was caused by manipulation, news, liquidations, or ordinary order flow.
- Bid/ask spread, executable depth, queue position, or market impact.
- Exact tick-level jump timing inside a 1-minute candle.
- Liquidation cascades or funding shocks unless those data are separately available and verified.
- Whether volume represents base units, quote units, contracts, or another exchange-specific measure.

The processed funding data and signal files are stored outside the current repository in other project directories; their lineage and matching date coverage must be checked before combining them.

## 7. Proposed reporting tables

For each asset and direction, eventually report:
- Number of detected episodes and event-days.
- Median, mean, and 10th/25th/75th/90th/95th percentiles of event size.
- Median and percentile duration to peak/trough.
- Volume multiple distribution, if volume semantics are verified.
- Continuation and retracement rates at each horizon.
- Time-to-retracement distribution.
- Co-event and post-BTC-event frequencies by asset and lag.
- Results by volatility regime and chronological 60/20/20 split.
- Sensitivity to event definitions and thresholds.

Always show sample counts. Rare extreme events can make averages unstable; include medians and quantiles.

## 8. Research questions

1. Are upward and downward episodes different in size, speed, duration, and retracement?
2. Does each coin have its own normal movement scale, and how do event frequencies change after volatility normalization?
3. Do large moves cluster in time, and how long do high-activity periods persist?
4. After a sharp upward move, does the coin more often continue, consolidate, or retrace? Does the answer change for sharp downward moves?
5. How often do BTC events precede events in ETH, SOL, DOGE, or AVAX, and at what lag?
6. Is any lead/lag effect robust across trend, sideways, and shock regimes?
7. Do volume changes add information beyond price range and return, once volume units are verified?
8. How much of an apparent opportunity remains after a causal entry delay, fees, slippage, and adverse excursion?
9. Are extreme episodes concentrated in particular UTC hours or weekdays?
10. Are results stable in development and validation periods, and do they survive the untouched out-of-sample period?

## 9. Safeguards

- Event detection must be causal: thresholds use only prior observations.
- Avoid selecting events by looking for a later peak or trough and then pretending the event was tradable at that point.
- Do not call a large move a “pump-and-dump scheme” without independent evidence.
- Treat historical literature as hypotheses, not OKX-specific facts.
- Report upward and downward episodes separately.
- Keep all five assets visible; do not let BTC dominate pooled metrics.
- Avoid survivorship bias and incomplete event windows at dataset boundaries.
- Preserve the chronological 60/20/20 split. The final 20% remains untouched until definitions are frozen.
- Do not start new backtests, scripts, or experiments as part of this desk-research chapter.

## 10. Current conclusions and next action

- Crypto price jumps can cluster, and historical multi-exchange research reports negative-jump asymmetry and BTC/altcoin interdependence. These results are sample- and method-specific.
- Identified pump-and-dump schemes can feature sharp rises and quick reversals, but ordinary price spikes cannot be classified as manipulation from OHLCV alone.
- BTC-to-altcoin lead/lag deserves a local, regime-aware study, but the cited 2026 Binance study does not establish the same effect for our five OKX contracts.
- The next step is a data-lineage audit before any empirical calculation. No local scripts, tests, backtests, or experiments are authorized by this chapter. The 66-experiment telemetry batch remains paused.

## References

1. Saef, D., Nagy, O., Sizov, S., & Härdle, W. (2024). https://doi.org/10.1007/s42521-024-00116-1
2. Li, T., Shin, D., & Wang, B. (2025). https://doi.org/10.1017/S0022109025000201
3. Hamrick, J. T., et al. (2021). https://doi.org/10.1016/j.ipm.2021.102506
4. Kurihara, T., & Matsumoto, T. (2026). https://doi.org/10.1007/s10690-026-09589-z
