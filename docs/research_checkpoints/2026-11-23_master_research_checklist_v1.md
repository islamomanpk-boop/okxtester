# Master Research Checklist V1 — OKX Price Action Research

**Repository:** `islamomanpk-boop/okxtester`  
**Branch:** `price-action-v1`  
**Created:** 2026-11-23  
**Purpose:** One readable, numbered source of truth for what has been researched, what is only provisional, what remains open, and what must wait. This checklist consolidates the main roadmap and later research checkpoints; it does not replace the detailed methods or historical reports.

## Status legend

- **[DONE]** Completed and supported by a recorded check/report. This means only the stated scope passed.
- **[PARTIAL]** Some descriptive work exists, but important parts are missing or not yet accepted.
- **[OPEN]** Not completed; do not treat as established evidence.
- **[LATER]** Depends on earlier research and is not authorized to start yet.
- **[HOLD]** An earlier attempt has a known defect; preserve it for history but do not use its results.

## Executive view

The project has useful five-asset data-quality, market-behaviour, sideways-detector, boundary-rejection, and breakout/retest evidence. It does **not** yet have a complete explanation of sideways-market behaviour, a validated matched-control comparison, a full general-signal study, or a validated executable strategy.

**Immediate research gate:** review and build a corrected matched-breakout-control implementation. Before any matching/outcome calculation, it must reproduce the 20 accepted breakout event counts exactly. If even one count differs, stop.

No strategy backtest, exit sweep, parameter optimization, profitability claim, or live-trading conclusion is authorized by this checklist.

---

## 1. Data foundation, identity, and coverage

- **[DONE]** Individual 1M OHLCV quality checks for BTC, ETH, SOL, DOGE, AVAX: duplicate timestamps, missing internal minutes, invalid OHLCV, and timestamp errors passed.
- **[DONE]** Five-asset timestamp intersection checked: 569,125 common minutes; use exact timestamps, never row-index alignment.
- **[DONE]** 1M-to-15M/4H aggregation audit passed for the identified input files and conventions: complete 15M/4H bars and OHLCV fields reconciled.
- **[PARTIAL]** Record and re-confirm exact file identity, date coverage, and lineage when necessary; do not repeat already-passed audits without a specific discrepancy.
- **[OPEN]** Verify original exchange/API provenance and exact instrument identity. Intended OKX configuration is not proof that historical files came from OKX.
- **[OPEN]** Verify volume units and meaning.
- **[OPEN]** Verify funding-rate source, coverage, timestamp convention, units, and gaps.
- **[OPEN]** Verify the provenance and generation rules of the 15M signal dataset.

**Gate:** no claims of verified OKX source, volume interpretation, or complete funding coverage until evidence exists.

## 2. Broad market behaviour across five assets

- **[DONE]** Daily/weekly range and return distributions and cross-asset comparisons.
- **[DONE]** Daily and multi-day movement thresholds, rolling 30/90-day behaviour, volatility-state persistence, and pump/dump or impulse follow-up descriptions.
- **[PARTIAL]** Chronological stability has been examined in several studies, but a consolidated robustness review remains.
- **[OPEN]** Full weekly path: day-by-day development of weekly range, timing/order of weekly high and low, pullbacks, directional legs, and path efficiency.
- **[OPEN]** Broader weekly-path robustness by asset and chronological subperiod.

## 3. Sideways-market definitions and regime taxonomy

- **[DONE]** Historical 48H detector formula-level reconstruction using `research/sideways_detector_original_v1.py`; its recorded test and historical reference-count checks passed.
- **[DONE]** Candidate strict P25 and broad P40 sideways definitions, plus 24H/48H/72H comparisons and rolling coverage/persistence descriptions.
- **[PARTIAL]** Current width quantiles are full-sample retrospective exploratory cutoffs, not live-safe thresholds.
- **[OPEN]** Separate and characterize at least:
  1. quiet/narrow/compressed sideways;
  2. wide but orderly sideways;
  3. volatile/choppy sideways;
  4. range-to-trend and trend-to-range transitions;
  5. volatility-shock/disorderly conditions.
- **[OPEN]** Measure regime label flicker, stability, transition timing, duration, and sensitivity to definitions.
- **[OPEN]** Compare causal range definitions and test sensitivity to lookback, width normalization, and thresholds. Do not silently promote a diagnostic indicator into a strategy filter.

