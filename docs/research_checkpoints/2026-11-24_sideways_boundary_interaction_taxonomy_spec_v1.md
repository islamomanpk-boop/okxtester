# Sideways Boundary Interaction and Penetration Taxonomy V1
## Frozen Research Specification
Date: 2026-11-24
Project: OKX Price Action V1
Phase: Phase 3 — Sideways / Range
Status: SPECIFICATION FROZEN — IMPLEMENTATION NOT STARTED

---

## 1. Research purpose

Measure how price interacts with each frozen boundary of a historically
available sideways/range snapshot.

The study expands the existing historical boundary-test reconstruction.
It distinguishes approach, exact boundary contact, penetration, closes
outside the boundary, and re-entry from outside.

The purpose is descriptive market-behaviour research. It is not a
trading strategy, profitability test, or recommendation to trade.

## 2. Relationship to existing research

The existing historical boundary-event reconstruction and its accepted
reports are preserved unchanged.

Its existing `touch` concept means entry into an outer approach zone.
It must not be interpreted as exact contact with the boundary.

This study introduces a separate candle-level taxonomy. It must not
rewrite, replace, or silently alter the existing reconstruction,
historical event ledger, scripts, tests, or reports.

Existing strong-rejection classification may be recorded as a separate
reference flag using its already documented definition. It must not be
redefined by this study.

## 3. Market data and scope

Assets:
- BTC
- ETH
- SOL
- DOGE
- AVAX

LINK remains excluded.

Input data:
`~/okx_scalping_data/{ASSET}_USDT_USDT_1m.csv`

Expected columns:
`ts, open, high, low, close, vol`

The analysis uses the existing accepted 4H sideways snapshot and
15-minute observation framework.

The two existing range definitions are retained:
- STRICT_P25
- BROAD_P40

No volume-based conclusions are permitted because source volume units
have not been verified.

## 4. Observation grain

The base observation is one eligible 15-minute candle, one applicable
frozen 4H snapshot, and one boundary side.

Upper and lower sides are evaluated independently.

Therefore, a single 15-minute candle may produce:
- an upper-boundary observation;
- a lower-boundary observation;
- both observations if it interacts with both sides.

Do not force a candle that interacts with both boundaries into only
one side. Record a dual-boundary-interaction indicator.

Candle-level rows are observations, not necessarily independent events.
Consecutive candles around one boundary must not be presented as
independent boundary tests.

This first study produces candle-level classifications and summaries.
Episode construction and episode-level summaries are deferred to a
separate, explicitly defined stage.

## 5. Causal snapshot and timing rules

Use only a 4H snapshot after it is causally available.

The applicable upper and lower boundaries must be frozen from that
snapshot. Do not move or recalculate boundaries using later candles.

Retain the accepted historical reconstruction's timing convention,
including suppression of the first 15-minute bar after snapshot
availability, unless a documented source audit proves that convention
must be changed. Any proposed change requires a new specification.

Do not use future information to decide snapshot availability,
boundary values, eligibility, or candle classification.

Preserve exact 15-minute timestamp continuity requirements. Do not
bridge timestamp gaps. Reset or exclude observations according to the
accepted continuity rules and document every exclusion.

The final incomplete observation interval must be identified and
handled explicitly. It must not be silently treated as a complete
15-minute candle.

## 6. Boundary geometry and signed distance

Let:
- U = frozen upper boundary;
- L = frozen lower boundary;
- W = U - L = frozen channel width.

Require W > 0.

For the upper boundary, define signed distance for a price P as:

`d_upper(P) = (U - P) / W`

For the lower boundary:

`d_lower(P) = (P - L) / W`

Interpretation for either side:
- positive: price is inside the channel relative to that boundary;
- zero: price is exactly at the boundary;
- negative: price is beyond the boundary.

Calculate and retain signed normalized distances for the candle's:
- open;
- high/low extreme relevant to that boundary;
- close.

Also retain the corresponding price distances where useful.

Upper-boundary extreme is the candle high.
Lower-boundary extreme is the candle low.

## 7. Approach bands

Use three predeclared approach bands:
- 5% of channel width;
- 10% of channel width;
- 15% of channel width.

The 10% band is primary.
The 5% and 15% bands are sensitivity analyses.

For each boundary side, record separate Boolean approach indicators
for all three bands.

An approach indicator is true when the relevant candle extreme enters
the band from inside the channel but does not reach the exact boundary.

Operational definition, using the signed normalized extreme distance d:

- approach_5: 0 < d <= 0.05
- approach_10: 0 < d <= 0.10
- approach_15: 0 < d <= 0.15

These indicators are false when the extreme exactly touches or
penetrates the boundary. Those interactions have their own classes.

The approach bands do not redefine the boundary. Exact contact and
penetration are always evaluated against U or L itself.

Changing the approach band must not change the frozen snapshot,
boundary prices, channel width, or exact contact/penetration measures.

## 8. Mutually exclusive candle interaction classes

Assign one interaction class for each boundary side and each
approach-band definition.

Classification priority is:

1. CLOSE_OUTSIDE
2. REENTRY_INSIDE
3. WICK_PENETRATION
4. BOUNDARY_TOUCH
5. APPROACH_ONLY
6. NO_APPROACH

Definitions:

### CLOSE_OUTSIDE

Upper side: candle close is strictly greater than U.
Lower side: candle close is strictly less than L.

This class takes precedence regardless of the candle open or wick.

A close exactly at the boundary is not a close outside.

