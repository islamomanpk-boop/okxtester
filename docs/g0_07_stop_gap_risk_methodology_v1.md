# G0-07 — Historical Stop-Gap Risk Methodology V1

## Purpose

Quantify how often one-minute candle opens have already crossed a hypothetical stop level, and measure the observed open-through-stop overshoot. This is a risk-control audit, not a strategy test.

## Method

For every pair of consecutive, exactly one-minute candles:

- Use the previous candle close as a hypothetical reference entry.
- Apply each sensitivity stop distance (default grid: 0.25%, 0.5%, 1%, 1.5%, 2%, 3%, 5%).
- For a long, count an open-through-stop event when the next candle open is at or below the hypothetical stop.
- For a short, count an event when the next candle open is at or above the hypothetical stop.
- Divide event counts by the number of contiguous one-minute transitions to calculate the event rate.
- Report gap loss multiple, stop overshoot in basis points, and adverse open move distributions (p50/p90/p95/p99/max).

Nonconsecutive candle pairs are excluded from the denominator and reported separately. Duplicate, reversed, invalid, or malformed OHLC rows fail the audit.

## Interpretation

- gap_loss_multiple is the adverse reference-close-to-next-open price move divided by the hypothetical stop distance. A value of 1.5 means the open-through-stop price move was 1.5 times the planned stop distance before fees or execution slippage.
- stop_overshoot_bps measures the distance from the stop level to the next open, in basis points of the stop level.
- gap_rate_pct is the percentage of contiguous one-minute transitions whose next open is through the hypothetical stop.

## Explicit limitations

- One-minute candle opens are a proxy for the first observed price in the minute, not actual executable fills.
- This does not measure order-book depth, spread, market impact, queue position, exchange latency, or actual stop-order slippage.
- It does not model intraminute paths or determine whether a stop was touched before the minute opened.
- Stop distances are a sensitivity grid, not selected strategy parameters.
- It does not calculate strategy PnL, execute strategy signals, simulate trades, or authorize Gate 2+ work.
- It does not resolve G0-08 contract multiplier/lot/tick/minimum-quantity metadata or G0-09 funding settlement marks.

## Acceptance status

The script and synthetic unit tests are infrastructure for the empirical audit. G0-07 remains OPEN until the historical audit completes, results are reviewed, stress assumptions are documented, and exchange contract rounding requirements are resolved after G0-08 metadata is verified. The output must not be interpreted as a maximum-loss guarantee.
