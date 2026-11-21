# 1-Minute Execution Data and Funding Audit

Funding data status: **NOT FOUND — funding costs must not be assumed to be zero**

## Execution candle results

| Asset | Rows | First UTC | Last UTC | Unexpected intervals |
|---|---:|---|---|---:|
| BTC | 569,125 | 2025-10-20 08:50:00+00:00 | 2026-11-19 14:14:00+00:00 | 0 |
| ETH | 569,125 | 2025-10-20 08:50:00+00:00 | 2026-11-19 14:14:00+00:00 | 0 |
| SOL | 569,126 | 2025-10-20 08:50:00+00:00 | 2026-11-19 14:15:00+00:00 | 0 |
| DOGE | 569,126 | 2025-10-20 08:50:00+00:00 | 2026-11-19 14:15:00+00:00 | 0 |
| AVAX | 569,127 | 2025-10-20 08:50:00+00:00 | 2026-11-19 14:16:00+00:00 | 0 |

## Funding data

No funding-related files were found in the local data directory.

Funding must be obtained and validated separately before claiming fully cost-adjusted perpetual-swap backtest results.

## Execution assumptions required by the backtester

- 15-minute signals become executable only after candle close.
- Market-style entries use the next eligible 1-minute open.
- Limit fills must be checked using 1-minute OHLCV.
- Stop-loss takes priority if stop and target are both touched within one 1-minute candle.
- Maker/taker fees and slippage must be explicit configuration.
- Missing funding data must be reported, never silently set to zero.

## Issues

None detected.

Raw execution CSV files remain local and are not committed to Git.
