# Five-Phase Research Support Matrix

## Purpose

`okx-research-agent` is a reusable operations and evidence-reconciliation agent for the complete OKX Price Action V1 research sequence. It is not a Phase 3-only tool. The same safety controller, ordered queue, provenance checks, and report format apply across all five phases.

This document defines the shared support model without inventing phase-specific research definitions or overriding any active handoff.

## Authoritative phase order

1. Phase 3 — Sideways / Range
2. Phase 1 — Uptrend / Bullish
3. Phase 2 — Downtrend / Bearish
4. Phase 4 — Choppy / High Volatility
5. Phase 5 — Transition / Expansion

The order in this document must remain consistent with `config/phase_permissions.json` and `config/task_queue.json`. A later phase remains blocked until every required earlier phase has been formally closed by human authority.

## Shared capabilities in every phase

Once that phase is eligible and its current handoff permits the activity, the agent may support:

- **Repository and evidence discovery:** locate existing phase documents, research outputs, manifests, source snapshots, checkpoints, and relevant code references without changing them.
- **Evidence mapping:** connect findings to exact files, commits, source records, and declared provenance.
- **Consistency review:** compare documented counts, definitions, schema fields, and report claims; distinguish confirmed facts from assumptions and unresolved discrepancies.
- **Gap and dependency tracking:** list missing evidence, unresolved questions, prerequisites, and blockers without silently resolving them.
- **Deterministic reporting:** prepare structured JSON/Markdown reports with task identity, repository/branch/commit context, input hashes, findings, limitations, and explicit not-run/blocked statuses.
- **Operational follow-through:** keep the task queue and phase-readiness record aligned with the approved phase order; never self-approve completion or advance a gate.

The agent must read the active phase's handoff before selecting or performing work. A handoff may narrow or prohibit any capability above. The most restrictive applicable rule wins.

## Phase-specific queue coverage

| Order | Phase | Initial queue task | Eligibility |
|---:|---|---|---|
| 1 | Phase 3 — Sideways / Range | G0-05 real-row identity/source-lineage reconciliation; handoff/provenance documentation review | Active, but current G0-05 handoff restricts work to permitted read-only reconciliation. |
| 2 | Phase 1 — Uptrend / Bullish | Inspect existing evidence and document readiness, missing evidence, and dependencies | Blocked until Phase 3 is human-authorized closed and Phase 1's own handoff permits the task. |
| 3 | Phase 2 — Downtrend / Bearish | Inspect existing evidence and document readiness, missing evidence, and dependencies | Blocked until Phase 1 is human-authorized closed and Phase 2's own handoff permits the task. |
| 4 | Phase 4 — Choppy / High Volatility | Inspect existing evidence and document readiness, missing evidence, and dependencies | Blocked until Phase 2 is human-authorized closed and Phase 4's own handoff permits the task. |
| 5 | Phase 5 — Transition / Expansion | Inspect existing evidence and document readiness, missing evidence, and dependencies | Blocked until Phase 4 is human-authorized closed and Phase 5's own handoff permits the task. |

These initial queue entries are readiness/reconciliation tasks, not permission to run research pipelines. Before a phase begins, its task scope must be expanded only from that phase's actual handoff and approved research plan; do not copy Phase 3 assumptions or G0-05 rules into another phase.

## Restrictions that apply across phases

Unless a future, explicit, phase-specific authorization changes the applicable boundary, the agent must not:

- execute research scripts, tests, or workflows;
- modify research data, canonical definitions, or source datasets;
- generate trading candidates, run backtests, make PnL claims, or select strategies;
- close research gates or advance phases;
- merge branches, commit to `price-action-v1`, deploy to a VPS, or change secrets/permissions.

The current G0-05 prohibition is a global Phase 3 authorization lock in the safety controller. It must not be bypassed by relabelling tasks, using a different queue entry, dispatching an inherited workflow, or moving work into another phase.

## Phase lifecycle

1. Read the phase's current handoff and identify its exact permitted scope.
2. Check predecessor gate status and phase permission.
3. Select only an exact queued task whose definition is approved through the trusted task-hash allowlist.
4. Perform only the permitted read-only work; if execution is not authorized, remain at preflight/report-only.
5. Produce a provenance-bound report that states findings, gaps, limitations, and what was not run.
6. A human reviews evidence and decides whether the phase gate is closed.
7. Only after human-authorized closure may the next phase become eligible.

## Current implementation status

- Shared five-phase ordering and six initial queue tasks are configured.
- Phase 3 has two read-only G0-05 tasks; the four later-phase readiness tasks are blocked.
- The safety controller validates the complete queue and requires human-authorized predecessor closure.
- The task runner is currently a preflight-only dispatcher; there is no research-task executor.
- Execution, scheduling, and task allowlist approval remain disabled/empty.
- Regression tests are authored but have not been executed because the current research handoff prohibits test execution.
- This matrix is a design and queue-coverage record, not evidence that the agent is operational or that any research phase is complete.
