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
