# Breakout Prior-Test Count Study — Frozen Specification V1

**Date:** 2026-11-24  
**Repository:** `islamomanpk-boop/okxtester`  
**Branch:** `price-action-v1`  
**Status:** FROZEN FOR CLASSIFICATION DIAGNOSTIC; no new results yet  
**Assets:** BTC, ETH, SOL, DOGE, AVAX  
**Research only:** no strategy simulation, fills, fees, slippage, funding, or profitability claims.

## 1. Research question

Among the accepted original sideways-channel breakout events, does the number of distinct prior confirmed rejection tests at the same frozen 4H boundary correspond to different subsequent breakout behaviour?

Classify upper resistance breakouts and lower support breakdowns separately into:
- 0 prior confirmed rejection tests;
- 1 prior confirmed rejection test;
- 2 prior confirmed rejection tests;
- 3 or more prior confirmed rejection tests.

The primary count is **confirmed rejection tests**, not the number of 15M candles that touched the boundary. Also retain the total number of distinct prior touch tests and the number of contact-only tests (tests with no confirmed rejection before breakout).

A zero-rejection event is called “0 prior confirmed rejections” in tables. It is not necessarily an untouched boundary: it may have one or more contact-only tests.

## 2. Immutable original breakout reference

Use the recovered original source as the immutable event reference:

- File: `research/archive/final_timing_corrected_breakout_and_retest_recovered_original_2026-11-22.py`
- Git blob SHA: `95d2975947c449f3813d80ee7b12008db14f071f`
- Do not edit or replace this source.

Reproduce its data construction and event gate exactly:
- Five assets and common 1M timestamp intersection.
- Complete 15M and 4H bars from the common 1M data, with the original `label="right", closed="left"` resampling.
- 4H channel from the previous 12 completed 4H bars:
  `upper = high.rolling(12).max().shift(1)`;
  `lower = low.rolling(12).min().shift(1)`.
- Preserve the original efficiency, overlap, and channel-width formulas.
- Preserve full-sample joined-15M channel-width P25 and P40 populations and thresholds.
- Sideways state: selected width threshold, efficiency <= 0.30, overlap >= 0.70.
- Preserve the original 15M close-label `merge_asof(direction="backward")`, `same_snapshot` condition, and upper/lower close-crossing conditions.
- Do not add a previous-sideways gate, cooldown, de-clustering, or any other event filter.
- Signal is known at the completed 15M close. Original 1M follow-up timing, if later used, starts at the next 1M candle open.

### Mandatory reproduction gate

Before classifying any prior tests, reproduce:
1. All 20 asset × strict/broad × direction breakout counts exactly.
2. All 10 asset × P25/P40 channel-width thresholds exactly, to the original recorded precision.

Expected event counts:

| Asset | Broad lower | Broad upper | Strict lower | Strict upper |
|---|---:|---:|---:|---:|
| BTC | 91 | 115 | 62 | 81 |
| ETH | 87 | 77 | 51 | 51 |
| SOL | 117 | 96 | 77 | 71 |
| DOGE | 81 | 75 | 55 | 65 |
| AVAX | 84 | 109 | 64 | 83 |

Expected thresholds:

| Asset | P25 (%) | P40 (%) |
|---|---:|---:|
| BTC | 3.242203 | 3.948630 |
| ETH | 4.242326 | 5.481886 |
| SOL | 5.067043 | 6.114542 |
| DOGE | 5.165724 | 6.264058 |
| AVAX | 5.703625 | 6.916216 |

Any mismatch is a hard failure. Do not proceed to classification or interpret results until the discrepancy is investigated and documented.

## 3. Data and time alignment

Build the complete 1M, 15M, and 4H series from the same common 1M timestamps and source files used by the recovered original script. Keep the original 15M **closing-time labels** throughout the breakout and prior-test calculation.

Do not use the older `sideways_boundary_events_historical_v1` event ledger as the primary prior-test source. Its implementation uses 15M opening-time feature assignment and suppresses the first observed 15M bar at/after feature availability. That is a distinct eligibility convention from the recovered original script's close-labelled `same_snapshot` breakout gate. Rebuild the prior-test history on the original detector's joined 15M timeline instead.

For each breakout, use only the same 4H snapshot and the same continuous 15M segment as the breakout. Do not carry tests across:
- a 4H snapshot change;
- a missing/non-consecutive 15M timestamp (expected interval exactly 15 minutes);
- an invalid or non-selected sideways context.

A 15M bar closing exactly at the 4H snapshot timestamp may be used as a prior touch observation only if the original 4H context is available at that close; it is not itself an eligible original breakout signal when `same_snapshot` is false. Every prior rejection must have a completed close timestamp strictly earlier than the breakout close.

## 4. Boundary touch and test state machine

Let frozen channel width in price units be `W = upper - lower`, with finite `W > 0`. Freeze both boundaries and W for the full 4H snapshot.

### Primary touch zone: 10% of W

- Upper resistance touch: `high >= upper - 0.10 * W`.
- Lower support touch: `low <= lower + 0.10 * W`.

Touch is wick-based; the touch candle does not need to close inside the zone.

### Distinct test and separation

A test begins on the first eligible touch in a snapshot/direction/continuity segment.

Repeated touch candles before confirmed separation remain part of the same test. A new test can begin only after a completed **non-touch** 15M candle confirms separation from the same frozen boundary:

- After an upper test: `close <= upper - 0.20 * W`.
- After a lower test: `close >= lower + 0.20 * W`.

The 20% separation threshold is fixed by the existing predeclared repeated-test protocol. The separation candle closes the active test and arms the next test; it cannot also start a new test. A later touch starts the next test. A mere non-touch pause without the 20% close-distance condition does not create a new test.

