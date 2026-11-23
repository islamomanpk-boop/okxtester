# Historical Boundary Rejection Forward-Outcome Study — Specification V1

Date: 2026-11-23
Branch: `price-action-v1`
Status: **DESIGN FROZEN BEFORE IMPLEMENTATION; no forward outcomes calculated.**

## 1. Accepted event source

Use only the accepted output:
`reports/sideways_boundary_events_historical_v1/boundary_tests_historical_v1.csv`

Primary event-study population:
- `definition == broad`
- `first_strong_rejection_ts_ms` is non-null
- 1,154 events across BTC, ETH, SOL, DOGE, AVAX

The strict cohort is a fully contained subset of broad. It may be reported as a separately labelled subgroup, but never added to broad or pooled as independent events. Do not use the unreconciled earlier 2,095-event population or its outcome results.

## 2. Signal confirmation and entry-time convention

The ledger's `first_strong_rejection_ts_ms` is the OPEN timestamp of the 15M rejection candle. The close is confirmed 15 minutes later.

Derive:
```
rejection_confirmed_at_ts_ms = first_strong_rejection_ts_ms + 900000
```

The 1M audit passed for all 1,154 broad events:
- exact 1M timestamp exists at confirmation;
- all 16 timestamps from confirmation through +15 minutes are consecutive.

For this descriptive event study, define the reference entry price as the OPEN of the 1M candle whose timestamp equals `rejection_confirmed_at_ts_ms`. This is a standardized next-candle reference price, not proof of an executable fill. Any later trading simulation must separately model latency, spread, slippage, fees, and funding.

Do not use any part of the 15M rejection candle as post-confirmation outcome data.

## 3. Direction convention

- Upper-bound rejection: expected direction is DOWN / short-side.
- Lower-bound rejection: expected direction is UP / long-side.

For each event and horizon, report both:
1. Raw underlying return.
2. Direction-adjusted return, positive when movement is in the expected rejection direction.

For upper events, direction-adjusted return is the negative of raw return. For lower events, it equals raw return.

## 4. Fixed forward horizons

Calculate outcomes at:
- 15 minutes
- 1 hour
- 4 hours
- 24 hours

Use exact elapsed-time horizons from the 1M reference-entry timestamp. For horizon H:
- Required 1M bars have opening timestamps from entry through entry + H - 1 minute, inclusive.
- Horizon exit/reference price is the close of the final required 1M candle, whose close time is entry + H.
- Require every expected 1M timestamp exactly once. Do not forward-fill, interpolate, or bridge gaps.
- If the complete horizon is unavailable, mark that event/horizon censored or incomplete and do not calculate its return.

## 5. Excursion definitions

Within each complete horizon, use only 1M bars in the forward interval beginning at the reference entry timestamp.

Let E be the reference entry price, HIGHEST the maximum 1M high, and LOWEST the minimum 1M low in the horizon.

For upper rejection (expected DOWN):
- favorable excursion = (E - LOWEST) / E
- adverse excursion = (HIGHEST - E) / E

For lower rejection (expected UP):
- favorable excursion = (HIGHEST - E) / E
- adverse excursion = (E - LOWEST) / E

Also preserve raw maximum high/low and horizon closing price so results can be independently audited. Excursions are path statistics, not realized trade P&L; they do not specify stop/target ordering or executable fills.

## 6. Required reporting

Produce event-level outcomes and aggregate summaries:
- event identity, asset, direction, definition, rejection timestamp, confirmation timestamp, reference entry price;
- each horizon's completeness status, ending close, raw return, direction-adjusted return, favorable excursion, adverse excursion;
- sample size and censored count for every asset, direction, and horizon;
- broad cohort overall and asset/direction breakdowns;
- strict subgroup separately labelled, with no pooling with broad;
- medians and distribution quantiles, not only means;
- positive direction-adjusted return frequency, explicitly described as a historical event-study frequency, not a win rate.

Retain enough raw fields to independently recalculate each metric.

## 7. Dependence, censoring, and interpretation

- Events can overlap in time and are not independent observations; upper/lower and strict/broad cohorts overlap.
- Do not use naive independent-event confidence intervals or imply five assets/events are independent.
- Report per-asset and per-direction samples, and disclose event overlap.
- Exclude incomplete horizons from that horizon's return denominator and report their counts explicitly.
- The final source-history tail is truncated. Any event without a complete required horizon must be censored for that horizon.
- Snapshot-end and 15M-gap closure reasons are not rejection signals; only rows with a recorded first strong rejection enter this study.
- No fees, spread, slippage, latency, funding, liquidation, portfolio sizing, or order execution are included in V1.
- Results are descriptive historical forward outcomes, not predictive probabilities, a trading edge, or profitability evidence.

## 8. Implementation safeguards

Before running:
1. Confirm input file schemas and timestamp units.
2. Validate unique event keys and exact confirmation timestamps.
3. Validate entry minute and every expected horizon timestamp.
4. Check that no outcome bar timestamp precedes confirmation.
5. Reconcile event counts to 1,154 broad rejection events and strict subgroup counts to 838.
6. Write only to a new output directory; refuse to overwrite non-empty output.
7. Add unit tests for upper/lower signed returns, exact horizon boundaries, missing-minute censoring, and no look-ahead.
8. Do not modify source candles, detector features, event ledger, or previous reports.

## 9. Explicit exclusions

This specification does not authorize reusing the old 2,095-event outcome files, changing the event definition, optimizing thresholds, selecting horizons after seeing results, or making live-trading claims.
