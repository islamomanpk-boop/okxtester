# Phase 3 Sideways / Range — Knowledge Synthesis V1

**Review date:** 2026-11-25  
**Status:** Evidence synthesis of archived Phase 3 work; core descriptive scope complete.  
**Important:** This is a research interpretation, not a strategy recommendation or profitability claim.

## Executive conclusion

Phase 3 produced a useful descriptive map of how price interacted with reconstructed sideways-range boundaries, what happened after selected rejection events, and how breakout outcomes varied with event context. The strongest defensible lessons concern event mechanics and measurement:

- A range-boundary interaction is not one event type. Approach, touch, wick penetration, close outside, and re-entry are distinct observations and should not be collapsed into a generic bounce or breakout label.
- After selected rejection events, retests were common and often quick. The order of early retest versus inward separation was heterogeneous; there was no single universal path.
- Early-path sequence classes showed different subsequent price paths in this historical sample. These are observational associations, not causal or executable trading edges.
- Breakout prior-test counts and forward paths were studied descriptively, but the archive does not establish a universal monotonic rule that more tests always strengthen or weaken a breakout.
- The V6 matched-control branch did not produce a sufficiently comparable cohort. V7–V10.11 diagnostics confirmed serious covariate and joint-support limitations. The correct decision was to stop and not compare future outcomes using those pairs.

Phase 3 gives us market-structure knowledge and methodological warnings. It does not tell us to buy or sell a boundary, prove a breakout edge, establish causal effects, or validate a strategy.

## 1. Research scope

The work used BTC, ETH, SOL, DOGE, and AVAX. Research streams:

1. Historical sideways-boundary reconstruction and candle-level interaction / penetration taxonomy.
2. Rejection episode and retest anatomy at 15m, 1h, 4h, and 24h horizons.
3. Early-path sequence and conditional follow-through.
4. Calendar moving-block bootstrap contrasts.
5. Per-asset and leave-one-asset-out robustness.
6. Breakout prior-test-count classification and descriptive forward outcomes.
7. Pre-event matched-control development, balance, feasibility, distributional-overlap, and joint-common-support audits.
8. Source-data quality and cross-asset timestamp alignment.

Broad and strict cohorts overlap or are nested. They are not independent replications and must not be pooled as if they were separate samples.

## 2. Boundary interaction: what price did at the range edge

### Measurement

The taxonomy archive contains **153,540 candle-level observations** across five assets, two overlapping context definitions (BROAD_P40 and STRICT_P25), upper/lower boundaries, and 5%, 10%, and 15% approach bands.

It distinguishes:
- NO_APPROACH: no qualifying approach to the boundary band.
- APPROACH_ONLY: price entered the approach region but did not meet a stronger interaction class.
- BOUNDARY_TOUCH: exact parsed-price contact under the study's strict equality rule.
- WICK_PENETRATION: intrabar high/low crossed the boundary while the close did not establish a close outside.
- CLOSE_OUTSIDE: candle close was outside the boundary.
- REENTRY_INSIDE: price returned inside after an outside condition under the frozen event rule.

These are candle-level observations, not independent trade opportunities or proof of market intent.

### Findings and lessons

- Boundary interaction is sparse relative to all candles in the snapshot windows. Most observations are NO_APPROACH; wider approach bands naturally classify more candles as APPROACH_ONLY.
- Exact boundary touches are rare under exact-price equality. A near-touch is not an exact touch.
- Wick penetration, close outside, and re-entry are distinct. A wick through a boundary is not equivalent to a close beyond it.
- In the broad definition, positive penetration rates by asset/side were approximately 4.5%–6.4% of candle observations in the relevant windows. Conditional positive penetration-depth distributions had long tails and differed across assets/sides. This argues against assuming a fixed, asset-invariant boundary buffer from one average.
- Strict and broad cohorts overlap, so comparisons are sensitivity views, not independent confirmations.

The taxonomy excludes the final truncated 4-hour snapshot interval, suppresses the first observed 15-minute candle at or after snapshot availability, requires strict continuous 15-minute cadence, and does not bridge gaps. Volume was retained for source validation only; no volume-based inference was made. Consecutive candle rows are dependent.

