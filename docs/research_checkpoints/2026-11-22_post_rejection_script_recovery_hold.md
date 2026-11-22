# Post-Rejection Outcome Script Recovery — 2026-11-22

## Status
**ORIGINAL CALCULATION SCRIPT NOT RECOVERED — OUTCOME AUDIT REMAINS ON HOLD**

## Recovery checks completed
1. User searched the Termux home/project tree (maximum depth 5) for the exact filename `part1_build_events.py`; no result was returned.
2. The user attempted `exec(open("part1_build_events.py").read())` at the Bash prompt and received a shell syntax error. This was a shell-versus-Python execution-context mistake, not evidence that the script ran.
3. GitHub branch `price-action-v1` was inspected. Its recursive repository tree contains no `part1_build_events.py` and no clearly corresponding repeated-boundary outcome calculation script.
4. GitHub code search in `islamomanpk-boop/okxtester` for `POST-REJECTION OUTCOME WINDOWS`, `MFE_med MAE_med Boundary_retest_`, `first_move_order hit_0.25 hit_0.50`, `part1_build_events`, and `BOTH_SAME_MINUTE` returned no results.
5. The existing provisional audit and predeclared repeated-test protocol were reviewed. They preserve the reported output and event definitions, but explicitly state that the calculation source was not supplied and formulas remain unaudited.

## What remains trustworthy
- The previously saved provisional checkpoint remains a record of supplied outputs and their arithmetic reconciliation.
- It is not evidence that the underlying MFE/MAE, directional-net, threshold-hit, first-move, wick-failure, boundary-retest, midpoint, or complete-window formulas have passed code review.
- Do not use those outputs to infer profitability or a trading edge.
- Do not overwrite or silently relabel the provisional findings.

## Next recovery step
Inspect local Git history (including all refs and deleted paths) for filenames or commits mentioning sideways, boundary, rejection, outcome, or part1. If history has no source, rebuild a new, separately named, auditable calculation script from the preserved protocol and actual local datasets; validate it independently and report whether its outputs reproduce the provisional numbers. Do not claim reproduction unless demonstrated.

## Decision
No matched-control study or strategy conclusions should proceed from the unvalidated post-rejection outcome calculations until the source formulas are recovered or the study is independently rebuilt and audited.
