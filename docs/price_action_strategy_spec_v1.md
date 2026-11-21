# OKX Multi-Regime Price Action Strategy V1
## Research and Backtesting Specification

Status: Initial specification — pending implementation and testing
Branch: price-action-v1
Starting capital: $1,000
Risk per trade: 0.5% of current equity
Assets: BTC, ETH, SOL, DOGE, AVAX

---

## 1. Objective

Research whether objectively defined price-action setups can produce
positive results after realistic execution costs.

No setup is assumed profitable in advance.

Test signal families independently before testing combinations.
Do not change historical results or rules after observing the final
out-of-sample test results.

## 2. Market data and timeframe architecture

- 1D: broad market environment.
- 4H: regime classification.
- 15M: signal generation.
- 1M: entry, stop-loss and take-profit execution simulation.

Use the audited OHLCV data and indicator files.

A candle's information is unavailable until that candle has closed.
A signal generated on a completed 15M candle cannot execute before
the next eligible 1M candle.

Never use future candles, future pivots, or unconfirmed levels.

## 3. Regime filters

Use the existing verified regime labels.

BULLISH:
- Long setups permitted.
- Short setups excluded in the baseline.

BEARISH:
- Short setups permitted.
- Long setups excluded in the baseline.

SIDEWAYS:
- Test support/resistance rejection and range setups separately.
- Longs near confirmed support and shorts near confirmed resistance.

TRANSITION:
- No trades in the baseline.
- May be tested separately in a later experiment.

WARMUP:
- No trades.

Regime information must be available at the time the signal is formed.

## 4. Price-action signal families

Each family must first be tested independently.

### A. Support and resistance

Use confirmed 15M swing pivots.

Initial pivot definition:
- Three completed candles to the left.
- Three completed candles to the right.
- A pivot is usable only after all three right-side candles close.

Group nearby confirmed pivots into zones using a tolerance of
0.25 times the ATR14 value available when the level is formed.

A zone requires at least two distinct confirmed pivot touches.

A rejection requires price to enter the zone and the completed
15M candle to close back outside the zone in the expected direction.

Do not use a pivot before it is confirmed.

### B. Engulfing candles

Bullish engulfing:
- Current candle closes above its open.
- Previous candle closes below its open.
- Current real body covers the previous real body.

Bearish engulfing:
- Current candle closes below its open.
- Previous candle closes above its open.
- Current real body covers the previous real body.

Use only completed candles.

Test standalone signals and signals occurring at confirmed
support/resistance separately.

### C. Pin bars

Bullish pin bar:
- Lower wick is at least twice the real body.
- Upper wick is no larger than the real body.
- Close is in the upper 25% of the candle range.

Bearish pin bar:
- Upper wick is at least twice the real body.
- Lower wick is no larger than the real body.
- Close is in the lower 25% of the candle range.

Exclude zero-range candles and candles with zero real body.

Test standalone signals and signals occurring at confirmed
support/resistance separately.

### D. Order blocks

Use an objective displacement-based definition.

Bullish order block:
- Identify a bearish candle among the five candles preceding
  a bullish displacement candle.
- The displacement candle has a real body at least 1.5 times
  the 15M ATR14 available before that candle closes.
- It closes above the highest high of the preceding five candles.
- The last qualifying bearish candle defines the candidate zone.

Bearish order block:
- Identify a bullish candle among the five candles preceding
  a bearish displacement candle.
- The displacement candle has a real body at least 1.5 times
  the 15M ATR14 available before that candle closes.
- It closes below the lowest low of the preceding five candles.
- The last qualifying bullish candle defines the candidate zone.

Use the full high-low range of the identified order-block candle
as the initial zone.

The zone becomes available only after the displacement candle closes.
Test the first subsequent retest only.

Record zone invalidation and expiry rules explicitly in the
implementation before running the experiment.

## 5. Entry methods

Compare these methods separately:

1. Market-style entry:
   Enter at the next eligible 1M candle open after the 15M signal closes.

2. Signal-candle midpoint limit:
   Place a limit order at the midpoint of the completed signal candle.
   Expire after three completed 15M candles (45 minutes) if not filled.

3. Order-block midpoint limit:
   Place a limit order at the midpoint of the confirmed order-block zone.
   Expire after three completed 15M candles (45 minutes) if not filled.

A limit order is not filled merely because a 15M candle touches its price.
Use 1M OHLCV data to determine whether the price was reached.

Apply conservative fill assumptions and realistic slippage.

## 6. Stop-loss experiments

Test independently:

- Fixed 0.50% from entry.
- Fixed 0.75% from entry.
- Fixed 1.00% from entry.
- Exact signal-candle extreme: low for longs, high for shorts.
- Signal-candle extreme plus a buffer of 0.10 times 15M ATR14.

For longs, stops are below entry or the relevant signal low.
For shorts, stops are above entry or the relevant signal high.

