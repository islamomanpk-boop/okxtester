# Cross-Asset Timestamp Alignment Audit

Status: **PASS_WITH_TRAILING_DIFFERENCES**

- Assets: BTC, ETH, SOL, DOGE, AVAX
- Union timestamps: 569,127
- Common timestamps: 569,125
- Combined dataset rows: 569,125
- Trailing-only differences: True
- Synchronized dataset: `/data/data/com.termux/files/home/okx_scalping_data/synchronized_5asset_1m.csv`

## Per-asset results

| Asset | Rows | Duplicates | Out of order | Unexpected intervals |
|---|---:|---:|---:|---:|
| BTC | 569125 | 0 | 0 | 0 |
| ETH | 569125 | 0 | 0 | 0 |
| SOL | 569126 | 0 | 0 | 0 |
| DOGE | 569126 | 0 | 0 | 0 |
| AVAX | 569127 | 0 | 0 | 0 |

## Issues

None detected.

Only exact common timestamps were retained.
No forward filling or fabricated candles were used.
Original source CSV files were not modified.

This audit checks data alignment, not strategy profitability.
