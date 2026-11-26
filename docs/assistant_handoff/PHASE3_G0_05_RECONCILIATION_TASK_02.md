# Phase 3 G0-05 — Reconciliation Task 02 (Read-Only)

**Repository:** `islamomanpk-boop/okxtester`  
**Branch:** `price-action-v1`  
**Status:** Open research gate; this task does not authorize closure.  
**Mode:** Read-only source inspection. Do not execute scripts, tests, workflows, serializers, or data pipelines. Do not modify production/research code or source datasets.

## Objective

Resolve the remaining G0-05 evidence questions at both cohort-row and physical-event grain. Produce an evidence-backed reconciliation, not a narrative estimate.

## Critical terminology rule

Never use “unique events” for a cohort-row count. Report separately:
- cohort rows;
- physical event identities after grouping by the documented physical key;
- nested cohort memberships (e.g. strict rows that are also broad);
- overlap clusters, which are not independent events;
- horizon rows, distinguishing cohort-row grain from physical-event grain.

For Module B, the currently reported figures are **1,592 cohort rows**, comprising **932 BROAD_P40 rows** and **660 STRICT_P25 rows**, with strict membership nested inside broad membership; the source audit groups rows by physical identity `(asset, direction, signal_time_ms, snapshot)`. The reported **6,368 horizon rows** are four horizons per cohort row, not 6,368 independent physical observations. Verify these statements directly from source and identify any caveat or contradiction. Do not assume the number of distinct physical keys without showing the actual grouping logic/results.

## Required investigations

### A. Module A — rejection lifecycle
1. Verify 1,992 cohort rows and the broad/strict membership counts (reported 1,154 broad + 838 strict).
2. Show the exact physical identity key and how nested memberships collapse.
3. Verify the reported 1,154 physical rejection identities and 380 overlap clusters, explaining what each count represents.
4. Identify any mismatch between implementation, tests, reports, and closeout wording.

### B. Module B — breakout/failure lifecycle
1. Verify 1,592 cohort rows, 932 BROAD_P40 rows, 660 STRICT_P25 rows, and strict-subset semantics.
2. Show the exact physical identity key, grouping/deduplication procedure, and actual distinct-key count if statically derivable from source artifacts.
3. Reconcile 6,368 horizon rows at cohort-row grain. State the expected physical-event × horizon count only if the physical-event count is proven.
4. Verify the reported 454 lifecycle overlap clusters and explain their unit of counting.
5. Identify wording/count inconsistencies across implementation, tests, reports, closeout and checkpoint documents.

### C. G0-05 source-ledger reconciliation
1. Reconcile the reported source-only ledger rows: 1,154 rejection + 2,861 breakout + 932 failed-breakout = 4,947 ledger rows.
2. Explicitly map failed-breakout rows to their originating breakout identities where evidence exists. Do not call the 4,947 rows independent physical events.
3. Verify disposition arithmetic:
   - rejection: 1,083 eligible + 31 rejected + 40 expired = 1,154;
   - breakout: 1,038 eligible + 1,823 rejected = 2,861;
   - failed breakout: 736 eligible + 30 rejected + 166 expired = 932.
4. Identify missing, duplicated, ambiguous, orphaned, or many-to-one source mappings. Do not infer that a matching count proves identity-level completeness.

### D. Canonical 60-field sourceability matrix
For each of the 60 canonical fields and for each of the three family row types (rejection, breakout, failed-breakout), provide:
- exact canonical field name;
- source file and exact source column/expression;
- derivation or transformation, if any;
- whether sourceable directly, derivable, conditionally available, unavailable, or synthetic-only;
- nullability/absence semantics;
- evidence location (file and line/function/test/report);
- unresolved ambiguity.

Do not run the serializer or materialize real candidate rows. Static inspection only. If all 60 fields cannot be established from current accessible evidence, state exactly what is missing.

### E. G0-04 threshold-row explanation
Verify the reported 65,310 threshold rows. The current interpretation is six variants (three policies × two populations) over 10,885 asset/context combinations in aggregate. Confirm from source and reports. Do not invent equal per-asset allocations; provide per-asset counts only if explicitly supported by source artifacts.

## Output format

Return a structured report with:
1. Executive disposition: resolved / partially resolved / unresolved, and why G0-05 remains open.
2. Count reconciliation table with separate cohort-row, physical-event, membership, overlap-cluster and horizon-row units.
3. Exact identity-key definitions and deduplication logic for each family.
4. Source-ledger mapping findings, including linked failed-breakout lineage.
5. Full 60-field × 3-family sourceability matrix, or a precise account of why it cannot yet be completed.
6. Threshold-row reconciliation.
7. A discrepancy register: claim, source evidence, corrected interpretation, impact, next verification.
8. Exact file paths and line numbers for every material claim.

## Hard boundaries

- No edits to research code, tests, workflows, reports, datasets, manifests or branch state.
- No script/test/workflow execution.
- No candidate generation, parameter/threshold selection, backtesting, PnL analysis, profitability claims or strategy selection.
- Do not close G0-05 or mark Phase 3 complete.
- Do not silently repair documents; report proposed wording corrections separately.
- If a result requires runtime/data execution, mark it **not verified** and specify the smallest safe next step, rather than executing it.

## Review standard

Prefer primary implementation and tests over summaries. Cross-check reports and checkpoint documents. Distinguish facts directly proven by code from figures merely asserted in documentation. Quote exact line ranges and describe the identity grain. A count equality alone is not proof of one-to-one source mapping.
