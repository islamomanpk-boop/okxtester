# G0-08 Historical Instrument Parameter-Change Review V1 — 2026-11-28

## Key finding

Current public instrument metadata is not sufficient to reconstruct historical order constraints over the project's 2025-10 to 2026-11 data interval.

OKX announced on 2025-12-23 that automatic tick-size and minimum-trade-amount adjustments would begin on 2026-01-15. Except in special cases, routine changes would no longer be individually announced; advance notice would be available through GET /api/v5/public/instruments or the Instruments WebSocket channel.

On 2026-04-24, OKX announced a parameter-adjustment notification page consolidating upcoming position-tier, discount-rate, tick-size and minimum-order-size changes. The page supports filters by business line, instrument and status. Whether completed history can be exported/recovered for our five instruments has not yet been established.

## API behavior

The public instruments response field upcChg is an upcoming-change list. It reports the parameter, new value and effective time for pending changes. For SWAP/FUTURES, a minSz change also changes lotSz synchronously. An empty upcChg list in the current snapshot means no pending change at that capture; it is not evidence that no prior change occurred.

The Instruments WebSocket channel publishes a parameter-change event when a task is created and again when it becomes effective. No archived event log for the five project instruments was found in the repository.

## Historical announcement sample

A dated pre-sample example exists: OKX announced on 2023-08-17 that AVAX/USDT perpetual tick size would change from 0.01 to 0.001 effective 2023-08-24. The current AVAX-USDT-SWAP tickSz is 0.001, consistent with that post-change value. This adjustment predates the project dataset start in 2025-10.

The targeted official notices reviewed for 2025 and early 2026 did not list BTC, ETH, SOL, DOGE or AVAX in their affected pairs. However, routine adjustments became automatic from 2026-01-15, so absence from individual notices is not a complete historical record.

## Official sources

- Automatic parameter adjustments effective 2026-01-15: https://www.okx.com/en-us/help/okx-to-enable-automatic-adjustment-of-several-trading-parameters
- Parameter adjustment notification page, 2026-04-24: https://www.okx.com/en-gb/help/okx-launches-parameter-adjustment-notification-page
- AVAX perpetual tick-size adjustment notice, 2023-08-17: https://www.okx.com/en-us/help/okx-to-adjust-tick-size-and-trading-amount-precision-2023-08-17
- Public instruments API and upcChg: https://www.okx.com/docs-v5/en/#public-data-rest-api-get-instruments

## Disposition and next step

Historical tickSz, minSz and lotSz effective dates for 2025-10 through 2026-11 remain UNVERIFIED. Inspect the parameter notification page's completed/status history for BTC-USDT-SWAP, ETH-USDT-SWAP, SOL-USDT-SWAP, DOGE-USDT-SWAP and AVAX-USDT-SWAP, or obtain archived Instruments WebSocket events. Do not apply the current snapshot retroactively.

G0-08 remains OPEN. G0-07 contract rounding remains blocked pending historical effective metadata and account-specific fee assumptions. Gate 0 remains CONDITIONAL HOLD. No strategy PnL, execution simulation, orders or fills were performed or authorized.
