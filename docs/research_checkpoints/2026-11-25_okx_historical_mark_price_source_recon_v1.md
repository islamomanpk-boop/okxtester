# OKX Historical Mark-Price Source Reconnaissance V1

**Date:** 2026-11-25  
**Purpose:** Determine whether historical OKX mark-price data can improve or replace the current candle-close proxy used for funding cashflow reconstruction.  
**Status:** API capability identified; historical coverage and settlement-price equivalence NOT YET VERIFIED.

## Findings from official OKX documentation

1. OKX documents separate endpoints for **Get mark price candlesticks** and **Get mark price candlesticks history** in its [V5 API guide](https://www.okx.com/docs-v5/log_en/). The API guide also lists 1-minute mark-price candle intervals.
2. OKX's historical-data page advertises downloadable historical candlestick data from July 2023 and historical perpetual funding rates from March 2022: https://www.okx.com/historical-data
3. The documented funding-rate history endpoint returns a realized funding rate and funding timestamp per settlement. It does not, in the documented response schema reviewed for this checkpoint, expose a settlement mark-price field.
4. Mark-price candlesticks are OHLC aggregates. Even if the 1-minute candle timestamp aligns with a funding timestamp, its open/close is not automatically proven to equal the exact mark-price snapshot used by OKX to debit/credit funding.

## Research conclusion

A historical mark-price candle source appears available and is worth testing against the five audited instruments and full funding window. However, this source alone does **not** establish exact settlement marks. Until timestamp semantics and settlement-price equivalence are independently validated, a mark-price candle open/close must be labelled as a candle-derived proxy, not exact realized settlement price.

The current `candle_close_proxy` remains explicitly approximate. Do not change the engine's `exact` mode or mark the funding data as exact based only on the existence of mark-price candle endpoints.

## Next technical validation

1. Inspect current OKX endpoint parameters, history limits, pagination, and retention for historical mark-price candles.
2. Retrieve a small sample for BTC-USDT-SWAP, ETH-USDT-SWAP, SOL-USDT-SWAP, DOGE-USDT-SWAP, and AVAX-USDT-SWAP around known funding timestamps.
3. Verify candle timestamp semantics, coverage, missing rows, duplicates, and whether funding timestamps coincide with minute boundaries.
4. Compare mark-candle open and close values against the existing 1-minute trade-candle close proxy to quantify differences.
5. Search for an official settlement ledger or endpoint that explicitly returns the mark price used for each funding debit/credit. If none exists, define the highest defensible proxy tier and keep it distinct from exact settlement marks.

## Research-use policy pending validation

- **Exact mode:** only when the actual exchange settlement mark or an independently validated equivalent is supplied.
- **Mark-candle proxy mode:** only after full source audit; identify whether open, close, or another field is used.
- **Trade-candle close proxy mode:** remains a lower-confidence fallback and must never be presented as exact.
- Do not authorize final strategy PnL claims while the chosen funding-price approximation is not disclosed and stress-tested.

## Follow-up verification against the current official API guide

A second documentation pass on 2026-11-25 confirmed the following distinctions:

- The official OKX V5 API guide lists separate market-data endpoints for mark-price candles and historical mark-price candles. The historical-mark-price endpoint is a distinct source from the ordinary trade-price candle endpoint. The official guide's market-data section is available at https://www.okx.com/docs-v5/en/ and the API change-log/documentation index at https://www.okx.com/docs-v5/log_en/.
- The documented candle schema is OHLC plus candle timestamp/status. That is a time-bucket summary, not a per-settlement execution/valuation ledger. A matching minute timestamp therefore does not prove which instant within that minute supplied the funding valuation.
- The official account bills documentation also distinguishes funding-fee expense/income event subtypes (173/174) and documents an archived bill-history endpoint for historical account bills. Those records can potentially corroborate actual funding debits/credits for an account, but they are account-specific realized cashflows; they do not provide a universal historical settlement mark series for hypothetical backtests. See https://www.okx.com/docs-v5/en/ (Account bills / bills history archive sections).

### Updated decision

The historical mark-price candle route is technically actionable for a controlled sample test, but it is still only a candidate proxy until validated. The account-bills route is a useful independent cross-check for actual account funding cashflows, not a replacement source for hypothetical strategy funding marks.

No exact settlement-price source has yet been established. Keep Gate 0 / G0-03 open and keep PnL backtests blocked pending a documented decision on acceptable funding-price fidelity.

## Endpoint parameters verified from the current official API guide

The current official guide specifies:

- Historical endpoint: `GET /api/v5/market/history-mark-price-candles`.
- Required `instId`; optional `after`, `before`, `bar`, and `limit`.
- Default bar is `1m`; the documented maximum page size is 100.
- `after` paginates toward records earlier than the supplied candle timestamp; `before` paginates toward newer records.
- The response candle schema is `[ts,o,h,l,c,confirm]`; `ts` is the candle opening timestamp, and `confirm` indicates whether the candle is complete.
- The endpoint description says history is available "from recent years", but the guide does not specify a precise earliest timestamp or guarantee uninterrupted 1-minute coverage for every instrument.

Official endpoint documentation: https://my.okx.com/docs-v5/en/ (Public Data → Get mark price candlesticks history).

### Controlled sample probe added

Added `src/inspect_okx_mark_price_history.py`. It:
1. Loads the five funding CSVs only after validating their hashes and metadata against the committed manifest.
2. Selects first, middle, and last funding timestamps for each instrument (15 sample points total).
3. Requests the 1-minute historical mark-price candle page around each timestamp using the documented `after` cursor.
4. Reports exact timestamp matches, nearest candle timestamp when absent, mark OHLC/confirmation, and the difference between mark-candle close and the local trade-candle close where both exist.
5. Does not write or alter source data, does not label any OHLC field as the settlement mark, and does not run a backtest.

Run from the repository root after syncing:
```bash
PYTHONPATH=src python src/inspect_okx_mark_price_history.py
```

This is deliberately a small coverage/timestamp probe, not a bulk downloader. If it passes, the next stage is a broader but still bounded sample across multiple funding times and all five assets, followed by explicit coverage and difference-distribution analysis. A full 1-minute history pull is not justified until the sample demonstrates that the endpoint returns usable, correctly aligned records.

### Current gate status

The endpoint contract is now sufficiently specified to test pagination and timestamp alignment. Actual API responses for the five assets have not yet been inspected. Gate 0 / G0-03 remains OPEN; no PnL backtest is authorized by this reconnaissance alone.

Implementation note: the probe scans each local 1-minute trade-candle CSV for only the three requested close values instead of loading all five large candle histories into memory. This keeps the first source check practical on the Termux/mobile environment.


## First live sample results (Termux, 2026-11-25)

The user ran the probe against the local funding/candle files and the public OKX endpoint after compiling it successfully.

Observed output:
- 15 requests attempted (first, middle, last settlement for each of five instruments).
- 15 exact-timestamp mark-price candles found.
- 0 API errors and 0 missing mark-price candles.
- All 15 returned candles had `confirm=1`.
- At the five middle samples, mark-candle close and local trade-candle close matched exactly at the printed precision (0.000000 bps).
- The first and last samples for all five assets had no matching local trade candle (10 boundary misses); this was not an OKX mark-candle coverage failure.

The local trade-candle file boundaries reported by the user:
- All assets start at `1760950200000`.
- BTC ends at `1795097640000`; SOL and DOGE at `1795097700000`; AVAX at `1795097760000`; ETH at `1795097640000`.
- The sampled first funding timestamp is `1760918400000`, which is 8 hours 50 minutes before the local trade-candle start.
- The sampled last funding timestamp is `1795104000000`, which is 1 hour 44–46 minutes after the local trade-candle end, depending on asset.

Interpretation:
- The 10 missing trade closes are explained by the local trade-candle dataset boundaries. They must not be counted as missing OKX mark-price candles or as evidence of corrupted candle data.
- This first sample confirms that the historical mark-price endpoint returned complete, exact-minute candles for these 15 selected funding timestamps.
- The five middle close matches are encouraging but are only five observations. They do not establish a general equality between mark-price candles and trade-price candles, nor do they identify the exact funding settlement mark.
- The sample does not establish full-window mark-candle coverage, pagination correctness over the full range, or exact settlement-price equivalence.

Next validation:
1. Expand to a bounded, evenly spaced sample across the full funding history for all five assets (for example, 12 settlements per asset, 60 requests).
2. Record mark-candle open/high/low/close and compare both open and close with local trade-candle close only when the trade timestamp is within local file coverage.
3. Report exact timestamp matches, duplicates, missing mark candles, confirmation status, boundary-excluded trade comparisons, and per-asset difference distributions.
4. Keep `candle_close_proxy` unchanged and Gate 0 / G0-03 OPEN until the broader evidence and settlement-price semantics are assessed.

This section supersedes the earlier statement that actual API responses had not yet been inspected. It does not change the decision that no exact settlement-price source has been established and no PnL backtest is authorized by this reconnaissance.
