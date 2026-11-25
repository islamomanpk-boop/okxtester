# Phase 3 Boundary Lifecycle Closure — Frozen Research Protocol V1

**Date:** 2026-11-25  
**Project:** OKX Price Action V1 — Phase 3 Sideways / Range  
**Status:** Protocol frozen before implementation; no new outcome calculations or strategy simulation authorized by this document alone.  
**Controlling roadmap:** `docs/research_checkpoints/2026-11-25_phase3_execution_and_backtest_roadmap_v1.md`  
**Gate:** Gate 1 — complete descriptive lifecycle.

## 1. Purpose and research questions

The accepted Phase 3 archive already measures boundary interactions, selected rejection anatomy and first retest, rejection early-path sequence, breakout prior-test history, and breakout forward outcomes. It does not yet provide a complete, de-clustered lifecycle record for repeated rejection retests and failed-breakout/reclaim behaviour.

This protocol closes only those descriptive lifecycle gaps. It does not define executable entries, choose parameters, rank signal quality, or test profitability.

Two independent modules are specified and must remain separate:

- **Module A — Rejection lifecycle:** after a confirmed 15-minute rejection at a frozen range boundary, what are the subsequent retest episodes, inward continuation, boundary penetrations, close-through failures, repeated close-crosses, and signal-candle anatomy relationships?
- **Module B — Breakout failure lifecycle:** after a confirmed 15-minute breakout, how often and when does price continue outside, retest the broken boundary, close back inside, confirm a 15-minute return inside, reclaim the breakout side, or extend in the reversal direction?

Exploratory hypotheses only:
- H-A1: a first retest, repeated retests, and a close-through failure have distinguishable subsequent path distributions.
- H-A2: rejection-candle anatomy may be descriptively associated with subsequent path, but no causal or predictive interpretation is assumed.
- H-B1: breakout continuation, outside retest/hold, 1-minute return-inside, and completed-15-minute close-back-inside are distinct lifecycle states with different subsequent paths.
- H-B2: failed upside and failed downside breakouts may be asymmetric; do not pool them as if symmetric.

Null/alternative formal significance tests are not specified. This is a descriptive, event-level study with overlapping windows and dependent observations.

## 2. Immutable source population and accepted inputs

### Module A — Rejection

Primary source event ledger:
- `reports/sideways_boundary_events_historical_v1/boundary_tests_historical_v1.csv`

Accepted frozen boundary snapshots:
- `reports/sideways_detector_original_v1/{ASSET}_features_original_v1.csv`

Existing accepted event/anatomy source:
- `reports/sideways_phase3_research_archive_v1/episode_retest_anatomy_v1/event_anatomy_v1.csv`
- `reports/sideways_phase3_research_archive_v1/episode_retest_anatomy_v1/run_metadata_v1.json`

Minute data:
- `data/market_1m/{ASSET}_USDT_USDT_1m.csv`

Use only source-ledger events with non-null `first_strong_rejection_ts_ms` that pass the existing exact snapshot join and complete confirmation-minute requirements. Revalidate the accepted counts from the committed ledger before implementation: broad 1,154; strict 838; total eligible across the nested cohorts 1,992. Strict is contained within broad; report it separately and never add strict to broad as an independent population.

The event identity must preserve the accepted key and existing `event_id`; do not regenerate event IDs or recompute boundaries. Use the existing frozen 10% boundary band and 20% inward-separation distance as the primary geometry. Any 5%/15% band sensitivity must be labelled secondary and must not replace the primary result.

### Module B — Breakout

Primary source population:
- `reports/breakout_prior_test_count_v1/breakout_prior_test_classifications_v1.csv`, filtered to the predeclared primary `zone_pct_of_channel = 10.0`.
- `reports/breakout_prior_test_count_v1/breakout_prior_test_links_v1.csv` for prior-test links and status.
- `reports/breakout_forward_outcome_v1/run_metadata.json` and `breakout_forward_outcomes_v1.csv` for the accepted breakout event identity, original reproduction and prior forward-path context.
- The original recovered source is identified in the metadata by blob SHA `95d2975947c449f3813d80ee7b12008db14f071f`; preserve it unchanged.

