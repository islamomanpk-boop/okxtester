# Phase 3 Gate 0 — Source and Execution-Engine Readiness Audit V1

**Audit date:** 2026-11-25  
**Branch:** `price-action-v1`  
**Status:** **CONDITIONAL HOLD — foundation exists, but Gate 0 is not passed**  
**Scope:** All three Phase 3 strategy families: support/resistance rejection, breakout continuation, and failed-breakout reversal.  
**Purpose:** Inspect the existing repository evidence and code before authorizing Phase 3 trade simulation. This is a read-only source/code review; no strategy code was changed and no backtest was run.

## 1. Executive decision

The project has substantial usable foundations: five-asset 1M market data, historical Phase 3 rejection/breakout research outputs, a causal 15M trend-signal pipeline, an execution engine, a portfolio engine, and a historical funding reconciliation report.

However, **these pieces are not yet a verified Phase 3 trading pipeline**. The current candidate engine is explicitly Model A trend-only and excludes `NO_TREND`; it does not generate the required sideways-range trade families. The portfolio engine accepts prepared candidates rather than generating Phase 3 candidates. The portfolio engine also lacks limit-order/expiry handling, does not include all transaction costs in initial risk sizing, and uses a proxy for funding mark price when no exact mark is supplied.

A material funding inconsistency also exists: the funding reconciliation report and backtest preflight report funding rows, while the older execution data audit says funding was not found. In addition, the single-trade execution function defaults to an empty funding-event iterable, and the portfolio validator accepts an empty funding list for an asset. Those interfaces can silently represent missing funding as zero unless the caller performs a separate completeness check.

**Decision: do not run a Phase 3 strategy backtest yet.** Resolve the blockers below, then issue a Gate 0 pass/hold decision with reproducible evidence.

## 2. Source-data inventory

### 2.1 One-minute market data

The Git tree contains:
- `data/market_1m/BTC_USDT_USDT_1m.csv`
- `data/market_1m/ETH_USDT_USDT_1m.csv`
- `data/market_1m/SOL_USDT_USDT_1m.csv`
- `data/market_1m/DOGE_USDT_USDT_1m.csv`
- `data/market_1m/AVAX_USDT_USDT_1m.csv`

The recorded backtest preflight reports:
- 569,125 rows each for BTC and ETH; 569,126 for SOL and DOGE; 569,127 for AVAX.
- Shared execution window: 2025-10-20 08:50 UTC through 2026-11-19 14:14 UTC.
- No issues detected by that preflight.
- The breakout-forward reconstruction audit independently reports 569,125 common 1M timestamps and zero gaps in the common timeline.

The earlier execution data audit reports zero unexpected 1M intervals for each asset. These are prior report results; this audit did not re-read or re-hash the complete CSV contents.

**Provenance/documentation discrepancy:** `docs/execution_data_audit_v1.md` says raw market data remains local and is not committed to Git, but the current Git tree contains the five large `data/market_1m/*.csv` blobs. Correct the documentation and define the canonical source location, immutable source hashes, and retention policy. Do not maintain conflicting claims about whether the source candles are committed.

### 2.2 Funding history

The repository contains `reports/funding_data_audit.md`, which records a reconciliation for BTC, ETH, SOL, DOGE, and AVAX USDT perpetual swaps:
- 1,188 merged realized funding rows per asset.
- 1,130 archive rows, 277 API rows, and 219 overlapping timestamps checked per asset.
- No overlapping rate conflicts.
- Observed settlement interval: 480 minutes for 1,187 intervals per asset.
- First settlement: 2025-10-20 00:00 UTC; last settlement: 2026-11-19 16:00 UTC.
- The merge code uses OKX `realizedRate`, not predicted `fundingRate`.

`reports/backtest_input_preflight.md` also records 1,188 funding rows for each asset. But `reports/execution_data_audit.md` says funding files were not found and funding must not be assumed to be zero. That older report is a historical snapshot and is superseded for availability-at-run-time by the later preflight; it should not be treated as the current funding status.

The processed funding CSVs are not present in the current Git tree; the collection documentation says raw and processed funding files are local and excluded from normal Git history. Therefore, the report proves a prior reconciliation was recorded, but this repository snapshot alone does not prove the exact local funding files are currently available to the runtime that will execute a backtest.

**Required resolution:** locate the five current processed funding CSVs in the intended execution environment; verify schema, instrument IDs, timestamp uniqueness/order, first/last coverage, missing settlements, and checksums; link the resulting audit to the exact market-data hashes. Update the older execution-data audit so it is clearly labelled as a historical pre-funding snapshot, and extend the current audit to validate funding coverage rather than merely file presence. Do not replace missing settlements with zero.

### 2.3 Instrument and fee provenance

