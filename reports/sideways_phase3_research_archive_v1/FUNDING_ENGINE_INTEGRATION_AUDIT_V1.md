# Funding Engine Integration Audit — Phase 3 Gate 0

**Date:** 2026-11-25  
**Result:** PARTIAL IMPLEMENTATION — NOT READY FOR STRATEGY BACKTESTING  
**Scope:** Source-level inspection of single-trade and portfolio funding interfaces; no strategy PnL tests or parameter optimization.

## Findings

| Area | Single-trade engine | Portfolio engine |
|---|---|---|
| Funding cashflow arithmetic | Implemented | Implemented |
| Positive-rate sign | Long pays; short receives | Long pays; short receives |
| Input omission | funding_events defaults empty; no funding | Mapping required; missing asset key rejected |
| Empty event list | Accepted | Accepted |
| Rate validation | Only events inside active trade interval | Up-front finite/range validation |
| Event ordering/duplicates | Not validated up front | Strictly increasing timestamps required |
| Mark price | Supplied mark preferred; else exact-timestamp 1m close proxy | Supplied mark preferred; else settlement-minute 1m close proxy |
| Source coverage/hash binding | None | None |
| Coverage-vs-backtest interval check | None | None |

## Important interpretation

A zero funding PnL may mean no event was passed, not that a verified source showed no settlement. The separate local coverage audit passed for five assets and a specific historical interval, but its manifest is not currently required by either engine. Therefore, the source audit and engine calculations are not yet joined by an enforceable provenance/coverage contract.

The candle-close fallback is only a proxy. It must not be labelled exact realized funding cost. Exact settlement reconstruction needs historical exchange mark price aligned to each settlement timestamp.

## Required next implementation

1. Require explicit funding coverage metadata in strict backtest mode.
2. Validate requested dates and all expected settlements against the coverage manifest.
3. Reject missing, incomplete, unverified, malformed, duplicate, or out-of-order event streams.
4. Permit zero events only when verified coverage establishes no settlement was due.
5. Add a selectable exact-mark requirement versus explicitly labelled proxy mode.
6. Add comprehensive unit tests and an integration test connecting manifest-verified events to engine PnL.

## Gate decision

G0-03 remains OPEN. Gate 0 remains CONDITIONAL HOLD. Phase 3 strategy PnL backtesting remains NOT AUTHORIZED. This audit makes no claim about strategy edge or profitability.