Use only the five accepted assets, BROAD_P40 / STRICT_P25, UPPER / LOWER, and the 10% primary zone for the primary analysis. Report strict and broad separately. The 5% and 15% zone variants are not to be mixed into the primary sample. Revalidate the primary event population and joins against the archived source before implementation.

## 3. Time-zero, availability, and no-lookahead rules

### Module A — Rejection

- The source `first_strong_rejection_ts_ms` is the OPEN timestamp of the 15-minute rejection candle.
- Confirmation/availability is exactly `first_strong_rejection_ts_ms + 900000`.
- The first eligible 1-minute bar opens exactly at this confirmation timestamp.
- Do not include any part of the 15-minute rejection candle in post-confirmation path metrics.
- Use the frozen upper/lower values from the exact feature snapshot already linked by the accepted event ledger. Never recalculate or move boundaries with future data.

### Module B — Breakout

- Preserve the original breakout study's close-labelled 15-minute `signal_time` convention.
- The first eligible 1-minute post-signal bar opens at `signal_time`; it is the first candle after the completed 15-minute signal interval under the accepted timestamp convention.
- Reproduce this mapping against the original source and prior-test classifications before implementation. If a signal timestamp does not map exactly, exclude it with a reason; do not shift to a nearby candle.
- The 15-minute return-inside confirmation must use a fully completed 15-minute candle whose close is available at its close timestamp. Do not treat an intrabar wick or 1-minute close as a completed 15-minute failure confirmation.
- All higher-timeframe classifications and boundary values must be available by the signal timestamp.

For both modules:
- Use UTC and integer millisecond timestamps internally.
- No forward-fill, interpolation, gap bridging, synthetic candles, or inferred intrabar ordering.
- A 1-minute OHLC bar can show that multiple price levels were crossed during the minute, but cannot establish their order. Mark same-bar ordering as ambiguous.
- Every output event must carry source event identity, source row linkage, asset, regime definition, boundary direction, frozen upper/lower/width, source signal timestamp, and availability timestamp.

## 4. Module A — Rejection lifecycle measurement

### 4.1 Observation window

Start at rejection confirmation. Observe up to 24 hours using exact consecutive 1-minute bars. The 15-minute, 1-hour, 4-hour and 24-hour cut points must be reported to align with the accepted anatomy archive. A horizon is complete only when every required minute exists; otherwise mark it censored with an explicit reason.

### 4.2 Retest episode state machine

Use the accepted geometry:
- (W = U-L), finite and positive.
- Upper-boundary rejection: retest band begins at (U-0.10W); inward separation is a 1-minute close at or below (U-0.20W).
- Lower-boundary rejection: retest band begins at (L+0.10W); inward separation is a 1-minute close at or above (L+0.20W).

A retest episode begins at the first post-confirmation 1-minute bar whose relevant extreme reaches the 10% band. Consecutive bars that continue to intersect the band belong to the same episode; they are not separate tests.

Record approach depth using the most boundary-ward extreme within the episode: for upper rejection, signed distance is `(U - episode_max_high) / W`; for lower rejection, `(episode_min_low - L) / W`. Negative values indicate wick penetration beyond the frozen boundary. Separately record penetration magnitude as `max(0, (episode_max_high-U)/W)` for upper and `max(0, (L-episode_min_low)/W)` for lower.

An episode is considered resolved only when one of these observable states occurs:
1. **INWARD_SEPARATION:** a completed 1-minute close reaches the existing 20% inward-separation line;
2. **CLOSE_THROUGH_BOUNDARY:** a completed 1-minute close is strictly outside the frozen boundary;
3. **HORIZON_CENSORED:** the 24-hour window ends or becomes incomplete before either resolution.

A later retest episode may start only after a prior episode has resolved by inward separation and price subsequently returns to the 10% band. A close-through event ends the current rejection episode as a boundary failure; any later reclaim is recorded as a separate recovery state, not silently counted as another successful rejection.

If a single 1-minute candle's OHLC satisfies both retest and inward-separation conditions, record SAME_BAR_AMBIGUOUS. Do not infer which happened first. If it both reaches the retest band and closes outside the boundary, record both conditions and resolve as CLOSE_THROUGH_BOUNDARY with intrabar ordering marked ambiguous.

