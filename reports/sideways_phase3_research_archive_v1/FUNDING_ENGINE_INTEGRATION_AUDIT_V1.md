# Funding Engine Integration Audit — Phase 3 Gate 0

**Original audit date:** 2026-11-25  
**Document status:** HISTORICAL BASELINE — SUPERSEDED BY THE IMPLEMENTATION CHECKPOINT  
**Current decision:** G0-03 remains OPEN for mark-price policy and fresh project-wide call-site audit; local source verification and focused contract integration tests are complete.

## 1. Why this file is retained

This file preserves the pre-migration findings that motivated the funding coverage contract. Its original findings below describe the engine state **before** the changes recorded in [G0-03 Funding Contract Implementation Plan V1](../../docs/research_checkpoints/2026-11-25_g0-03_funding_contract_implementation_plan_v1.md). Do not treat the pre-migration table as a description of the current engine APIs.

## 2. Pre-migration findings (historical)

Before migration, the standalone engine accepted an optional empty funding-event iterable, the portfolio engine accepted empty per-asset event lists, neither engine enforced source coverage/hash provenance, and both could use a settlement-minute 1m candle-close proxy when no mark was supplied. These were material fail-open risks.

The candle-close fallback was and remains a proxy, not an exact OKX settlement mark.

## 3. Current implementation status (2026-11-25)

The shared funding contract is now integrated into both engines:

- `src/execution_engine.py` requires an explicit `funding_contract`; silent omission of funding events is no longer the public interface.
- `src/portfolio_backtester.py` requires per-asset `{events, coverage}` contracts and validates schedule completeness, coverage, and settlement alignment to its 1m execution timeline.
- `src/funding_coverage.py` validates instrument identity, source SHA-256, coverage boundaries, explicit schedule metadata, expected settlements, event ordering/uniqueness, rate validity, and exact/proxy mark mode.
- The historical loader verifies the local source files against the committed manifest and passes the verified full history and manifest-derived schedule to the engines.
- Per-trade and experiment metadata retain source identity and mark-price mode. Proxy use remains explicitly labelled.

## 4. Verification evidence

- Exact-commit GitHub Actions run: https://github.com/islamomanpk-boop/okxtester/actions/runs/45545754508 — **75 focused tests passed**.
- User's Termux local manifest verification: **PASS** for BTC, ETH, SOL, DOGE, and AVAX; 1,188 settlements per asset; all hashes matched the archived manifest; no backtest was run.
- The local verification result does not establish exact settlement mark prices. The audited source CSVs contain realized funding rates and timestamps, not exact exchange settlement marks.

## 5. Remaining G0-03 acceptance work

1. Complete a fresh project-wide call-site audit after the API migration; the saved grep inventory is explicitly a pre-migration snapshot and is not a substitute for this final audit.
2. Decide and document whether candle-close proxy pricing is allowed for exploratory research only, or whether exact settlement marks are mandatory for the project's final performance claims.
3. If exact marks are required, obtain and validate an appropriate historical source. Do not relabel candle OHLC or candle-close values as exact settlement marks.

**Gate decision:** G0-03 remains OPEN; Gate 0 remains CONDITIONAL HOLD. Phase 3 strategy PnL backtesting remains NOT AUTHORIZED until all Gate 0 blockers are formally resolved. This audit makes no claim about strategy edge or profitability.
