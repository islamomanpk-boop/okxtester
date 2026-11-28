# G0-07 Stop-Trigger Reference and Execution-Model Review V1 — 2026-11-28

## Disposition

This is a read-only engineering and API-contract review. It does not select a stop trigger reference, change execution behavior, or authorize strategy PnL backtesting, execution simulation, orders, fills or live trading. G0-07 remains OPEN; Gate 0 remains CONDITIONAL HOLD.

## Existing project model

- `src/execution_engine.py` checks stop touches against one-minute candle lows/highs and handles a gap using the next candle open.
- `src/portfolio_backtester.py` applies the same candle-based stop/target logic.
- The underlying market candles are last-trade OHLC; no explicit OKX `triggerPxType` field or policy is represented.
- Both engines apply configured fixed `slippage_bps` to entry/exit; fee and slippage values are required configuration, not calibrated universal constants.
- The existing model is therefore an implicit last-price candle approximation, not a verified OKX conditional/trigger-order emulator.

## Current OKX API contract

The official V5 algo-order documentation specifies:
- Trigger reference options for derivatives: `last`, `index`, `mark`.
- `last` is the documented default.
- OKX describes `mark` as wick-resistant and recommends it for derivatives.
- `orderPx=-1` submits a market order after a trigger; `slOrdPx=-1` does the same for a stop-loss.
- Trigger price and eventual fill price are separate concepts.

The official order-book documentation says the REST order book is refreshed about every 50 ms and supports up to 400 levels per side. It returns a current cached snapshot, not a historical archive. It cannot retrospectively prove historical spread, depth, queue position, latency, market impact or stop-market slippage.

Official sources:
- https://www.okx.com/docs-v5/en/#order-book-trading-algo-trading-post-place-algo-order
- https://www.okx.com/docs-v5/en/#order-book-trading-market-data-get-order-book

## Decision not made

No trigger reference is selected in this checkpoint. A mark/index-trigger model requires historical mark/index candles aligned to the stop evaluation interval and explicit tests for the trigger path. Existing mark-price work contains full-window 4H candles and bounded 1m samples around funding timestamps; it does not establish full-window 1m mark-trigger coverage for all stop checks.

If the project retains last-price triggering, it must be explicitly documented as a deliberate research assumption rather than inferred from OKX's default. In either case, candle-open gaps remain separate from actual executable stop fills.

## Required evidence before G0-07 acceptance

1. Decide and document the intended stop trigger reference (last, mark or index) and why it matches the research objective.
2. Ensure the historical trigger-price series has matching timestamp coverage and validate intraminute stop-touch handling.
3. Obtain historical order-book/trade evidence if available, or define conservative, clearly labelled stress assumptions for spread, depth, latency, market impact and stop-market slippage.
4. Keep actual taker fee assumptions separate; account-specific fee tier cannot be inferred from public instrument metadata.
5. Complete tick/lot/minimum-quantity rounding after G0-08 instrument metadata is verified, including effective-time changes where available.

## Current G0-07 evidence checkpoint

- Corrected terminology commit: `1ecf70f0b7771b5906934b00f8373cd8ad12c2ad`.
- Successful workflow: https://github.com/islamomanpk-boop/okxtester/actions/runs/46159298047
- Corrected artifact ID: `15268323536`.
- Artifact ZIP SHA-256: `30b87233aac3c06f52f68407cd698a6fb1e523e41e19311c475d8dc687c15397`.
- Historical open-through-stop events: 48 at 0.05% hypothetical stop distance; 2 at 0.10%; none at 0.15% or wider.
- Largest observed gap-loss multiple: 2.6256R on SOL short at 0.05% stop distance (3 events); these are candle-open proxies, not fills.
- Public OKX source sample: 35/35 OHLC matches and 35/35 CSV volume matches to base-currency `volCcy`; full-file provenance remains unverified.

No strategy PnL, trade simulation, execution simulation, orders, fills, Gate 2+ or live trading was performed or authorized.
