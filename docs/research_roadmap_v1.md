# Research Roadmap V1 — OKX Price Action Research

**Branch:** `price-action-v1`  
**Status:** Research plan; workstreams are not yet all implemented or completed.  
**Purpose:** Preserve the agreed research sequence, hypotheses, controls, and repository-cleanup rules so the project can be resumed consistently.

## 1. Research principles

1. Measure market behaviour before designing more stop-loss/take-profit parameter sweeps.
2. Treat every strategy idea as a hypothesis to test, not as an assumed edge.
3. Preserve causal execution: a signal formed from a completed candle cannot execute before the next eligible execution candle.
4. Keep development, validation, and untouched out-of-sample periods chronological (currently planned as 60% / 20% / 20%). Do not select or tune a strategy using the final OOS period.
5. Include realistic fees, slippage, funding, gaps, and execution timing. Report gross and net results separately.
6. It is acceptable—and may be preferable—for a system to avoid trading in regimes where evidence does not support a trade.
7. Keep pure price-action Model A separate from indicator-assisted benchmark Model B. Diagnostic indicators must not silently become Model A entry filters.
8. Do not infer live-trading readiness or profitability from backtest results.

## 2. Existing project framework to preserve

The current research architecture is:
- 1D: broad market environment.
- 4H: market-regime classification.
- 15M: price-action signal generation.
- 1M: primary execution simulation.
- 5M: secondary execution-robustness comparison using the same 15M signals; this is not automatically a separate 5M signal strategy.

The existing strategy specifications remain the authoritative definitions:
- `docs/price_action_strategy_spec_v1.md`
- `docs/pure_price_action_structure_v1.md`

Do not change these definitions implicitly. Any new 5M-entry strategy or other material scope change must be documented as a separate experiment group.

## 3. Research sequence

### Workstream A — Data and repository audit

- Confirm the five assets (BTC, ETH, SOL, DOGE, AVAX) have clean, correctly timestamped 1-minute OHLCV inputs and aligned timestamps.
- Verify funding-rate coverage, timestamp conventions, units, and missing periods.
- Verify the 15M signal dataset's provenance, generation rules, and alignment with execution data.
- Record exact input paths, date ranges, row counts, and audit results in reproducible reports.
- Distinguish current-project inputs from files belonging to older projects.

**Known prior status:** Individual 1-minute quality audits for all five assets passed for duplicate candles, missing 1-minute intervals, invalid OHLCV, and timestamp errors. Cross-asset alignment was checked previously. Re-run or inspect the relevant evidence before relying on it after any data changes.

### Workstream B — Five-asset market behaviour

Study BTC, ETH, SOL, DOGE, and AVAX individually and comparatively:
- Average and distribution of daily and weekly movement.
- Return distributions, volatility, candle ranges, and volatility clustering.
- Large upward and downward impulses (“pumps” and “dumps”): magnitude, duration, continuation, and reversal.
- Intraday/time-of-day and day-of-week behaviour, with timezone conventions stated explicitly.
- Differences between assets and whether behaviour is stable across chronological periods.
- Cross-asset correlation and lead/lag behaviour, including whether BTC moves precede or coincide with moves in other assets.

Report sample sizes and uncertainty. Avoid treating correlation or apparent lead/lag as proof of causation.

### Workstream C — Sideways-market research (explicit priority)

Do not treat all non-trending markets as one category. Investigate at least:
1. Quiet, narrow sideways ranges.
2. Wide but orderly ranges.
3. Volatile/choppy sideways markets.
4. Range-to-trend and trend-to-range transitions.
5. Volatility shocks and disorderly conditions.

Measure:
- Range duration, width, and width normalized by volatility.
- Boundary touches/tests, spacing between tests, and reactions after tests.
- False breakouts and failed breakdowns.
- Breakout follow-through, continuation distance, and time to failure.
- Mean-reversion distance and time back toward the range interior or midpoint.
- Pullbacks within ranges and after breakouts.
- Changes in volatility and range structure over time.
- Net tradability after fees, slippage, funding, and realistic entry delay.

Study these behaviours on relevant 15M, 1H, 4H, and daily horizons. Define range boundaries and event labels causally, using only information available at the time. Avoid look-ahead from future-confirmed swing points. Test classification stability and regime flicker.