The funding pipeline identifies the instruments as `BTC-USDT-SWAP`, `ETH-USDT-SWAP`, `SOL-USDT-SWAP`, `DOGE-USDT-SWAP`, and `AVAX-USDT-SWAP`. The inspected execution configuration requires explicit fee and slippage inputs, but the reviewed reports do not establish the user's actual OKX fee tier, maker/taker eligibility, historical fee schedule, contract multiplier/lot size, minimum order size, or tick-size constraints.

**Required resolution:** document the exact contract specifications and fee assumptions used for the test period. Until verified, any fee/slippage values are research scenarios, not exchange-exact costs.

## 3. Phase 3 event and signal readiness

### 3.1 Support/resistance rejection evidence

The historical boundary-test ledger contains:
- asset, definition, upper/lower direction, snapshot index and availability timestamps;
- test start/end timestamps and OHLC;
- first strong rejection timestamp and rejection-candle OHLC where present;
- closure reason.

The rejection episode/retest anatomy ledger additionally contains `confirmation_ts_ms`, frozen upper/lower levels, rejection-candle OHLC/anatomy, and snapshot availability fields. Its run metadata records 1,992 eligible rejection events (1,154 broad and 838 strict; strict is nested within broad) and a 15-minute confirmation delay.

This is useful source evidence for building causal range-rejection candidates. It is **not yet a ready order ledger**: the event definitions, availability timestamp convention, repeated/overlapping event policy, side mapping, setup invalidation, and one-trade-per-event/asset constraints must be frozen for the trading cohort. The broad and strict populations must not be treated as independent samples.

### 3.2 Breakout continuation evidence

The breakout forward-outcome archive records 4,776 classification rows and 19,104 horizon rows over five assets, with 19,104 complete horizon rows. It explicitly states that its historical outcome study has no fees, slippage, spread, funding, sizing, stops, or portfolio constraints, and that full-sample channel-width quantiles are retrospective rather than live calibrated.

The metadata's historical entry convention is the first 1M candle opening at `signal_time`; that convention does not by itself prove that every feature/threshold used to form the signal was available at that time. Reconfirm the original breakout event's causal availability and the exact 15M/4H feature provenance before turning it into an order candidate.

### 3.3 Failed-breakout reversal evidence

A complete, frozen failed-breakout/re-entry/reclaim/reversal candidate ledger was not established by the reviewed files. This remains a Gate 1 descriptive work item. Do not infer failed-breakout trades from a generic breakout forward path or invent confirmation times.

### 3.4 Existing trend candidate engine is not the Phase 3 range engine

`docs/trade_candidate_engine_v1.md` and `src/trade_candidate_engine.py` explicitly define the current candidate generator as Model A trend candidates. It requires `LONG_ONLY` or `SHORT_ONLY` direction permission and emits no candidate for `NO_TREND`. The candidate audit reports 17,945 candidates, including support/resistance rejection labels, but those candidates are filtered through the trend permission system. They are not proof that range-regime support/rejection strategies are implemented.

The existing 15M signal dataset builder is causal by its documented availability convention (15M close) and backward as-of higher-timeframe joins, but it serves the trend/price-action pipeline. It does not replace the frozen Phase 3 sideways boundary event definitions.

**Required resolution:** create a separate Phase 3 candidate schema and generator that consumes frozen sideways context/boundary data and emits three explicit families:
1. support rejection long / resistance rejection short;
2. resistance breakout long / support breakout short;
3. failed upside breakout short / failed downside breakout long.

Every candidate must carry a stable event ID, family, asset, side, boundary type, signal timestamp, `signal_available_at`, frozen boundary/structure references, invalidation level, and provenance. Signal availability must be proven to be no earlier than the completed confirmation information.

## 4. Execution-engine inspection

### 4.1 Single-trade engine

`src/execution_engine.py` provides 1M market-entry simulation, long/short sizing, stop/target handling, adverse slippage, explicit taker fees, and funding calculations. It selects the first 1M candle whose opening timestamp is at or after `signal_available_at`. Stop priority is conservative when stop and target are both touched in a candle; stop gaps use the worse open.

Issues requiring resolution:
- `simulate_trade(..., funding_events=())` permits funding to be omitted and then records zero funding PnL. This conflicts with the policy that missing funding must never be silently treated as zero.
- The single-trade `size_position` path sizes from stop distance and exposure cap only; it does not reserve for entry/exit fees or adverse slippage. The integrated portfolio path does include an effective per-unit risk term for entry/stop-exit slippage and both taker fees before allocation (see lines around the `effective_risk_per_unit` calculation in `src/portfolio_backtester.py`). Stop gaps can still make realized losses exceed the nominal risk budget.
- No maker limit entry, order expiry, cancellation, partial fill, or missed-fill model exists in this engine.
- Funding uses an exact mark only if supplied; otherwise it uses the 1M close at the settlement timestamp as a proxy. This must be labelled as an approximation and sensitivity-tested.
- End-of-data liquidation at final close is a simulation convention; it must not hide incomplete trade horizons or data-end censoring.

