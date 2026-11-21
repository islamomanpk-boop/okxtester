# OKX Historical Funding Data — Reconciliation Audit

- Requested range: 2025-10-20 00:00 UTC to 2026-11-19 23:59:59 UTC
- Instruments: BTC, ETH, SOL, DOGE, AVAX USDT perpetual swaps
- Archive source: OKX monthly historical funding ZIP files
- API source: OKX public funding-rate-history endpoint
- API field used: `realizedRate` (actual settled rate)
- Overlapping archive/API timestamps were compared before merging.
- Rate comparison tolerance: 1E-12

## Results

| Asset | Archive rows | API rows in range | Overlap checked | Merged rows | First UTC | Last UTC |
|---|---:|---:|---:|---:|---|---|
| BTC | 1130 | 277 | 219 | 1188 | 2025-10-20T00:00:00+00:00 | 2026-11-19T16:00:00+00:00 |
| ETH | 1130 | 277 | 219 | 1188 | 2025-10-20T00:00:00+00:00 | 2026-11-19T16:00:00+00:00 |
| SOL | 1130 | 277 | 219 | 1188 | 2025-10-20T00:00:00+00:00 | 2026-11-19T16:00:00+00:00 |
| DOGE | 1130 | 277 | 219 | 1188 | 2025-10-20T00:00:00+00:00 | 2026-11-19T16:00:00+00:00 |
| AVAX | 1130 | 277 | 219 | 1188 | 2025-10-20T00:00:00+00:00 | 2026-11-19T16:00:00+00:00 |

## Observed settlement intervals

Intervals are measured from the actual timestamps. No fixed eight-hour schedule is assumed.

### BTC

`{480: 1187}` minutes

### ETH

`{480: 1187}` minutes

### SOL

`{480: 1187}` minutes

### DOGE

`{480: 1187}` minutes

### AVAX

`{480: 1187}` minutes

## Validation

- All five assets passed archive schema and instrument checks.
- All API records used for merging contained `realizedRate`.
- Archive/API overlap met the minimum comparison count.
- No overlapping funding-rate conflicts were found.
- Duplicate timestamp conflicts were rejected.
- Output timestamps are sorted and unique.
- Processed CSV files were replaced only after all five assets passed.

## Storage

Processed CSVs and raw ZIP archives remain outside normal Git history. Code, tests, documentation and this audit report belong in Git.