Reject invalid configurations where the stop is on the wrong side
of the entry.

## 7. Take-profit experiments

Test fixed price targets independently:

- 0.75%
- 1.00%
- 1.50%
- 2.00%

For the two signal-candle stop models, also test risk-multiple targets:
- 1R
- 1.5R
- 2R

R is the absolute distance between actual entry and the selected stop.
Long targets are above entry; short targets are below entry.

Do not select the best target using the final test period.

Record gross and net returns separately.

## 8. Risk and capital management

Initial equity: $1,000.

Risk budget: 0.5% of current equity per trade.

Calculate position size from the entry-to-stop distance and the
risk budget. Include estimated execution costs in risk calculations.

Use a maximum gross notional exposure of 1x equity in the initial
baseline. Any leverage experiments must be separately specified.

Allow at most one open position per asset in the baseline.

All assets share one portfolio equity balance and one gross exposure cap.
Existing open positions consume exposure capacity before new positions
are allocated. The total gross notional exposure must not exceed 1x
current portfolio equity.

Multiple assets may hold positions simultaneously, subject to the shared
exposure cap and the one-position-per-asset rule.

When simultaneous candidates exceed available exposure, rank them
deterministically:
1. Signal priority 3: confirmed support/resistance rejection or first
   order-block retest.
2. Signal priority 2: engulfing or pin bar at a confirmed S/R level.
3. Signal priority 1: standalone engulfing or pin bar.
Within a priority tier, prefer the smaller ATR-normalized stop distance.
Use asset symbol alphabetically as the final tie-breaker.

The ranking must use only information available at the decision time.
Never rank candidates using their future returns.

Record portfolio exposure and simultaneous positions.

Do not increase risk after losses.

## 9. Execution costs

The backtester must support configurable:

- Maker fees.
- Taker fees.
- Slippage in basis points.
- Funding payments and timestamps.

Use the applicable OKX instrument fee assumptions and historical
funding data where available.

Do not silently assume funding is zero when funding data is missing.
Report any missing cost data as a limitation.

For limit orders, use maker fees only when the fill assumptions
justify maker execution. Otherwise apply the appropriate fee model.

## 10. Intrabar execution rules

Use 1M candles for execution simulation.

If both stop-loss and take-profit are touched within the same 1M candle
and their order cannot be established, assume the stop-loss occurs first.

If a position is opened and its stop or target is also touched in the
same candle, use conservative execution assumptions.

Model gaps through stop prices conservatively.

Do not allow fills before orders become active.

## 11. Experiment sequence

Stage 1:
- Validate signal definitions and timestamps.
- Test each signal family independently.

Stage 2:
- Compare entry methods.

Stage 3:
- Test the original 16 combinations of four stop-loss models and four
  fixed-percentage take-profit models.
- Add three R-multiple targets for the exact signal-candle stop.
- Add three R-multiple targets for the buffered signal-candle stop.
- This produces 22 baseline configurations.
- Test trailing stop-loss independently on all 22 configurations.
- Test trailing take-profit independently on all 22 configurations.
- Do not combine trailing stop-loss and trailing take-profit in this stage.
- Total planned exit configurations: 66.

Stage 4:
- Compare results by asset and market regime.

Stage 5:
- Test combinations of signals only after individual results
  are understood.

Avoid an uncontrolled parameter search.

## 12. Validation and reporting

Use chronological data splits:

- First 60%: development/training.
- Next 20%: validation.
- Final 20%: untouched out-of-sample test.

Do not shuffle time-series observations.

Report at minimum:

- Number of trades.
- Win rate.
- Gross profit and loss.
- Net profit and loss after costs.
- Profit factor.
- Expectancy per trade.
- Maximum drawdown.
- Average win and average loss.
- Average holding time.
- Fees, slippage and funding costs.
- Results by asset.
- Results by regime.
- Long and short results separately.
- Out-of-sample performance.

Include a no-trade result when a setup produces no valid trades.

## 13. Reproducibility and GitHub

Save all strategy code, configuration, test reports and documentation
in the price-action-v1 branch.

Do not upload large raw market-data files or credentials.

Every completed task must be committed and pushed to GitHub.
Verify the commit and branch status after each save.

## 14. Current status

- Market data audits: passed.
- Higher-timeframe data audit: passed.
- Indicator inventory audit: passed.
- Regime integrity audit: passed.
- Price-action specification: initial draft.
- Price-action signal implementation: implemented and unit-tested; strategy integration pending.
- Single-trade execution engine: implemented and unit-tested; portfolio integration pending.
- Strategy performance: not established.


## 15. Additional portfolio and experiment decisions

- Preserve the original 16 stop/fixed-target combinations.
- Add exact and buffered signal-candle stops with 1R, 1.5R and 2R targets.
- Test 22 baseline configurations, 22 trailing-stop variants and 22
  trailing-take-profit variants: 66 configurations total.
