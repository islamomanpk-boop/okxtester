# Matched-Control V2 — Failed Balance Audit

**Date:** 2026-11-24
**Status:** Run completed and original event reproduction passed; matching balance failed. Results are not accepted for strategy decisions.

## Run artifact

`reports/matched_control_study_v2_run_2026-11-24.log`

SHA-256:
`4ffc0faaf08f5b483dca42052f4d754db65c4f48625df8019b68ef94343b865f`

The log contains 1,995 lines and 318,969 bytes.

## What passed

- Common 1M timestamps: 569,125.
- All 20 accepted original breakout event counts reproduced exactly.
- All 10 original joined-15M P25/P40 thresholds reproduced within the encoded tolerance.
- All 20 matching strata completed under the programmed distance caliper.
- Total matched pairs: 971.
- Matching was greedy, one-to-one and without replacement.

## What failed

The post-match signed boundary-distance standardized mean difference exceeded 0.10 in absolute value in all 20 of 20 strata.

The signed distance is structurally different for the two groups:
- Breakouts are beyond the boundary (negative signed distance).
- Controls remain inside the boundary (positive signed distance).

The matching algorithm therefore did not establish adequate covariate balance. A distance-caliper pass is not proof of balance.

The log also lacks explicit exclusion counts by reason, including incomplete follow-up and missing/non-finite covariates. This is an additional reporting gap.

## Interpretation hold

- Do not treat the matched groups as adequately balanced.
- Do not use the V2 bootstrap intervals as evidence that breakouts outperform or underperform controls.
- Do not infer causality, tradability or profitability.
- Preserve the script, specification and run log unchanged as a failed-design diagnostic.
- Any revised matched-control method must have a new versioned specification and implementation, with common-support and balance diagnostics reviewed before outcomes are interpreted.

The successful event-reproduction gate remains a valid reproduction check. It does not rescue the failed matching design.
