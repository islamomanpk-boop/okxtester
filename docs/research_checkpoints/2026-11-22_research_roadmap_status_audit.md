# Research Roadmap Status Audit — 2026-11-22

**Project:** OKX Price Action Research V1  
**Repository:** `islamomanpk-boop/okxtester`  
**Branch:** `price-action-v1`  
**Status:** Roadmap review / work-in-progress inventory  
**Purpose:** Compare the current research artifacts and accepted findings against the main roadmap and the later post-signal research sequence. This is a status audit, not a claim that every workstream is complete.

## Executive status

The research programme has made substantial progress in descriptive five-asset behaviour and sideways/breakout analysis. It is **not complete**. Several important empirical workstreams remain, and some chapters in `docs/research/` are desk-research frameworks rather than calculations on the local five-asset data.

The latest original-breakout reproduction gate passed **20/20** on 2026-11-22. This validates reconstruction of the accepted breakout event counts only. It does not validate matched controls, forward-outcome inference, execution feasibility, or profitability.

Backtests and strategy experiments remain paused. Continue read-only descriptive research only unless the user explicitly changes that instruction.

## Status by workstream

### A. Data quality, alignment, lineage and coverage

**Status: Partially complete; provenance remains an important open item.**

Completed / evidenced:
- Individual 1-minute candle quality audits for BTC, ETH, SOL, DOGE and AVAX passed for duplicate timestamps, missing minute intervals, invalid OHLCV values and timestamp errors.
- Cross-asset common-timestamp alignment was checked.
- The current common intersection contains 569,125 synchronized 1-minute timestamps with no non-consecutive intervals in the latest reproduction check.
- The five datasets were found as inputs in an older adaptive-bot archive, but this only confirms workflow inclusion, not original exchange/API provenance.

Still open:
- Independently verify the original exchange/API source and exact instrument identity for the five 1-minute files.
- Establish volume units and meaning.
- Verify funding-rate data source, coverage, timestamps, units and gaps.
- Verify exact signal-dataset provenance and its relationship to these inputs.
- Preserve the distinction between intended OKX market configuration and verified historical candle source.

Relevant checkpoints include:
- `2026-11-22_five_asset_timestamp_alignment_review.md`
- `2026-11-22_data_provenance_inventory_findings.md`
- `2026-11-22_adaptive_bot_archive_confirms_five_1m_inputs.md`
- `2026-11-22_original_breakout_event_reproduction_pass.md`

### B. Daily, weekly and multi-day movement behaviour

**Status: Core descriptive studies completed; expanded weekly-path study remains.**

Completed:
- Daily and weekly range / return distributions and cross-asset comparisons.
- Daily and multi-day threshold frequencies.
- Rolling 30-day / 90-day behaviour and volatility-state persistence.
- Daily pump/dump and multi-day impulse follow-up behaviour.
- Several chronological comparisons and descriptive distribution summaries.

Still open:
- Weekly path development: how much of final weekly range occurs by each UTC day.
- Timing/order of weekly high and low.
- Weekly intraperiod pullbacks, directional legs and path efficiency.
- Broader weekly movement distribution and robustness across subperiods.

Important distinction: weekly high-low range and weekly close-to-close return have been measured, but that does not mean the full weekly path/timing study in the expanded plan is complete.

### C. Sideways-market behaviour

**Status: Substantial descriptive work completed; taxonomy and stability work remain.**

Completed:
- Candidate 48-hour sideways definitions and joint feature-frequency comparisons.
- 24H / 48H / 72H horizon comparison.
- Rolling label coverage/persistence analysis.
- 15M movement inside selected sideways conditions.
- 15M close-position zones within the channel.
- Boundary-touch and rejection descriptive studies.
- 1-minute follow-up after strong boundary rejection.
- Breakout and retest price-path research with timing corrections.
- Exact reproduction of all 20 accepted breakout event counts (20/20 PASS).

Still open:
- Matched non-breakout control comparison for breakout events. The first attempt is on audit hold and must not be treated as accepted evidence.
- Re-run the corrected replacement only after code review; preserve the event definitions of the accepted final breakout study.
- Better empirical separation of quiet/compressed, wide/orderly and volatile/choppy sideways conditions.
- Regime transition, label flicker and classification stability tests.
- Broader boundary-test spacing / repeated-visit episode analysis with exact continuity safeguards.
- Confirmed range-definition comparisons beyond the current exploratory 48-hour channel classifier.

Caution: the current P25/P40 thresholds are full-sample retrospective exploratory thresholds, not approved live regime thresholds.

### D. Breakout, failed-breakout and post-breakout behaviour

**Status: Breakout continuation/retest descriptive study completed with an important matched-control extension pending.**

Completed:
- Timing-corrected breakout event definitions and follow-up mapping.
- Frozen original channel boundary for follow-up.
- 15M / 1H / 4H / 12H descriptive path outcomes.
- Band approach versus actual boundary penetration separated.
- Retest hold conditional outcomes measured.
- Original event counts independently reproduced at 20/20.

