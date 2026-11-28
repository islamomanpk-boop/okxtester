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


## Local account-specific fee probe — 2026-11-28

A local-only authenticated fee probe was added in commit a5ac62831cfba902b2af5dae3b35c13b46a4d333:
- Script: src/inspect_okx_account_fee_rates_readonly.py
- Offline tests: src/test_okx_account_fee_rates_readonly.py
- Successful CI validation: https://github.com/islamomanpk-boop/okxtester/actions/runs/46159858988
- Artifact ID: 15269490178
- Artifact ZIP SHA-256: c789262b49b71841d91afb41fe541155128d93f14c4aa40f96af4f12fbc6a911

The workflow compiled the probe, passed its 10 offline tests, and repeated the current public metadata snapshot. It did not call the authenticated fee endpoint and did not receive credentials. The probe is intended to be run locally with a dedicated API key having Read permission only and no Trade/Withdraw permissions. It calls only the public server-time and authenticated trade-fee GET endpoints; it does not place or modify orders and does not print or save credentials. The account-specific output is written locally and is not uploaded to GitHub.

Termux instructions: docs/g0_08_fee_instrument_assumptions_methodology_v1.md.

The account fee rates remain unknown until the owner runs the local probe or supplies a fee statement/export. G0-08 remains OPEN; no fee tier is inferred from instrument groupId 4.


## Historical parameter-change policy review

OKX announced that automatic tick-size and minimum-trade-amount adjustments would begin on 2026-01-15. Routine changes would no longer be individually announced except special cases; advance notices are available through the public instruments endpoint and Instruments WebSocket channel. On 2026-04-24, OKX announced a parameter-adjustment notification page for upcoming tick-size, minimum-order-size, position-tier and discount-rate changes.

The current public instruments response field upcChg is an upcoming-change list. Its empty value at capture proves only that no change was pending then; it does not prove there were no prior changes. The Instruments WebSocket channel pushes both task creation and effective-time events. No archived channel-event history for the five project instruments was found in the repository.

One dated pre-sample example was identified: AVAX/USDT perpetual tick size changed from 0.01 to 0.001 effective 2023-08-24, matching the current AVAX tick size. This predates the project data window beginning 2025-10. The targeted individual 2025/early-2026 notices reviewed did not list the five target instruments, but routine adjustments became automatic from 2026-01-15, so those notices are not a complete historical record.

The parameter notification page has an instrument and status filter, but completed-history retrieval/export for these five instruments has not yet been established. Historical tickSz, minSz and lotSz effective dates for 2025-10 to 2026-11 remain UNVERIFIED. Do not apply current values retroactively.

Official references:
- https://www.okx.com/en-us/help/okx-to-enable-automatic-adjustment-of-several-trading-parameters
- https://www.okx.com/en-gb/help/okx-launches-parameter-adjustment-notification-page
- https://www.okx.com/en-us/help/okx-to-adjust-tick-size-and-trading-amount-precision-2023-08-17
- https://www.okx.com/docs-v5/en/#public-data-rest-api-get-instruments
