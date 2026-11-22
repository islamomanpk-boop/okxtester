# Research chapter 02 — daily and weekly movement measurement
Date: 2026-11-22
Branch: price-action-v1

## Objective
Characterize typical and extreme daily and weekly price movement for BTC, ETH, SOL, DOGE, and AVAX before choosing stop distances, targets, position sizing, or asset-specific strategy rules.

This document defines the empirical study. It does not contain results calculated from the project's local OHLCV data and does not authorize a backtest.

## Why multiple movement measures are required
"Average movement" is ambiguous. At least three different concepts must be separated:
1. Intraperiod high-low range: how far price travelled between its high and low, regardless of where it closed.
2. Close-to-close return: net price change from one period close to the next.
3. Realized path movement/volatility: how much price moved during the period, including intraperiod fluctuations.

These are not interchangeable. A day can have a large high-low range but finish near its open; its net return can be small despite substantial movement.

## Required daily metrics (per asset)
Use complete UTC calendar days and exclude partial first/last days from daily summary statistics.
- High-low range percentage: (high - low) / open * 100.
- Log high-low range: ln(high / low), for scale-comparable analysis.
- Close-to-close simple and log return.
- Absolute close-to-close return.
- Open-to-close return.
- Positive-day and negative-day counts and frequencies.
- Mean, median, standard deviation, 10th/25th/75th/90th/95th/99th percentiles of range and absolute return.
- Mean positive return and mean negative return, separately; report conditional sample counts.
- Largest positive and negative close-to-close days and largest high-low range days, with UTC dates.
- Intraday realized volatility from 1-minute log returns: square root of sum of squared intraday returns. Report separately from range and close-to-close measures.

## Required weekly metrics (per asset)
Use fixed UTC weeks (Monday 00:00 through Sunday 23:59 UTC) and only complete weeks.
- Weekly high-low range percentage: (weekly high - weekly low) / weekly open * 100.
- Weekly log range: ln(weekly high / weekly low).
- Weekly close-to-close return and absolute return.
- Weekly open-to-close return.
- Mean, median, standard deviation and 10th/25th/75th/90th/95th/99th percentiles.
- Positive/negative week frequencies and conditional mean gain/loss.
- Largest positive/negative close-to-close weeks and largest range weeks.
- Seven-day rolling volatility/range measures as supplementary indicators, not substitutes for fixed calendar-week statistics.

## Movement thresholds and frequency
For both daily and weekly observations, count how often absolute close-to-close returns and high-low ranges exceed 1%, 2%, 3%, 5%, and 10%, where sample support permits. Show both count and percentage of eligible periods. Threshold exceedance of range is not the same as threshold exceedance of close-to-close return.

## Distribution and stability
- Compare mean with median to identify outlier influence.
- Examine tail quantiles and skewness; do not assume normal returns.
- Report rolling 30-day and 90-day volatility/range to show time variation.
- Compare subperiods and development/validation/OOS chronologically.
- Compare all five assets on the same common-date sample, then show each asset's full valid sample separately.
- Do not rank coins by one mean alone. Consider movement, tails, costs, liquidity evidence, and stability together.

## Cross-asset comparison
- Correlation of daily and weekly returns.
- Conditional correlation on high-volatility days/weeks and during BTC shock periods.
- Compare asset-specific range and return distributions.
- Distinguish correlation from lead/lag or causal influence.

## Interpretation safeguards
- A high average range does not prove a coin is more profitable or more tradable.
- A large high-low range can contain adverse reversals and substantial execution costs.
- Close-to-close return can hide large intraperiod adverse/favorable excursions.
- Historical averages are descriptive, not forecasts or guarantees.
- Compare percentage and volatility-normalized movement, not raw dollar changes.
- Use only complete UTC periods and document missing candles.
- The 60/20/20 chronological split remains mandatory for any later hypothesis testing; final OOS data must not be used to tune thresholds.

## Published methodology context
- Intraday realized volatility is commonly estimated as the square root of the sum of squared intraday returns; crypto's continuous trading allows 24-hour aggregation. See the 2026 study, *Time-Varying Factor-Augmented Models for Volatility Forecasting*, https://doi.org/10.1145/3768292.3770407.
- A recent BTC/ETH realized-volatility study (sample through 2026-10) illustrates that volatility differs materially by asset and calendar period; its estimates are not substitutes for measurements on our five OKX perpetual datasets: https://tommasozeri.github.io/research/foundation-models-crypto-realized-volatility/
- Cross-asset daily return research reports substantial differences in volatility and heavy tails across cryptoassets; samples and instruments vary: https://link.springer.com/article/10.1007/s10690-026-09637-8

## Next action
After data provenance, coverage, and UTC alignment are confirmed, calculate this descriptive dashboard from the five local 1-minute datasets. Do not resume the paused 66-experiment exit batch for this work.
