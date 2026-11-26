# ChatGPT → Copilot research handoff
## Phase 3 — G0-05 canonical mapping and population reconciliation
**Target branch:** `price-action-v1`  
**Mode:** READ-ONLY RESEARCH ONLY  
**Priority:** Continue Phase 3 Sideways/Range. Do not advance to another phase.

### Objective
Independently audit the existing G0-05 canonical candidate/source mapping and reconcile the reported populations across Module A, Module B, G0-04, and G0-05. The purpose is to establish what the real source rows support—not to generate candidates or select a strategy.

### Required investigations
1. **Module A:** Explain the relationship between 1,992 cohort rows and 1,154 physical rejection events after strict/broad collapse. Identify the exact keys, deduplication rules, and overlap-cluster semantics. Explain the reported 380 overlap clusters.
2. **Module B:** Reconcile 1,592 lifecycle events, 454 lifecycle overlap clusters, and 6,368 event/horizon rows with the G0-04 population. Explain which are rows, identities, clusters, or horizon expansions.
3. **G0-04:** Reconcile 2,861 unique raw breakout-crossing identities and 1,037 raw-crossing overlap clusters. Explain the reported 65,310 threshold rows and how they relate (or do not relate) to canonical identities.
4. **G0-05 source-only rows:** Investigate the reported 4,947 source-only rows. Identify their source, meaning, exclusions, and whether any are expected or unexplained.
5. **Canonical contract:** Inspect the full 60-field contract and determine, field by field or by defensible groups, which fields can be populated from real source rows, which are derived, missing, ambiguous, synthetic-only, or unsupported. Do not fill gaps by assumption.
6. **Disposition counts:** Trace the reported counts and exact definitions:
   - Rejection: 1,083 eligible, 31 rejected, 40 expired.
   - Breakout: 1,038 eligible, 1,823 rejected.
   - Failed breakout: 736 eligible, 30 rejected, 166 expired.
   Explain denominators, overlap, exclusions, and any apparent arithmetic or semantic inconsistencies.
7. Check timestamp alignment, join cardinality, key collisions, duplicate identities, nulls, source coverage, cluster consistency, and whether any population is silently filtered or counted more than once.
8. Recommend the **smallest safe next implementation task**, with precise input/output contracts and tests. Do not implement it.

### Evidence requirements
- Inspect the actual source, scripts, tests, reports, workflow definitions, and relevant commit history on `price-action-v1`.
- Cite exact repository paths and line numbers wherever possible; include relevant commit SHA(s) and workflow/run references.
- For every count, state its source artifact and counting unit. Clearly distinguish raw rows, cohort rows, physical events, unique identities, overlap clusters, and event/horizon rows.
- Separate independently verified facts from prior reported figures, assumptions, and unresolved questions.
- If you cannot reproduce a figure without executing code, say so. Do not imply that you ran scripts or tests unless you actually did.
- Report any mismatch between documentation, implementation, tests, and generated reports.

### Strict boundaries
- READ ONLY: do not edit files, create commits, open PRs, change workflows, or alter datasets.
- Do not execute research scripts or tests during this audit.
- Do not generate candidates, calculate PnL, backtest, optimize thresholds, rank strategies, or make profitability claims.
- Keep the five outside-retest fields descriptive only: `outside_retest`, `outside_retest_boundary_crossed`, `outside_retest_minutes`, `outside_retest_depth_pct_of_boundary`, `outside_retest_hold`.
- Do not close G0-05 or declare the gate passed unless the evidence fully supports that conclusion.

### Required response format
1. Executive conclusion: what is verified, unresolved, and blocking.
2. Population reconciliation table with counting unit, source, arithmetic, and status.
3. Module A, Module B, G0-04, and G0-05 findings.
4. Canonical 60-field sourceability assessment.
5. Disposition-count audit.
6. Risks and unresolved questions, ranked by severity.
7. Smallest safe next implementation task (proposal only), including exact files likely affected and acceptance tests.
8. Explicit statement confirming whether any code, tests, scripts, workflows, or data were changed/executed.

Treat this as an independent audit. Challenge earlier conclusions where evidence requires it; do not merely repeat prior summaries.
