# Phase 3 Module B — Independent Review Timing Finding

**Date:** 2026-11-25  
**Project:** OKX Price Action V1 — Phase 3 Sideways / Range  
**Module:** Breakout / failed-breakout lifecycle V1.1  
**Status:** Review in progress; not a Module B acceptance or closure.

## Verified archive review

The historical workflow completed successfully and archived seven report files on `price-action-v1`. The run metadata and group summary show:

- 1,592 unique primary breakout events (932 BROAD_P40; 660 nested STRICT_P25).
- 6,368 event/horizon rows across 15M, 1H, 4H and 12H.
- 6,368/6,368 archived comparisons passed, checking 18 fields per row.
- The four horizons each cover all 1,592 events; 1,592 complete and zero censored at each horizon.
- 244 group-summary rows (61 groups per horizon).
- 454 overlap clusters.
- Five lifecycle retest fields remain unavailable in the frozen historical forward-outcome archive and are descriptive only, without an independent archived cross-check.

The archived run is descriptive research only. It does not test orders, fills, fees, funding, PnL or profitability.

## Timing issue found during independent code review

The frozen V1.1 amendment requires the first completed 15-minute close **strictly after** the retest candle. The helper `_first_15m_close_after` previously selected a close timestamp greater than or equal to the 1-minute candle's close timestamp. If both timestamps were equal (for example, a retest in the final minute of a 15-minute bar), it could treat a simultaneous close as a post-retest hold.

The implementation is corrected to require a strictly later 15-minute close, and a regression test covers the equality boundary. This aligns implementation with the already-frozen amendment; it does not change the research definition or retest distance.


## Additional same-bar ambiguity finding

A second review check found that an inside retest can begin with a failure-confirmation close already inside the boundary band. If the next 1-minute candle both closes beyond the inner edge (moving away) and its range also reaches back into the band, OHLC cannot establish whether the move-away preceded the touch. The prior implementation skipped this candle and could miss the ambiguity.

The state machine now records `SAME_BAR_AMBIGUOUS` for this case on both UPPER and LOWER directions. It does not count the ambiguous candle as a definite inside retest and does not assign a subsequent 15-minute hold result to it. Event and horizon outputs expose an explicit ambiguity flag. Synthetic tests cover both directions and preserve the separate move-away-then-later-retest case.

## Remaining review gates

- Re-run the complete synthetic suite and historical workflow after the correction.
- Review event-level output contract, row counts, timing fields, ambiguity handling and summary consistency.
- Retain the explicit limitation that the five retest fields lack an independent archived historical benchmark.
- Do not close Module B or Gate 1 until independent review is complete and the project register is reconciled.


## 2026-11-25 — Historical rerun and independent report review

