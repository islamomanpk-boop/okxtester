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

## 13. Full market-phase research — all phases, not sideways only

**Purpose:** Build a complete descriptive understanding of every important market condition before designing regime-specific trading rules. The phase labels below are research categories, not claims that markets always fit neatly into one category. A market may be ambiguous, mixed across timeframes, or in transition.

**Coverage rule for every phase:** Study BTC, ETH, SOL, DOGE, and AVAX individually and comparatively; use the relevant 1M, 15M, 1H, 4H, and 1D views without mixing information that was unavailable at the decision time. Report sample counts, missingness, chronological stability, uncertainty, and overlapping-event dependence. Define each event causally and preserve an explicit uncertain/no-classification state.

### 13.1 Bullish trend / uptrend

- **[OPEN]** Define trend structure using causally confirmed higher highs and higher lows; record swing confirmation delay and avoid future-confirmed pivots being treated as known earlier.
- **[OPEN]** Measure trend direction, slope, directional efficiency, persistence, duration, speed, and distance travelled.
- **[OPEN]** Separate early, developing, mature, accelerating, weakening, and exhausted uptrends using predeclared descriptive labels.
- **[OPEN]** Measure impulse legs: size, duration, candle anatomy, volatility expansion, pauses, and continuation after each leg.
- **[OPEN]** Measure pullbacks/corrections: depth in price and prior-leg percentage, duration, speed, retracement, number of countertrend candles, and recovery time.
- **[OPEN]** Study higher-low formation, failed higher lows, support retests, breakout from prior highs, acceptance above highs, and failed upside breakouts.
- **[OPEN]** Measure trend pauses, consolidations, flags/ranges, volatility contraction/expansion, and whether continuation or transition follows.
- **[OPEN]** Study trend failure and reversal warning behaviour: loss of structure, lower highs, failed recovery, downside expansion, and time from first warning to confirmed state change.
- **[OPEN]** Measure forward MFE/MAE, continuation-first versus pullback-first, threshold timing, and outcomes after pullback/retest events.
- **[OPEN]** Compare strong versus weak trends, asset, timeframe, chronological period, and contemporaneously known higher-timeframe context.

### 13.2 Bearish trend / downtrend

- **[OPEN]** Mirror the uptrend structural study using causally confirmed lower lows and lower highs, with confirmation delay recorded.
- **[OPEN]** Measure direction, slope, efficiency, persistence, duration, speed, downside legs, and volatility behaviour.
- **[OPEN]** Separate early, developing, mature, accelerating, weakening, and exhausted downtrends.
- **[OPEN]** Measure bearish impulse legs and countertrend rallies: size, duration, retracement, speed, and continuation after the rally.
- **[OPEN]** Study lower-high formation, failed lower highs, resistance retests, breakdown from prior lows, acceptance below lows, and failed breakdowns.
- **[OPEN]** Measure pauses, bear flags, consolidations, squeeze/compression, and downside continuation versus reversal.
- **[OPEN]** Study trend failure and reversal: reclaim of structure, higher lows, failed downside continuation, upside expansion, and confirmation delay.
- **[OPEN]** Measure forward MFE/MAE, continuation-first versus rally-first, threshold timing, and outcomes after retests.
- **[OPEN]** Compare downside behaviour with bullish trends rather than assuming symmetry; split by asset, timeframe, and chronological period.

### 13.3 Sideways / range conditions

