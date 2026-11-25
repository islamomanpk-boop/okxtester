# Price Action V1 — Integrated Portfolio Backtester

## Scope

This module runs multiple assets on one synchronized one-minute timeline.
It manages shared equity, open positions, candidate allocation, exits,
fees, slippage and funding.

It accepts prepared signal candidates. It does not yet generate signals
from the historical 15-minute signal datasets.

## Timeline and event order

For each one-minute timestamp:

1. Apply funding settlements to positions that were already open before
   the settlement timestamp.
2. Process stop-loss and take-profit exits for existing positions.
3. Calculate current marked equity and available gross exposure.
4. Rank and allocate candidates becoming eligible at this timestamp.
5. Enter accepted market-style candidates at the one-minute open.
6. Apply conservative same-minute stop/target handling to new positions.
7. Mark remaining positions at the one-minute close.

At the end of the data, remaining positions are closed at the final
available close with adverse slippage.

## Candidate input

Each candidate must contain:

- `asset`
- `side`: 1 for long, -1 for short
- `signal_available_at`: timestamp in milliseconds
- `signal_priority`: 1, 2 or 3
- `stop_price`
- `stop_distance_atr`
- `target_pct`: decimal percentage, e.g. 0.01 for 1%

The first one-minute candle opening at or after signal availability is
used for entry.

## Portfolio and costs

- Initial equity defaults to $1,000.
- Risk budget defaults to 0.5% of current marked equity per trade.
- Gross exposure is capped at 1x current marked equity.
- One open position per asset.
- Different assets may be held simultaneously.
- Market entries and exits use the configured taker fee and adverse
  slippage assumptions.
- Funding data must be explicitly provided for every asset.
- Positive funding means longs pay and shorts receive.

If a funding event has no explicit mark price, the close of the
one-minute candle at the funding timestamp is used as a proxy. This is
an approximation, not the exact exchange settlement mark.

## Conservative execution

- Stop-loss wins when stop and target are both touched in one minute.
- Stop gaps fill at the opening price with adverse slippage.
- Target gaps fill at the target price with adverse slippage.
- New positions are checked against the entry candle's high and low.
- No entry is allowed before the signal availability timestamp.

## Current limitations

- Only market-style entries are implemented.
- Limit order placement, 45-minute expiry and setup invalidation are not
  implemented yet.
- Candidate generation from the actual signal and regime datasets is
  not implemented yet.
- Portfolio candidate sizing includes an effective per-unit risk estimate:
  entry-to-adverse-stop-exit distance after modeled slippage, plus taker
  fees on entry and stop exit. This cost-adjusted estimate is passed to the
  portfolio allocator. It is still a planned stop-risk estimate, not a
  maximum-loss guarantee: stop gaps, lot/tick rounding and fee-tier mismatch
  can increase realized loss. The standalone single-trade engine has a
  separate stop-distance-only sizing function.
- Funding mark-price fallback is approximate.
- This module is an integration foundation, not a strategy profitability
  result.


## Risk-sizing clarification — 2026-11-25

The portfolio implementation already passes a cost-adjusted `risk_per_unit` to the allocator. This documentation now reflects that code path. The standalone single-trade engine remains less complete; do not assume the two engines have identical sizing semantics.

## Funding validation status — 2026-11-25

The portfolio engine requires a mapping key for each asset and validates supplied events, but an empty list for an asset is accepted and produces no funding cashflows. There is no coverage metadata contract connecting supplied events to audited source files or the requested backtest date range. The 1m-close fallback is approximate, not an exchange settlement mark. Funding source completeness and strict-mode fail-closed validation remain open; see the Gate 0 audit for required remediation. A zero funding PnL is not evidence that funding data was complete.