Test numbering/state resets at each new 4H snapshot and each 15M continuity gap. Upper and lower boundary state machines are independent.

### Confirmed strong rejection

Count at most the first strong rejection per test. The rejection must be confirmed on a completed touch candle:

- Upper: upper touch AND `close < upper - 0.10 * W` AND `close > lower`.
- Lower: lower touch AND `close > lower + 0.10 * W` AND `close < upper`.

A rejection is only known at that 15M candle's close. A test with no such qualifying candle is a contact-only test.

The test remains active after its first rejection until the non-touch 20% separation rule closes it. Later touch candles in that same test cannot create additional rejection counts.

## 5. Causal classification at each breakout

For each original breakout event:
1. Identify its exact asset, strict/broad definition, direction, 15M close timestamp, and 4H snapshot.
2. Inspect only earlier 15M bars in that same snapshot and uninterrupted segment. Exclude the breakout candle itself from all prior-test counts.
3. Count distinct test episodes that began strictly before the breakout close.
4. Count a test as a prior confirmed rejection only if its first qualifying rejection close is strictly earlier than the breakout close.
5. Count a test without a qualifying prior rejection as contact-only. This includes an active touch test that has started before the breakout but has not confirmed a rejection by the breakout close.
6. Do not use any information from after the breakout close to complete, reject, or reclassify a prior test.

Store at least:
- `prior_touch_test_count`;
- `prior_confirmed_rejection_count` (primary classifier);
- `prior_contact_only_test_count`;
- primary group: `0`, `1`, `2`, or `3+`;
- timestamps and details for every linked prior test, including test start, first rejection (if any), separation/closure (if any), touch-zone width, and frozen boundary values.

The primary group is determined only by `prior_confirmed_rejection_count`. Do not substitute total touch-test count or test rank for confirmed rejection count.

## 6. Zone-width sensitivity

The primary diagnostic uses the predeclared 10% touch zone and fixed 20% separation rule.

Also calculate classification sensitivity using 5% and 15% touch zones while keeping the separation close fixed at 20% of W. This isolates the effect of changing the touch-zone definition while preserving the existing separation rule. Report each sensitivity as a separate definition; never pool it with the 10% primary result.

For each zone width, the strong-rejection close threshold uses that zone's inner edge. The 20% separation threshold remains fixed.

## 7. Diagnostic outputs

This first implementation is a **classification diagnostic only**, not the forward-outcome study.

Write only to a new, versioned directory:
`reports/breakout_prior_test_count_v1/`

Required outputs:
- breakout-level classification CSV, one row per original event and definition/zone variant;
- prior-test linkage CSV, one row per breakout-to-prior-test link, with test and rejection timestamps and status;
- group-count summary CSV by asset, strict/broad definition, direction, zone variant, and 0/1/2/3+ prior confirmed rejection group;
- audit CSV or Markdown with source rows, common timestamps, complete bars, snapshot and continuity resets, original event reproduction, exclusion counts, and invariant checks;
- run log and metadata with source paths, script version, timestamp conventions, thresholds, and hashes where practical.

Refuse to write into a non-empty output directory. Do not overwrite any earlier report, source file, detector feature, or historical event ledger.

## 8. Mandatory validation

The diagnostic must fail closed unless all applicable checks pass:
1. Original 20/20 event counts reproduce exactly.
2. Original 10/10 P25/P40 thresholds reproduce within the documented numeric tolerance.
3. All 1M timestamps are unique and ordered; common timeline continuity is audited.
4. Every 15M timestamp interval used for test state is exactly 15 minutes or triggers a documented reset.
5. Every test starts on a qualifying wick touch.
6. Every strong rejection satisfies its direction's touch and close rules.
7. At most one first strong rejection is recorded per test.
8. Every new test after the first is preceded by a qualifying non-touch 20% separation candle.
9. No test state crosses a snapshot or continuity reset.
10. Every prior-test/rejection timestamp is strictly earlier than the associated breakout close.
11. The breakout candle is excluded from prior-test counts.
12. Per-event counts reconcile to the linked prior-test rows.
13. Strict events are expected to be a subset of broad events for the same asset/direction/signal time; audit this relationship without treating overlapping labels as independent samples.
14. The output directory was new/empty before writing; all input files remain unchanged.

If any invariant fails, mark the run failed and do not interpret group counts.

## 9. Reporting and interpretation limits

- Report denominators for every group and every asset/direction/strict-broad/zone variant.
- Strict is a subset of broad; strict and broad rows are overlapping labels, not independent samples. Do not add them as unique events.
- The 5%, 10%, and 15% variants are repeated classifications of the same underlying breakouts, not independent event samples.
- Upper/lower events and nearby breakout follow-up windows may be dependent.
- Full-sample P25/P40 thresholds are retrospective/exploratory, not live-calibrated.
- A prior rejection count is a descriptive market-history feature, not proof of a causal effect or tradable edge.
- No MFE/MAE, continuation, return-inside, retest, forward outcomes, fills, costs, or profitability are calculated in this diagnostic.
- Do not use volume; source volume units remain unverified.

## 10. Next stage (not part of this diagnostic)

Only after the classification diagnostic passes and representative event sequences are manually reviewed, freeze a separate forward-outcome specification. That later study may compare the 0/1/2/3+ groups from the next eligible 1M open across 15M, 1H, 4H, and 12H, with explicit incomplete-horizon handling, event dependence, and time-block uncertainty. Post-breakout retests remain a separate experiment.

No strategy selection or trading backtest is authorized by this diagnostic alone.