- **[PARTIAL]** Existing detector, boundary, rejection, breakout, and retest research is recorded in Sections 3–7; it does not yet constitute a complete range taxonomy.
- **[OPEN]** Quiet/narrow/compressed range: compression depth, duration, volatility contraction, boundary stability, false moves, and eventual expansion.
- **[OPEN]** Wide but orderly range: width, orderly swings, repeated boundary reactions, midpoint crossings, and mean-reversion path.
- **[OPEN]** Volatile/choppy range: whipsaws, overlapping candles, unstable boundaries, repeated crossings, and absence of durable directional progress.
- **[OPEN]** Range lifecycle: formation, maturation, expansion/contraction, boundary migration, weakening, termination, and transition to another state.
- **[OPEN]** Range geometry: width, height, slope, symmetry/asymmetry, internal swing structure, time near each boundary, and time spent in the interior.
- **[OPEN]** Range behaviour: first/repeated tests, rejection anatomy, midpoint reversion, failed breakout/breakdown, acceptance outside, retest, and post-break path.
- **[OPEN]** Distinguish a genuine range from a temporary pause within an existing trend and from a volatile/noisy market.
- **[OPEN]** Preserve the full boundary/rejection and breakout/failure studies in Sections 4–7; do not duplicate or replace their accepted definitions.

### 13.4 Choppy / high-volatility / disorderly conditions

- **[OPEN]** Define choppiness independently from quiet sideways and from orderly high-volatility trends; do not equate high ATR with choppiness.
- **[OPEN]** Measure direction changes, overlapping candle ranges, wick/body structure, directional efficiency, whipsaw frequency, and repeated failed pushes.
- **[OPEN]** Measure volatility level, volatility-of-volatility, sudden expansion/contraction, extreme candle clusters, and persistence of shocks.
- **[OPEN]** Study rapid support/resistance crossings, unstable swing structure, false signals, and time required for direction to become clear.
- **[OPEN]** Separate two-sided disorder from high-volatility directional movement; characterize both.
- **[OPEN]** Measure forward path distributions, adverse/favourable excursions, reversals, and whether movement is persistent or quickly retraced.
- **[OPEN]** Study spread/slippage only when reliable execution data becomes available; do not infer liquidity from candle volume alone.
- **[OPEN]** Evaluate whether the state is best classified as uncertain/no-trade for research purposes, without assuming a trading rule.

### 13.5 Transition, breakout, expansion, and volatility-shock conditions

- **[OPEN]** Study transitions between every major pair of states: range-to-uptrend, range-to-downtrend, trend-to-range, trend-to-opposite-trend, orderly-to-choppy, and shock-to-normalization.
- **[OPEN]** Measure transition onset, confirmation delay, duration, failed transitions, temporary flips, and label flicker.
- **[OPEN]** Distinguish breakout attempt, close outside, sustained acceptance, retest, continuation, failed breakout, and return into the prior range.
- **[OPEN]** Measure expansion magnitude, speed, duration, realized volatility change, follow-through, and post-expansion retracement.
- **[OPEN]** Study volatility shocks separately from ordinary breakouts: shock size, clustering, cross-asset spread, persistence, and normalization time.
- **[OPEN]** Measure false starts and transition reversals, including how often an apparent new phase quickly returns to the previous phase.
- **[OPEN]** Compare detection using only information available at the time against retrospective final labels; report the delay/uncertainty cost of causal classification.

### 13.7 Entry opportunity and execution research within every market phase

**[OPEN — REQUIRED FOR EVERY PHASE]** Entry execution must not be studied only as one general timeframe comparison. Once each phase has a validated causal definition and eligible event/signal cohort, study entry opportunity and execution separately within that phase. Do not assume an entry method that works in one phase transfers to another.

For each phase (bullish trend, bearish trend, quiet/compressed range, wide/orderly range, volatile/choppy range, disorderly high-volatility conditions, and each transition type), investigate:

