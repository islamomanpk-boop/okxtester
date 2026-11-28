# G0-08 — Fee and Instrument Assumptions Methodology V1

## Purpose

Establish verified OKX instrument contract metadata, order-size rounding constraints and applicable trading-fee assumptions for the five project USDT perpetuals: BTC, ETH, SOL, DOGE and AVAX.

## Public instrument metadata

Use the unauthenticated OKX V5 endpoint:

GET /api/v5/public/instruments?instType=SWAP&instId=<ASSET>-USDT-SWAP

Required fields:
- Identity/status: instId, instType, state, listTime, expTime
- Contract model: ctType, ctVal, ctValCcy, ctMult, settleCcy
- Price/quantity precision: tickSz, lotSz, minSz
- Exchange size limits: maxMktSz, maxStopSz, maxTriggerSz
- Fee mapping: groupId
- Scheduled metadata changes: upcChg

For derivatives, lotSz and minSz are expressed in contracts, not base currency. For linear USDT swaps, contract notional is based on contract count × contract value × mark price. Do not treat candle CSV base-currency volume as exchange order contract count.

## Current snapshot evidence

The current-only public snapshot is in docs/research_checkpoints/2026-11-28_g0_08_public_instrument_metadata_snapshot_v1.md and artifact 15269286504.

| Instrument | ctVal | tickSz | lotSz | minSz |
|---|---:|---:|---:|---:|
| BTC-USDT-SWAP | 0.01 BTC | 0.1 USDT | 0.01 contracts | 0.01 contracts |
| ETH-USDT-SWAP | 0.1 ETH | 0.01 USDT | 0.01 contracts | 0.01 contracts |
| SOL-USDT-SWAP | 1 SOL | 0.01 USDT | 0.01 contracts | 0.01 contracts |
| DOGE-USDT-SWAP | 1,000 DOGE | 0.00001 USDT | 0.01 contracts | 0.01 contracts |
| AVAX-USDT-SWAP | 1 AVAX | 0.001 USDT | 0.1 contracts | 0.1 contracts |

All five currently report linear contracts, multiplier 1, USDT settlement, live state and groupId 4.

## Contract rounding principles to validate before engine integration

- Convert base-asset exposure to contract count using the verified contract-value convention for each instrument.
- Floor contract quantity to a valid lotSz increment; never round up beyond the risk budget.
- If the floored quantity is below minSz, reject/skip the candidate rather than rounding up.
- Apply the exchange price tick to stop/trigger prices in the explicitly conservative direction, then recompute risk using the rounded stop.
- Enforce current/historical maxMktSz, maxStopSz and maxTriggerSz limits where applicable.
- Test BTC/ETH/SOL/DOGE/AVAX separately; DOGE and AVAX have materially different contract increments and base units.
- Do not integrate the current snapshot into historical backtests until effective-date metadata is verified for the full data period.

## Fee assumptions

The public instrument groupId identifies the instrument fee group; it does not establish the user's account VIP level or actual taker rate. OKX's GET /api/v5/account/trade-fee endpoint is authenticated and returns current-account fee data. No API credentials are used by the public metadata audit.

Account-specific maker/taker rates must be supplied from an authorized, read-only account source or a user-provided fee statement. Never infer the fee tier from groupId, assume the lowest VIP level, or paste API secrets into chat. If the exact account tier is unavailable, keep fee assumptions explicitly provisional and do not close G0-08.

## Historical metadata limitation

The public instruments endpoint returns current metadata and an upcChg list of upcoming changes. It does not provide a historical effective-dated tick/lot/contract-value timeline. The current snapshot therefore cannot prove that the same values applied throughout 2025-10 to 2026-11. Historical changes must be reconstructed from archived exchange snapshots or authoritative dated OKX notices before using current values across the historical research period.

## Acceptance status

G0-08 remains OPEN until:
1. Current metadata for all five instruments is captured and validated.
2. Historical effective metadata is verified for the full research interval, including any tick/lot/contract-value changes.
3. Actual account fee tier/rates or a clearly approved conservative fee assumption are documented.
4. Contract quantity and stop-price rounding are implemented with fail-closed tests and risk is recalculated after rounding.