Possible diagnostic features include normalized ATR, directional efficiency, ADX, Bollinger bandwidth, and confirmed OHLC structure. These are candidate measurements, not pre-approved trading rules. Do not use a single indicator threshold (for example, ADX alone) as the definition of sideways conditions. Keep diagnostic regime research separate from pure price-action Model A unless a deliberate, documented model change is approved.

### Workstream D — Signal and opportunity behaviour

Before optimizing exits, evaluate the forward behaviour of the existing 15M signals:
- Maximum favourable excursion (MFE) and maximum adverse excursion (MAE).
- Forward movement after 15 minutes, 1 hour, 4 hours, 12 hours, and 24 hours.
- Probability of reaching candidate target levels before candidate stop levels.
- Time-to-target, time-to-stop, and proportion of signals that reach neither within the observation horizon.
- Results by long/short side, signal type, asset, and contemporaneously known market regime.
- Distribution tails and sample counts, not only averages.

Define all event windows and labels without look-ahead. Account for overlapping signals and dependent observations when estimating uncertainty.

### Workstream E — Costs and execution

Quantify:
- Maker/taker fee assumptions and the account fee tier actually applicable (verify before final calibration).
- Slippage sensitivity by asset, volatility, order type, and time of day where data permits.
- Funding payments and holding-time effects.
- Entry delay, missed limit fills, order expiry, gaps, and stop/target execution assumptions.
- Gross versus net expectancy, turnover, fee burden, and holding-time distributions.

A rough current planning assumption is 0.05% taker fee per side plus 2 basis points slippage per side, approximately 0.14% round-trip cost on traded notional before funding. This is an assumption for analysis, not a verified account-specific fee schedule. Calculate actual costs using the simulator's traded notional and fill model.

For a simplified full-stop/full-target model with stop distance S, reward multiple R, win probability p, and round-trip cost C expressed on the same notional basis:
`Net expectancy = p(RS) - (1-p)S - C`
The simplified break-even reward multiple is:
`R_min = ((1-p)S + C) / (pS)`
These formulas are sanity checks only. Real results must account for variable fills, gaps, sizing, funding, and trade-path effects.

### Workstream F — Focused strategy experiments

Only after Workstreams A–E:
- Write a specific hypothesis, expected mechanism, and falsification condition before coding each experiment.
- Test a small number of economically motivated variants rather than broad, arbitrary parameter grids.
- Consider separate hypotheses for directional trend conditions and range mean-reversion conditions.
- Consider no-trade rules for volatile/choppy sideways, transitions, and shocks, but test rather than assume their value.
- Compare against simple baselines and report per-asset as well as shared-portfolio results.
- Freeze choices using development/validation only; evaluate the final OOS period once as a final check.
- Require robustness across assets and periods, realistic costs, and acceptable drawdown before considering any further stage.

## 4. Existing experiment status and telemetry caution

The original 66-experiment exit batch completed previously. Its reported results were negative overall; no viable strategy has been identified. Do not present the best member of a losing grid as a profitable strategy.

A separate telemetry-enabled rerun was started to record trailing-stop/target activation details that were not present in the original trade exports. The first two experiments completed and were saved under:
`reports/exit_experiments_telemetry_v1/`
The third experiment had started when the run was interrupted. Treat this directory as a partial run. Do not overwrite, delete, or resume the remaining batch automatically. First inspect the checkpoint, log, and existing outputs, then decide whether only a smaller targeted telemetry rerun is necessary.

The telemetry fields were added because activation times, levels, update counts, and related path information cannot be reliably reconstructed from summary results alone. Automated tests passed after the instrumentation change, but tests do not by themselves prove the economic correctness of the resulting research.

## 5. Repository hygiene and deletion policy

Keep source code, tests, strategy specifications, data-quality evidence, reproducible research scripts, and final/decision-relevant reports.

Before deleting anything:
1. Inventory tracked files on `price-action-v1`.
2. Identify each file's purpose and whether it is referenced by code, tests, documentation, workflows, or later research.
3. Distinguish generated outputs, temporary logs, duplicate data, obsolete experiments, and files from older projects.
4. Check whether any raw data is actually tracked in this repository; do not assume local Termux data folders are part of GitHub.
5. Preserve useful historical findings in a clearly labelled archive rather than deleting research history.
6. Make a backup or recoverable commit before cleanup.
7. Delete only after dependency/reference checks and a clear explanation of why the file is unnecessary.