- **[OPEN]** Define the eligible setup and the exact moment it becomes knowable. Entries must occur only after all required signal candles close; record confirmation time and earliest eligible execution time.
- **[OPEN]** Compare execution resolutions using the same underlying event cohort where possible: 1M, 3M, 5M, and 15M. Keep signal timeframe fixed when the question is execution resolution; a different signal timeframe is a separate study.
- **[OPEN]** Compare entry methods where structurally relevant: immediate/market after confirmation, pullback, limit at a predeclared level, structural retest, breakout/retest, and post-retest confirmation. Do not force irrelevant methods into every phase.
- **[OPEN]** Measure entry delay, entry price, distance from signal close and structural reference, price movement while waiting, maximum adverse/favourable movement before entry, and whether the opportunity was missed.
- **[OPEN]** Measure touch, estimated fill, partial fill, expiry, cancellation, missed entry, and no-opportunity outcomes separately. State assumptions for order priority, intrabar ordering, gaps, and limit-price touches.
- **[OPEN]** Measure post-entry adverse/favourable excursion, immediate adverse selection, continuation/pullback after entry, and whether price reaches the intended structural area before invalidation.
- **[OPEN]** Test whether entry quality changes by phase maturity, phase strength, volatility state, signal-candle anatomy, asset, direction, time of day, and higher-timeframe context, using only information available at entry.
- **[OPEN]** Include failed setups and no-fill opportunities in denominators; do not evaluate only the trades that would have filled.
- **[OPEN]** Compare phase-specific entry behaviour with a common baseline and report sample size, uncertainty, chronological stability, overlap/dependence, and sensitivity to reasonable predeclared assumptions.
- **[OPEN]** Separate descriptive price-path opportunity from simulated fills, then from fees/slippage/funding and net profitability. OHLC touch is not a verified fill; realistic cost and profitability work remains subject to the later execution/cost gate and explicit authorization.

**Phase-specific questions to answer:**
- **Uptrend:** How do immediate continuation entries compare with pullback-to-structure, higher-low retest, and breakout-retest entries? How deep and long are ordinary pullbacks before continuation or failure?
- **Downtrend:** How do immediate entries compare with countertrend-rally, lower-high retest, and breakdown-retest entries? How often do sharp short-covering rallies invalidate an apparent continuation?
- **Quiet/compressed range:** Are boundary-rejection or interior entries actually reachable? How long does price remain near a level, and how often does compression resolve before a limit entry fills?
- **Wide/orderly range:** Compare entries near upper/lower boundaries, midpoint, and after confirmed rejection; measure travel to the interior/opposite boundary and invalidation.
- **Volatile/choppy range:** Quantify whipsaw, adverse movement immediately after entry, repeated level crossings, and false confirmation; include no-trade/no-fill outcomes.
- **Disorderly/high-volatility conditions:** Measure execution delay and adverse movement during fast candles and shocks; do not infer executable fills or liquidity from OHLCV alone.
- **Transitions and breakouts:** Compare early transition attempts with entries after confirmation, acceptance outside a range, and retests; measure how much movement is missed by waiting for confirmation and how often early entries fail.

**Sequencing:** First establish and validate phase definitions and phase-specific event cohorts. Then study signal/entry opportunity and post-signal paths. Next compare execution resolutions and entry methods on comparable cohorts. Only after those descriptive gates should cost-aware execution simulation or strategy profitability be considered, with separate explicit authorization.

### 13.6 Cross-phase and multi-timeframe questions

- **[OPEN]** Build a phase-transition matrix with counts, duration distributions, and uncertainty by asset and chronological period.
- **[OPEN]** Compare phase frequencies, duration, path characteristics, and transition behaviour across all five assets.
- **[OPEN]** Measure how often 1D, 4H, 1H, and 15M classifications agree, conflict, or change at different times; do not assume a lower timeframe must follow a higher timeframe.
- **[OPEN]** Study whether BTC phase changes lead, coincide with, or lag other assets; treat this as association, not causation.
- **[OPEN]** Compare phase-specific return, range, volatility, MFE/MAE, pullback, breakout, and reversal distributions.
- **[OPEN]** Test chronological stability and predeclared subperiods; disclose small samples and multiple comparisons.
- **[OPEN]** Audit phase-label reproducibility, missing data, exact timestamp continuity, and causal availability.
- **[OPEN]** Keep diagnostic indicators (ATR, ADX, efficiency, bandwidth, etc.) as candidate measurements, not automatic definitions or filters for pure price-action Model A.

