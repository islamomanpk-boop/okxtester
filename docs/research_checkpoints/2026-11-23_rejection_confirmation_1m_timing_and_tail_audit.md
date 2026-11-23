# Rejection Confirmation 1M Timing and Final Snapshot Tail Audit

Date: 2026-11-23
Branch: `price-action-v1`
Status: **PASS for rejection-event 1M continuity; final snapshot tail is incomplete and must be censored/excluded where relevant.**

## Rejection confirmation timing

The event ledger stores `first_strong_rejection_ts_ms` as the OPEN timestamp of the 15-minute rejection candle. Its close is confirmed 15 minutes later:

```
rejection_confirmed_at_ts_ms = first_strong_rejection_ts_ms + 900000
```

A corrected read-only diagnostic checked the broad cohort's 1,154 first-strong-rejection events against the original 1-minute files for BTC, ETH, SOL, DOGE, and AVAX.

| Asset | Events | Exact confirmation minute | 16 consecutive 1M timestamps |
|---|---:|---:|---:|
| BTC | 220 | 220/220 | 220/220 |
| ETH | 217 | 217/217 | 217/217 |
| SOL | 242 | 242/242 | 242/242 |
| DOGE | 216 | 216/216 | 216/216 |
| AVAX | 259 | 259/259 | 259/259 |
| **Total** | **1,154** | **1,154/1,154** | **1,154/1,154** |

For each asset, every checked offset from 0 through 15 minutes matched exactly, and the full 1M source timeline contained no unusual timestamp gaps.

## Correction to an earlier diagnostic

An earlier validation printed zero passing 16-minute sequences. That result was a diagnostic-code defect, not a source-data failure: its Boolean accumulator was initialized to all False and then updated using in-place logical AND, which can never turn a False value into True. The corrected diagnostic independently evaluated all 16 timestamp offsets. Do not cite or reuse the earlier zero counts.

## Final 15M snapshot tail

For all five assets, the final feature snapshot interval contained only 9 observed 15M bars; after suppressing the first bar, only 8 eligible bars remained.

| Asset | Interval bars | Eligible bars | Last eligible open | Last eligible close | Expected next boundary |
|---|---:|---:|---:|---:|---:|
| BTC | 9 | 8 | 1795096800000 | 1795097700000 | 1795104000000 |
| ETH | 9 | 8 | 1795096800000 | 1795097700000 | 1795104000000 |
| SOL | 9 | 8 | 1795096800000 | 1795097700000 | 1795104000000 |
| DOGE | 9 | 8 | 1795096800000 | 1795097700000 | 1795104000000 |
| AVAX | 9 | 8 | 1795096800000 | 1795097700000 | 1795104000000 |

The final eligible candle closes before the expected next snapshot boundary. The final feature interval is therefore truncated by the available source history. This is a dataset-tail limitation, not a 15M gap inside the available history.

## Downstream study rules

1. Preserve the event ledger unchanged.
2. Derive a separate confirmation timestamp as rejection candle open + 15 minutes.
3. Do not start forward returns or execution before confirmation.
4. For 1M data, require the first eligible execution/outcome candle to open at or after confirmation.
5. Apply explicit future-data completeness requirements to each outcome horizon.
6. Exclude or mark right-censored any event whose required future horizon extends beyond available data.
7. Do not treat a snapshot-end or gap closure as a rejection signal.
8. Keep the final truncated snapshot interval out of any analysis requiring a complete 4H snapshot interval, unless a specifically designed partial-interval method is justified and documented.

## Scope

This audit validates timestamp availability and continuity around the reconstructed broad-cohort rejection events. It does not validate trade fills, price-path outcomes, costs, funding, profitability, or predictive power. No source files or prior reports were modified by the diagnostic.