The repository was previously reported to be approximately 873 KB, so storage pressure alone is not a reason for risky cleanup. No deletion is authorized by this roadmap.

## 6. Immediate next actions

1. Confirm the interrupted telemetry batch process is stopped; inspect its log, checkpoint, and first two completed outputs.
2. Inventory the current repository and relevant local data directories; verify paths rather than assuming that older-project folders belong to this project.
3. Record data provenance, coverage, and alignment in a reproducible audit report.
4. Begin descriptive five-asset market-behaviour analysis.
5. Make sideways-market analysis a dedicated report and test suite of event definitions.
6. Analyse signal MFE/MAE and forward paths.
7. Reconcile cost and execution assumptions.
8. Only then propose the next small, hypothesis-driven experiment set.

## 7. Decision log

- Sideways-market behaviour is an explicit research workstream, not an afterthought.
- Quiet ranges and volatile/choppy sideways conditions must be studied separately.
- A no-trade regime is a valid system outcome.
- The current 5M role is execution comparison for 15M signals; a 5M signal-entry study requires a separately documented experiment.
- No repository files should be deleted before a full inventory and dependency/reference audit.
- No further broad 66-combination rerun should be launched without a specific diagnostic reason.


## 8. Explicit post-signal, signal-candle, and execution-timeframe research

These are required empirical research workstreams, not optional strategy variations. They remain research-only until separately authorized. Use the same completed 15M signal events when comparing execution timeframes; do not silently change the signal-generation timeframe.

### Workstream D1 — Signal-candle anatomy and size

For every eligible 15M signal, record:
- Total high-low range, absolute body, body/range ratio, upper wick, lower wick, and close location within the candle.
- Candle range and body normalized by prior 15M ATR and by recent rolling 15M range distributions, using only data available at signal close.
- Signal direction and signal type, asset, and contemporaneously known 1D/4H environment.
- Distribution and sample counts by asset, direction, signal type, and chronological subperiod.

Compare subsequent paths across predeclared signal-candle size groups (for example, within-asset volatility-normalized quantiles). Measure whether larger/smaller candles are followed by continuation, pullback, retest, failure, or no meaningful movement. Do not assume large signal candles are stronger. Avoid full-sample future-informed cutoffs for any live-style classification; label retrospective descriptive bins clearly.

### Workstream D2 — What happens after a completed 15M signal?

Starting only after the signal candle has fully closed, map the subsequent price path at 1M resolution. For each signal, measure:
- Immediate continuation versus pullback-first behaviour.
- Whether price revisits the signal candle's open, midpoint, close, high/low, and relevant structural level.
- Retest incidence, first-retouch time, depth/penetration, duration around the level, and reaction after the retest.
- Whether the level holds, rejects, is cleanly crossed, or is repeatedly crossed; define these labels before calculation.
- MFE, MAE, net directional movement, and time to favourable/adverse thresholds over 15M, 1H, 4H, 12H, and 24H where complete data exists.
- Failure, reversal, continuation, and unresolved/no-touch outcomes, with explicit denominators.
- Results by signal type, side, asset, signal-candle size, and causally available market regime.

Use frozen signal-candle levels and exact timestamp continuity. A retest must occur after the signal is confirmed; do not count touches that happened before confirmation. Treat overlapping signal windows as dependent observations and report that limitation.

### Workstream F1 — Execution timeframe comparison: 1M / 3M / 5M / 15M

Use identical completed 15M signal events for all four execution-timeframe arms. Compare 1M, 3M, 5M, and 15M execution bars built from the same underlying 1M source. This is an execution-resolution comparison, not a 3M/5M/1M signal-generation study.

Predefine comparable causal entry rules and record:
- Earliest eligible execution-bar close/open and actual entry delay from 15M signal confirmation.
- Entry price, entry distance from signal close and signal structure, and price movement while waiting.
- Immediate/market entry versus explicitly defined pullback, signal-midpoint, structural retest, and confirmation entries as separate entry-method comparisons.
- Entry opportunity, touch, fill, missed-entry, expiry, and partial-fill rates under stated assumptions.
- Adverse selection after fills, post-fill MFE/MAE, and how execution resolution changes observed entry quality.
- Results by asset, side, signal type, signal-candle size, and market regime.

