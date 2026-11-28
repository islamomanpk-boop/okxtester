# G0-08 Public Instrument Metadata Snapshot V1 — 2026-11-28

## Disposition

Current public metadata snapshot passed for all five project USDT perpetuals. This closes the current public-snapshot subtask only. G0-08 remains OPEN because historical effective metadata and account-specific fee rates remain unverified.

## Reproducible evidence

- Code commit: 2030c5a0976d8a54d984dda928f65c2f0ac1ebce.
- Successful workflow: https://github.com/islamomanpk-boop/okxtester/actions/runs/46159574942
- Artifact name: g0-08-public-instrument-metadata-v1.
- Artifact ID: 15269286504.
- Artifact ZIP SHA-256: 2db7e1ef98469d0ca4a08702c92600d8dfca55e32b606eb8728a6bee3b6ca5f8.
- Canonical raw metadata SHA-256: b435bb456abb3cc388462ff3cd28067ecf95a2cebd572602d11a67216dace9cf.
- Report status: OKX_PUBLIC_INSTRUMENT_METADATA_SNAPSHOT_PASS_CURRENT_ONLY.
- Capture time: 2026-11-28 15:23:07.736–15:23:09.254 UTC.
- API errors: none; upcoming changes: none for all five instruments at capture.

## Current instrument snapshot

| Instrument | Contract value | Multiplier | Tick size | Lot size | Minimum size | Minimum base units | Max market / stop size | Fee group |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC-USDT-SWAP | 0.01 BTC | 1 | 0.1 USDT | 0.01 contracts | 0.01 contracts | 0.0001 BTC | 35,000 / 35,000 contracts | 4 |
| ETH-USDT-SWAP | 0.1 ETH | 1 | 0.01 USDT | 0.01 contracts | 0.01 contracts | 0.001 ETH | 90,000 / 90,000 contracts | 4 |
| SOL-USDT-SWAP | 1 SOL | 1 | 0.01 USDT | 0.01 contracts | 0.01 contracts | 0.01 SOL | 39,000 / 39,000 contracts | 4 |
| DOGE-USDT-SWAP | 1,000 DOGE | 1 | 0.00001 USDT | 0.01 contracts | 0.01 contracts | 10 DOGE | 24,000 / 24,000 contracts | 4 |
| AVAX-USDT-SWAP | 1 AVAX | 1 | 0.001 USDT | 0.1 contracts | 0.1 contracts | 0.1 AVAX | 27,000 / 27,000 contracts | 4 |

All five records passed validation for exact instrument ID, SWAP type, linear contract, base-currency contract value, USDT settlement, live state, positive contract/tick/lot/minimum values, integer minSz/lotSz relationship, and upcoming-change schema.

For derivatives, OKX expresses lotSz and minSz in contracts. The base-unit minimums above are derived from current contract value × minimum contract count; they are not a substitute for exchange contract quantity when submitting an order.

## Fee-tier boundary

All five instruments currently report groupId=4. This is the instrument fee-group mapping, not the account's VIP level or actual fee rate. The OKX GET /api/v5/account/trade-fee endpoint is authenticated and returns current-account fee rates. No private credentials or account endpoint were used. Actual account-specific taker/maker fees remain unknown.

## Historical metadata boundary

This endpoint returns current instrument metadata and upcoming upcChg changes; it does not provide a historical effective-dated metadata timeline. The snapshot does not prove that current ctVal, tickSz, lotSz or minSz values applied throughout the historical dataset from 2025-10 to 2026-11. Archived snapshots or authoritative dated OKX change notices are still required.

## Next safe work

1. Reconstruct effective-dated historical metadata for all five instruments across the research period.
2. Obtain actual account fee rates through an authorized read-only source, without sharing API secrets in chat; otherwise document a clearly approved conservative fee assumption.
3. Implement and test contract conversion, floor-to-lot rounding, minimum-size rejection, conservative stop-price tick rounding and post-rounding risk recalculation.
4. Keep G0-07 open until the above rounding and stop-gap/execution assumptions are verified.

No strategy PnL, trade simulation, execution simulation, orders, fills, Gate 2+ or live trading was performed or authorized.

## Official OKX references

- https://www.okx.com/docs-v5/en/#public-data-rest-api-get-instruments
- https://www.okx.com/docs-v5/en/#trading-account-rest-api-get-fee-rates
