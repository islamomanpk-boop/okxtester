# Breakout Forward Outcome Study V1 — Final Research Audit

Date: 2026-11-24
Research phase: Phase 3 — Sideways / Range
Study: breakout_forward_outcome_study_v1
Status: Study run and output integrity checks completed; archived commit pending.

## 1. Research question

After a confirmed sideways-channel breakout, how does price behave over the
following 15 minutes, 1 hour, 4 hours and 12 hours?

The study also examines whether prior boundary-test and confirmed-rejection
history is associated with different forward price behaviour.

This is descriptive market research. It is not a trading strategy test and
does not establish profitability.

## 2. Frozen methodology and source

The study follows:

- docs/research_checkpoints/2026-11-24_breakout_forward_outcome_study_spec_v1.md
- docs/research_checkpoints/2026-11-24_breakout_forward_outcome_study_measurement_clarification_v1.md

Recovered original breakout source Git blob SHA:

95d2975947c449f3813d80ee7b12008db14f071f

Assets: BTC, ETH, SOL, DOGE, AVAX.

Definitions:
- BROAD_P40
- STRICT_P25

Directions:
- UPPER
- LOWER

Boundary-touch zones:
- 5% sensitivity
- 10% primary
- 15% sensitivity

Pre-breakout groups:
- DIRECT: zero prior touch tests.
- CONTACT_ONLY: one or more prior touch tests, zero confirmed rejections.
- ONE_REJECTION: exactly one prior confirmed rejection.
- TWO_REJECTIONS: exactly two prior confirmed rejections.
- THREE_PLUS_REJECTIONS: three or more prior confirmed rejections.

The 10% zone remains the primary measurement because it was selected as
the pre-declared middle-ground definition. It was not selected because it
produced the most favourable results. The 5% and 15% variants remain
sensitivity checks.

## 3. Entry and measurement rules

The 15-minute signal timestamp is the candle close label.

The entry is the OPEN of the first 1-minute candle whose timestamp equals
the signal timestamp. The final 1-minute candle belonging to the signal
period is not used as the entry candle.

Measured horizons use 15, 60, 240 and 720 consecutive 1-minute candles,
including the entry candle.

Measurements include:
- Signed directional close return.
- Maximum favourable excursion (MFE).
- Maximum adverse excursion (MAE).
- MFE and MAE normalized by the original frozen channel width.
- Time to first MFE and MAE extreme.
- First post-entry 1-minute close back through the original breakout boundary.
- Immediate adverse entry condition, recorded separately.

MFE and MAE use candle highs and lows. A first-extreme tie is assigned to
the earliest candle. The timestamp identifies the candle containing the
extreme, not an exact intraminute occurrence time.

No fees, slippage, funding, execution simulation, stop-loss, take-profit
or trading profitability are included.

## 4. Population and reconstruction results

The study reproduced:
- Original breakout event counts: 20/20.
- Original channel-width quantiles: 10/10.
- Original recovered source Git blob SHA: verified.
- Every classified event maps to exactly three prior-test zones.
- Prior-test links reconcile with prior touch-test counts.

Common 1-minute timestamps: 569,125.
Common timestamp gaps: 0.
Original breakout events in the study population: 1,592.
Prior-test classification rows: 4,776.
Forward event-zone-horizon rows: 19,104.
Complete horizon rows: 19,104.
Excluded or incomplete horizon rows: 0.

The original event helper used by this study requires at least 15 complete
1-minute follow-up candles for event eligibility. This population rule was
retained unchanged. All four measured horizons were complete for every
included event-zone row in this run.

## 5. Primary 10% zone group counts

BROAD_P40:
- DIRECT: 91
- CONTACT_ONLY: 404
- ONE_REJECTION: 407
- TWO_REJECTIONS: 29
- THREE_PLUS_REJECTIONS: 1
- Total: 932

STRICT_P25:
- DIRECT: 69
- CONTACT_ONLY: 261
- ONE_REJECTION: 303
- TWO_REJECTIONS: 27
- THREE_PLUS_REJECTIONS: 0
- Total: 660

BROAD_P40 and STRICT_P25 are overlapping event definitions. They must
remain separate and must not be combined as independent samples.

The two-rejection groups are small. The three-plus group has only one
BROAD_P40 observation and no STRICT_P25 observations. These groups do
not support reliable general conclusions.

## 6. Pooled primary-zone findings

The pooled analysis uses event-level rows across assets and directions
within each definition. It does not average asset-level group averages.

At the 12-hour horizon, boundary-failure rates were:

| Group | BROAD_P40 | STRICT_P25 |
|---|---:|---:|
| DIRECT | 75.8% | 76.8% |
| CONTACT_ONLY | 90.3% | 89.7% |
| ONE_REJECTION | 83.3% | 84.5% |

Boundary failure means a post-entry 1-minute candle closed back through
the original frozen breakout boundary. It is not automatically a losing
trade and is not a stop-loss result.

Across the pooled horizons, directional close returns were often near
zero or negative, and positive-return rates were generally around
40%-52% for the adequately populated groups.

There was no consistent monotonic improvement in forward outcomes as
prior confirmed rejection counts increased.

The contact-only group showed higher pooled boundary-failure rates than
the direct group, particularly at longer horizons. This is descriptive
and does not establish that contact-only events cause weaker breakouts.

## 7. Asset and direction heterogeneity

