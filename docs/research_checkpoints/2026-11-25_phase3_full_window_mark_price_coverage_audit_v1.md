# Phase 3 full-window historical mark-price coverage audit V1

**Recorded:** 2026-11-25  
**Funding source:** committed audited funding coverage manifest  
**Manifest SHA-256:** `59c08bb34ac82e00e60066dad7e50d0cc62b4097a3580e186251a6c23de67c7e`  
**Research script:** `src/phase3_funding_mark_price_full_coverage_v1.py`  
**Research/test source commit:** `fc1e030d95a1c4cbd6a4ca4c46b3640d2d152ef4`  
**Synthetic helper tests:** workflow run [45659424766](https://github.com/islamomanpk-boop/okxtester/actions/runs/45659424766) — PASS  
**Hosted-runner full audit:** [45659424729](https://github.com/islamomanpk-boop/okxtester/actions/runs/45659424729) — PASS; artifact `15043858498`, SHA-256 `632501e666f91c4b7d5b3f88a0345077d986923d308624be874bf370c1250dea`  
**VPS-runner full audit:** [45659811546](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45659811546) — PASS; artifact `15045165371`, SHA-256 `55f1330f735323b1353ca424ee101090bab7f9754432d7fb0858a172c89a76f5`

## 1. Scope and method

The audit used the previously accepted five-asset funding coverage manifest. It records 1,188 actual funding timestamps per instrument, identical cross-asset timestamp sets, no missing settlements, no irregular intervals, and an observed 480-minute cadence throughout this specific historical window. The script reconstructs the timestamp sequence from each manifest row count, first/last timestamp, and verified interval; it does not assume that eight-hour funding is universal outside this audited period.

For BTC, ETH, SOL, DOGE, and AVAX USDT swaps, the script paginated the public OKX historical mark-price-candles endpoint for 4H candles over 2025-10-20 00:00 UTC through 2026-11-19 16:00 UTC. It matched each funding timestamp to a 4H mark candle opening at that exact timestamp. It also requested 12 evenly spaced 1M mark candles per asset (60 total) to check cross-resolution consistency.

The VPS run compared the mark proxy with all 1,188 corresponding 1M trade candles per asset. The independent hosted-runner run used the canonical Git 1M files; those files contain 1,185 of the 1,188 funding timestamps per asset because the canonical snapshot does not cover three start/end boundary events. Both runs retrieved identical 4H coverage summaries and identical 60-point 1M mark cross-resolution values.

No API credentials were used. No raw funding file, market CSV, SQLite database, or VPS service was modified. Only small JSON summary artifacts were uploaded.

## 2. Full-window mark-candle coverage

| Asset | Funding events | 4H mark candles in window | Exact funding-time matches | Missing | Unconfirmed | 4H gaps |
|---|---:|---:|---:|---:|---:|---:|
| BTC | 1,188 | 2,375 | 1,188 | 0 | 0 | 0 |
| ETH | 1,188 | 2,375 | 1,188 | 0 | 0 | 0 |
| SOL | 1,188 | 2,375 | 1,188 | 0 | 0 | 0 |
| DOGE | 1,188 | 2,375 | 1,188 | 0 | 0 | 0 |
| AVAX | 1,188 | 2,375 | 1,188 | 0 | 0 | 0 |
| **Total** | **5,940** | **11,875** | **5,940** | **0** | **0** | **0** |

All retrieved 4H mark candles were confirmed. Every audited funding timestamp aligned exactly with a 4H mark candle opening timestamp.

## 3. Cross-resolution verification

The 60-point 1M mark-price sample returned 60/60 exact timestamp matches, all confirmed. At every one of the 60 sample points, the 1M mark candle open was **exactly equal** to the 4H mark candle open at the same timestamp (zero difference at source precision).

The 1M mark candle close was not equal to the 4H open in general; it represents the mark price later in the minute. Its pooled sample difference versus the 4H open had median -2.06 bps, mean absolute difference 7.77 bps, and observed range -23.56 to +19.12 bps. This is why the opening value, not the later close, is the relevant candle-derived proxy candidate for the nominal funding timestamp.

## 4. Comparison with trade-candle proxies

The VPS comparison covers all 5,940 funding timestamps. Differences are calculated as `(mark_proxy / trade_price - 1) × 10,000` basis points.

| Asset | Mark 4H open vs trade 1M open: mean absolute bps | p05 to p95 bps | Mark 4H open vs trade 1M close: mean absolute bps | p05 to p95 bps |
|---|---:|---:|---:|---:|
| BTC | 0.261 | -0.656 to +0.650 | 4.965 | -10.259 to +10.615 |
| ETH | 0.347 | -0.848 to +0.903 | 6.538 | -12.817 to +14.303 |
| SOL | 0.777 | -2.306 to +1.036 | 8.041 | -16.406 to +16.582 |
| DOGE | 0.837 | -2.213 to +1.127 | 7.972 | -17.364 to +15.458 |
| AVAX | 1.030 | -2.680 to +1.386 | 10.056 | -22.171 to +18.760 |

Pooled results:
- **Mark 4H open vs trade 1M open:** 5,940 observations; median -0.023 bps; p05 -2.073; p95 +1.072; p99 +2.122; mean absolute difference 0.650 bps; observed range -8.236 to +5.563 bps.
- **Mark 4H open vs trade 1M close:** 5,940 observations; median 0.000 bps; p05 -16.217; p95 +15.428; p99 +29.380; mean absolute difference 7.514 bps; observed range -190.710 to +363.923 bps.

The trade 1M open is much closer to the mark 4H open than the trade 1M close is in this sample. This is consistent with the mark-open timestamp interpretation. It does not make trade open an exact mark price. The 4H candle close is not a settlement proxy: it is four hours later and differs substantially from the trade close (pooled mean absolute difference 83.722 bps).

## 5. Interpretation and recommended policy direction

The best-supported **public candle-derived proxy candidate** is the 4H mark-candle open at the exact funding timestamp (equivalently, the 1M mark-candle open at that timestamp, as confirmed on the 60-point sample). It is a mark-price series rather than a trade-price series, has full exact timestamp coverage in the audited window, and is substantially closer to trade-candle open than trade-candle close.

Recommended policy direction for consideration:
1. Keep `exact` mode reserved for an independently supplied, verified settlement mark. Do not populate it from a candle.
2. Add an explicit `mark_candle_open_proxy` mode for research use, using the 4H mark-candle open at the expected funding timestamp. Label it approximate in all result metadata.
3. Retain the existing `candle_close_proxy` as a legacy sensitivity comparator, not as an unlabelled exact mark.
4. Before any PnL backtest is authorized, test cashflow arithmetic under both proxy modes and stress the observed mark-vs-trade differences. Do not optimize a strategy on one funding proxy alone.

This is a recommendation, **not an accepted engine-policy change**. The current engine contract has not been changed and the new proxy mode has not been implemented.

## 6. Why exact settlement mark remains unverified

A 4H or 1M candle open is a candle-derived value. Exact timestamp alignment and cross-resolution equality do not independently prove that OKX used that precise mark snapshot for the funding assessment. The exchange's funding assessment may occur over a short window after the nominal timestamp.

The official OKX V5 account-bills documentation describes `px` for funding-fee expense/income bill subtypes 173/174. A read-only production account-bill sample could provide an independent realized-settlement cross-check, but no production account bills were accessed. Such account records would validate actual account events, not automatically provide a universal mark-price series for hypothetical backtests.

Official API reference: https://app.okx.com/docs-v5/en/ (Public Data → Get mark price candlesticks history; Account → Bills history).

## 7. Gate disposition

The public mark-price source is now fully coverage-audited for all 5,940 funding timestamps in the frozen historical window. This materially improves the evidence base for G0-03/G0-09 and identifies a preferred proxy candidate. It does **not** establish exact settlement marks, approve a proxy policy, implement the new engine mode, or complete the required real-input funding-engine acceptance checks.

G0-03 and G0-09 remain **OPEN** pending explicit funding-price policy acceptance, engine integration/tests for the selected mode, and independent settlement validation if exact mode is claimed. Gate 0 remains **CONDITIONAL HOLD**. No Phase 3 candidate generation, Gate 2 execution-resolution comparison, strategy PnL backtest, or Phase 1 handoff is authorized by this audit.
