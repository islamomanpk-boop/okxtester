# G0-07 — OKX Public OHLCV Source Sample Verification V1 — 2026-11-28

## Result

A read-only sample verifier compared 7 deterministic samples per asset against the public OKX V5 history-candles endpoint. Samples cover exact-open/previous-close transitions, changed-open transitions, and each asset's largest adjacent opening jump.

| Asset | OHLC matches | CSV volume matches OKX base volume | CSV volume matches OKX contract volume |
|---|---:|---:|---:|
| BTC | 7/7 | 7/7 | 0/7 |
| ETH | 7/7 | 7/7 | 0/7 |
| SOL | 7/7 | 7/7 | 7/7 |
| DOGE | 7/7 | 7/7 | 0/7 |
| AVAX | 7/7 | 7/7 | 7/7 |
| **Total** | **35/35** | **35/35** | **14/35** |

No API errors occurred. The overall status is `OKX_SAMPLE_OHLC_AND_BASE_VOLUME_MATCH_NOT_FULL_PROVENANCE`.

## Interpretation

- The sampled OHLC rows match OKX V5 exactly, strongly supporting OKX as the source of these five market datasets.
- The CSV volume field matches OKX `volCcy` (base-currency volume) in all 35 samples.
- It does not match contract volume (`vol`) for BTC, ETH or DOGE. It matches contract volume for SOL and AVAX in the sampled rows because the two units coincide for those sampled instruments.
- Treat the CSV volume column as base-currency volume, not exchange contract count. Do not use it as contract quantity or for lot-size rounding.
- The 53.86%–58.47% exact adjacent open/previous close match rates are consistent with the sampled OKX candles. They are not, by themselves, proof of synthetic stitching.
- This is a deterministic sample check, not a full-file row-by-row certification. The original full-file acquisition/normalization manifest remains undocumented.

## Reproducible evidence

- Code commit: `d64fda55b62bb1f4a086bb1c820d4cfac8d64952`.
- Successful workflow: [46157813117](https://github.com/islamomanpk-boop/okxtester/actions/runs/46157813117).
- Job: [141018443115](https://github.com/islamomanpk-boop/okxtester/actions/runs/46157813117/job/141018443115).
- Artifact: `g0-07-stop-gap-and-source-verification-v1`, ID `15267999478`.
- Combined artifact ZIP SHA-256: `9deaae351954f7046c42e4a189cef8a7f61b68bbfb09371aaa18f3cee14ea76d`.
- Gap report JSON SHA-256: `5262b452e72c9cd1765c9b8576a5fcfaa11bb22b8d81058f46e7d75e0252800c`.
- Source verification JSON SHA-256: `346b81ad2beb3f82848ff47b1516be9d382b2f8dc12613c3e0108cbafc7de4e8`.

## Remaining G0-07 work

1. Retain the historical gap results as sample-supported but preliminary; this is not a maximum-loss guarantee.
2. Resolve actual stop-order trigger reference, order-book depth, spread, latency, market impact and stop-market slippage assumptions.
3. Complete lot/tick/minimum-quantity rounding only after G0-08 instrument metadata and fee assumptions are verified.
4. Preserve the base-currency volume unit explicitly in data contracts and loaders.

No strategy PnL, strategy trade simulation, execution simulation, orders, fills, Gate 2+ or live trading was performed or authorized. G0-07 remains OPEN; Gate 0 remains CONDITIONAL HOLD.
