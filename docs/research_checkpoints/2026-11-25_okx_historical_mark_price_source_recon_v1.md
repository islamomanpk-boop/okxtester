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
