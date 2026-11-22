# Batch pause and five-asset behavior research plan — 2026-11-22

## Decision
Pause the telemetry 66-experiment batch and do not resume it while the research questions below are being addressed. Preserve all existing reports and the telemetry manifest. No deletion, reset, cleanup, or rerun is authorized by this decision.

## Research objective
Before designing more stop/target experiments, characterize BTC, ETH, SOL, DOGE, and AVAX behavior using the existing historical OHLCV and funding inputs, after verifying provenance and alignment.

## Research workstreams
1. **Data lineage and coverage:** verify source file identity, exchange/instrument, candle schema, UTC timestamps, coverage, missing/duplicate intervals, funding coverage, and signal-generation provenance. Existing files are in directories belonging to other local projects; their presence alone does not establish that they are the exact inputs for this repository.
2. **Individual asset behavior:** returns and realized volatility by 1m/15m/1h/4h/1d; daily/weekly ranges; gap/jump and tail behavior; volatility clustering; trend persistence and directional efficiency; time-of-day/day-of-week patterns.
3. **Impulse behavior:** define pumps/dumps causally and symmetrically; measure size, duration, speed, continuation, retracement, and reversal after fixed horizons. Normalize moves by prior volatility and compare assets.
4. **Cross-asset behavior:** rolling BTC correlations and lead/lag diagnostics for ETH/SOL/DOGE/AVAX; co-movement during calm, trend, shock, and selloff periods; distinguish correlation from predictive leadership.
5. **Sideways-market taxonomy:** distinguish quiet narrow ranges, wide orderly ranges, volatile/choppy sideways, transition periods, and volatility shocks. Measure range width/duration, boundary tests, false breaks, breakout follow-through/failure, mean reversion, and post-breakout continuation.
6. **Signal behavior:** for existing 15m signals, measure MFE/MAE, forward returns and barrier-hit probabilities at 15m/1h/4h/12h/24h, time to favorable/adverse barriers, and results conditioned on asset, direction, and causally available regime.
7. **Execution and costs:** quantify fee, slippage, funding, entry delay, spread/liquidity limitations where data exists, and net tradability. Keep maker/taker assumptions explicit.
8. **Research design:** define all event thresholds and features using only information available at the decision time; use chronological 60/20/20 development/validation/OOS partitions; do not tune on final OOS.

## Method safeguards
- Use only local historical data for empirical claims about these five instruments; published research is background, not a substitute for measurements on the project data.
- Do not infer a coin is more tradable from volatility alone.
- Do not assume sideways markets are one homogeneous regime.
- Do not add indicators or regime filters to Model A without a separately documented hypothesis and test.
- Keep the 5m execution robustness comparison separate from 5m signal-entry research.
- Do not resume the 66-experiment sweep merely because it is paused; first establish which behavior hypotheses need testing.

## Immediate next steps
1. Keep the batch stopped.
2. Review published evidence on crypto volatility, cross-asset dependence, and regime/sideways classification.
3. Agree on operational definitions and metrics.
4. Audit local data provenance and schemas before calculating empirical results.
5. Save each meaningful finding, decision, and test in GitHub.
