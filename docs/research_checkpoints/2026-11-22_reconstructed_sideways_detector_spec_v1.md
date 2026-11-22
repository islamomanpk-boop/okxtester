# Reconstructed Sideways Detector Specification — Frozen v1

**Date:** 2026-11-22  
**Repository branch:** `price-action-v1`  
**Status:** FORMAL RECONSTRUCTED SPECIFICATION — approved for independent implementation and audit; not a claim that the missing original source code has been recovered.

## 1. Purpose and scope

This specification freezes the mathematical definitions for the 4H sideways-context detector used by the repeated-boundary-test study across BTC, ETH, SOL, DOGE, and AVAX.

It is separate from the existing EMA/ADX regime classifier. It does not establish a profitable strategy and does not authorize live trading.

## 2. Input data and snapshot schedule

- Use the validated 4H OHLCV series, whose candles are left-labelled and represent complete intervals.
- Each snapshot uses the current completed 4H candle and the preceding 11 completed 4H candles: exactly 12 candles / 48 hours.
- Create a rolling snapshot after every completed 4H candle.
- A snapshot labelled by the 4H candle's opening timestamp becomes available only at that candle's closing timestamp (opening timestamp + 4 hours).
- No value from an incomplete 4H candle may enter the snapshot.
- Freeze the computed upper and lower channel boundaries for the associated 15M evaluation period.
- The first 15M candle beginning at or immediately after the snapshot availability time is excluded from touch/test eligibility, consistent with the existing protocol. Eligibility begins with the following 15M candle.
- Never align assets by row number. Use timestamps.

## 3. Channel boundaries and width

For the 12-candle window:

- `upper = max(high)`
- `lower = min(low)`
- `midpoint = (upper + lower) / 2`
- `channel_width_pct = ((upper - lower) / midpoint) * 100`

A snapshot is invalid if midpoint is non-positive, any required OHLC value is missing/non-finite, or the 12-candle window is incomplete.

## 4. Directional efficiency

Use the 12 closing prices belonging to the 12-candle window, which form 11 adjacent close-to-close changes.

```
net_move = abs(close_last - close_first)
path_length = sum(abs(close[i] - close[i-1]) for i = 1..11)
directional_efficiency = net_move / path_length
```

If `path_length == 0`, define directional efficiency as 0.0 (no directional movement).

A snapshot passes the directional-efficiency filter when:

```
directional_efficiency <= 0.30
```

The numerator and denominator must use the same 12 closes; do not silently switch to 12 price changes / 13 closes.

## 5. Mean adjacent-candle range overlap

For each of the 11 adjacent pairs in the 12-candle window, define:

```
intersection = max(0, min(high[i-1], high[i]) - max(low[i-1], low[i]))
union = max(high[i-1], high[i]) - min(low[i-1], low[i])
pair_overlap = intersection / union, if union > 0
```

If `union == 0` (both ranges are the same zero-width point), define `pair_overlap = 1.0`.

Then:

```
mean_overlap = arithmetic_mean(pair_overlap for all 11 pairs)
```

A snapshot passes the overlap filter when:

```
mean_overlap >= 0.70
```

Do not substitute intersection divided by the smaller candle range, or any other overlap normalization.

## 6. Asset-specific channel-width percentiles

For each asset independently:

1. Compute `channel_width_pct` for every valid rolling 12-candle snapshot in the complete available research history.
2. Calculate P25 and P40 using the linear quantile method (equivalent to NumPy's `method="linear"`).
3. Strict width condition: `channel_width_pct <= asset_P25`.
4. Broad width condition: `channel_width_pct <= asset_P40`.

The strict and broad classifications are nested and may overlap; they are not independent samples.

**Look-ahead limitation:** these full-history percentiles use future observations relative to earlier snapshots. They are acceptable only for retrospective exploratory research. They are not valid live thresholds or an out-of-sample detector. Any later live/forward test must estimate percentile cutoffs using training data only, freeze them, and apply them unchanged to validation/test periods.

## 7. Final sideways classification

For each valid snapshot:

```
strict_sideways = (channel_width_pct <= P25)
                  AND (directional_efficiency <= 0.30)
                  AND (mean_overlap >= 0.70)

broad_sideways = (channel_width_pct <= P40)
                 AND (directional_efficiency <= 0.30)
                 AND (mean_overlap >= 0.70)
```

Store the raw metrics, asset-specific P25/P40 values, snapshot timestamp, availability timestamp, and each Boolean filter separately. Do not store only the final class; the audit must be able to reproduce every decision.

## 8. Existing 15M boundary-test protocol retained

This detector specification does not change the established downstream protocol:

- 15M upper/lower touches use a 10% channel-width zone.
- Upper touch: `high >= upper - 0.10 * width`.
- Lower touch: `low <= lower + 0.10 * width`.
- A new test rank begins only after a completed 15M candle closes at least 0.20 channel widths away from the tested boundary, followed by a later eligible touch. The separation candle cannot also start the next test.
- First strong rejection per test only.
- Upper strong rejection: touch, close below `upper - 0.10 * width`, and close above lower.
- Lower strong rejection: touch, close above `lower + 0.10 * width`, and close below upper.
- Reset test numbering on snapshot change, invalid sideways context, or a 15M timeline gap.
- Keep the existing rule excluding the first 15M candle after each new 4H snapshot.

## 9. Implementation and audit acceptance gates

Before replacing or reconciling any provisional event/outcome results:

1. Implement this specification in a new, separately named script/module. Do not overwrite the provisional calculation or historical checkpoint.
2. Unit-test the 12-candle window boundaries, 11-change efficiency indexing, zero-path case, 11-pair overlap indexing, zero-union case, width normalization, and linear percentile calculation.
3. Produce per-asset detector diagnostics: valid snapshot count, P25/P40 cutoffs, distributions of width/efficiency/overlap, and strict/broad pass counts.
4. Independently recompute a sample of snapshots directly from source OHLC rows and compare every raw metric and classification.
5. Verify 4H-to-15M availability mapping and first-15M exclusion by timestamp, including boundary timestamps and gaps.
6. Only after these gates pass, reconstruct 15M tests/rejections and reconcile event counts against the provisional run.
7. Recalculate all post-rejection outcomes from the independently audited event set. Preserve incomplete horizons as incomplete; never fill them.
8. Record failures and discrepancies as well as passes. Do not describe results as validated until the relevant gates pass.

## 10. Provenance and limitations

The earlier protocol and provisional outcome checkpoint remain historical records. The exact original detector source/formula bibliography was not recovered. This document formalizes the agreed reconstructed definitions, informed by the available research notes and candidate mathematical references; it does not establish that these were the exact formulas used in the original run.

Relevant source references consulted during formula recovery:

- CME Group / Graham Capital Management, *The Trendiness of Markets* (August 2017): https://www.cmegroup.com/content/dam/cmegroup/education/files/trendiness-of-markets-august-2017.pdf
- Perry Kaufman, *Smarter Trading: Improving Performance in Changing Markets* (excerpt): https://c.mql5.com/3/133/Kaufman.Perry-Smarter.Trading.Improving.Performance.In.Changing.Markets.pdf
- MarketVolume, Efficiency Ratio: https://www.marketvolume.com/technicalanalysis/efficiencyratio.asp
- MQL5, *Price Action Analysis Toolkit Development (Part 58): Range Contraction Analysis and Maturity Classification Module*: https://www.mql5.com/en/articles/21109
- TradersWeek, *Constructing range overlap and bar-pattern filters from neighboring OHLC bars*: https://tradersweek.com/research/articles/constructing-ohlc-range-overlap-and-bar-pattern-filters

These references support candidate mathematical concepts; they are not proof of the missing original implementation or of the selected numeric thresholds.