Use the same signal cohort and comparable order assumptions across timeframes. A 15M execution bar cannot act before it is complete; do not grant it intrabar information unavailable at the decision time. Distinguish OHLC touch-based fill approximations from verified fills. Initially report descriptive execution opportunity and price-path results without fees or strategy profitability; cost integration belongs to Workstream E and requires explicit authorization.

### Research safeguards and sequencing

1. Complete signal-candle anatomy and post-signal path/retest descriptions before choosing entry variants.
2. Then compare execution resolutions on the same frozen 15M signal cohort.
3. Report missing/incomplete horizons, exclusions, overlapping-event dependence, and exact denominators.
4. Keep descriptive observations separate from fill assumptions and from net profitability.
5. No strategy backtest or local file modification is authorized by adding these workstreams.


## 9. Dedicated sideways-boundary rejection follow-up research

This is a separate required study from breakout/retest analysis and from the general 15M signal study.

For confirmed 15M rejection events at the frozen upper/lower boundary of a causally defined sideways channel, follow the subsequent path from the next eligible 1M candle. Measure:
- Rejection event frequency by asset, side, strict/broad regime definition, and first/repeated boundary test.
- Follow-through away from the boundary, return to the channel interior, midpoint, opposite boundary, and failure through the rejected boundary.
- Immediate continuation versus pullback-first; retest of the rejection candle and boundary; time-to-retest, retest depth, hold/rejection/crossing, and subsequent movement.
- MFE, MAE, net directional close movement, and time to predeclared favourable/adverse thresholds over 15M, 1H, 4H, 12H and 24H where complete data exists.
- Rejection candle range, body, wick proportions, close location and volatility-normalized size, then compare subsequent paths across size groups.
- First versus second/third boundary tests, spacing between tests, and whether prior tests change subsequent rejection behaviour.

Use frozen context/boundary levels, completed-candle confirmation, next-eligible-minute timing, and exact timestamp continuity. Define rejection labels and denominators before calculation. Report incomplete windows and overlapping-event dependence.

**Audit warning:** Earlier preliminary rejection-episode output contained an upper-side variable error (`ls` used instead of `us`) and did not enforce 15M continuity in its episode helper. Do not reuse those episode counts as accepted evidence. Reconstruct and validate the event masks and continuity before reporting results.

This workstream is distinct from confirmed breakout/retest study, matched breakout controls, and the general all-signal post-signal study. It remains outstanding; no strategy backtest or local data modification is authorized.

---

## 10. Complete trade-lifecycle research — end-to-end system evidence

This workstream connects market-behaviour, signal, entry, execution, cost, risk, and portfolio studies into one auditable causal process. It is a required research framework, not permission to start a strategy backtest. It supplements Sections 3, 5, and 8; it does not replace their definitions or change the current immediate research gate recorded in the master checklist.

### 10.1 Market condition and context
- Establish the market condition using validated causal phase definitions: bullish trend, bearish trend, sideways/range (including subtypes), choppy/disorderly, and transition/expansion/shock.
- Record phase maturity, strength, volatility, transition risk, uncertainty, and mixed or unclassified states.
- Compare contemporaneously available 1D/4H/1H/15M context without assuming higher timeframes dictate lower-timeframe outcomes.
- Do not force ambiguous observations into a phase or use future-confirmed structure as if it were known at the time.

### 10.2 Signal formation and qualification
- Freeze the signal definition, direction, structural reference, completed-candle confirmation time, and earliest eligible decision time.
- Measure signal frequency, clustering, overlap, invalidation, failure, and no-signal periods by asset and phase.
- Keep signal/path quality separate from entry reachability and executable fills.
- Ensure future price paths, retrospective pivots, or later regime labels cannot change whether a signal qualified at its original timestamp.

### 10.3 Entry execution
- Link each qualified signal to the first eligible entry decision and order time.
- Study predeclared immediate, pullback, limit, structural retest, breakout/retest, and post-retest confirmation methods where relevant.
- Record entry price, delay, distance from signal/structure, price movement while waiting, missed opportunity, no-fill, expiry, partial-fill assumptions, and adverse selection.
- Compare execution resolutions on the same frozen signal cohort and report exact denominators and exclusions.
- Keep OHLC touch, estimated fill, and verified fill as distinct evidence categories.

