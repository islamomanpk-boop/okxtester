# Cross-Coin Correlation and Market Connectedness — Chapter 5

**Date:** 2026-11-22  
**Project:** OKX Price Action Research V1  
**Status:** Desk-research framework; no local empirical results yet  
**Branch:** `price-action-v1`

## 1. Purpose

Study how BTC, ETH, SOL, DOGE, and AVAX move together, how those relationships change during market stress, and whether any asset consistently leads or lags another at useful horizons.

This matters directly to portfolio risk. Five simultaneous positions do not represent five independent risks if returns and downside moves are strongly correlated.

No fixed correlation estimate, diversification assumption, or BTC-leading rule is accepted in this chapter.

## 2. What published research reports

### 2.1 Correlations vary over time and can rise during stress

Demiralay and Golitsis (2021), “On the dynamic equicorrelations in cryptocurrency market,” *The Quarterly Review of Economics and Finance*, study dynamic cryptocurrency co-movement using a DECO-GARCH framework. They report time-varying equicorrelations and substantially stronger interlinkages around the COVID-19 pandemic stress period. They also identify BTC trading volume and uncertainty-related variables as determinants of market integration.  
DOI: https://doi.org/10.1016/j.qref.2021.04.002

Smales (2021), “Volatility Spillovers among Cryptocurrencies,” *Journal of Risk and Financial Management*, 14(10), 493, reports time-varying conditional correlations that peaked during the March 2020 sell-off. In that sample, BTC and ETH had bidirectional return and long-term volatility spillovers, with a short-term volatility spillover from BTC to ETH.  
DOI: https://doi.org/10.3390/jrfm14100493

**Interpretation:** A single full-sample correlation matrix is not enough for risk planning. Stress-period dependence may be materially different from normal-period dependence. These studies do not give the current correlations of our five OKX contracts.

### 2.2 Correlation can depend on volatility regime

Research on regime-switching volatility and co-jumps reports that cryptocurrency correlations differ across combinations of low- and high-volatility states. One study finds stronger correlations when both assets are in similar volatility states than when one is in a high-volatility state and the other in a low-volatility state.  
Article: https://doi.org/10.1080/00036846.2023.2170970

**Interpretation:** Compare correlation not only in calm versus stress periods, but also in matched and mismatched volatility regimes.

### 2.3 BTC does not lead every asset at every horizon

Kurihara and Matsumoto (2026), “Price Transmission from Bitcoin to Altcoins: High-Frequency Evidence and Implications for Trading Strategy,” examine Binance 1-minute data. Their reported cross-correlations show that large and medium-cap assets such as ETH often have strong contemporaneous correlation with BTC, with little additional lagged response. Some smaller assets exhibit delayed reactions in their sample. The authors also report faster reactions during downturns than upturns for some assets.  
DOI: https://doi.org/10.1007/s10690-026-09589-z

**Interpretation:** It is unsafe to assume that BTC always moves first and that ETH, SOL, DOGE, and AVAX provide a predictable delay. The exact five instruments and OKX venue require separate analysis.

### 2.4 Connectedness and spillovers are not the same as simple correlation

Aliu and Nuhiu (2025), “Analyzing the Interconnectedness Within the Volatile Crypto Market: Evidence from Two Consequent Non-economic Shocks,” study daily return spillovers among 15 major cryptocurrencies during 2020–2023 and report substantial spillovers, with BTC and ETH among the main influences in their models.  
DOI: https://doi.org/10.1177/21582440251340458

**Interpretation:** Correlation describes co-movement; spillover models attempt to describe directional predictive relationships under particular model assumptions. Neither alone proves causal transmission or an executable trading advantage.

## 3. Measurements for our five assets

Use aligned UTC timestamps and calculate returns rather than correlating raw price levels. Nonstationary price levels can create misleadingly high correlations.

### 3.1 Contemporaneous return correlation

For each of the ten unique pairs:
- Pearson correlation of 1-minute, 15-minute, 1-hour, 4-hour, and daily log returns.
- Spearman rank correlation as a robustness measure.
- Rolling correlations over pre-defined windows, with sample counts.
- Correlation distribution: median, 10th/90th percentiles, and time spent in high-correlation states.
- Pairwise scatterplots and residual diagnostics where appropriate.

The ten pairs are BTC–ETH, BTC–SOL, BTC–DOGE, BTC–AVAX, ETH–SOL, ETH–DOGE, ETH–AVAX, SOL–DOGE, SOL–AVAX, and DOGE–AVAX.

### 3.2 Downside and stress dependence

Calculate separately:
- Correlation on all observations.
- Correlation when BTC return is negative.
- Correlation when both assets are negative.
- Correlation during the most extreme BTC downside-return quantiles, using thresholds estimated only from the relevant training window.
- Joint downside-event frequency versus the frequency expected under independence.
- Conditional loss distribution of each asset when BTC experiences an extreme downside event.
- Co-exceedance rates for all five assets and for each pair.

A conditional correlation estimated only on negative observations can be noisy. Always show sample counts and uncertainty intervals. Also report joint-tail event frequencies directly rather than relying only on correlation.

### 3.3 Volatility and shock connectedness

- Compare realized-volatility changes across assets.
- Measure co-jumps / simultaneous extreme returns using pre-defined, volatility-adjusted event rules.
- Estimate whether large BTC volatility events are followed by changes in other assets' volatility.
- Compare lead/lag relationships separately for returns and volatility.
- Analyze normal, trend, quiet-range, choppy-range, and shock states after those states have been defined causally.

