# G0-07 — Historical Stop-Gap Risk Methodology V1.2

## Purpose

Quantify minute-to-minute opening jumps and how often the next traded one-minute candle opens beyond a hypothetical stop. This is a risk-control audit, not a strategy test.

## Empirical method

- Require OHLCV columns and validate timestamp order, OHLC structure, finite values, and nonnegative volume.
- For adjacent one-minute diagnostics, compare each candle open with the immediately preceding candle close.
- For active-trade gap scenarios, use positive-volume candles only. Compare the next positive-volume candle open with the previous positive-volume candle close; zero-volume rows are bridged, and elapsed minutes between active candles are recorded.
- Nonconsecutive timestamp breaks reset the active comparison rather than being treated as market gaps.
- Apply the sensitivity stop grid (default: 0.05%, 0.1%, 0.15%, 0.2%, 0.25%, 0.5%, 1%, 1.5%, 2%, 3%, 5%).
- Report event rate, price-loss multiple, stop overshoot, p50/p90/p95/p99/max, source hashes, date bounds, active/zero-volume row counts, and data discontinuities.

## Synthetic stress grid

A separate synthetic table adds hypothetical gaps beyond the stop (default: 0.05%, 0.1%, 0.25%, 0.5%, 1%, 2% of reference entry). Its price-loss multiple is (stop distance + extra gap) / stop distance. These are hypothetical, not observed events or execution-price estimates. Fees, slippage, and market impact are excluded.

## Interpretation and limitations

- Active-trade gap events use positive-volume bars to avoid counting zero-volume carry-forward candles as real trade openings.
- One-minute candle opens are still proxies for first observed traded prices, not actual executable fills.
- Volume may be aggregated or represented differently by the upstream source; positive volume does not prove order-book executability.
- This does not measure order-book depth, spread, market impact, queue position, exchange latency, or actual stop-order slippage.
- It does not model mark/index-triggered stop logic or intraminute paths.
- Stop distances are sensitivity scenarios, not selected strategy parameters.
- It does not calculate strategy PnL, execute strategy signals, simulate trades, or authorize Gate 2+ work.
- It does not resolve G0-08 contract multiplier/lot/tick/minimum-quantity metadata or G0-09 funding settlement marks.

## Acceptance status

This is evidence input only. G0-07 remains OPEN until the results and upstream OHLCV provenance are reviewed, stress assumptions are documented, and exchange contract rounding requirements are resolved after G0-08 metadata is verified. The output is not a maximum-loss guarantee.


## Additional source-continuity diagnostic

The audit also reports the percentage of adjacent minute opens that exactly equal the preceding candle close, both across all bars and across positive-volume bars. A high exact-match rate is not proof of synthetic data, but it is a reason to verify the OHLCV provider and any candle stitching/forward-fill process before treating small measured opening gaps as representative of executable market gaps.


## OKX source sample follow-up — 2026-11-28

A separate read-only sample verifier compared 7 deterministic samples per asset (exact-open transitions, changed-open transitions, and the largest adjacent opening jump) against the public OKX V5 history-candles endpoint.

- 35/35 sampled OHLC candles matched exactly.
- 35/35 CSV volume values matched OKX volCcy (base-currency volume).
- CSV volume matched OKX vol (contract count) for SOL and AVAX, whose contract/base units coincide in these samples; it did not match contract volume for BTC, ETH or DOGE.
- No API errors occurred.

Therefore the CSV vol field should be treated as base-currency volume, not contract count. OKX documents derivative vol in contracts and volCcy in base currency. This is sample-level source evidence, not a full-file certification; the original acquisition/normalization manifest is still absent.
