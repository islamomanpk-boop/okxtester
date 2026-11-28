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