Still open:
- Matched non-breakout controls, after corrected script review and validation.
- More complete false-breakout / failure taxonomy and comparison of breakout events against comparable non-breakout boundary approaches.
- Robustness to regime definition, asset, direction and chronological subperiod.
- Dependence-aware uncertainty for overlapping events.

These studies are descriptive price-path research, not proof of a tradable breakout strategy.

### E. General 15M signal behaviour

**Status: Not yet completed as a full-signal-set study.**

Still open:
- MFE / MAE and forward return distributions for the existing 15M signal set.
- 15M / 1H / 4H / 12H / 24H outcomes.
- Time-to-favourable/adverse barriers and neither-hit outcomes.
- Continuation versus pullback-first paths.
- Breakdowns by asset, direction, signal type and causally available market environment.
- Overlapping-event and sample-dependence treatment.

The existing sideways-boundary rejection and breakout studies cover specific event families; they do not substitute for the broader general 15M signal study.

### F. Execution timeframe and entry-method research

**Status: Not yet completed.**

Still open:
- Compare 1M, 3M, 5M and 15M execution using the same completed 15M signals.
- Causal earliest eligible entry, delay and price-path while waiting.
- Missed-entry and fill opportunity rates under explicit rules.
- Immediate, pullback/limit, retest and confirmation entry comparisons.
- Order expiry, partial/missed fills and adverse-selection assumptions.

The planned 5M comparison is an execution-timeframe comparison using the same 15M signals, not a new 5M signal-generation experiment.

### G. Costs, risk, exits and portfolio behaviour

**Status: Planning/specification exists; empirical integration and later strategy validation remain.**

Still open:
- Verify applicable fee schedule rather than treating planning fee assumptions as account-verified.
- Funding coverage and realized funding effects.
- Slippage sensitivity and execution realism.
- Coin-specific stop/target hypotheses grounded in structure and volatility evidence.
- Shared portfolio risk, simultaneous exposure and correlation-aware aggregate risk.
- Net rather than gross evaluation when strategy testing is later authorized.

No final SL/TP settings or profitable strategy are established by the descriptive research completed so far.

### H. Cross-asset dependence

**Status: Desk-research framework exists; local empirical five-asset study not yet completed.**

Still open:
- Pairwise return correlation at 1M / 15M / 1H / 4H / daily horizons.
- Rolling correlation and chronological stability.
- Downside/stress conditional dependence and co-exceedance.
- BTC-to-altcoin lead/lag at pre-defined lags.
- Co-jumps / volatility connectedness.
- Portfolio-level joint-loss and simultaneous stop-out implications.

The chapter in `docs/research/cross_coin_correlation_connectedness_chapter_05.md` is explicitly a desk-research framework with no local empirical results yet.

### I. Time-of-day and weekday behaviour

**Status: Desk-research framework exists; local empirical study not yet completed.**

Still open:
- UTC-hour and weekday return/range/volatility distributions.
- Hour-by-weekday interactions.
- Weekend/weekday comparison.
- Extreme-event timing and stability across chronological periods.

The chapter in `docs/research/time_of_day_weekday_behaviour_chapter_04.md` is a desk-research framework, not a completed local empirical report.

## Recommended remaining research order

Respecting the user's current instruction to pause strategy backtests and focus on behaviour research:

1. **Finish matched breakout controls**: review the replacement script, preserve exact accepted event masks, validate 20/20 counts before matching, and stop on any mismatch.
2. **Complete provenance and coverage audit**: especially source/instrument identity, volume units, funding coverage and signal provenance. Do not imply OKX source verification until evidence exists.
3. **Weekly path and movement-distribution study**: high/low timing, day-by-day range development, pullbacks and weekly path efficiency.
4. **Cross-asset dependence study**: correlation, downside dependence, co-jumps and lead/lag, with dependence-aware uncertainty.
5. **Time-of-day / weekday study**: UTC-based local calculations.
6. **General 15M signal forward-path study**: MFE/MAE and horizons across the complete signal set.
7. **Broaden sideways taxonomy and stability**: quiet vs wide/orderly vs choppy, transitions and label flicker.
8. **Review all descriptive findings together** and identify what is supported, contradicted or still unknown.

Execution timeframe, entry-method, cost/portfolio integration and strategy tests should follow only when the user explicitly authorizes those next stages. No backtest or experiment is authorized by this status audit.

## Important status distinctions

- A research chapter or plan existing in GitHub does not mean its empirical calculations have been completed.
- A preliminary result is not automatically accepted if a later audit found a methodology defect.
- The first matched-control run remains on audit hold; its pair counts and outcomes are not accepted.
- The 20/20 breakout reproduction PASS validates event-count reconstruction only.
- Descriptive movement, MFE/MAE, range touches and breakout excursions do not establish fills, net profitability or live-trading readiness.
- No local data files were modified by this GitHub status audit.