**Practical lesson:** Future range/breakout research must preserve approach, touch, wick penetration, close beyond, and re-entry as separate labels. Normalize distances to range width or volatility and test asset differences rather than assuming one universal buffer.

## 3. Rejection episode and retest anatomy

### Cohort and horizons

The episode/retest study began with 2,452 source-ledger rows and retained **1,992 eligible rejection events**: 1,154 broad and 838 strict. It generated 7,968 event-horizon rows at 15m, 1h, 4h, and 24h.

The study is a selected-event descriptive cohort. OHLC cannot establish intrabar order or executable fills. Broad/strict are nested; overlapping events are dependent; incomplete horizons are censored, never gap-bridged.

### Broad-cohort 15-minute observations

For 1,154 broad events:
- First boundary retest was observed in 621 (**53.8%**).
- First inward separation was observed in 410 (**35.5%**).
- First penetration was observed in 103 (**8.9%**).
- Among the 621 observed retests, median time to first retest was 5 minutes.
- Among the 410 observed inward separations, median time was 2 minutes.
- Among the 103 observed penetrations, median time was 6 minutes.
- A retest-close-inward condition occurred in 616 of 621 observed-retest cases (**99.2%**) under the study's specific event definition. This conditional statistic is not a 99.2% probability of a profitable bounce or winning trade.

These are frequencies for a selected event cohort, not unconditional market probabilities.

**Lesson:** Rejection does not necessarily mean immediate one-way movement away from the boundary. Retests are common; a future event model must distinguish confirmation, retest, separation, penetration, and censoring. A descriptive intrabar extreme cannot be assumed to be an executable fill.

## 4. Early-path sequence and follow-through

The early-path study classified the first 15 minutes after the event and measured later paths from the post-landmark point. For broad events at the 1-hour horizon (1,154 events):

| Early sequence | Events | Share |
|---|---:|---:|
| RETEST_FIRST | 584 | 50.6% |
| SEPARATION_FIRST | 350 | 30.3% |
| NEITHER_WITHIN_15M | 219 | 19.0% |
| SAME_BAR_AMBIGUOUS | 1 | 0.1% |

The market path was heterogeneous: about half retested first, around three in ten separated first, and about one in five did neither within the classification window. Same-bar ambiguity was retained rather than inventing an intrabar order from OHLC.

### Historical broad-cohort 1h contrast

The calendar moving-block bootstrap compared SEPARATION_FIRST (n=350) with RETEST_FIRST (n=584). Across 3-, 7-, and 14-day blocks:
- Direction-adjusted final close from midpoint difference: about **+0.164 range-width units**, with 95% intervals approximately **+0.138 to +0.191**.
- Maximum inward-excursion difference: about **+0.170 width units**, with intervals approximately **+0.152 to +0.189**.
- Maximum outward-penetration difference: about **−0.053 width units**, with intervals approximately **−0.074 to −0.032**.

Interpretation: in this selected historical cohort, events classified as separating first subsequently showed more inward movement and less outward penetration on these measures than retest-first events. This does not show that waiting for separation is profitable. Classification uses the first 15 minutes; subsequent paths are observational; no executable entry/exit, costs, slippage, or causal adjustment was established.

### Robustness

The per-asset/leave-one-asset-out analysis used 71 broad and 45 strict pairs. Per-asset counts were small (broad 12–16; strict 6–12). The archived summary reports that the main broad 1h inward-excursion association was not driven by a single asset, while some longer-horizon and close/outward results weakened when assets were omitted. Per-asset intervals were often wide.

**Practical lesson:** Early sequence is a useful descriptive dimension and candidate explanatory feature, not a ready-made entry rule. It needs independent chronological validation and realistic execution modelling before any strategy use.

## 5. Breakout prior-test counts and forward outcomes

Separate studies classified breakout events by prior rejection/test counts and measured forward paths at 15m, 1h, 4h, and 12h, stratified by asset, direction, context definition, boundary-zone width, and pre-breakout group.

The archived outputs include directional close return, maximum favourable/adverse excursion, time to extremes, positive-return share, and boundary-failure share. The results are highly stratified, with variable sample sizes across cells.