### 10.4 Position management
- Define initial risk budget, position size, leverage/exposure cap, and initial invalidation before entry.
- Specify which post-entry information may trigger stop/trailing updates, target changes, partial closes, add/reduce actions, break-even moves, or time-based actions.
- Measure open and remaining risk, realized/unrealized P&L, exposure, holding time, and funding through the entire position.
- Include adverse paths, stalled trades, and losing positions; do not evaluate management only on eventual winners.
- Treat each management policy as a separately specified hypothesis with a fixed entry cohort and explicit risk constraints.

### 10.5 Exit execution
- Connect every exit trigger to its first causally eligible order/action and assumed execution price.
- Record exit reason: stop/invalidation, target, trailing stop, time/no-progress, thesis failure, phase change, emergency/portfolio control, or operational/manual closure.
- Predefine gap-through, intrabar stop/target ordering, partial fills, expiry, and slippage assumptions. Resolve ambiguous OHLC sequences conservatively or with finer data where available.
- Report gross exit effects separately from fees, slippage, and funding; do not infer exact fills or liquidity from OHLCV alone.

### 10.6 Portfolio outcome
- Aggregate simultaneous positions across assets in a common timestamped equity, cash, position, and exposure ledger.
- Measure net return, drawdown, tail loss, turnover, capital usage, concentration, correlated exposure, simultaneous adverse moves, and holding-time/funding effects.
- Account correctly for rejected signals, missed entries, no-fills, partial fills, open positions, forced exits, and overlapping positions.
- Test portfolio loss/exposure limits and operational stop conditions separately; reconcile per-asset results to portfolio totals without future information.

### 10.7 End-to-end event-chain and acceptance checks

Maintain a reproducible event chain:

**Market snapshot → phase/context label → signal → entry decision/order → fills → position-management events → exit decision/order → exit fills → fees/funding → portfolio ledger.**

Require stable identifiers, exact timestamps, causal event ordering, complete position reconciliation, and auditable links between every stage. Test missing candles, data outages, duplicate events, simultaneous stop/target touches, rejected orders, partial fills, gaps, and funding-boundary cases.

Report stage-level diagnostics and full-system outcomes together. A promising phase, signal, or entry is not evidence of a profitable complete system. Stratify results where sample sizes permit by asset, side, phase/maturity, entry method, exit policy, and chronological period; disclose overlap/dependence and uncertainty limitations.

**Dependency and authorization:** Phase definitions and signal cohorts must be validated before lifecycle comparisons; signal/post-signal research precedes entry comparisons; entry assumptions must be frozen before position-management/exit comparisons; verified cost/funding assumptions and portfolio accounting are required before net system conclusions. This section does not alter the immediate matched-breakout-controls gate or authorize a new experiment.

## 11. Dedicated exit and position-management research

Exit research is a distinct, required workstream downstream of descriptive signal and entry research. Its inclusion does not authorize exit sweeps, parameter optimization, or strategy-level backtests.

### 11.1 Initial stop and thesis invalidation
- Compare justified stop families: causal structural/swing invalidation, range-boundary invalidation, fixed-distance baseline, and volatility-normalized distance.
- Measure stop distance, risk per unit, relation to known structure, stop-before-favourable-objective frequency, and time-to-stop.
- Distinguish thesis invalidation from a risk-control stop and record the reason for every stop.
- Use only levels confirmed and available at entry; do not use future-confirmed pivots retrospectively.

### 11.2 Take-profit and target families
- Study predeclared fixed R-multiple, prior-structure, range midpoint/opposite-boundary, measured-move, and trend-extension targets where the phase makes them meaningful.
- Measure target reachability, time-to-target, target-before-stop ordering, favourable excursion surrendered, and unresolved outcomes.
- Distinguish target touch from executable limit fill; state queue, partial-fill, and expiry assumptions.
- Compare full exits and runner policies on the same frozen entry cohort.

### 11.3 Trailing exits
- Study fixed-distance, volatility-normalized, confirmed-swing/structure-based, and phase-aware trailing methods.
- Record activation condition/time, initial and updated stop levels, update frequency, stop distance, and whether activation occurred.
- Measure profit retained, MFE surrendered, stop-out timing, whipsaw/re-entry exposure, and gap-through behaviour.
- Require event-level telemetry; do not infer activation/update history from summary exports when it was not recorded.

### 11.4 Partial exits and position scaling
- Compare full close with predeclared partial-close schedules and runner policies.
- Measure realized profit, remaining position/risk, average exit price, runner contribution, turnover, fees, and opportunity cost.
- Study scale-in, scale-out, and add/reduce policies separately with a hard cap on total risk and exposure.
- Do not count multiple partial fills from one position as independent trades.

