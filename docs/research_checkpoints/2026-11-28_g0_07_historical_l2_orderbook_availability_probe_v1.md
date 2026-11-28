# G0-07 Historical L2 Order-Book Availability Probe V1 — 2026-11-28

## Purpose and status

This checkpoint records a new official OKX data source that may materially improve the project's stop-execution-cost evidence. It is a discovery and availability probe only. No historical archive is downloaded by this workflow, and no execution or PnL simulation is run.

G0-07 remains OPEN and Gate 0 remains CONDITIONAL HOLD until actual archive availability, contents, timestamps, continuity, depth units and representativeness are verified.

## Official source discovery

OKX's public historical market-data endpoint is:

`GET /api/v5/public/market-data-history`

The current API documentation identifies:
- Module 4: 400-level historical order book.
- Module 5: 5,000-level historical order book, available from 2025-11-01.
- Module 6: 50-level order book, being gradually deprecated in favor of modules 4 and 5.
- The endpoint returns downloadable archive metadata (file name, size, URL), not the archive bytes.
- Daily queries are limited to 10 days; order-book timestamps are interpreted in UTC.
- OKX explicitly warns that historical backfill is in progress and availability can vary by module, instrument and period. Order-book data is typically available T+3.

The public Historical Market Data page advertises high-resolution L2 order-book data from March 2023. This is a product-level availability statement, not a guarantee that every target instrument/date has a complete archive.

Official references:
- https://www.okx.com/docs-v5/en/#public-data-rest-api-get-historical-market-data
- https://www.okx.com/historical-data

## Probe scope

The read-only probe queries five project instrument families:
BTC-USDT, ETH-USDT, SOL-USDT, DOGE-USDT and AVAX-USDT.

Sample points:
- 2025-10-20, module 4 (project dataset start).
- 2025-11-01, modules 4 and 5 (module 5 stated availability start).
- 2026-06-01, modules 4 and 5 (mid-period).
- 2026-11-19, modules 4 and 5 (latest project data date).

The probe records returned archive names, URLs, sizes and missing instrument/date combinations. It uses public GET requests only and no API credentials. It does not download archives or claim intraday completeness.

## Acceptance requirements after availability check

1. Verify archive presence for each asset and relevant date.
2. Download a small representative archive for each module and inspect its format, schema, timezone, timestamp granularity and depth units.
3. Verify archive timestamps, sequence/continuity where available, missing intervals, duplicates and bid/ask integrity.
4. Determine whether the L2 snapshots can be aligned to the strategy's entry/stop event times and used to estimate spread and visible depth.
5. Build a conservative execution-cost model that separates observed spread/depth from unobserved latency, queue position and market impact.
6. Do not interpret visible L2 depth as guaranteed executable liquidity or a historical fill guarantee.

The historical OHLCV gap audit remains candle-open proxy evidence. Historical L2 data, if available and validated, can improve spread/depth analysis but cannot alone recreate matching-engine queue priority, hidden liquidity, latency or exact stop-market fills.

## Files

- Probe: `src/probe_okx_historical_orderbook_availability.py`
- Tests: `src/test_probe_okx_historical_orderbook_availability.py`
- Workflow: `.github/workflows/g0-07-historical-orderbook-availability.yml`
- Local/CI manifest: `reports/g0_07_historical_orderbook_availability_v1.json` (CI artifact only; no private data).

No existing backtest engine, strategy logic, historical candle dataset, or execution configuration is modified.
