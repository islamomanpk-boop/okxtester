# 1-Minute Data Quality Audit

Audit date: 2026-11-20
Assets: BTC, ETH, SOL, DOGE, AVAX
Timeframe: 1 minute

| Coin | Rows | Duplicates | Missing | Invalid OHLCV |
|---|---:|---:|---:|---:|
| BTC | 569125 | 0 | 0 | 0 |
| ETH | 569125 | 0 | 0 | 0 |
| SOL | 569126 | 0 | 0 | 0 |
| DOGE | 569126 | 0 | 0 | 0 |
| AVAX | 569127 | 0 | 0 | 0 |

Historical coverage:
Start: 2025-10-20 08:50 UTC

BTC / ETH end: 2026-11-19 14:14 UTC
SOL / DOGE end: 2026-11-19 14:15 UTC
AVAX end: 2026-11-19 14:16 UTC

All five datasets passed the reported
individual data-quality checks.

No duplicate timestamps.
No missing 1-minute candles.
No invalid timestamps.
No out-of-order timestamps.
No invalid numeric rows.
No invalid OHLCV rows.

IMPORTANT:
Cross-asset timestamp synchronization
still needs verification before portfolio
backtesting.

Source: Termux data quality audit output.