### REENTRY_INSIDE

The candle opens strictly outside the relevant boundary and closes
inside or exactly at that boundary.

Upper side: open > U and close <= U.
Lower side: open < L and close >= L.

This class is distinct from an ordinary wick penetration because
the candle began outside the boundary and returned inside by close.

### WICK_PENETRATION

The candle opens inside or exactly at the boundary, its relevant
extreme moves strictly beyond the boundary, and its close finishes
inside or exactly at the boundary.

Upper side: open <= U, high > U, close <= U.
Lower side: open >= L, low < L, close >= L.

### BOUNDARY_TOUCH

The relevant candle extreme reaches the exact boundary but does not
move strictly beyond it, and the candle is not classified by a
higher-priority class.

Upper side: high == U.
Lower side: low == L.

### APPROACH_ONLY

The relevant extreme enters the selected approach band from inside
the channel but does not reach the exact boundary.

This class depends on the selected 5%, 10%, or 15% band.

### NO_APPROACH

The relevant extreme does not enter the selected approach band and
does not satisfy any higher-priority interaction class.

## 9. Equality and numeric handling

Use the parsed source prices and frozen boundary values consistently.

Do not introduce an undocumented epsilon or rounding tolerance to
manufacture boundary touches.

Use strict comparisons for outside/penetration and exact equality
for exact contact as specified above.

Record the numeric representation and any precision conversion in
the implementation metadata.

If exact equality is too rare to be informative, report that fact.
Do not silently replace exact contact with an approximate zone.

## 10. Additional measurements and flags

For every boundary-side observation, retain as applicable:

- asset;
- range definition;
- snapshot identifier and availability timestamp;
- observation timestamp;
- frozen upper and lower boundaries;
- channel width;
- boundary side;
- approach indicators at 5%, 10%, and 15%;
- signed normalized open distance;
- signed normalized extreme distance;
- signed normalized close distance;
- maximum penetration distance, with zero when no penetration occurs;
- whether the candle opened outside;
- whether the candle closed outside;
- whether price returned inside after being outside;
- exact boundary contact indicator;
- strict penetration indicator;
- interaction class under each approach-band definition;
- dual-boundary-interaction indicator;
- existing strong-rejection reference flag, if it can be calculated
  without changing its accepted definition.

Penetration depth must be measured beyond the exact frozen boundary,
normalized by channel width. Approach-band entry is not penetration.

## 11. OHLC and structural validation

Validate every input candle:

- high >= open;
- high >= close;
- low <= open;
- low <= close;
- high >= low;
- timestamps are unique and ordered;
- timestamp continuity follows the accepted 15-minute rules.

Validate every snapshot:

- upper boundary > lower boundary;
- channel width is positive;
- snapshot is available before the observation is eligible;
- each observation uses the correct frozen snapshot;
- no future snapshot or future boundary information is used.

Upper and lower classifications must be independently reproducible
from the source OHLC values and frozen boundaries.

## 12. Required reporting

Produce, at minimum:

1. Candle-level interaction dataset.
2. Class counts and proportions by asset, side, range definition,
   and approach band.
3. Penetration-depth distributions.
4. Upper-versus-lower comparisons.
5. STRICT_P25-versus-BROAD_P40 comparisons.
6. 5%, 10%, and 15% approach-band sensitivity results.
7. Dual-boundary-interaction counts.
8. Existing strong-rejection reference-flag comparison, if valid.
9. Timestamp continuity and observation eligibility audit.
10. Snapshot and boundary reconstruction audit.
11. Exclusion and incomplete-tail accounting.
12. Run metadata and reproducibility information.

Report chronological subperiods where supported by the available
sample. Do not hide asset or period differences inside pooled totals.

All denominators must be explicit. Class counts must reconcile to
eligible observations for each relevant side, definition, and band.

## 13. Interpretation limits

This study is descriptive.

It does not establish:
- independent statistical samples from consecutive candles;
- predictive value;
- causal effects;
- profitable entries or exits;
- executable fills;
- net returns after fees, slippage, or funding;
- strategy robustness.

Do not turn observed class frequencies into trading rules.

Do not interpret a wick penetration, close outside, or re-entry as
a breakout failure or successful rejection without a separately
specified and tested outcome definition.

## 14. Stop conditions

Stop the run and report the failure if any of the following occurs:

- duplicate or out-of-order timestamps;
- unexplained 15-minute continuity gaps;
- a boundary used before its snapshot is available;
- incorrect snapshot assignment;
- non-positive channel width;
- invalid OHLC relationships;
- unaccounted eligible or excluded observations;
- class counts that do not reconcile to denominators;
- approach-band sensitivity changes frozen boundary values;
- incomplete final intervals are silently included as complete candles;
- upper/lower classifications cannot be independently reproduced.

Do not patch around a failed audit by silently dropping problematic
rows or weakening acceptance rules. Document the issue and obtain
methodological review first.

## 15. Implementation and version control rules

This document is the frozen V1 specification.

Implementation must be in a new, separately named research module
with its own tests and report directory.

Do not overwrite existing sideways reconstruction scripts, tests,
reports, specifications, logs, or audits.

Before implementation:
- review the accepted source and timing rules;
- map each specification requirement to a test;
- identify all required input and output fields;
- confirm the implementation will preserve the existing reconstruction.

Any methodological change after this freeze requires a dated,
versioned amendment or a new specification version.

No strategy selection is authorized by this study.

---

End of frozen specification.