**Questions this section must answer:** What makes a range quiet versus merely narrow? What distinguishes orderly movement from choppy movement? How often does a range change state, and how early can that change be known without future data?

## 4. Sideways boundaries, touches, and repeated tests

- **[DONE]** Descriptive 15M close-position zones, boundary-touch and rejection investigations exist.
- **[PARTIAL]** Earlier repeated-visit/episode counts and some preliminary rejection counts are not accepted because an upper-side variable error and missing exact 15M continuity were identified.
- **[OPEN]** Reconstruct timestamped detector snapshots and boundary-test state machine with exact 15M continuity and causal 4H availability.
- **[OPEN]** Define a boundary test consistently: approach, touch, penetration, close outside, and rejection must be separate labels.
- **[OPEN]** Measure first, second, third, and later tests; spacing between tests; time spent near the boundary; and whether prior tests change the next reaction.
- **[OPEN]** Compare upper and lower boundaries separately, by asset and strict/broad regime.
- **[OPEN]** Compare alternative boundary bands (for example 5%, 10%, 15% of the defined band convention) only as predeclared sensitivity analyses, not as post-hoc winner selection.

## 5. Sideways-boundary rejection: full path study

- **[DONE — LIMITED SCOPE]** A rejection forward-outcome dataset and dependence-aware block-bootstrap analysis were completed and validated for the currently defined event cohort. The broad primary 24H upper-minus-lower mean difference had a 7-day-block 95% interval that included zero. This is not evidence of a trading edge.
- **[PARTIAL]** The above does not complete the full rejection-episode, retest, candle-anatomy, or regime-conditioned study.
- **[OPEN]** Reconcile every accepted rejection event to its source snapshot, boundary, confirmation time, and next eligible 1M start.
- **[OPEN]** Measure path to channel interior, midpoint, opposite boundary, and failure through the rejected boundary.
- **[OPEN]** Separate continuation-first from pullback-first.
- **[OPEN]** Measure retests of rejection candle and boundary: incidence, first-retouch time, depth, duration, hold, rejection, clean crossing, and repeated crossing.
- **[OPEN]** Compare first versus repeated boundary tests and spacing between them.
- **[OPEN]** Measure rejection-candle range, body, wick proportions, close location, and volatility-normalized size; compare subsequent outcomes across predeclared groups.
- **[OPEN]** Report MFE, MAE (non-positive adverse-excursion convention), net directional movement, threshold timing, and complete/incomplete denominators at 15M, 1H, 4H, 12H, and 24H.
- **[OPEN]** Robustness by asset, side, strict/broad definition, subperiod, and reasonable predeclared boundary-band sensitivity.
- **[OPEN]** Use exact minute and 15M continuity; freeze context/boundaries; start only after completed rejection confirmation; disclose overlapping-event dependence.

**Important:** Do not reuse the defective preliminary episode counts. Keep the accepted forward-outcome/bootstrap result distinct from the still-open comprehensive episode study.

## 6. Sideways-channel breakouts and retests

- **[DONE]** Timing-corrected descriptive breakout/retest path study exists, including frozen boundaries, approach versus actual penetration, retest-hold descriptions, and fixed-horizon path outcomes.
- **[DONE]** Original breakout event masks reproduced exactly: 20/20 asset × definition × direction counts.
- **[DONE]** Accepted counts are recorded in `2026-11-22_original_breakout_event_reproduction_pass.md`.
- **[PARTIAL]** Existing work does not fully explain all false-breakout/failure paths or establish whether breakouts differ from comparable non-breakout approaches.
- **[OPEN]** Build a failure taxonomy: immediate return inside, shallow penetration then failure, failed retest, repeated boundary crossing, delayed failure, continuation, and unresolved outcomes. Define labels before counting.
- **[OPEN]** Measure time and distance outside the channel, retained breakout movement, retest depth/time, return-inside time, and opposite-side movement.
- **[OPEN]** Test robustness by asset, direction, strict/broad definition, and chronological subperiod.
- **[OPEN]** Account for overlapping breakout events and dependent follow-up windows.

