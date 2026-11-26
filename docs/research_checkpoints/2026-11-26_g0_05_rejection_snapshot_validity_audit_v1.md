# G0-05 Rejection Snapshot-Validity Audit — V1

**Date:** 2026-11-26  
**Source:** `reports/sideways_boundary_events_historical_v1/boundary_tests_historical_v1.csv` on `price-action-v1`  
**Related contract:** `2026-11-26_g0_05_three_family_candidate_contract_preparation_v1.md`  
**Status:** Source-timing edge case verified; candidate generator not run.

## 1. Finding

The accepted rejection lifecycle records `first_strong_rejection_ts_ms` as the **open** of the 15-minute rejection candle. The completed candle becomes knowable 900,000 ms later:

`rejection_confirmed_at_ts_ms = first_strong_rejection_ts_ms + 900000`

The historical boundary ledger records the current snapshot's availability and the next snapshot's availability. The old snapshot's valid interval is therefore treated as half-open:

`[snapshot_available_at_ts_ms, snapshot_next_available_at_ts_ms)`

A rejection event whose confirmation equals the next snapshot availability is not eligible under the old boundary. At that instant, the next 4-hour snapshot becomes available and the old snapshot ceases to be current. The fact that the rejection candle opened while the old snapshot was active does not make its later close-confirmation available under that expired snapshot.

## 2. Direct source audit

The committed ledger contains 2,452 classification rows with a non-null first strong rejection timestamp. The audit recomputed confirmation timestamps and compared them with the recorded next-snapshot availability.

| Asset | Strict rows expired at confirmation | Broad rows expired at confirmation | Distinct underlying tests |
|---|---:|---:|---:|
| BTC | 8 | 9 | 9 |
| ETH | 2 | 4 | 4 |
| SOL | 4 | 8 | 8 |
| DOGE | 7 | 10 | 10 |
| AVAX | 8 | 9 | 9 |
| **Total** | **29** | **40** | **40** |

All 69 affected classification rows have confirmation exactly equal to the next snapshot availability; none is a later-than-end case. The 29 strict rows are nested within the 40 broad source tests.

## 3. Contract disposition

- Preserve all 2,452 original classification rows and source OHLC/event identities unchanged.
- For causal candidate availability, require confirmation strictly before the snapshot's next-availability endpoint.
- Assign the 40 broad / 29 strict affected classifications the explicit disposition `SNAPSHOT_EXPIRED_BEFORE_CONFIRMATION`.
- These are exclusions from candidate eligibility, not deletions from the descriptive historical archive.
- The remaining source counts before any other G0-05 validation/exclusion are 1,114 broad and 809 strict. These are provisional source-eligibility ceilings, not final candidate counts.
- The candidate record must retain the original snapshot identifiers, both snapshot endpoint timestamps, the rejection-candle open, the confirmation timestamp, and the exclusion reason.

## 4. Required regression tests

1. Confirmation at `snapshot_next_available_at_ts_ms - 1 ms` is eligible if all other conditions pass.
2. Confirmation exactly at `snapshot_next_available_at_ts_ms` is rejected.
3. Confirmation after the endpoint is rejected.
4. Rejection candle open inside the snapshot interval but confirmation at its endpoint is rejected.
5. Strict/broad paired source classifications receive the same timing disposition and remain correctly nested.
6. Every excluded event remains present in the disposition/reconciliation ledger.
7. The first eligible 1-minute execution bar cannot precede confirmation.

## 5. Interpretation

This is a causal availability correction for G0-05. It does not invalidate the accepted descriptive Module A rejection archive or its historical 1,154 broad / 838 strict event counts. It prevents an old boundary from being treated as current after the replacement 4-hour snapshot is available.

No order, fill, execution price, outcome, PnL, or profitability conclusion is created by this audit.