### 3.4 Lead/lag analysis

For each pair, calculate cross-correlations over a small pre-registered lag range at 1-minute, 5-minute, 15-minute, and 1-hour sampling resolutions.

Define lag sign explicitly in all reports. For example, positive lag k can mean asset B's return is compared with asset A's return k intervals earlier; do not rely on ambiguous chart conventions.

Measure:
- Contemporaneous relationship (lag 0).
- Whether lagged correlation is materially greater than lag 0.
- Whether the result survives multiple-testing correction.
- Whether it is stable across subperiods and market regimes.
- Whether any apparent lag is larger than the data timestamp / candle construction uncertainty.

A lagged correlation does not establish causality. Common news, market-wide order flow, asynchronous trading, and timestamp alignment errors can all create apparent lead/lag.

## 4. Portfolio-risk implications

The portfolio uses shared equity and can hold multiple assets at once. Therefore measure:
- Number of simultaneous open positions.
- Pairwise correlation among assets while positions overlap.
- Portfolio return and drawdown compared with the sum of isolated asset returns.
- Gross notional and risk-at-stop across simultaneous positions.
- Historical joint stop-hit frequency.
- Concentration of portfolio loss on market-wide downside days.
- Whether the 1x gross-notional cap and 0.5% per-trade risk cap actually limit aggregate portfolio risk when positions are highly correlated.

Do not assume that five positions each risking 0.5% means total portfolio risk is always 0.5%. In the current architecture, per-trade risk can accumulate across simultaneous positions. The aggregate exposure and joint-loss distribution must be measured and explicitly controlled.

Potential later risk controls to evaluate (not approved now):
- Maximum total open risk across all assets.
- BTC / market-wide shock pause.
- Correlation-aware position sizing.
- Limit on simultaneous positions in highly correlated assets.
- Portfolio-level daily loss and drawdown limits.

Any risk control must be tested for false pauses, missed opportunities, and out-of-sample stability. Do not add one solely because a correlation statistic looks high.

## 5. Data and statistical safeguards

- Confirm exact instrument identity and data source for every file.
- Align all five assets to the same UTC timestamps for common-sample analysis.
- Do not forward-fill missing prices to manufacture zero returns.
- Report both common-date and each-asset-full-sample results.
- Use log returns or simple returns consistently; never correlate price levels as the main measure.
- Be aware that overlapping multi-minute returns induce serial dependence.
- Use block bootstrap or other dependence-aware uncertainty estimates.
- Correct for multiple comparisons across ten pairs, timeframes, lags, and regimes.
- Do not select lag windows or stress thresholds on the final out-of-sample data.
- Keep chronological development / validation / untouched OOS partitions.
- Report pairwise and portfolio-level results, not only an average correlation.
- Do not infer causality from correlation, Granger tests, or temporal precedence alone.

## 6. Questions for our five coins

1. Which pair has the strongest contemporaneous relationship at 1M, 15M, 1H, 4H, and daily horizons?
2. Are SOL, DOGE, and AVAX more strongly related to BTC during downside shocks than in calm conditions?
3. Does ETH behave more like BTC than the other three altcoins in our sample?
4. Are there periods when one coin decouples from the rest?
5. Do correlations rise during market-wide crashes or volatile sideways episodes?
6. Are co-jumps more common than expected under independence?
7. Does BTC lead any of the four assets at a stable, economically meaningful lag?
8. Are lead/lag relationships asymmetric between upward and downward moves?
9. Do high pairwise correlations coincide with higher portfolio drawdowns and simultaneous stop-outs?
10. How much does holding several assets at once increase aggregate portfolio risk?
11. Does any observed relationship survive subperiod analysis and the untouched OOS period?

## 7. Current conclusions

- Cryptocurrency correlations and volatility spillovers are time-varying; historical studies report stronger interlinkages during some stress events.
- BTC and ETH have shown meaningful interdependence in historical samples.
- High-frequency evidence does not support a universal rule that BTC leads every altcoin; some large assets respond contemporaneously.
- Five separate coin positions can still represent concentrated market-wide exposure.
- Correlation is not causality, and diversification must be assessed in downside and portfolio-loss terms, not only with average correlation.
- No fixed correlation threshold, BTC-leading filter, or portfolio-risk rule is approved by this chapter.

## 8. Next step (no execution authorized)

The desk-research chapters now cover market behaviour, daily/weekly movement definitions, sideways states, pump/dump/jump events, time-of-day / weekday patterns, and cross-coin connectedness.

The next phase should be a **read-only data-lineage and provenance audit** before any empirical statistics are calculated. It must confirm the source, venue, contract identity, timezone, schema, coverage, alignment, volume units, funding coverage, and signal provenance for all five assets.

The 66-experiment telemetry batch remains paused. This chapter does not authorize scripts, tests, backtests, or new experiments.

## References

1. Demiralay, S., & Golitsis, P. (2021). https://doi.org/10.1016/j.qref.2021.04.002
2. Smales, L. A. (2021). https://doi.org/10.3390/jrfm14100493
3. Katsiampa, P. (2019). https://doi.org/10.1016/j.ribaf.2019.06.004
4. https://doi.org/10.1080/00036846.2023.2170970
5. Kurihara, T., & Matsumoto, T. (2026). https://doi.org/10.1007/s10690-026-09589-z
6. Aliu, F., & Nuhiu, A. (2025). https://doi.org/10.1177/21582440251340458