**Accepted event-mask rules to preserve:** same frozen 4H snapshot for prior/current 15M observations; prior close at/inside boundary and current close outside; no added previous-sideways condition; no de-clustering/cooldown. The 15M close label maps to the final 1M candle at label minus one minute; follow-up begins at the next minute.

## 7. Matched non-breakout controls — immediate priority

- **[DONE]** Study design and matching specification documented.
- **[DONE]** Accepted original breakout event counts reproduced 20/20.
- **[HOLD]** First matched-control run is rejected as empirical evidence: breakout counts differed; some width thresholds were hard-coded incorrectly; MAE convention was wrong; exact minute continuity was not proven; outcome and matching-balance diagnostics were incomplete.
- **[OPEN — NEXT GATE]** Review/create a corrected replacement script and tests. The current GitHub tree did not contain a committed replacement implementation at the last review.
- **[OPEN]** Reproduce all 20 accepted breakout counts before any control construction. Stop on any mismatch.
- **[OPEN]** Use exact recovered full-sample thresholds computed by the accepted method; do not substitute rounded values.
- **[OPEN]** Correct non-positive MAE and require exact 1M continuity through every reported horizon.
- **[OPEN]** Validate control eligibility and pre-start-only matching covariates.
- **[OPEN]** Report standardized mean differences before/after matching, feature distributions, pair distances, unmatched events, and matching limitations.
- **[OPEN]** Label the specified greedy one-to-one matching accurately; do not claim globally optimal assignment.
- **[OPEN]** Complete all specified outcomes and same-direction breakout incidence during control follow-up. Never exclude a control because of future behaviour.
- **[OPEN]** Any uncertainty analysis must account for time blocks/event overlap; do not treat overlapping events as independent.
- **[OPEN]** Keep calculations read-only and conclusions conditional/descriptive, not causal or profitable.

**Gate:** no matched-control result is accepted until code review, tests, exact event-count validation, continuity checks, and matching diagnostics pass.

## 8. General 15M signal-candle anatomy and post-signal behaviour

- **[OPEN]** Build the complete eligible 15M signal cohort, not only sideways rejection or breakout subsets.
- **[OPEN]** Measure candle range, body, body/range, upper/lower wick, close location, and volatility-normalized size using only information available at signal close.
- **[OPEN]** Measure continuation-first versus pullback-first and revisits of signal open, midpoint, close, high/low, and structural levels.
- **[OPEN]** Measure retest time, depth, duration, hold/rejection/crossing, failure, reversal, and unresolved/no-touch outcomes.
- **[OPEN]** Measure MFE/MAE and forward movement at 15M, 1H, 4H, 12H, and 24H, with exact denominators and incomplete horizons.
- **[OPEN]** Break down by signal type, side, asset, candle-size group, and causally available market regime.
- **[OPEN]** Handle overlap/dependence and avoid future-informed groups or thresholds.

## 9. Execution-resolution and entry-opportunity research

- **[LATER]** Compare 1M, 3M, 5M, and 15M execution using the same completed 15M signal cohort.
- **[LATER]** Measure causal earliest entry, delay, entry price, price movement while waiting, and missed opportunities.
- **[LATER]** Compare immediate, pullback/limit, structural retest, and confirmation methods with explicit expiry/touch/fill assumptions.
- **[LATER]** Report touch, fill approximation, missed, expiry, partial-fill assumptions, and adverse selection separately.
- **[LATER]** Do not imply OHLC touch is a verified fill. A 15M execution candle cannot act before it closes.
- **[LATER]** Initially keep this descriptive; costs and profitability require later explicit authorization.

## 10. Cross-asset dependence and portfolio context

- **[OPEN]** Empirical BTC/ETH/SOL/DOGE/AVAX return dependence at 1M, 15M, 1H, 4H, and daily horizons.
- **[OPEN]** Rolling correlation and chronological stability.
- **[OPEN]** Downside/stress dependence, co-exceedance, co-jumps, and volatility connectedness.
- **[OPEN]** Predefined BTC lead/lag tests; do not interpret correlation as causation.
- **[OPEN]** Joint-movement and simultaneous-loss context for a future portfolio study.

## 11. UTC time-of-day, weekday, and calendar effects