### 4.3 Required event-level measurements

For every rejection event and every retest episode, retain:
- episode index and stable derived episode ID linked to the immutable source event ID;
- start, resolution and censor timestamps; elapsed minutes;
- full OHLC of the start, deepest-penetration, and resolution candles;
- maximum approach/retest depth relative to the frozen boundary, in raw price and as a fraction of (W);
- maximum wick penetration beyond the frozen boundary, in raw price and as a fraction of (W);
- whether any close-through occurred, first close-through timestamp, and first later close back inside (reclaim);
- time from confirmation to first inward separation, first retest, first close-through, and first reclaim;
- count of distinct retest episodes, not count of candles touching the band;
- close-to-close transitions across the frozen boundary, counted separately as inside-to-outside and outside-to-inside;
- maximum inward and outward excursion, and close location at 15m, 1h, 4h and 24h;
- complete/censored bar counts and every exclusion/censoring reason.

Use close-to-close boundary transitions for repeated-cross counts. Do not count wicks as close-crosses. Do not infer multiple crosses within a single candle.

### 4.4 Signal-candle anatomy

Join the existing accepted `event_anatomy_v1.csv` by immutable `event_id`. Reuse its unrounded values for rejection range, body, upper/lower wick, body/range ratio, wick/range ratios, close location, channel-width-normalized components, and zero-range flag. Do not recompute or alter those accepted measures.

Report continuous descriptive summaries and predeclared asset / upper-lower / strict-broad / test-rank / UTC-month breakdowns. Any binned anatomy view must be explicitly exploratory and cannot select a trading threshold.

## 5. Module B — Breakout / failed-breakout lifecycle measurement

### 5.1 Time window and frozen boundary

Start at the first eligible 1-minute bar opening at the accepted 15-minute `signal_time`. Measure the existing 15m, 1h, 4h and 12h horizons. Do not extend the primary horizon or alter the original breakout event set.

Use the exact frozen boundary and channel width attached to the accepted prior-test classification. Preserve the original upper/lower breakout direction. Do not infer a breakout from the 1-minute path if the original 15-minute event was absent.

### 5.2 Distinct lifecycle states

Record the following first-passage events independently; more than one may occur in the same 1-minute bar, in which case ordering is ambiguous:

1. **OUTSIDE_CONTINUATION:** closes remain beyond the broken boundary in the breakout direction.
2. **OUTSIDE_RETEST:** first 1-minute bar whose range reaches the 10% band around the broken boundary from the outside. For UPPER, the bar low reaches or falls below (U+0.10W); for LOWER, the bar high reaches or exceeds (L-0.10W). Record whether the bar closes outside or back inside.
3. **ONE_MINUTE_RETURN_INSIDE:** first completed 1-minute close at or inside the broken boundary. UPPER: close (le U); LOWER: close (ge L). This is a descriptive first passage, not yet a 15-minute confirmed failed-breakout signal.
4. **FIFTEEN_MINUTE_RETURN_INSIDE_CONFIRMATION:** first completed 15-minute close at or inside the boundary after the breakout. Build subsequent 15-minute bars only from exactly 15 consecutive 1-minute candles aligned to UTC quarter-hour boundaries; require all 15 bars and valid OHLC. The close timestamp is the 15-minute bar open timestamp plus 900,000 ms and is the confirmation/availability timestamp for the descriptive failed-breakout state. Do not use a partial 15-minute bar.
5. **BREAKOUT_SIDE_RECLAIM:** after a 15-minute return-inside confirmation, first subsequent completed 15-minute close back beyond the original boundary in the breakout direction. Record its availability timestamp.
6. **INSIDE_RETEST_AFTER_FAILURE:** after the 15-minute return-inside confirmation, first 1-minute bar whose range revisits the 10% band from inside. Record whether the completed 15-minute close remains inside or reclaims the breakout side; same-bar ordering remains ambiguous.
7. **REVERSAL_DIRECTION_PATH:** after the 15-minute return-inside confirmation, measure the adverse-to-breakout / reversal-direction excursion and time to its extremes over the remaining original horizon. This is a descriptive path, not a trade return.