**Completion standard:** No phase is considered fully researched merely because a detector labels it. Each phase needs validated causal definitions, lifecycle and transition analysis, path/outcome descriptions, cross-asset and multi-timeframe comparisons, chronological robustness, and documented limitations. Strategy filters or entries remain unauthorized until the descriptive work is reviewed and separately approved.

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

---

## 14. Complete trade-lifecycle research — connect every stage

**Purpose:** Study the complete opportunity-to-portfolio process as one causal chain, not as isolated signal, entry, or exit studies. This section is a research specification, not authorization to run a strategy backtest.

### 14.1 Market condition and context

- **[OPEN]** Identify the market condition using validated, causal phase definitions from Section 13.
- **[OPEN]** Record phase maturity, strength, volatility, transition risk, and classification uncertainty using only information available at the decision time.
- **[OPEN]** Record 1D/4H/1H/15M agreement or conflict and distinguish context from an actual entry signal.
- **[OPEN]** Include ambiguous, mixed, and no-trade conditions rather than forcing every observation into a phase.

### 14.2 Signal formation and qualification

- **[OPEN]** Define each candidate signal precisely, including the completed candle/event, direction, structural reference, confirmation timestamp, and earliest eligible decision time.
- **[OPEN]** Measure signal frequency, clustering, overlap, invalidation, failure, and no-signal periods by asset and phase.
- **[OPEN]** Separate signal quality/path behaviour from whether an executable entry was available.
- **[OPEN]** Prevent future information, retrospective pivots, or post-signal outcomes from changing signal qualification.

### 14.3 Entry execution

- **[OPEN]** Connect signal confirmation to the earliest eligible entry decision and actual/assumed execution time.
- **[OPEN]** Compare predeclared immediate, pullback, limit, structural retest, breakout/retest, and confirmation methods where relevant.
- **[OPEN]** Record entry price, delay, distance from signal/structure, movement while waiting, no-fill, expiry, missed opportunity, and partial-fill assumptions.
- **[OPEN]** Preserve the same signal cohort when comparing execution resolutions or entry methods; report exclusions and denominators.
- **[OPEN]** Distinguish observed OHLC touches from simulated fills and verified fills.

### 14.4 Position management after entry

- **[OPEN]** Define the initial position size, risk budget, leverage/exposure cap, and initial invalidation before entry.
- **[OPEN]** Study whether stop levels, trailing levels, targets, or position size are allowed to change after entry, and specify exactly which information can trigger each change.
- **[OPEN]** Research partial profit-taking, adding/reducing exposure, break-even movement, trailing, time-based management, and no-progress handling as separate predeclared policies.
- **[OPEN]** Measure open risk, remaining risk, realized/unrealized P&L, exposure, holding time, and funding through the full position lifecycle.
- **[OPEN]** Include adverse paths and management decisions, not only winning-trade examples.

### 14.5 Exit execution

- **[OPEN]** Connect each exit trigger to its first causally eligible order/action and the resulting assumed execution price.
- **[OPEN]** Distinguish stop, target, trailing, structural invalidation, time exit, regime-change exit, emergency exit, and manual/operational exit reasons.
- **[OPEN]** Define gap-through, intrabar stop/target ordering, partial fills, expiry, and slippage assumptions; report ambiguous OHLC sequences conservatively.
- **[OPEN]** Measure gross and net exit effects separately, including fees, slippage, and funding where validated.

### 14.6 Portfolio outcome and feedback

- **[OPEN]** Aggregate simultaneous positions across assets using a common timestamped equity/exposure ledger.
- **[OPEN]** Measure net returns, drawdown, tail losses, turnover, capital usage, concentration, correlated exposure, and simultaneous adverse moves.
- **[OPEN]** Include rejected signals, missed entries, no-fills, open positions, forced exits, and overlapping positions in the correct denominators and accounting.
- **[OPEN]** Evaluate daily/weekly loss limits, portfolio exposure limits, drawdown controls, and operational stop conditions as separate policies.
- **[OPEN]** Check that portfolio constraints do not use future information and that per-asset results reconcile to portfolio totals.