### 4.2 Portfolio engine

`src/portfolio_backtester.py` is an event-driven multi-asset 1M engine with shared equity, market-style entries, stop/target exits, fees, slippage and funding event application. It consumes prepared candidates; it does not generate Phase 3 signals.

The documentation and code inspection identify:
- Limit orders, expiry and setup invalidation are not implemented.
- The portfolio backtester currently calculates cost-adjusted `risk_per_unit` from entry and stop-exit slippage plus entry/exit taker fees and passes it to the allocator. This is stronger than the older documentation states. It still does not cover stop-gap losses, contract lot/tick rounding, or prove exchange-specific fee assumptions. The standalone single-trade engine remains stop-distance-only for sizing.
- Funding mark-price fallback is a 1M close proxy.
- Candidate generation from actual Phase 3 signal/regime data is not integrated.
- Funding validation requires a mapping key for every asset but accepts an empty event list. A separate coverage validator is required to distinguish a genuinely complete interval with no settlement from missing funding data.
- The engine uses taker-style market entries/exits; it does not yet model maker fills or order-book queue position.
- The common-timeline requirement is strict; the five-asset shared 569,125-minute window is the natural synchronized execution reference.

### 4.3 Portfolio/order realism not yet demonstrated

Before strategy results are trusted, test contract sizing/lot rounding, tick rounding, fee calculations, spread and slippage, funding settlement boundaries, mark-price provenance, order/position event ordering, same-bar stop/target ambiguity, gap fills, concurrent positions, equity allocation, and end-of-data handling. Existing unit tests are useful but their presence is not proof that the entire integrated Phase 3 pipeline passes.

## 5. Gate 0 blocker register

| ID | Blocker | Severity | Required evidence to close |
|---|---|---|---|
| G0-01 | Funding evidence is from different audit runs; later preflight reports 1,188 rows/asset, but no current file hashes or settlement-gap proof | Critical | Re-run current audit against the exact five processed files; update stale snapshot and publish hashes/coverage |
| G0-02 | Funding files are not in the Git tree; runtime availability and hashes not verified in this audit | Critical | Confirm files in execution environment, hash and schema/coverage audit |
| G0-03 | Single-trade engine defaults to empty funding events; portfolio engine accepts empty per-asset funding lists | Critical | Fail-closed funding coverage validation and tests |
| G0-04 | Phase 3 event ledgers are descriptive; frozen live-knowable candidate schema/availability not yet proven end-to-end | Critical | Candidate protocol, source linkage, event IDs, causal timing audit |
| G0-05 | Current candidate engine is trend-only and suppresses NO_TREND; it is not a range strategy generator | Critical | Separate Phase 3 three-family candidate generator and tests |
| G0-06 | Limit orders, expiry, cancellation, partial/missed fills are not implemented | High | Implement only after Gate 2/3 establishes which entry rules need them |
| G0-07 | Portfolio path has cost-adjusted sizing, but standalone engine does not; gap loss and contract rounding remain unbounded/unverified | High | Add parity/acceptance tests, quantify gap risk, and apply contract constraints before accepting either path |
| G0-08 | Exact fee tier, contract multiplier/lot size, tick size and minimum quantity not documented | High | Verified instrument/fee specification and frozen test assumptions |
| G0-09 | Funding mark-price fallback is a close proxy | High | Exact mark-price source or explicitly approved conservative proxy/sensitivity |
| G0-10 | Documentation says raw market data local, but 1M CSVs are tracked in Git | Medium | Reconcile storage/provenance/retention documentation |

## 6. Readiness decision

| Component | Current assessment |
|---|---|
| Five-asset 1M historical candles | Prior audits pass; exact current file hashes still need a single frozen manifest |
| Common execution timeline | Prior reports support 569,125 aligned timestamps with no gaps |
| Historical funding source/reconciliation | Reconciliation report exists; current local file presence and hashes not independently verified here |
| Phase 3 support/resistance rejection events | Descriptive ledgers exist; causal order-candidate contract still open |
| Breakout continuation events | Descriptive outcomes exist; causal signal availability/provenance needs final reconciliation |
| Failed-breakout reversal events | Full taxonomy/candidate ledger remains open |
| Trend signal/candidate pipeline | Exists, but is not a substitute for the Phase 3 range candidate generator |
| Single-trade execution engine | Useful baseline, but not accepted for Phase 3 until funding and risk-cost issues are fixed |
| Portfolio engine | Useful integration foundation, but not accepted for Phase 3 until blockers are fixed |
| Phase 3 strategy backtest | **Not authorized / not run** |