The reporting amendment at `939dad6783c37b0638c24ea7cf27e5713b68beff` completed successfully in GitHub Actions run [45639123024](https://github.com/islamomanpk-boop/okxtester/actions/runs/45639123024). The workflow ran all 19 synthetic tests successfully, completed the frozen historical run, passed the archive contract, uploaded the seven-file artifact, and committed the generated reports as `fe176e98a95470659a387d3547d4999e8c14cb48`.

Verified run totals:
- 1,592 primary events (932 BROAD_P40 and 660 nested STRICT_P25).
- 1,537 prior-test links; 160 events have zero prior touch tests.
- 6,368 event/horizon rows; all 6,368 matched the frozen forward archive across 18 archived fields per row.
- 454 overlap clusters.
- 569,125 common 1-minute timestamps across the five assets; zero common-timeline gaps.
- Five lifecycle retest fields remain absent from the frozen forward archive and are not independently benchmarked.

Independent output review:
- Event CSV contains 1,592 rows; group-summary CSV contains 244 rows (61 group combinations for each of four horizons).
- Event-level 12H totals independently agree with the group-summary 12H totals: 107 outside-retest same-bar-ordering ambiguities, 551 inside-retest same-bar-ordering ambiguities, and 630 inside retests confirmed after separation.
- The group summary now has separate outside- and inside-retest ambiguity columns. Counts are horizon-scoped rather than copied unchanged across horizons; for example, the 15M/1H/4H outside ambiguity totals are 61/82/99, and the 15M/1H/4H inside ambiguity totals are 0/248/455.
- The code keeps same-bar ambiguity distinct from a confirmed retest. The inside-retest ambiguous state does not receive a hold status; the confirmed-after-separation state remains separate.
- The strict-later 15M close rule and both-direction same-bar ambiguity regression tests are present and passed in the 19-test run.

This confirms the reporting amendment and the stated count propagation. It does **not** constitute final Module B acceptance. Remaining independent closeout checks include horizon-level lifecycle timestamp/censor propagation, a full event-to-horizon consistency review, and reconciliation of this evidence into the project research register/control center. Keep Module B and Gate 1 open until those checks and the formal closeout are complete. No strategy simulation, orders, fills, fees, funding, PnL, or profitability inference was performed.


## 2026-11-25 — Independent event-to-horizon closeout audit

A second, programmatic audit read the committed event, horizon, and group-summary CSV blobs directly and parsed the CSV records with quoted-field handling. The audit independently recomputed the output relationships rather than relying only on the workflow's archive-contract step.

Verified structural reconciliation:
- 1,592 event rows and 1,592 unique event IDs.
- 6,368 horizon rows and 6,368 unique event/horizon keys; every event has exactly one row for each of 15M, 1H, 4H and 12H.
- Each horizon contains 1,592 rows; all 1,592 are marked complete in each horizon.
- 244 group-summary rows; all group event counts and both ambiguity totals reconcile exactly to their underlying horizon rows.
- Independent horizon totals:
  - 15M: 831 outside retests, 61 outside same-bar ambiguities; no confirmed inside retests or inside ambiguities.
  - 1H: 1,155 outside retests, 82 outside ambiguities; 303 confirmed inside retests and 248 inside ambiguities.
  - 4H: 1,312 outside retests, 99 outside ambiguities; 519 confirmed inside retests and 455 inside ambiguities.
  - 12H: 1,395 outside retests, 107 outside ambiguities; 630 confirmed inside retests and 551 inside ambiguities.

Timestamp and horizon propagation checks:
- Recomputed outside-retest membership from event-level retest candle timestamps against each horizon end; all 6,368 horizon rows agree.
- Recomputed confirmed inside-retest and inside same-bar-ambiguity membership using the event-level status and candle-availability time; all rows agree.
- Recomputed outside/inside hold-close visibility against each horizon end; all rows agree.
- All observed outside and inside hold-close timestamps are strictly later than the corresponding retest candle close.
- No ambiguous inside retest has an assigned event-level hold status.
- Breakout-side reclaim timestamps, where present, are later than the corresponding 15M failure-confirmation timestamps.
- No issues were found in these checks.

This is an independent output-consistency audit, not an independent historical benchmark of the five lifecycle retest measurements. Those five fields remain absent from the frozen forward archive. Module B therefore remains open pending formal closeout and project-wide register reconciliation; Gate 1 remains PARTIAL / OPEN. The study remains descriptive only, with no orders, fills, fees, funding, PnL or profitability inference.


## 2026-11-25 — Follow-up synthetic coverage and historical workflow

The follow-up workflow [45643682550](https://github.com/islamomanpk-boop/okxtester/actions/runs/45643682550) completed successfully on commit `52e89472bf5ea39044376f9f5535e8a07eaa3dcc`.

Verified job steps:
- All **21/21** Module B synthetic tests passed. The two added regressions explicitly cover immediate adverse entry with incomplete 1H/4H/12H horizon censoring, and the availability timestamp of the first completed 15M failure bar.
- Frozen historical lifecycle generation completed.
- Archived result-contract validation passed: 1,592 events, 6,368 horizon rows and 454 overlap clusters.
- Seven report files were uploaded as immutable artifact `phase3-breakout-lifecycle-v1-1` (artifact ID `15036347661`); the workflow's report-commit step found no further report changes.

### Reproducibility comparison limitation

The new artifact ZIP is 817,698 bytes with SHA-256 `079be5d846911d94a591dc260923468b78434872a73fe52fdef07e15275217e6`. The earlier artifact from run 45639123024 is also 817,698 bytes but has SHA-256 `93c3f83c36c1bb283ff05317c20142adc3752ce16ee190caab0090a786a40106`; therefore the ZIP archives are not byte-identical.

A file-level Git-tree comparison found that the two report snapshots differ in three files: the group summary, horizon CSV, and run metadata. Inspection shows the newer report schema includes the separately scoped outside/inside same-bar ambiguity columns and records event-level ambiguity totals (107 outside, 551 inside, 630 confirmed inside retests). The event-level CSV, forward-crosscheck CSV and prior-link CSV retain their prior Git blob identities; the source inputs and principal cohort totals are unchanged. The old comparison run predates this report-schema/ambiguity-count addition, so it is **not** a same-code/same-schema deterministic rerun.

**Disposition:** the latest run is a successful corrected workflow and its report outputs are archived. Deterministic byte-identical rerun on identical code, schema and inputs is **not yet independently demonstrated**. Do not describe this as a determinism pass. A second run of the same revision is still required if the frozen protocol requires byte-for-byte reproducibility. The differing artifact ZIP hashes alone are not evidence of a research-data mismatch because the compared report schemas differ.

Module B remains open pending the remaining formal protocol closeout and same-revision reproducibility evidence. Gate 1 remains PARTIAL / OPEN; Gate 2 and strategy PnL backtests remain unauthorized.


## 2026-11-25 — Protocol-to-test coverage gap identified

A line-by-line comparison against the frozen parent protocol found two acceptance items that were enforced by the historical source-reconstruction code but did not yet have dedicated synthetic regression tests:
- strict-cohort nesting inside the broad cohort;
- rejection of duplicate immutable primary event identities.

The production guards are now exposed as small validation helpers and called by the same historical workflow path. Two synthetic tests exercise both positive and negative cases. This is a test-coverage improvement, not a change to the frozen source population or event definitions.

The update is committed in source/test commits `ce4027b0336bf770ec121eefea90045ce186f510` and `13c12c785c2473a84bf7459f12900fdc90a2b78a`. The initial source-helper workflow [45644677445](https://github.com/islamomanpk-boop/okxtester/actions/runs/45644677445) and the latest-branch workflow [45644799449](https://github.com/islamomanpk-boop/okxtester/actions/runs/45644799449) both completed successfully. The latter ran on revision `d791361a7fea4aa448907de3dfb5d3559c194d60`; the checked-in suite contains 23 tests and its test step passed. See the full-run record below. Module B remains open.


## 2026-11-25 — Full protocol regression run passed

Workflow [45644799449](https://github.com/islamomanpk-boop/okxtester/actions/runs/45644799449) completed successfully on branch revision `d791361a7fea4aa448907de3dfb5d3559c194d60`. Every workflow step passed, including synthetic tests, frozen historical generation, archived-result validation, artifact upload and output-commit step.

The checked-in test file at that exact revision contains **23 test methods**. The workflow's synthetic test step completed successfully, so the 23-test suite passed. The two new cases explicitly verify (1) strict-cohort nesting within broad and (2) duplicate immutable source-event identity rejection.

The result metadata at the prior corrected run revision `52e89472bf5ea39044376f9f5535e8a07eaa3dcc` and this run revision `d791361a7fea4aa448907de3dfb5d3559c194d60` report identical SHA-256 hashes for all five principal CSV outputs. Event and horizon totals, plus the three ambiguity totals, are also identical. This is strong cross-revision output consistency evidence. It is not yet a strict same-revision rerun because the compared commits differ in source/test changes; a repeat run with unchanged analysis source/schema/input hashes is still required for the frozen deterministic gate.

Latest artifact ID: `15036019010`; digest `sha256:3005665eab7908b4d4f8bed806be34eca3e89ceacbaa466748dc49820e8b3184`. The artifact ZIP digest is an archive-level property; the deterministic comparison above uses the five output-file SHA-256 values recorded in run metadata.

**Disposition:** the newly identified test-coverage gaps are closed at the synthetic-test level. Module B is still not formally accepted: same-revision deterministic rerun, full protocol/source audit, lifecycle fields absent from the frozen forward archive, and Gate 0 execution/data readiness remain outstanding.
