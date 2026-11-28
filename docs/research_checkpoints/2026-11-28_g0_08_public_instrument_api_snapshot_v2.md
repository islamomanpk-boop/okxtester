# G0-08 Public OKX instrument API snapshot — 2026-11-28

## Capture provenance

- Captured at: 2026-11-28T18:50:46Z (UTC), as printed by the VPS Python process.
- Source: unauthenticated OKX V5 public instruments REST endpoint.
- Successful host tested: `openapi.okx.com`; `www.okx.com` also returned HTTP 200 in the diagnostic test.
- Request: `GET /api/v5/public/instruments?instType=SWAP&instId=<instrument>` separately for each of the five project instruments.
- API response code: `0` for each instrument; all five returned `state=live`.
- No API key or account credentials were used.

## Captured fields

| Instrument | tickSz | lotSz | minSz | ctVal | ctMult | maxMktSz | maxStopSz | maxTriggerSz |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC-USDT-SWAP | 0.1 | 0.01 | 0.01 | 0.01 | 1 | 35000 | 35000 | 100000000.0000000000000000 |
| ETH-USDT-SWAP | 0.01 | 0.01 | 0.01 | 0.1 | 1 | 90000 | 90000 | 100000000.0000000000000000 |
| SOL-USDT-SWAP | 0.01 | 0.01 | 0.01 | 1 | 1 | 39000 | 39000 | 100000000.0000000000000000 |
| DOGE-USDT-SWAP | 0.00001 | 0.01 | 0.01 | 1000 | 1 | 24000 | 24000 | 100000000.0000000000000000 |
| AVAX-USDT-SWAP | 0.001 | 0.1 | 0.1 | 1 | 1 | 27000 | 27000 | 100000000.0000000000000000 |

All five returned `ctMult=1`, `upcChg=[]`, and the requested instrument IDs. The `ctVal` values are in each instrument's base currency (BTC, ETH, SOL, DOGE, AVAX respectively); `lotSz` and `minSz` are contract quantities. The API response also returned each instrument as a live SWAP. The values above are copied from the user's VPS output; raw response bodies were printed to the terminal but were not saved as a separate raw JSON file or accompanied by a response hash.

## Interpretation and limitations

This is a timestamped current-state snapshot only. An empty `upcChg` array means no upcoming changes were listed at capture; it does not establish that no completed changes occurred previously. It does not provide a historical effective-dated parameter ledger and must not be applied retroactively to the 2025-10 onward research history. Historical `tickSz`, `lotSz`, `minSz`, `ctVal`, `ctMult`, `maxMktSz`, `maxStopSz`, and `maxTriggerSz` remain unverified until supported by archived events or authoritative OKX records.

Official reference: https://www.okx.com/docs-v5/en/#public-data-rest-api-get-instruments