What we can safely conclude:
- Prior-test count was recorded as event context rather than assumed to be a universal boundary-strength score.
- A single pooled monotonic rule such as “more tests always weaken the boundary” or “more tests always strengthen the breakout” is **not established** by the reviewed archive.
- Small cells, exclusions, and differing asset/side/horizon strata require denominators and exclusions to be read alongside each estimate.
- These are descriptive event analyses; they do not provide a valid matched counterfactual proving what would have happened without the breakout context.

**Practical lesson:** Prior-test count may be useful context, but must not become a deterministic trading rule without adequate sample sizes, chronological replication, and stability across assets, sides, and periods.

## 6. Why matched controls were rejected

The matching project aimed to compare rejection/breakout events with similar non-event controls. Matching versions V1–V6 were followed by outcome-blind diagnostics V7–V10.11.

Key evidence:
- Earlier versions had residual imbalance or too few pairs.
- V6 achieved maximum feasible pair cardinality for its candidate graph: broad 21 / 36 / 48 / 58 pairs and strict 11 / 21 / 29 / 34 pairs across four target calipers. Maximum feasible count does not mean adequate comparability.
- Correlation/redundancy diagnostics did not justify deleting difficult covariates solely to improve balance.
- The balance-retention frontier found no configuration that balanced all covariates. Every represented asset-direction stratum retained at least one covariate with absolute SMD above 0.10.
- V10.9 distributional overlap remained weak: broad median KS 0.208 and normalized Wasserstein 0.314 pooled SD; strict 0.225 and 0.355. Signed close-to-boundary distance was especially separated: median normalized Wasserstein 1.49 broad / 1.43 strict, with median central-range overlap 27.1% / 25.2%.
- V10.10 central-90% joint support retained only 2 broad pairs across the four calipers and zero strict pairs; median stratum pair retention was zero.
- V10.11 tested central 80%, 90%, 95%, and 98% ranges without changing frozen V6 pairs. Central 80% retained no pairs. Central 90% retained 2 broad and 0 strict pairs (reproducing V10.10). Even central 98% retained only 9 / 14 / 14 / 16 broad pairs and 3 / 6 / 9 / 11 strict pairs across increasing calipers.
- At central 98%, pooled eligible-event retention was 29.14% broad separation, 27.23% broad retest, 18.23% strict separation, and 20.36% strict retest.

**Decision: close the V6 matched-control branch for this cohort.** Do not widen support percentiles further, relax constraints to manufacture a cohort, rematch the same cohort until it looks balanced, or compare future outcomes using these pairs.

This is a genuine negative research finding: event and non-event populations differed materially before the event, especially in signed distance to the boundary. Marginal overlap does not imply adequate joint overlap. A counterfactual cannot be manufactured from a sparse, poorly overlapping candidate population.

This does not prove no future causal design could ever work. It means this cohort/design is unsuitable. A future attempt would require a separately justified population, estimand, and protocol—not another tuning round to rescue this cohort.

## 7. What we know, what is suggested, and what is not proven

### Established as descriptive facts within these definitions/sample
- Five-asset source data passed recorded quality checks and had near-complete timestamp alignment, with only two trailing union timestamps outside the common five-asset intersection.
- The boundary taxonomy distinguishes multiple interaction types and contains 153,540 observations under explicit snapshot/cadence policies.
- The selected rejection ledger contains 1,992 eligible events (1,154 broad; 838 strict), studied across four horizons.
- Early paths were heterogeneous; broad 1h sequence counts are reported above.
- The V6 matched-control cohort failed the balance/common-support acceptance requirements and was correctly rejected for outcome comparison.

### Suggested, not proven as general market laws
- Early separation may be associated with more favourable subsequent inward-path metrics than retest-first behaviour in this selected historical cohort.
- Prior tests, boundary side, asset, and range geometry may help explain breakout-path variation.
- Penetration depth and event timing differ across assets and contexts.

### Not established
- Range boundaries reliably cause reversals.
- Wick penetration, close outside, re-entry, or retest alone predicts profitable outcomes.
- Early separation is profitable after fees, slippage, funding, latency, and realistic fills.
- Prior-test count has a universal monotonic effect.
- The observed associations are causal.
- Any Phase 3 strategy, parameter set, or live deployment is validated.

