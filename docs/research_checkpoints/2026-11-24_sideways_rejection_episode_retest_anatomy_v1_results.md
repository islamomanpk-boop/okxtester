# Sideways Rejection Episode and Retest Anatomy V1 — Results and Audit Checkpoint

**Date:** 2026-11-24  
**Repository:** `islamomanpk-boop/okxtester`  
**Research branch:** `price-action-v1`  
**Workflow:** `Sideways Rejection Episode and Retest Anatomy V1 - Historical Study`  
**Workflow run:** [45414635491](https://github.com/islamomanpk-boop/okxtester/actions/runs/45414635491)  
**Job:** `138517425833`  
**Run conclusion:** SUCCESS  
**Implementation SHA-256:** `695f2fa1783ce2fd7b9654bc84a560a1c18579912c47bbbfb092be580d33e102`

## 1. Scope and disposition

The frozen V1 descriptive study ran against the accepted five-asset source population and produced all five required output files. This checkpoint records the first-pass results and a reporting/code-interpretation audit. It does **not** authorize strategy selection, profitability claims, or changes to the detector or event definitions.

The study is descriptive selected-event research, not a trading backtest.

## 2. Execution and population reconciliation

- Source event-ledger rows: 2,452.
- Eligible rejection events: 1,992.
- Broad cohort: 1,154.
- Strict cohort: 838; fully nested within broad.
- Event/horizon rows: 7,968 (1,992 × 4 horizons).
- Assets: BTC, ETH, SOL, DOGE, AVAX.
- Horizons: 15m, 1h, 4h, 24h.
- Confirmation delay: 15 minutes after the 15m rejection candle open.
- Output artifact: `sideways-rejection-episode-retest-anatomy-v1` (five files).

All 12 job steps completed successfully, including compilation, both test suites, frozen-input checks, the five-asset historical run, and artifact upload.

## 3. Input validation

| Asset | 1m rows | Feature rows | Broad | Strict | 1m gaps | Snapshot mismatches | Zero-range rejection candles |
|---|---:|---:|---:|---:|---:|---:|---:|
| BTC | 569,125 | 2,358 | 220 | 161 | 0 | 0 | 0 |
| ETH | 569,125 | 2,358 | 217 | 155 | 0 | 0 | 0 |
| SOL | 569,126 | 2,358 | 242 | 173 | 0 | 0 | 0 |
| DOGE | 569,126 | 2,358 | 216 | 158 | 0 | 0 | 0 |
| AVAX | 569,127 | 2,358 | 259 | 191 | 0 | 0 | 0 |
| **Total** | **2,845,629** | **11,790** | **1,154** | **838** | **0** | **0** | **0** |

All 1,992 events had an exact confirmation-minute row. The 15m, 1h, and 4h horizons were complete for every event. At 24h, 8 broad events and 2 strict events were censored at the end of available history; censored rows were not gap-bridged or treated as complete.

## 4. Primary results

The table reports the fraction of events with a first boundary-zone touch observed within each horizon, its median elapsed time among observed touches, inward-separation-close incidence, and strict outward-penetration incidence. These are first-passage descriptions, not trade outcomes.

| Cohort | Horizon | Events | Boundary-zone touch | Median touch time | Inward separation | Outward penetration |
|---|---:|---:|---:|---:|---:|---:|
| Broad | 15m | 1,154 | 53.8% (621) | 1m | 35.5% (410) | 8.9% (103) |
| Broad | 1h | 1,154 | 73.0% (842) | 3m | 56.9% (657) | 29.8% (344) |
| Broad | 4h | 1,154 | 83.1% (959) | 5m | 75.0% (866) | 55.0% (635) |
| Broad | 24h | 1,154; 8 censored | 92.0% (1,054) | 7m | 89.9% (1,037) | 81.2% (937) |
| Strict | 15m | 838 | 54.2% (454) | 1m | 36.4% (305) | 9.3% (78) |
| Strict | 1h | 838 | 74.7% (626) | 3m | 58.2% (488) | 31.9% (267) |
| Strict | 4h | 838 | 84.4% (707) | 5m | 74.8% (627) | 56.6% (474) |
| Strict | 24h | 838; 2 censored | 92.2% (772) | 7m | 90.2% (756) | 82.2% (689) |

Counts in parentheses are observed first-passage events. The denominators for fractions are the full cohort at that horizon; the 24h censor counts are disclosed above. Strict is nested within broad and must not be added to it.

### 4.1 First 15-minute window: asset variation

| Asset | Broad events | Broad touch | Strict events | Strict touch |
|---|---:|---:|---:|---:|
| BTC | 220 | 51.8% (114) | 161 | 47.8% (77) |
| ETH | 217 | 55.8% (121) | 155 | 56.8% (88) |
| SOL | 242 | 58.3% (141) | 173 | 59.0% (102) |
| DOGE | 216 | 50.0% (108) | 158 | 54.4% (86) |
| AVAX | 259 | 52.9% (137) | 191 | 52.9% (101) |

The broad 15m retest incidence ranges from 50.0% to 58.3% across assets. This spread is descriptive only; it is not evidence that one asset has a better tradable setup.

### 4.2 Boundary direction

At 15m, broad lower-boundary events recorded a touch in 55.7% (311/558), versus 52.0% (310/596) for upper-boundary events. Strict lower events were 55.1% (218/396), versus 53.4% (236/442) for strict upper events. This modest difference is not an independently validated directional effect.

### 4.3 Chronological stability

Across the 14 monthly buckets from 2025-10 through 2026-11, broad 15m retest incidence ranges from 44.0% to 71.4%; the 71.4% bucket contains only 21 events. Strict monthly incidence ranges from 48.8% to 71.4%, with the 71.4% bucket containing only 7 events. Sample sizes vary substantially by month. No claim of stable conditional behaviour or out-of-sample persistence is justified from these raw monthly proportions.

## 5. Event ordering and interpretation audit

In the broad 15m cohort:
- 584 events were classified retest-first;
- 350 were separation-first;
- 219 had neither first passage within 15m;
- 1 had same-bar ambiguity.

In the strict 15m cohort:
- 420 were retest-first;
- 260 were separation-first;
- 157 had neither;
- 1 had same-bar ambiguity.

The confirmation minute is intentionally included by the frozen specification. A touch is timestamped at the minute candle's **open timestamp**, so 245/1,154 broad events and 185/838 strict events have elapsed time recorded as 0 minutes. This means the touch occurred somewhere inside the confirmation-minute OHLC bar; it does **not** prove a touch at the exact confirmation instant or an executable fill at that instant. Any later reporting must label this as minute-resolution, same-bar timing.

The metric `retest_close_inward` is true for approximately 99% of observed retests. This is not a strong independent rejection-quality measure: the retest zone is defined close to the channel boundary, and the flag only asks whether that same candle closes on the inward side of the boundary. Do not present this percentage as a 99% success rate or as proof of rejection.

The OHLC data cannot reveal the intraminute order of a boundary touch and a close/separation condition. Same-bar cases remain ambiguous by design. Overlapping events are not independent observations.

## 6. Limitations

1. Selected historical rejection events only; no matched non-rejection control in this study.
2. Broad and strict cohorts are nested, not independent samples.
3. Event paths can overlap in time and across repeated tests.
4. 1-minute OHLC cannot establish tick sequence, spread, liquidity, queue position, or executable fills.
5. A first touch is a first-passage metric, not a count of repeated retest episodes.
6. No fees, slippage, funding, position sizing, P&L, expectancy, or strategy performance were evaluated.
7. The 24h horizon has 8 broad and 2 strict right-tail censored observations.
8. The source study's fixed 10% boundary band and 20% inward-separation geometry were retained; no threshold optimization was performed.

## 7. Research disposition and next authorized task

**Disposition: descriptive V1 execution passed; interpretation remains limited.** No trading rule or strategy should be selected from these results.

Next, continue Phase 3 (Sideways/Range) with a separately specified **retest-quality and matched-control study**, before any strategy selection. It should distinguish:
- immediate confirmation-minute touches from later retests;
- touch-only events from closes back inside and sustained inward separation;
- boundary retests followed by renewed penetration versus continued inward movement;
- rejection events from comparable boundary interactions without a strong-rejection label.

Any new cohort, matching method, outcome definition, or threshold must be frozen in a new specification before its historical run. Use dependence-aware uncertainty or event-clustered summaries if inferential comparisons are proposed. Do not retrofit thresholds to these V1 results.

## 8. Artifact contents

The successful workflow uploaded:
- `data_validation_v1.csv`
- `event_path_outcomes_v1.csv`
- `event_anatomy_v1.csv`
- `group_summary_v1.csv`
- `run_metadata_v1.json`

The artifact is retained by GitHub Actions until 2026-12-08 (subject to GitHub's artifact retention controls). The artifact should be preserved or downloaded before expiry if long-term reproducibility requires it.