### 11.5 Time-based, progress-based, and thesis-based exits
- Study maximum holding time, no-progress/stalled-trade exits, time-to-invalidation, and time-to-target.
- Define thesis-failure events before calculation: structural loss, failed continuation/retest, return inside a failed breakout range, or another explicit causal event.
- Compare action at the first warning with action after confirmed state change; quantify avoided adverse movement and prematurely abandoned continuation.
- Include funding timestamps and holding-period effects where relevant.

### 11.6 Phase-specific exit questions
- **Bullish trend:** confirmed higher-low/structure trailing, volatility trailing, prior-high/extension targets, and exits after weakening or failed continuation.
- **Bearish trend:** mirrored lower-high/structure trailing and downside targets; test rather than assume symmetry.
- **Quiet/compressed range:** midpoint/opposite-boundary targets, boundary-failure invalidation, and exits when compression resolves.
- **Wide/orderly range:** boundary-to-interior/opposite-boundary objectives, reversal warnings, and no-progress exits.
- **Volatile/choppy range:** rapid stop/target crossings, whipsaw, shorter-horizon invalidation, and whether avoiding trades is preferable to tightening exits.
- **Breakout/expansion:** continuation targets and trailing versus exits on failed acceptance, failed retest, or return inside the prior range.
- **Transition/shock/disorderly:** gaps, fast-market risk, stale levels, delayed exits, conservative stop assumptions, and explicit emergency risk controls.

### 11.7 Exit execution and cost measurement
- Verify applicable fee schedule and funding inputs before claiming realistic net exit results.
- Estimate slippage by asset, volatility, order type, and time of day where evidence supports it; OHLCV does not establish order-book liquidity or exact fills.
- Model market/stop-market and limit/stop-limit assumptions separately, including gaps, partial fills, unfilled orders, and expiry.
- Predefine intrabar ordering when stop and target are both touched in one candle; use finer data or conservative ambiguity rules.
- Report gross/net P&L, fees, slippage, funding, holding time, turnover, MFE captured, MAE endured, drawdown, and tail outcomes. Reconcile exits with the portfolio ledger.

### 11.8 Exit study sequence and acceptance gates
1. Begin with descriptive path, threshold-reachability, and time-to-event analysis.
2. Freeze the entry cohort and entry assumptions before comparing exit policies; exit arms must not select different favourable entries.
3. Pre-register the hypothesis, baseline, limited variants, risk constraints, horizons, costs, ambiguity rules, and falsification criteria.
4. Account for overlapping trades, multiple comparisons, chronological stability, and asset/regime heterogeneity.
5. Separate descriptive stop/target reachability, assumed fill simulation, and net profitability into distinct evidence levels.
6. Require code review, unit tests, event-level telemetry, event-count/continuity checks, and reproducible reports.

**[LATER — NOT AUTHORIZED]** Exit-family comparisons and strategy-level exit experiments require review of the relevant phase, signal, and entry research gates plus explicit user authorization. Broad exit grids, parameter tuning, and final OOS selection remain prohibited until the complete hypothesis and chronological development/validation/OOS protocol is approved.

**Existing-results safeguard:** The historical 66-experiment exit batch and later telemetry/local exit reports are prior evidence to audit and interpret. Do not overwrite, blindly resume, or repeat them. A negative batch is not justification for a larger parameter grid; first determine what the existing outputs and telemetry can validly establish.

### Roadmap coordination note

The master checklist at docs/research_checkpoints/2026-11-23_master_research_checklist_v1.md is the current progress/status tracker. Current phase: Phase 3 — Sideways / Range. The agreed phase sequence is Phase 3, Phase 1 — Bullish / Uptrend, Phase 2 — Bearish / Downtrend, Phase 4 — Choppy / High Volatility, then Phase 5 — Transition / Expansion. The prior-test classification and breakout forward-outcome studies are complete and audited. Matched-control V2 was attempted but failed its balance audit and is not accepted evidence; a replacement is not the automatic next gate. Sections 10–11 add lifecycle and exit research coverage but do not authorize experiments or override the agreed phase sequence. Before any future run, reconcile this roadmap with the latest master-checklist status and inspect relevant code, tests, reports, and existing local outputs.