### 14.7 End-to-end lifecycle validation

- **[OPEN]** Maintain an auditable event chain: market snapshot → phase label → signal → entry decision/order → fills → management events → exit decision/order → fills → funding/fees → portfolio ledger.
- **[OPEN]** Require exact timestamps, stable identifiers, reproducible event ordering, and reconciliation of every position from opening to final closure.
- **[OPEN]** Test edge cases: missing candles, exchange/data outages, duplicate events, simultaneous stop/target touches, partial fills, rejected orders, gaps, and position carry across funding timestamps.
- **[OPEN]** Compare stage-level diagnostics with end-to-end results so that a promising signal or entry is not mistaken for a profitable complete system.
- **[OPEN]** Report results by asset, direction, market phase/maturity, entry method, exit policy, and chronological period, with dependence and uncertainty limitations.

**Lifecycle rule:** A complete trade is not evaluated from signal price alone. Its causal sequence, executable entry, position changes, exit execution, costs, funding, and portfolio interactions must all reconcile. No stage may borrow information from a later stage.

## 15. Dedicated exit and position-management research

**Purpose:** Understand how trades should be invalidated, managed, and closed under different market conditions. This workstream is downstream of validated signal and entry research. Its presence on the checklist does not authorize exit sweeps, strategy backtests, or parameter optimization.

### 15.1 Initial stop-loss and invalidation research

- **[OPEN]** Compare structural invalidation (swing/level failure), range-boundary invalidation, fixed-percentage, volatility-normalized, and other explicitly justified stop families.
- **[OPEN]** Measure stop distance, initial risk per unit, stop placement relative to market structure, and how often price reaches the stop before a favourable objective.
- **[OPEN]** Separate a true thesis invalidation from a risk-control stop; record whether a stop is structural, time-based, volatility-based, or operational.
- **[OPEN]** Study stop behaviour by phase, phase maturity, asset, direction, entry method, and volatility state.
- **[OPEN]** Avoid retrospective swing points and levels that were not confirmed and available at entry.

### 15.2 Take-profit and target research

- **[OPEN]** Compare economically motivated target families: fixed R-multiples, prior structure, range midpoint/opposite boundary, measured move, and trend-extension levels.
- **[OPEN]** Measure target reach probability, time-to-target, favourable excursion given up, target-before-stop ordering, and unresolved outcomes.
- **[OPEN]** Distinguish target touch from executable target fill; define limit-order queue/partial-fill assumptions where fills are simulated.
- **[OPEN]** Compare fixed targets with policies that allow a runner, without selecting winners from broad uncorrected grids.

### 15.3 Trailing-stop research

- **[OPEN]** Study fixed-distance, volatility-normalized, confirmed-swing/structure-based, and phase-aware trailing families.
- **[OPEN]** Record activation condition/time, initial and updated levels, update frequency, stop distance, and whether the stop ever becomes active.
- **[OPEN]** Measure profit retained versus unrealized MFE surrendered, stop-out timing, re-entry/whipsaw exposure, and gap-through behaviour.
- **[OPEN]** Do not infer trailing-stop activation or update history from summary trade exports when the underlying event telemetry is absent.

### 15.4 Partial exits and position scaling

- **[OPEN]** Compare full exit with predeclared partial-close schedules and runner policies.
- **[OPEN]** Measure realized profit, remaining size/risk, average exit price, later runner contribution, fees/turnover, and opportunity cost.
- **[OPEN]** Study scale-in, scale-out, and add/reduce policies separately; specify whether total initial risk can increase and enforce an explicit cap.
- **[OPEN]** Avoid treating multiple partial fills from one position as independent trades.

### 15.5 Time, progress, and thesis-based exits