The current public snapshot completes only item 1. It does not close G0-08 or authorize strategy PnL backtesting, execution simulation, orders, fills or live trading.

## Official OKX references

- Public instrument metadata: https://www.okx.com/docs-v5/en/#public-data-rest-api-get-instruments
- Authenticated account fee rates: https://www.okx.com/docs-v5/en/#trading-account-rest-api-get-fee-rates


## Local account fee-rate capture

The current account's actual maker/taker rates are available through the authenticated OKX endpoint GET /api/v5/account/trade-fee. The local-only probe is src/inspect_okx_account_fee_rates_readonly.py. It requests each SWAP family using instType=SWAP and instFamily=<ASSET>-USDT, then matches the response feeGroup entry to the current public instrument groupId (currently 4 for all five).

Use a dedicated API key with Read permission only. Do not enable Trade or Withdraw permission. The script never calls order/trade/withdrawal endpoints, never prints credentials, and writes the fee report locally. The report contains account-specific fee level/rates and should not be committed or uploaded unless the owner explicitly chooses to share it.

Termux example (run from the repository root; these read prompts do not echo the values in the terminal):

```bash
read -r -s -p "OKX API key (Read only): " OKX_API_KEY; echo
read -r -s -p "OKX API secret: " OKX_API_SECRET; echo
read -r -s -p "OKX API passphrase: " OKX_API_PASSPHRASE; echo
export OKX_API_KEY OKX_API_SECRET OKX_API_PASSPHRASE
python src/inspect_okx_account_fee_rates_readonly.py --output reports/g0_08_account_fee_rates_local_v1.json
unset OKX_API_KEY OKX_API_SECRET OKX_API_PASSPHRASE
```

The script uses OKX server time for request signing. It fails closed if any asset's fee row or groupId mapping is missing. Negative raw rates are commissions and are converted to positive cost rates; positive raw rates are rebates and are not credited as negative costs. The offline tests are included in the G0-08 CI workflow; the authenticated probe itself is deliberately not run in GitHub Actions.

If the owner does not want to use an API key, an account fee-rate statement/export can be reviewed instead. Never send API secrets in chat.


## Exchange parameter-change history — important 2026 policy

OKX announced on 2025-12-23 that automatic tick-size and minimum-trade-amount adjustments would begin on 2026-01-15. Except in special cases, routine changes would no longer be individually announced; advance notice would be available through the public instruments endpoint or the Instruments WebSocket channel.

On 2026-04-24, OKX announced a parameter-adjustment notification page for upcoming position-tier, discount-rate, tick-size and minimum-order-size changes. Routine changes would no longer be individually announced. The page offers business-line, instrument and status filters.

The public instruments field upcChg is explicitly an upcoming-change list. It contains the parameter name, new value and effective time for pending changes. For SWAP/FUTURES, a minSz change is accompanied by a synchronous lotSz change. An empty upcChg list in the current snapshot is not a historical no-change guarantee.

The Instruments WebSocket channel pushes a parameter-change event when the task is created and another when the change becomes effective. If archived event logs exist, they can provide effective-dated metadata. No such archive is currently recorded in the repository.

A pre-sample historical example was found: the OKX 2023-08-17 notice states that AVAX/USDT perpetual tick size changed from 0.01 to 0.001 effective 2023-08-24. This predates the project candle dataset beginning in 2025-10 and matches the current AVAX-USDT-SWAP tick size of 0.001. The targeted 2025/early-2026 individual notices reviewed did not list BTC, ETH, SOL, DOGE or AVAX; however, routine adjustments became automatic from 2026-01-15, so absence from individual notices is not complete proof.

Official references:
- https://www.okx.com/en-us/help/okx-to-enable-automatic-adjustment-of-several-trading-parameters
- https://www.okx.com/en-gb/help/okx-launches-parameter-adjustment-notification-page
- https://www.okx.com/en-us/help/okx-to-adjust-tick-size-and-trading-amount-precision-2023-08-17
- https://www.okx.com/docs-v5/en/#public-data-rest-api-get-instruments

