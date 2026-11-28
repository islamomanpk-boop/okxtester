# Price Action V1 — Execution Engine

## Scope

The initial execution engine simulates one market-entry trade using
one-minute OHLC candles. It supports long and short positions, risk-based
quantity sizing, stop-loss and take-profit exits, fees, slippage and
historical funding events.

## Entry timing

A signal becomes eligible only at its explicit `signal_available_at`
timestamp. The entry selector chooses the first one-minute candle whose
opening timestamp is at or after that availability timestamp.

## Position sizing

- Default risk budget: 0.5% of current equity.
- Default gross exposure cap: 1.0x equity.
- Quantity is the lower of stop-risk-based quantity and exposure-capped
  quantity.

## Execution assumptions

- Market entry uses the eligible candle open.
- Slippage is adverse to the trader.
- Fees are explicit configuration inputs; no exchange fee tier is assumed.
- Stop-loss has priority if stop and target are both touched in one candle.
- A stop gap is filled at the candle open, with adverse slippage.
- A target gap is conservatively filled at the target, with adverse slippage.
- If neither stop nor target is reached, the trade exits at the last
  available candle close.

## Funding

Funding input is a required `funding_contract` containing explicit `events`
and `coverage` metadata. The shared validator checks instrument identity,
source SHA-256, coverage bounds, versioned settlement schedule, event
completeness, chronological uniqueness, finite rates, and mark-price mode.
The trade's complete holding interval is checked against verified coverage
and expected settlements before a result is returned.

Positive funding means longs pay and shorts receive. Funding notional uses
quantity multiplied by the settlement price. `exact` mode requires a positive
finite `mark_price` on every event. `candle_close_proxy` mode may use the
settlement-minute candle close when an event has no mark; this is explicitly
labelled in trade output and is not the exact OKX settlement mark. The current
audited realized-rate CSVs do not contain exact settlement marks.

## Limitations

This is the single-trade execution foundation, not the complete portfolio
backtester. It does not yet implement maker limit orders, multiple
simultaneous positions, portfolio-wide capital allocation, or strategy
signal generation. These will be added and tested in later stages.


## Risk-sizing update — 2026-11-28

Standalone sizing now uses the same planned per-unit stop-risk model as the portfolio allocator:
- entry price is the adverse-slippage-adjusted fill;
- stop exit is adjusted for adverse exit slippage;
- entry and stop-exit taker fees are included in planned per-unit risk;
- quantity is capped by both the configured risk budget and gross-exposure limit.

The reported `planned_stop_risk` remains the price-distance component. The additional `planned_cost_adjusted_risk` and `risk_per_unit` fields expose the full modeled sizing amount. This is a planned-stop model, not a maximum-loss guarantee: gap-through-stop losses can exceed the budget, and exchange lot/tick/minimum-quantity constraints are not yet applied. Those contract constraints require verified G0-08 instrument metadata before implementation.

## Funding contract implementation — 2026-11-25

The standalone engine now requires an explicit `funding_contract`; omission can no longer silently mean zero funding. Coverage and schedule validation are shared with the portfolio engine through `src/funding_coverage.py`. Trade output includes mark-price mode, source hash, instrument, schedule ID, and settlement count. The current runner uses explicitly labelled candle-close proxy marks. Real local CSV hash verification and exact-mark policy acceptance remain outstanding G0-03 acceptance items; see `docs/research_checkpoints/2026-11-25_g0-03_funding_contract_implementation_plan_v1.md`.
