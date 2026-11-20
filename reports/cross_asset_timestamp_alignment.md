# Cross-Asset Timestamp Alignment Audit

Status: **FAIL**

- Assets checked: BTC, ETH, SOL, DOGE, AVAX
- Union timestamps: 569,127
- Common timestamps: 569,125
- Identical timestamp sets: False

## Per-asset results

| Asset | Rows | Duplicates | Out of order | Unexpected intervals |
|---|---:|---:|---:|---:|
| BTC | 569125 | 0 | 0 | 0 |
| ETH | 569125 | 0 | 0 | 0 |
| SOL | 569126 | 0 | 0 | 0 |
| DOGE | 569126 | 0 | 0 | 0 |
| AVAX | 569127 | 0 | 0 | 0 |

## Issues

- BTC: missing timestamps
- ETH: missing timestamps
- SOL: missing timestamps
- DOGE: missing timestamps
- The five timestamp sets are not identical

No missing candles were fabricated or forward-filled.

This audit checks timestamp alignment, not strategy profitability.
