# G0-07 — Historical Stop-Gap Risk Methodology V1.1

## Purpose

Quantify minute-to-minute opening jumps and how often the next one-minute open has already crossed a hypothetical stop. This is a risk-control audit, not a strategy test.

## Empirical method

For every pair of consecutive, exactly one-minute candles:

- Use the previous candle close as a hypothetical reference entry.
- Apply the sensitivity stop grid (default: 0.05%, 0.1%, 0.15%, 0.2%, 0.25%, 0.5%, 1%, 1.5%, 2%, 3%, 5%).
- For a long, count an open-through-stop event when the next candle open is at or below the hypothetical stop.
- For a short, count an event when the next candle open is at or above the hypothetical stop.
- Report event rate, price-loss multiple, stop overshoot, and p50/p90/p95/p99/max.
- Independently report absolute and direction-specific adverse opening jumps across all contiguous transitions, including zero values for the non-adverse direction.
- Report dataset time bounds, row counts, source SHA-256, and nonconsecutive transitions skipped.

Nonconsecutive candle pairs are excluded from the denominator and reported separately. Duplicate, reversed, invalid, or malformed OHLC rows fail the audit.

## Synthetic stress grid

A separate synthetic table adds hypothetical gaps beyond the stop (default: 0.05%, 0.1%, 0.25%, 0.5%, 1%, 2% of reference entry). Its price-loss multiple is (stop distance + extra gap) / stop distance. These are deliberately hypothetical scenarios, not observed events or execution-price estimates. Fees, slippage, and market impact are excluded.

## Interpretation

- gap_loss_multiple is the adverse reference-close-to-next-open price move divided by the hypothetical stop distance. A value of 1.5 means the observed open-through-stop move was 1.5 times the planned stop distance before fees or execution slippage.
- stop_overshoot_bps measures the distance from the stop level to the next open, in basis points of the stop level.
- gap_rate_pct is counted open-through-stop transitions divided by contiguous one-minute transitions.
- open_jump_distributions_bps describe observed next-open differences from the previous close; they are not guaranteed executable fills.

## Explicit limitations

- One-minute candle opens are a proxy for the first observed price in the minute, not actual executable fills.
- This does not measure order-book depth, spread, market impact, queue position, exchange latency, or actual stop-order slippage.
- It does not model intraminute paths or determine whether a stop was touched before the minute opened.
- Stop distances are a sensitivity grid, not selected strategy parameters.
- It does not calculate strategy PnL, execute strategy signals, simulate trades, or authorize Gate 2+ work.
- It does not resolve G0-08 contract multiplier/lot/tick/minimum-quantity metadata or G0-09 funding settlement marks.

## Acceptance status

The empirical audit and synthetic tests are evidence inputs only. G0-07 remains OPEN until the results are reviewed, stress assumptions are documented, and exchange contract rounding requirements are resolved after G0-08 metadata is verified. The output must not be interpreted as a maximum-loss guarantee.
