# Sideways Boundary Repeated-Test Definition — Predeclared Protocol

**Date:** 2026-11-22  
**Status:** PREDECLARED METHODOLOGY — RESULTS NOT YET RUN  
**Research only:** No strategy backtest, fill simulation, costs, or profitability claims.

## Purpose

Define a reproducible first, second, third, and later test of a sideways 4H channel boundary. This is a new event definition. It does not claim to reproduce the older unverified rejection counts.

## Context and boundary

- Build 4H context from the common 1M data using the established 12-bar (48-hour) channel and the existing directional-efficiency and overlap definitions.
- Use dynamic full-sample P25 (strict) and P40 (broad) channel-width thresholds, explicitly exploratory and retrospective.
- Keep the existing sideways requirements: channel width at or below the selected percentile, directional efficiency <= 0.30, and mean overlap >= 0.70.
- Freeze the 4H upper/lower boundaries for each 4H snapshot.
- Preserve the existing same-snapshot eligibility rule: do not count the first 15M bar after a new 4H snapshot.
- Reset test numbering when the 4H snapshot changes, sideways context is invalid, or the 15M timeline has a gap.

## Boundary zone and touch

Let W = upper - lower.

- Upper boundary touch: 15M high >= upper - 0.10 * W.
- Lower boundary touch: 15M low <= lower + 0.10 * W.

This is a wick-entry definition. A touch candle need not close in the boundary zone.

## Predeclared separation and repeated-test rule

A test begins at the first eligible touch in a snapshot/direction.

A new test is not counted merely because one or more non-touch candles occur. The prior test must first be followed by a completed 15M candle that closes sufficiently far away from the tested boundary:

- After an upper test, separation is confirmed when close <= upper - 0.20 * W.
- After a lower test, separation is confirmed when close >= lower + 0.20 * W.

The 0.20 * W threshold is fixed in advance: it places the close an additional 0.10 * W beyond the inner edge of the 10% touch zone. The separation candle arms the next test; a subsequent eligible touch begins that next test. A candle cannot both establish separation and begin the next test. Repeated touches before confirmed separation remain part of the current test.

This definition deliberately avoids treating a brief one-candle pause outside the wick-touch zone as a fresh test unless price has closed an additional 10% of channel width away.

## Strong rejection within a test

Count at most the first qualifying strong rejection candle per test:

- Upper: touch condition, close < upper - 0.10 * W, and close > lower.
- Lower: touch condition, close > lower + 0.10 * W, and close < upper.

A test can have no strong rejection. Rejection incidence is reported as tests with a first strong rejection divided by all eligible tests at that test number.

## Required audit output

For each asset, strict/broad definition, and upper/lower boundary:

- Total tests.
- Tests ranked 1, 2, 3, and 4+ within each 4H snapshot.
- Tests with a qualifying strong rejection at each rank.
- Strong-rejection incidence by rank, with explicit denominators.
- Number of snapshots containing one, two, three, or four-plus tests.
- Timestamp continuity and snapshot-reset checks.

## Limits

- Test ranks are local to a single 4H snapshot, not a lifetime count of touches at a price level.
- A 4H snapshot spans a finite context; this is not a test of a persistent support/resistance level across multiple snapshots.
- Overlapping market contexts and adjacent events are dependent. Report descriptive counts/rates only.
- The thresholds are research definitions, not optimized trading parameters.
- No post-event outcomes are included in this audit. The later follow-up study must start after the completed 15M event close and use exact 1M continuity.
- Prior rejection counts (174 etc. from the preliminary visit audit and the older report references) remain unreconciled and must not be treated as accepted counts.

## Acceptance gate

Inspect the audit output and verify test-number totals, reset rules, and exact continuity before accepting the event cohort. Save results separately from this protocol. If any invariant fails, mark the run as failed and do not interpret rejection rates.
