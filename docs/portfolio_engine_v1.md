# Price Action V1 — Portfolio Allocator

## Purpose

The portfolio allocator processes candidates that become eligible at the
same decision timestamp. It allocates one shared equity balance across
BTC, ETH, SOL, DOGE and AVAX.

This module allocates positions only. It does not yet simulate exits or
produce strategy performance results.

## Capital rules

- Starting equity is $1,000.
- Risk budget per accepted trade is 0.5% of current equity.
- Gross notional exposure is capped at 1x current equity.
- Existing open positions consume exposure before new candidates.
- Only one open position per asset is allowed.
- Multiple different assets may be open simultaneously.

## Candidate priority

Priority is fixed and must not use future outcomes:

- Priority 3: confirmed support/resistance rejection or first OB retest.
- Priority 2: engulfing or pin bar at a confirmed S/R level.
- Priority 1: standalone engulfing or pin bar.

Within a priority tier, smaller ATR-normalized stop distance ranks first.
Asset symbol alphabetically breaks any remaining tie.

## Allocation

For each candidate, quantity is the smaller of:
- Risk budget divided by entry-to-stop distance.
- Remaining portfolio exposure divided by entry price.

Candidates are processed in deterministic priority order. Rejected
candidates include a reason.

## Important limitations

This first allocator assumes candidate entries are market-style entries
with known entry and stop prices. It does not yet reserve capital for
pending limit orders, model fees/slippage in risk sizing, or update
positions as minute-by-minute exits occur. Those belong in the integrated
portfolio backtester and will be tested separately.
