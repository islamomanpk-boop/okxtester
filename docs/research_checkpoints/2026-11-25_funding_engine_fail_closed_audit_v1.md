# Funding Engine Fail-Closed Audit V1

**Date:** 2026-11-25  
**Branch:** `price-action-v1`  
**Status:** **CRITICAL BLOCKER — data coverage passes, engine coverage contract does not**

## Executive finding

The actual five-asset processed OKX funding files passed the local coverage audit: 1,188 records per asset, 5,940 total, zero missing settlements, no gaps/irregular intervals, and identical timestamp sets over the configured historical window. However, the execution engines do not independently prove that funding input covers each simulated trade's holding interval. Local data availability alone therefore does not guarantee that a backtest cannot silently omit funding costs.

## Source findings

### 1. Standalone engine: optional funding input

In `src/execution_engine.py`, `simulate_trade(..., funding_events: Iterable = ())` defaults to an empty iterable. If a caller omits funding events, the function can return zero funding PnL. It has no coverage start/end metadata and cannot distinguish a genuinely settlement-free interval from missing data.

### 2. Portfolio engine: empty per-asset funding accepted

In `src/portfolio_backtester.py`, `_validate_funding` requires a mapping and a key for every asset. It validates event fields, rate finiteness/range, ordering, and optional mark price. It does not validate complete time coverage or expected settlement timestamps. An empty list is accepted for each asset, including when the simulation window overlaps the audited funding schedule.

### 3. Settlement mark-price approximation

Both engines accept an explicit settlement `mark_price`, but otherwise fall back to the close of the 1-minute candle at the funding timestamp. This is a proxy, not an exact OKX settlement mark. The current engine contract does not force callers to choose between exact-mark and proxy modes or label that choice in every result.

### 4. Current tests do not cover the missing-data failure mode

Existing unit tests verify funding arithmetic signs and that a settlement before entry is not charged. They do not verify omitted input, empty-but-incomplete funding, missing interior settlements, coverage-window boundaries, or strict mark-price requirements.

## Required input contract

Introduce explicit per-asset funding coverage metadata, separate from the event list. It should identify source instrument and file hash; verified coverage start/end; expected settlement schedule or explicit expected settlement timestamps (including schedule-version changes); mark-price mode (exact required, or explicitly named proxy mode); and provenance for the settlement mark series when exact marks are supplied.

The engine must reject any trade whose full holding interval is not covered. It must reject a missing expected settlement timestamp. An empty event list is permissible only when the declared schedule proves that no settlement falls inside the relevant holding interval. Do not hard-code the current eight-hour schedule as universal; it is only the verified schedule for the audited historical scope.

For the standalone engine, remove the default that silently makes funding optional. For the portfolio engine, validate coverage for each tradable asset, not merely the presence of a dictionary key.

## Acceptance tests required

1. Omitted funding input fails before simulation.
2. Missing coverage metadata for a tradable asset fails.
3. Empty events with an expected settlement in the holding interval fail.
4. Empty events with no expected settlement in the interval pass.
5. Missing one interior expected settlement fails.
6. Duplicate, out-of-order, invalid-rate, and non-finite events fail.
7. Holding interval before coverage start or beyond coverage end fails.
8. Entry/exit timestamp settlement ordering is explicitly tested and documented.
9. Positive and negative rates have correct long/short cashflow signs and notional basis.
10. Exact-mark mode rejects missing marks; proxy mode is explicitly selected and labelled in results.
11. Portfolio and standalone engines agree on identical trade/event/mark inputs.

## Gate decision

- Funding source availability and historical coverage audit: **PASS** for actual local Termux files (see archived report and manifest under `reports/sideways_phase3_research_archive_v1/funding_coverage_audit_v1/`).
- Funding engine fail-closed integration: **OPEN / CRITICAL**.
- Gate 0: **CONDITIONAL HOLD**.
- Phase 3 strategy PnL backtest: **NOT AUTHORIZED**.

This is a code-review finding and acceptance specification, not a claim that the required changes have already been implemented or tested.
