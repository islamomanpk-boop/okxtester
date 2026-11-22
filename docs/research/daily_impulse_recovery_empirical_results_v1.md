# Daily Pump/Dump Follow-up: Empirical Results V1

**Research status:** descriptive study only; no strategy or profitability test.  
**Branch:** `price-action-v1`  
**Study date:** 2026-11-22

## Data and sample

- Assets: BTC, ETH, SOL, DOGE, AVAX.
- Source files: existing 1-minute CSVs under `~/okx_scalping_data`; read-only.
- Common timestamp intersection: 569,125 minute candles.
- Complete UTC daily candles: 394 per asset, 2025-10-21 through 2026-11-18.
- Daily event return: current complete UTC daily close divided by prior complete UTC daily close, minus one.
- Pump thresholds: daily close-to-close return >= +3%, +5%, +7%, +10%.
- Dump thresholds: daily close-to-close return <= -3%, -5%, -7%, -10%.
- Follow-up windows: next 1, 3, and 7 complete daily candles. The event day is excluded from follow-up; event-day high/low is used as the starting extreme.
- All five datasets are aligned on the common minute timestamps before daily aggregation.

## Metric definitions

For a pump:
- Pullback: maximum percentage decline from the event day's high to the lowest low in the following horizon.
- Original impulse given back: that pullback distance in price units divided by the event's positive close-to-close price increase.
- Continuation: maximum percentage rise from the event day's high to the highest high in the following horizon.
- Full reversal: whether any subsequent low reaches or falls below the close immediately before the event day.

For a dump:
- Rebound: maximum percentage rise from the event day's low to the highest high in the following horizon.
- Original impulse given back: that rebound distance in price units divided by the event's negative close-to-close price decrease.
- Continuation: maximum percentage fall from the event day's low to the lowest low in the following horizon.
- Full reversal: whether any subsequent high reaches or exceeds the close immediately before the event day.

Reported pullback/rebound and continuation percentages are relative to the event-day high/low, not trade returns. Impulse-given-back percentages can exceed 100% because the post-event retracement can exceed the close-to-close impulse distance; this does not mean a price moved more than 100%.

## Selected results: >=5% daily events, 7-day follow-up

| Asset | Direction | Events | Median pullback/rebound | Median impulse given back | Median continuation | Full reversal |
|---|---|---:|---:|---:|---:|---:|
| BTC | Pump | 11 | 5.14% | 86.5% | 2.48% | 27.3% |
| ETH | Pump | 22 | 8.51% | 129.3% | 2.06% | 50.0% |
| SOL | Pump | 23 | 7.02% | 121.4% | 4.54% | 43.5% |
| DOGE | Pump | 20 | 12.42% | 129.6% | 3.62% | 60.0% |
| AVAX | Pump | 29 | 11.91% | 123.1% | 2.05% | 51.7% |
| BTC | Dump | 7 | 3.02% | 55.6% | 10.70% | 14.3% |
| ETH | Dump | 17 | 6.62% | 95.5% | 5.98% | 29.4% |
| SOL | Dump | 21 | 4.76% | 72.5% | 8.85% | 23.8% |
| DOGE | Dump | 19 | 8.44% | 129.4% | 6.89% | 31.6% |
| AVAX | Dump | 26 | 7.73% | 100.8% | 6.42% | 30.8% |

## Preliminary descriptive observations

1. Following >=5% daily pumps, the median seven-day pullback was largest in DOGE (12.42%) and AVAX (11.91%), and smallest in BTC (5.14%).
2. The median price-distance given back exceeded the original close-to-close pump impulse for ETH, SOL, DOGE, and AVAX. BTC was below the original impulse at 86.5%.
3. Following >=5% daily dumps, DOGE had the largest median seven-day rebound (8.44%), followed by AVAX (7.73%). BTC had the smallest (3.02%).
4. BTC's >=5% dump sample showed a relatively large median downside continuation (10.70%) and a small median rebound (3.02%), but only seven events were available.
5. DOGE and AVAX show larger post-event excursions in this sample, consistent with their higher observed daily ranges in the earlier movement study.
6. These observations are descriptive, not forecasts. They do not establish that fading pumps or buying dumps is profitable or executable.

## Important limitations and audit notes

- Events are not de-clustered. Multiple qualifying days can occur close together, so event follow-up windows can overlap and observations are not independent.
- Thresholds are nested: a >=7% event is also included in >=5% and >=3% results. Threshold tables must not be treated as independent samples.
- Event counts vary by horizon because events too close to the end of the available daily history are excluded when a full follow-up window is unavailable.
- Large thresholds have small samples. In particular, BTC >=5% dumps have only seven usable seven-day events; >=7% and >=10% results often have only one to a few events.
- Daily close-to-close thresholds do not capture every intraday pump/dump. The event-day high/low is used only as the post-event reference extreme.
- Daily OHLC follow-up cannot reveal the exact order or timing of the high and low within a day.
- High-low excursions are not equivalent to executable returns. Fees, slippage, funding, entry timing, liquidity, and stop/target path are not modelled.
- Data provenance caveat remains: the five CSVs have been aligned and quality-audited, but the original 1-minute download source and exact OKX instrument identity have not been independently verified.

## Next research steps

1. Re-run the event analysis with an explicit event-clustering/non-overlap rule and compare results with the raw event sample.
2. Study multi-day impulses (2, 3, 5, and 7-day close-to-close moves) and their subsequent retracements/rebounds.
3. Study post-event behaviour at 4H resolution to capture the timing of retracements and continuation.
4. Continue with sideways/ranging behaviour on 4H and 15M, then breakout and failed-breakout behaviour.
5. Keep all work descriptive until the user explicitly authorizes strategy testing. No backtests or trading were run for this study.

## Reproducibility

The calculation was run interactively in Termux using pandas against the existing five 1-minute CSVs. It printed results to the terminal and did not write or modify local files.
