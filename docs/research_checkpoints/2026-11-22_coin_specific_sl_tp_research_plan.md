# Research Decision: Coin-Specific Risk and Exit Design — Planning Note

**Date:** 2026-11-22  
**Project:** Price Action V1  
**Status:** Research plan only. No backtests or experiments authorized.

## Decision

Do not assign final stop-loss (SL) or take-profit (TP) distances to BTC, ETH, SOL, DOGE, or AVAX yet. First measure each asset's volatility, volatility changes, price structure, and execution characteristics. The eventual system may use coin-specific SL/TP rules, but those rules must be justified by evidence and evaluated with realistic costs and out-of-sample testing.

## Why coin-specific treatment may be appropriate

The current descriptive daily/weekly study shows material differences in movement distributions. For example, daily high-low range was at least 5% on 16.03% of BTC days versus 53.44% of AVAX days in the sample. Weekly high-low range was at least 10% on 31.48% of BTC weeks versus 79.63% of AVAX weeks.

These observations motivate testing asset-specific risk distances. They do not establish optimal stop distances, target distances, or profitability. A large range can include reversals and is not equivalent to a tradable directional move.

## Research sequence before SL/TP selection

1. **Rolling volatility and movement stability**
   - Calculate rolling 30-day and 90-day range, absolute close-to-close return, and ATR-style measures for each asset.
   - Compare median, upper quantiles, and time spent in low-, normal-, and high-volatility states.
   - Identify how frequently volatility states change and how long they persist.
   - Compare chronological subperiods to identify whether the full-sample averages conceal major changes.
   - Avoid look-ahead: any regime label used in a future strategy must be based only on information available at that time.

2. **Price behaviour and market structure**
   - Examine trend, range, breakout, failed-breakout, pullback, and reversal behaviour.
   - Measure typical adverse and favourable excursions after clearly defined price-action events, with causal event definitions.
   - Study wick/body proportions, candle clustering, and volatility expansion/contraction.
   - Treat these as descriptive research until a signal and execution rule are specified.

3. **Coin-specific SL/TP hypotheses**
   - Compare structure-based stops (e.g., beyond a valid swing or signal extreme) with volatility-scaled stops (e.g., ATR multiples).
   - Consider hybrid stops: structural invalidation plus a volatility buffer.
   - Compare fixed-R targets, structure-based targets, partial exits, and trailing exits separately.
   - Derive candidate distances from training/development data only; do not select them by inspecting the final out-of-sample period.
   - Keep a common portfolio risk budget across assets. Wider stops should generally reduce position size if the dollar risk budget is unchanged.

4. **Execution and cost reality**
   - Include taker/maker assumptions only when supported by the actual order type and fill model.
   - Include fees, slippage, funding where applicable, and missed/partial fills.
   - Evaluate stop/target collisions and intrabar ordering conservatively using one-minute data.
   - Distinguish price movement potential from movement that a causal strategy could actually capture.

5. **Validation**
   - Preserve the planned chronological development/validation/out-of-sample separation.
   - Compare a common baseline against coin-specific rules.
   - Require improvement in net expectancy and risk-adjusted/portfolio outcomes, not merely more trades or larger gross wins.
   - Check robustness across periods and parameter neighbourhoods; avoid selecting a fragile single optimum.
   - Keep asset-specific parameters simple and limit the number of degrees of freedom.

## Immediate next task

Continue the already agreed read-only rolling 30-day and 90-day behaviour study for the five assets. Report volatility level, dispersion/quantiles, regime persistence, and chronological variation. Save the empirical results before moving to the next research topic.

## Guardrails

- Backtests and experiments remain paused until the user explicitly authorizes them.
- Do not modify source datasets or run downloader/resampling pipelines.
- Do not treat descriptive range statistics as evidence of a profitable SL/TP.
- Do not assume all five assets require different rules; the research may show that some can share a risk model.
- Keep per-trade dollar risk and total portfolio exposure controlled even when stop distances differ.