## 8. Limitations to carry forward

1. **Selected event cohorts:** Results do not describe every market minute.
2. **Dependence:** Candle observations, overlapping events, repeated asset-time observations, and nested cohorts are not independent.
3. **OHLC ambiguity:** Bars do not reveal intrabar high/low order or executable fills.
4. **Censoring and gaps:** Incomplete horizons are censored; gaps are not bridged; snapshot-tail policies matter.
5. **Multiple comparisons:** Many assets, directions, horizons, groups, and metrics were examined. Bootstrap intervals do not erase selection bias or multiple-testing risk.
6. **Limited history:** Roughly 13 months may not represent multiple independent market cycles.
7. **No credible counterfactual:** Matching failed; observational contrasts remain confounded.
8. **No execution layer:** Phase 3 did not establish complete transaction-cost, slippage, funding, latency, order-book, or fill simulation.

## 9. Practical implications for the future system

These are research-design lessons, not activated trading rules:
- Keep regime classification separate from event classification and execution.
- Preserve approach, touch, wick penetration, close outside, re-entry, retest, and inward separation as separate labels.
- Record when each label becomes knowable. A completed 15m candle cannot be acted on before its close.
- Treat range-width-normalized distances as useful descriptive units, but validate asset-specific distributions before choosing fixed thresholds.
- Retain early sequence as a research variable; validate it on chronological holdout data before strategy use.
- Treat prior-test count as context, not a deterministic rule.
- Report sample sizes and dependence; repeated candles are not independent evidence.
- Require an explicit counterfactual design before causal claims. If common support is absent, report it and stop rather than force matching.
- Preserve negative findings and rejected methods.

## 10. Open questions — only reopen with a decision-based reason

1. **Independent chronological replication:** Do early-sequence associations persist in a later untouched period or genuinely new sample?
2. **Event-definition sensitivity:** Do patterns survive alternative predeclared range definitions without selecting the best-looking one?
3. **Execution feasibility:** If a candidate rule is proposed, can it survive realistic timestamps, fees, slippage, funding, and fill assumptions?
4. **Cross-regime interaction:** Does behaviour differ when a range occurs inside a larger uptrend/downtrend, using independently defined regime labels available at the time?
5. **New counterfactual design:** Is there a new defensible target population and identification strategy with genuine common support?

None is automatically required. Every proposed follow-up must first satisfy Research Governance Rules V1 and explain what decision its answer could change.

## 11. Final Phase 3 decision

**Core descriptive Phase 3 research is complete. The V6 matched-control branch is rejected for outcome comparison.**

The most useful Phase 3 output is a more precise description of sideways-market event mechanics, evidence that early paths are heterogeneous, and a clear warning that observational comparisons without adequate common support can mislead. It is not a ready-to-trade setup.

Preserve the archive. Do not optimize a Phase 3 strategy from these results. Reopen only for a specific unanswered question, a pre-registered protocol, decision criteria, and a clear practical reason.

## 12. Source archive index

- Boundary taxonomy: reports/sideways_boundary_interaction_taxonomy_v1/
- Breakout prior-test counts: reports/breakout_prior_test_count_v1/
- Breakout forward outcomes: reports/breakout_forward_outcome_v1/
- Episode/retest anatomy: reports/sideways_phase3_research_archive_v1/episode_retest_anatomy_v1/
- Early-path follow-through: reports/sideways_phase3_research_archive_v1/early_path_followthrough_v1/
- Calendar moving-block bootstrap: reports/sideways_phase3_research_archive_v1/sequence_block_bootstrap_v1/
- Asset robustness: reports/sideways_phase3_research_archive_v1/asset_robustness_v1/
- Matched-control diagnostics V6–V10.11: reports/sideways_phase3_research_archive_v1/
- Formal completion decision: reports/sideways_phase3_research_archive_v1/PHASE3_COMPLETION_DECISION_V1.md
- Mandatory project rules: docs/RESEARCH_GOVERNANCE_RULES_V1.md