- Use a shared portfolio equity balance across BTC, ETH, SOL, DOGE and AVAX.
- Permit simultaneous positions in different assets only while total gross
  exposure remains at or below 1x current equity.
- Permit no more than one open position per asset.
- Expire unfilled midpoint limit orders after three completed 15M candles
  (45 minutes).
- Cancel a pending limit order if its setup becomes invalid before filling.
- Use deterministic signal-priority ranking for simultaneous candidates.
- Treat SIDEWAYS range trading as a separate strategy family and report its
  results separately from trend-regime strategies.
- Do not combine sideways and trend results when selecting configurations.

---

## 16. Research model separation and pure price-action priority

Two models must be researched and reported independently.

### Model A — Pure multi-timeframe price action (primary)

- 1D: confirmed swing structure and HH/HL or LH/LL classification.
- 4H: independently confirmed swing structure and classification.
- 15M: objective price-action setup and signal generation.
- 1M: primary execution timeframe.
- 5M: secondary execution robustness comparison.

Model A must not use EMA, RSI, ADX, or indicator-based directional
filters. Its structure labels are generated from OHLC prices only.

A swing high or low uses three candles on each side and becomes
available only after the third right-side candle closes.

Bullish structure requires both HH and HL. Bearish structure
requires both LH and LL. Mixed, insufficient, or conflicting
structure is NEUTRAL in the first baseline.

A bullish BOS requires a completed close crossing above a previously
confirmed swing high. A bearish BOS requires a completed close
crossing below a previously confirmed swing low. No retroactive BOS
is allowed if the level was crossed before its confirmation.

Trend permission requires daily and 4H structure to agree:
- BULLISH + BULLISH permits long trend setups.
- BEARISH + BEARISH permits short trend setups.
- Conflict or NEUTRAL permits no trend trade.

Range trading is a separate experiment, not mixed into trend results.

### Model B — Indicator-assisted benchmark

Retain the existing verified indicator-assisted regime classifier
and its original rules as a separate benchmark. Its EMA/ADX-based
labels must not be used to construct Model A structure labels.

### Execution comparison

Use 1M execution as the primary baseline. Run 5M execution as a
separate robustness comparison using the same 15M signals, test
periods, fees, funding, sizing, and risk assumptions wherever
the data permits a fair comparison.

Do not compare results unless the execution assumptions are aligned
and differences are documented.

The detailed causal structure rules are documented in
`docs/pure_price_action_structure_v1.md`.

### Confirmed support/resistance touch flags

The signal detector records two additional informational flags:

- `support_zone_touch`: the completed candle overlaps an existing
  support zone formed from at least two confirmed pivot lows.
- `resistance_zone_touch`: the completed candle overlaps an existing
  resistance zone formed from at least two confirmed pivot highs.

A touch is not itself a trade signal. It is distinct from rejection:
a rejection additionally requires the candle to close back outside
the zone in the expected direction.

Zones confirmed on the current candle are not used to classify that
same candle. Only zones already confirmed before the current candle
are eligible. These flags support priority-2 classification when
combined with a directionally matching engulfing candle or pin bar.

## 17. Trailing exit experiments

Trailing exits are separate experiments. Never enable trailing stop-loss
and trailing take-profit together in this stage.

### A. Trailing stop-loss

- Keep the configuration's original stop and take-profit.
- Activate trailing after price first reaches +1R in the favourable direction.
- Trail the stop 1R behind the best favourable price reached since entry.
- The trailing stop may move only in the direction that reduces risk; it
  must never move farther away from the market.
- For longs, trail below the highest favourable price.
- For shorts, trail above the lowest favourable price.

### B. Trailing take-profit

- Keep the configuration's original stop-loss.
- Use that configuration's original take-profit level as the activation
  threshold.
- When the threshold is first reached, replace the fixed take-profit with
  a trailing exit.
- Trail the exit 0.5R behind the best favourable price reached after
  activation.
- For longs, trail below the highest favourable price after activation.
- For shorts, trail above the lowest favourable price after activation.

### C. Causal 1M execution rules

- Calculate initial R from actual entry and the selected initial stop.
- Determine activation and favourable extremes using 1M OHLC data only.
- Update trailing levels after a 1M candle has completed; a changed level
  becomes active on the next eligible 1M candle.
- Never use the completed candle's high/low to claim a trailing order was
  active earlier inside that same candle.
- Apply conservative gap and intrabar stop execution assumptions.
- Record activation time, trailing level changes and final exit reason.

Run each trailing method independently against all 22 baseline
configurations. Do not combine both trailing methods until their
individual effects have been measured.

The resulting research groups are:
- 22 baseline configurations.
- 22 configurations with trailing stop-loss.
- 22 configurations with trailing take-profit.
- 66 configurations in total.

Report all groups separately, including net performance after fees,
slippage and funding. Do not select trailing rules using the untouched
out-of-sample period.
\n