For UPPER breakouts, reversal direction is downward; for LOWER breakouts, reversal direction is upward. Do not assume symmetry.

### 5.3 Required event-level measurements

Retain:
- stable breakout event identity and source links to original event, prior-test classification and prior-test links;
- first outside retest timestamp, elapsed minutes, OHLC, depth relative to (W), and close-outside / close-inside status;
- first 1-minute return-inside timestamp and close;
- first completed 15-minute return-inside confirmation timestamp and close;
- first breakout-side reclaim timestamp after failure confirmation;
- first inside retest after failure confirmation and its depth / close status;
- continuation excursion, reversal-direction excursion, adverse excursion, time-to-extreme and final close at each original horizon;
- whether each horizon is complete or censored;
- every same-bar ambiguity and every missing/gap exclusion;
- asset, strict/broad definition, UPPER/LOWER, primary 10% zone, and prior-test group.

Do not count the 5% and 15% sensitivity-zone variants as independent events. Do not duplicate one original breakout as three observations in the primary cohort.

## 6. De-clustering, dependence, and reporting

- Immutable source events remain unchanged. Derived episode IDs must include the source event ID and an ordinal; never overwrite the source identity.
- Report the strict cohort as a nested sensitivity subgroup, not as an additional independent sample.
- Do not pool UPPER and LOWER or rejection and breakout families in a way that hides asymmetry.
- Report per asset, side, strict/broad definition, test-rank/prior-test group, and UTC calendar month where counts support it.
- Show event counts, complete/censored denominators, missing bars, and ambiguous ordering counts beside every proportion.
- Windows can overlap across events and assets; observations are dependent. No independent-event standard errors, p-values, or causal claims are authorized by V1.
- Preserve all event-level outputs and source-to-output linkage so later uncertainty methods can account for event/time clustering.

## 7. Protocol acceptance, decision criteria, and stopping rules

The study is accepted only if:
1. All source row counts and joins reproduce the accepted source ledgers and metadata.
2. Every eligible event has exact frozen boundary values and a verified causal availability timestamp.
3. Synthetic tests cover upper/lower symmetry, exact-boundary equality, repeated touches within one episode, separation then re-entry, close-through and reclaim, same-bar ambiguity, gap censoring, incomplete horizons, strict/broad nesting, and duplicate source identity rejection.
4. Re-running from the same input hashes produces byte-identical event-level outputs and summaries.
5. The closeout reports all exclusions, censored events, negative/contradictory findings, and limitations.

Stop and do not calculate outcomes if source reproduction, timestamp mapping, or frozen-boundary linkage fails. Stop at the fixed 24h rejection / 12h breakout horizons; do not extend windows or add thresholds in response to observed results. Any methodological change requires a new versioned protocol before implementation.

A positive result does not select a strategy or prove predictive value. A negative or mixed result closes the descriptive question and is an acceptable outcome. The practical consequence is to decide whether a family has sufficiently well-defined lifecycle states to proceed to Gate 2 execution-resolution research. It does not authorize Gate 3 entries, Gate 4 stops/targets, or Gate 6 PnL backtests.

## 8. Explicit exclusions

V1 does not:
- simulate fills, entries, exits, stops, targets, fees, spread, slippage, funding or PnL;
- infer intrabar event order from OHLC;
- optimize thresholds or select signal-candle anatomy cutoffs;
- use the rejected V6 matched-control pairs;
- reuse the unreconciled 2,095-event preliminary rejection cohort or its outcomes;
- redefine the accepted sideways detector, boundary reconstruction, breakout source, or prior-test classification;
- claim causality, predictiveness, profitability, or live readiness.

## 9. Implementation handoff

Only after this protocol is committed:
1. Reproduce the accepted source population and hashes.
2. Implement Module A and Module B separately with isolated tests.
3. Run synthetic tests before reading historical outcomes.
4. Run the fixed protocol once on the accepted sources.
5. Archive code, tests, run metadata, input/output hashes, event-level ledgers, summaries, logs, and closeout decision.
6. Update the project register and Gate 1 status. Keep Gate 2 closed until both modules pass their descriptive closeout criteria or are formally rejected.
