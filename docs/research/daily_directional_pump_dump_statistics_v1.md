# Daily Directional Pump and Dump Statistics — Five-Asset Study (V1)

**Status:** Descriptive research result; not a strategy test.  
**Assets:** BTC, ETH, SOL, DOGE, AVAX  
**Sample:** 393 measured daily close-to-close returns per asset, derived from 394 complete UTC daily candles.  
**Data basis:** Existing 1-minute CSVs joined on the common timestamp intersection (569,125 common minute candles).  
**Calculation:** Read-only; no local files were written or changed.

## Definitions

- Daily return: current complete UTC daily close divided by the previous complete UTC daily close, minus one.
- Pump day: daily return greater than zero. Pump magnitude is the positive return.
- Dump day: daily return less than zero. Dump magnitude is the absolute value of the negative return.
- Average and median pump/dump are calculated separately across positive and negative daily returns.
- P90 and P95 are the 90th and 95th percentiles of the relevant directional magnitudes.
- Largest pump/dump is the maximum directional close-to-close return magnitude, with its UTC daily date.
- Largest intraday range: (daily high - daily low) / daily open, with its UTC daily date. This is not a close-to-close return.

## Average and distribution of directional daily returns

All values are percentages. Dump magnitudes are shown as positive numbers.

| Asset | Pump days | Avg pump | Median pump | P90 pump | P95 pump | Dump days | Avg dump | Median dump | P90 dump | P95 dump |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | 188 | 1.561 | 1.047 | 3.760 | 5.158 | 205 | 1.644 | 1.369 | 3.531 | 4.492 |
| ETH | 196 | 2.033 | 1.118 | 5.268 | 6.813 | 197 | 2.317 | 1.775 | 4.833 | 6.616 |
| SOL | 184 | 2.412 | 1.436 | 5.655 | 6.938 | 209 | 2.461 | 1.997 | 5.026 | 6.481 |
| DOGE | 170 | 2.542 | 1.573 | 5.857 | 8.444 | 223 | 2.367 | 1.767 | 4.888 | 5.783 |
| AVAX | 181 | 2.756 | 1.944 | 6.882 | 7.836 | 212 | 2.698 | 2.043 | 5.530 | 7.703 |

## Largest daily close-to-close moves

| Asset | Largest pump | Pump date (UTC) | Largest dump | Dump date (UTC) |
|---|---:|---|---:|---|
| BTC | 12.176% | 2026-02-06 | 14.025% | 2026-02-05 |
| ETH | 17.484% | 2026-08-19 | 14.955% | 2026-02-05 |
| SOL | 11.662% | 2026-02-06 | 14.967% | 2026-02-05 |
| DOGE | 14.830% | 2026-02-14 | 14.802% | 2026-02-05 |
| AVAX | 23.019% | 2026-09-19 | 14.471% | 2026-02-05 |

## Largest daily high-low ranges

| Asset | Largest daily range | Date (UTC) |
|---|---:|---|
| BTC | 18.753% | 2026-02-06 |
| ETH | 22.802% | 2026-08-19 |
| SOL | 28.867% | 2026-02-06 |
| DOGE | 25.170% | 2026-02-06 |
| AVAX | 24.067% | 2026-09-19 |

## Descriptive observations

1. BTC has the smallest average directional daily move in this sample: 1.561% on pump days and 1.644% on dump days.
2. AVAX has the largest average directional daily moves: 2.756% pump and 2.698% dump.
3. ETH, SOL and AVAX have a higher average dump magnitude than pump magnitude. DOGE has a slightly higher average pump magnitude than dump magnitude; BTC's averages are close, with dumps modestly larger.
4. The median is below the mean for every asset and direction. Large directional days therefore pull the average upward; median values better describe the middle observation.
5. The largest daily high-low range is a different measure from the largest close-to-close pump or dump. A day can travel widely between its high and low but finish much closer to its previous close.
6. February 5, 2026 appears as the largest dump date for all five assets in this sample. This is a useful cross-asset event to examine in a separate market-event study, but this table alone does not establish its cause.
7. AVAX's largest observed close-to-close pump was 23.019% on September 19, 2026. This is an extreme sample observation, not a forecast or a suitable default target.

## Research interpretation and limitations

- These are historical descriptive statistics, not forecasts, trade signals, or evidence of profitability.
- A positive daily close-to-close return does not mean price moved upward throughout the day. Likewise, a negative return does not describe the intraday path.
- The daily high-low range does not establish that a trader could capture the full move. Entry timing, path, spread, fees, slippage, funding, liquidity, and execution are not modelled here.
- The sample has 393 daily returns per asset. Extreme maxima are particularly sensitive to sample length and should not be treated as stable expected limits.
- Daily candles are UTC-aligned and complete-day filtered on the common timestamp intersection. The 1-minute data's original exchange/API/instrument provenance remains unverified; filenames and downstream project configuration do not prove it.
- Results are specific to this sample period and data source. They should not be generalized to all market regimes or future conditions.

## How this fits the ongoing research

This fills the gap between overall mean absolute daily return and separate pump/dump behaviour. Earlier research already measured daily ranges, absolute returns, threshold frequencies, and post-event reactions after daily impulses. The next useful extension is multi-day impulse behaviour (2-, 3-, 5-, and 7-day moves), followed by 4H and 15M range/sideways behaviour. No backtests or strategy experiments are authorized by this research note.
