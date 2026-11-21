# Execution Data Audit V1

## Purpose

Validate the local one-minute OHLCV data used by the price-action
backtester and document whether historical funding data is available.

## Inputs

Five local files under `~/okx_scalping_data/`:

- BTC_USDT_USDT_1m.csv
- ETH_USDT_USDT_1m.csv
- SOL_USDT_USDT_1m.csv
- DOGE_USDT_USDT_1m.csv
- AVAX_USDT_USDT_1m.csv

Expected columns: ts, open, high, low, close, vol.

## Checks

- Required columns and nonempty datasets.
- Valid integer millisecond timestamps.
- Duplicate and chronological timestamp checks.
- One-minute interval continuity.
- Numeric and positive OHLC prices.
- Valid OHLC candle structure.
- Non-negative volume.

## Funding limitation

Funding data is audited separately. Missing funding history must not be
silently interpreted as zero funding. A fully cost-adjusted perpetual
swap backtest requires validated historical funding records.

## Output

`reports/execution_data_audit.md`

Raw market data remains local and is not committed to Git.