- **[OPEN]** UTC-hour and weekday return, range, volatility, and volume distributions (volume only after its units are understood).
- **[OPEN]** Hour-by-weekday interaction, weekend/weekday comparison, and extreme-event timing.
- **[OPEN]** Chronological stability and multiple-comparison caution.
- **[OPEN]** Treat findings as descriptive until independently validated; do not create time filters from uncorrected noisy comparisons.

## 12. Costs, funding, risk, exits, and strategy research

- **[OPEN]** Verify applicable fee tier and actual fee schedule; current 0.05% taker fee per side plus 2 bps slippage per side is a planning assumption, not account verification.
- **[OPEN]** Verify funding data and model holding-time funding effects.
- **[OPEN]** Estimate slippage by asset, volatility, order type, and time of day where data permits.
- **[LATER]** Develop structure/volatility-based stop hypotheses only after behaviour studies justify them.
- **[LATER]** Compare exit families only after entry and execution assumptions are defined; avoid arbitrary broad parameter grids.
- **[LATER]** Any strategy test needs a written hypothesis, falsification rule, baselines, realistic costs, fixed risk, chronological development/validation/OOS separation, and per-asset plus portfolio results.
- **[LATER]** Final OOS must remain untouched until choices are frozen.
- **[LATER]** No profitability or live-readiness conclusion without robust net results and independent review.

---

## Recommended working order

This is the practical sequence. A numbered item is not automatically authorized just because it appears here.

1. **[NOW] Matched breakout controls:** inspect/build corrected implementation; pass 20/20 event-count gate before matching.
2. **[NEXT] General signal anatomy and post-signal path/retest:** use the complete frozen 15M signal cohort.
3. **[NEXT] Execution-resolution comparison:** same 15M signals across 1M/3M/5M/15M; descriptive opportunity first.
4. **[THEN] Data provenance and coverage closure:** exchange/instrument identity, volume, funding, and signal lineage.
5. **[THEN] Weekly path study:** high/low timing, daily range development, pullbacks, efficiency.
6. **[THEN] Cross-asset dependence:** correlations, stress dependence, co-jumps, lead/lag.
7. **[THEN] UTC time-of-day and weekday study.**
8. **[THEN] Broader sideways taxonomy and regime stability:** quiet/orderly/choppy/transitions, label flicker, repeated tests.
9. **[THEN] Complete comprehensive sideways rejection study:** rebuild episode state machine, retests, anatomy, path and robustness; keep it distinct from the already completed limited forward-outcome/bootstrap study.
10. **[THEN] Complete breakout failure taxonomy and robustness; integrate with matched controls.**
11. **[REVIEW] Consolidate all descriptive evidence:** supported findings, contradictions, unknowns, and limitations.
12. **[LATER / NOT AUTHORIZED] Only after explicit user approval, consider focused strategy hypotheses and execution/cost/risk experiments.**

The ordering of items 8–10 may be adjusted only after reviewing dependencies and the current roadmap; do not silently skip any open workstream.

## Required standards for every future study

Before running:
1. State the research question and why it is next in the sequence.
2. Link the exact roadmap item and accepted prior definition.
3. Predefine cohort, event labels, horizons, thresholds, exclusions, denominators, and sensitivity analyses.
4. State what would falsify the hypothesis or make the result inconclusive.
5. Review the code and tests before execution.

After running:
1. Validate event counts and timestamps against accepted references.
2. Validate exact continuity, complete windows, and causal availability.
3. Report missingness, censoring, exclusions, and denominators.
4. Report asset, direction, regime, and chronological breakdowns where planned.
5. Address overlapping events and dependence.
6. Separate descriptive associations, statistical uncertainty, fill assumptions, and net profitability.
7. Save script, tests, report, metadata, and a dated checkpoint; fetch the saved GitHub files to verify the write.

## Permanent project rules

- Check this master checklist and the detailed roadmap before every new experiment.
- Preserve existing local untracked reports; never use broad cleanup or overwrite commands.
- Never use future information to define a live-style signal, match, or regime.
- Freeze levels and use exact timestamps; never bridge missing intervals.
- Do not reuse results explicitly marked provisional, superseded, or audit-hold.
- Do not repeat completed audits without a concrete reason.
- A completed descriptive study is not proof of causality, a tradable edge, profitability, or live readiness.
- No strategy backtests or parameter sweeps until the descriptive gates are reviewed and the user explicitly authorizes the next stage.
