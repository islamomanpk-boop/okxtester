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