**Gate 0 result: CONDITIONAL HOLD.** The data and code foundations are promising, but critical blockers remain. Do not begin Gate 6 strategy backtests or interpret any earlier generic trend backtest as a Phase 3 range strategy result.

## 7. Ordered next actions

1. Reconcile the funding reports against the actual five local processed CSVs and produce a current manifest/checksum audit.
2. Freeze a single market-data manifest: exact file paths, instrument IDs, SHA-256, row counts, first/last timestamps, common interval, and source provenance.
3. Inspect the original Phase 3 rejection and breakout scripts to freeze the exact signal-availability semantics and event de-clustering rules.
4. Specify the Phase 3 candidate schema for all three families, with support/resistance and long/short breakdowns retained.
5. Add fail-closed funding-coverage and cost-aware risk sizing tests to the engine before any Phase 3 PnL simulation.
6. Reassess whether the selected entry hypotheses require limit-order support; do not implement unused order types prematurely.
7. Reissue Gate 0 pass/hold decision with linked manifests and passing deterministic tests.

No strategy parameters, stops, targets, or profitability claims are selected by this audit.


## 8. Follow-up clarification — funding report chronology

A second inspection of `src/backtest_input_preflight.py` and the saved reports refines the initial funding finding:

- `reports/execution_data_audit.md` is an older snapshot reporting no funding files found at that time.
- `reports/backtest_input_preflight.md` is later evidence that the five funding files were available to its run: 1,188 rows per asset, expected instrument name, increasing timestamps, and finite funding rates; it records PASS.
- `reports/funding_data_audit.md` records archive/API reconciliation using OKX `realizedRate`, with 219 overlapping timestamps per asset and no conflicting rates.

Therefore, the reports are not proof of a same-run contradiction. The remaining issue is **current reproducibility and completeness**, not whether a later run once found files. The saved preflight does not record SHA-256 hashes and does not test the expected settlement cadence for gaps; the funding reconciliation report records 1,187 eight-hour intervals per asset, but its source CSVs remain outside Git. A fresh audit must run in the actual execution environment and produce hashes, exact file paths, instrument checks, duplicate checks, observed interval counts, and explicit missing-settlement analysis.

The Gate 0 hold remains because (a) the files are local and cannot be confirmed from the Git tree alone, (b) the engine interfaces can accept empty funding inputs, and (c) the Phase 3 candidate and cost-aware risk issues remain open. This clarification does not authorize a backtest.


## 9. Follow-up clarification — cost-aware portfolio sizing

A deeper line-by-line inspection of `src/portfolio_backtester.py` and `src/portfolio_engine.py` refines the initial sizing finding. The portfolio backtester computes `effective_risk_per_unit` as the entry-to-adverse-stop-exit distance after slippage plus taker fees on entry and stop exit, then passes that as `risk_per_unit` to the allocator. The allocator uses this value to cap quantity against the configured 0.5% risk budget. Therefore, it is inaccurate to say the current portfolio path entirely omits fees/slippage from initial sizing.

Remaining qualifications: the standalone `src/execution_engine.py:size_position` does not include fees/slippage; the portfolio calculation assumes the configured fee is appropriate and does not include exchange lot/tick rounding; and a gap through the stop can still exceed the planned cost-adjusted stop risk. Tests and documentation must distinguish planned stop-risk sizing from a hard maximum-loss guarantee.


## 10. Funding coverage audit implementation — 2026-11-25

A fail-closed local-file audit has now been added:
- Code: `src/funding_coverage_audit.py`
- Tests: `src/test_funding_coverage_audit.py`
- Documentation: `docs/funding_coverage_audit_v1.md`
- Test workflow: `.github/workflows/phase3-funding-coverage-audit.yml`

It records SHA-256 and absolute file paths, checks schema/instrument/rates, strict ordering and duplicates, configured first/last timestamps, an explicit 8-hour expected interval, missing/irregular settlements, and cross-asset timestamp-set equality. It writes JSON and Markdown reports and exits non-zero on any failure.

**Important:** the 8-hour cadence and coverage endpoints are explicit defaults based on the prior reconciliation report, not universal assumptions. GitHub Actions uses synthetic unit-test fixtures because processed funding CSVs are intentionally local and not tracked in Git. A passing workflow proves audit logic tests only; it does not prove the actual five funding files pass.

Gate 0 remains **CONDITIONAL HOLD** until the real-data command is run in the environment containing the five processed files and its output manifest is archived. The current run is not yet a real-data funding audit.