The asset/direction breakdown showed substantial variation.

Some lower-breakout groups, including examples in BTC and SOL, showed
positive median directional returns at longer horizons. Several upper
breakout groups in those same assets showed negative median returns.
Other assets and groups displayed different patterns.

The direction and asset patterns are not sufficiently consistent to
establish a general directional or asset-specific trading rule.

Many asset/direction/group cells have small sample sizes, especially
DIRECT groups. Individual small-cell percentages can change materially
with only a few observations.

The pooled results therefore must not be interpreted as a universal
property of all five assets or both breakout directions.

## 8. Integrity and output checks

The completed output audit found:

- 19,104 event-zone-horizon rows.
- 4,776 unique event-zone keys.
- Four horizons per event-zone key.
- Duplicate event-zone-horizon keys: 0.
- Unexpected horizon statuses: none.
- All horizon statuses: COMPLETE.
- Missing/nonfinite measured metrics: 0.
- Negative MFE values: 0.
- Negative MAE values: 0.
- MFE times outside their horizon: 0.
- MAE times outside their horizon: 0.
- Boundary-failure rows without failure timestamps: 0.
- Non-failure rows with failure timestamps: 0.

The 13,440 boundary-failure rows and 168 immediate-adverse-entry rows
are row-level counts across overlapping definitions, zones and horizons.
They are not counts of unique breakout events.

The exclusions audit contains no excluded or incomplete horizon rows.

The forward-study test suite passed 11/11 tests, including a dedicated
test verifying that entry uses the first 1-minute candle opening at the
15-minute signal timestamp.

## 9. Output SHA256 integrity record

The following output hashes were verified against the run metadata:

| Output | SHA256 |
|---|---|
| breakout_forward_outcomes_v1.csv | 71e1429a37ace9c38b2fae7cc2b42daa421709a701f864b97e5c206a7fbcfacf |
| breakout_forward_group_summary_v1.csv | e4f034af08a141640a938b3d7140f7bba6077a489dc7b3e86befcd1e773ae784 |
| breakout_forward_exclusions_audit_v1.csv | 7915f12d6292104f798055c6a471291239ae5fc356768eefbeeea7ea588c2c34 |
| original_event_reproduction_v1.csv | 954736383fa28b7382554bf7ac7235091713e33c43c3b2078f5434de8f0a2267 |
| original_quantile_reproduction_v1.csv | a9895c17c301194d885f266fc0d5622bb94cac5ef3eb471905c0d475dab03ebe |
| reconstruction_audit_v1.csv | 9f6b4a8adc5351da81ffc2ea1cba9deebcf6a21d4ebb390df392c24609fe7364 |
| run.log | 865719d7f8997049533b9b2b0dea6bbdc012a4c0f5ead73b490cd769f431bcd7 |
| run_metadata.json | 122e6b7afca3393eca9357e56a02b53ccb079b0b04d89708dfe407cac1ac268f |

The successful external retry log is:
reports/breakout_forward_outcome_v1_run_2026-11-24_retry1.log

The earlier failed attempt log is also preserved:
reports/breakout_forward_outcome_v1_run_2026-11-24.log

The failed first attempt documents a Pandas 3 compatibility error. The
successful retry followed the compatibility correction and produced the
outputs audited above. Both logs must be retained.

## 10. Limitations

1. This is descriptive forward price measurement, not a profitability test.
2. No fees, slippage, funding or execution mechanics are simulated.
3. Full-sample channel-width quantiles are retrospective, not live-calibrated.
4. BROAD_P40 and STRICT_P25 overlap and are not independent samples.
5. The 5%, 10% and 15% zone variants overlap and are not independent samples.
6. Small prior-rejection groups do not support reliable conclusions.
7. Asset and direction heterogeneity limits pooled generalization.
8. A boundary failure is not equivalent to a losing trade.
9. MFE is an observed maximum, not a realistically captured profit.
10. The results do not establish causality or a tradable edge.
11. Volume analysis remains excluded because source volume units are
    unverified.

## 11. Research decision

The study is accepted as a completed descriptive forward-outcome
measurement under its frozen specification.

It does not justify selecting a breakout trading strategy.

The evidence does not establish that more prior confirmed rejections
produce better breakouts. Breakout outcomes vary by asset and direction,
and boundary failures are common at longer horizons.

The original detector and measurement definitions remain unchanged.
No strategy-selection or profitability claim is authorized by this study.

## 12. Next research steps

1. Archive this audit, forward-study script, tests, reports and both run logs.
2. Update the master research roadmap to mark the forward-outcome study
   complete and its final audit archived.
3. Continue the remaining Phase 3 sideways/range research, including
   post-breakout retests and failed-breakout/reversal behaviour.
4. After Phase 3 is complete, move directly to Phase 1 — Uptrend/Bullish.
5. Continue the agreed numerical phase order: Phase 2, Phase 4, then Phase 5.
6. Only after broad phase research should candidate strategy hypotheses
   be selected for realistic backtesting.

## 13. Archival status

This audit document is prepared from the completed study outputs and
checks. Git commit and remote push are pending.

No unrelated untracked files are part of this study. In particular, do
not stage or modify:
- research/archive/final_timing_corrected_breakout_and_retest_recovered_original_2026-11-22.incomplete-local-2-lines.py
- src/portfolio_backtester.py.backup