Until completed parameter history can be recovered from the notification page or archived WebSocket events, historical tickSz/minSz/lotSz effective dates for 2025-10 to 2026-11 remain unverified. Do not apply the current snapshot retroactively.


### Additional targeted notice review — 2026-11-28

The 2025-10-21 OKX notice schedules a 2025-10-24 tick-size adjustment batch; its listed perpetual instruments do not include BTC, ETH, SOL, DOGE or AVAX. The 2025-12-22 notice schedules a 2025-12-24 batch; its listed perpetual instruments also do not include these five project instruments. These are only two dated notice batches, not an exhaustive change history.

The official parameter page is https://www.okx.com/en-gb/trade-market/parameter-changes. The 2026-04-24 announcement confirms filters for business line, instrument and status, but does not state the retention period for completed records or whether a complete export is available.

The current API's `upcChg` only reports upcoming changes. The documented parameter set is `tickSz`, `minSz` (with `lotSz` synchronously changed for SWAP/FUTURES), and `maxMktSz`. It does not provide a historical ledger for `ctVal`, `ctMult`, `maxStopSz`, or `maxTriggerSz`. The Instruments WebSocket channel can push metadata updates, but no archived event history for the five instruments is presently recorded in this repository.

**Next evidence requirement:** inspect the notification page's completed records for BTC-USDT-SWAP, ETH-USDT-SWAP, SOL-USDT-SWAP, DOGE-USDT-SWAP and AVAX-USDT-SWAP over 2025-10 through 2026-11. Record every before/after value and exact effective timestamp. Separately obtain authoritative evidence for any contract-value/multiplier or maximum stop/trigger-size changes; do not assume the parameter page covers them. If the page does not expose completed history, request an effective-dated change export from OKX support or locate archived Instruments WebSocket captures. Until then, historical metadata remains unverified and current values must not be applied retroactively.

Additional official notices:
- 2025-10-21 batch (effective 2025-10-24): https://www.okx.com/en-us/help/okx-to-adjust-tick-size-of-spots-margins-and-futures-20251021
- 2025-12-22 batch (effective 2025-12-24): https://www.okx.com/en-us/help/okx-to-adjust-tick-size-of-spots-margins-and-futures-20251222
- Parameter notification page: https://www.okx.com/en-gb/trade-market/parameter-changes


## VPS public instrument API capture — 2026-11-28 18:50:46 UTC

A read-only request from the project VPS successfully queried the five SWAP instruments through `https://openapi.okx.com/api/v5/public/instruments`. Both `openapi.okx.com` and `www.okx.com` returned HTTP 200 during the diagnostic test. No credentials were used. The response code was `0` for all five instruments; all were live and all returned an empty `upcChg` list.

| Instrument | tickSz | lotSz | minSz | ctVal | ctMult | maxMktSz | maxStopSz | maxTriggerSz |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC-USDT-SWAP | 0.1 | 0.01 | 0.01 | 0.01 BTC | 1 | 35,000 | 35,000 | 100,000,000 |
| ETH-USDT-SWAP | 0.01 | 0.01 | 0.01 | 0.1 ETH | 1 | 90,000 | 90,000 | 100,000,000 |
| SOL-USDT-SWAP | 0.01 | 0.01 | 0.01 | 1 SOL | 1 | 39,000 | 39,000 | 100,000,000 |
| DOGE-USDT-SWAP | 0.00001 | 0.01 | 0.01 | 1,000 DOGE | 1 | 24,000 | 24,000 | 100,000,000 |
| AVAX-USDT-SWAP | 0.001 | 0.1 | 0.1 | 1 AVAX | 1 | 27,000 | 27,000 | 100,000,000 |

Full capture note: `docs/research_checkpoints/2026-11-28_g0_08_public_instrument_api_snapshot_v2.md`.

**Interpretation:** this confirms a successful current-state capture, not historical parameter continuity. Empty `upcChg` means no upcoming changes were returned at capture; it is not evidence that no completed changes occurred. The raw response was not saved separately or hashed. Historical effective-dated values remain UNVERIFIED; do not apply this snapshot retroactively. G0-08 remains OPEN and Gate 0 remains CONDITIONAL HOLD.