- **[OPEN]** Study maximum holding time, no-progress/stalled-trade exits, time-to-invalidation, and time-to-target.
- **[OPEN]** Define measurable thesis invalidation: loss of supporting structure, failed continuation, failed retest, return into a failed breakout range, or other predeclared event.
- **[OPEN]** Compare exit at first causal warning versus confirmed state change; quantify both avoided adverse movement and prematurely abandoned continuation.
- **[OPEN]** Account for funding timestamps and holding-period effects when relevant.

### 15.6 Phase-specific exit questions

- **[OPEN] Bullish trend:** compare confirmed higher-low/structure trailing, volatility trailing, prior-high/extension targets, and exits after weakening or failed continuation.
- **[OPEN] Bearish trend:** compare mirrored lower-high/structure trailing and downside targets, while testing rather than assuming symmetry.
- **[OPEN] Quiet/compressed range:** examine midpoint and opposite-boundary targets, boundary-failure invalidation, and exits when compression resolves.
- **[OPEN] Wide/orderly range:** examine boundary-to-interior/opposite-boundary objectives, early reversal warnings, and time spent without progress.
- **[OPEN] Volatile/choppy range:** measure rapid stop/target crossings, whipsaw, shorter-horizon invalidation, and whether no-trade is preferable to tighter exits.
- **[OPEN] Breakout/expansion:** compare continuation targets and trailing with exits on failed acceptance, failed retest, or return inside the prior range.
- **[OPEN] Transition/shock/disorderly conditions:** study gap and fast-market risk, stale levels, delayed exits, conservative stop assumptions, and explicit emergency risk controls.

### 15.7 Exit execution, costs, and measurement

- **[OPEN]** Verify the applicable fee schedule and funding inputs before claiming realistic net exit results.
- **[OPEN]** Estimate exit slippage by asset, volatility, order type, and time of day where data supports it; OHLCV alone cannot establish order-book liquidity or exact fills.
- **[OPEN]** Model market/stop-market versus limit/stop-limit assumptions separately, including gaps, partial fills, unfilled orders, and order expiry.
- **[OPEN]** Specify intrabar ordering when stop and target are both touched in one candle; use finer data where available and conservative ambiguity rules otherwise.
- **[OPEN]** Report gross versus net P&L, fees, slippage, funding, holding time, turnover, MFE captured, MAE endured, drawdown, and tail outcomes.
- **[OPEN]** Use non-positive MAE convention consistently and reconcile trade-level exits with the portfolio ledger.

### 15.8 Exit study design and acceptance gates

- **[OPEN]** Begin with descriptive path/threshold and time-to-event analysis before comparing complete exit policies.
- **[OPEN]** Freeze the entry cohort and entry assumptions before comparing exits; do not let each exit arm select a different set of favourable entries.
- **[OPEN]** Pre-register the exit hypothesis, baseline, variants, risk constraints, horizons, costs, ambiguity rules, and falsification criteria.
- **[OPEN]** Account for overlapping trades, multiple comparisons, chronological stability, and asset/regime heterogeneity.
- **[OPEN]** Separate descriptive stop/target reachability, assumed fill simulation, and net strategy profitability into distinct evidence levels.
- **[OPEN]** Require code review, unit tests, event-level telemetry, exact event-count/continuity checks, and reproducible reports before accepting results.
- **[LATER — NOT AUTHORIZED]** Exit-family comparisons and strategy-level exit experiments may begin only after the relevant signal/entry research gates are reviewed and the user explicitly authorizes the experiment.
- **[LATER — NOT AUTHORIZED]** Parameter tuning, broad exit grids, and final OOS selection remain prohibited until the full hypothesis, development/validation/OOS, and realistic-cost protocol is approved.

**Existing-results safeguard:** The historical 66-experiment exit batch and later telemetry/local exit reports are prior evidence to audit and interpret. They must not be overwritten, blindly resumed, or repeated. A negative batch is not a reason to search a larger parameter grid; first identify what the telemetry and cost accounting can and cannot establish.

