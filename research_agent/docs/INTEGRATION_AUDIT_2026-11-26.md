# Agent integration audit — 2026-11-26

## Scope and method

Static inspection only on `agent/okx-research-agent-v1`. This review follows the controlling Phase 3 G0-05 boundary: no project scripts, tests, notebooks, workflows, Actions, or research code/data were executed or modified. This document is an integration-readiness record, not an activation approval.

Inspected the current source for the safety controller, task preflight, batch planner, assignment packaging and return review, evidence verification, report/artifact builder, event ledger, persistence contract, recovery policy, orchestration coordinator, and trusted-store design.

## What is connected today

1. **Queue → preflight:** `task_runner.py` loads the repository queue and calls `authorize_task()`; queue-wide preflight is a non-authorizing summary.
2. **Preflight → planning:** `batch_planner.py` requires exact per-task preflight rows, checks the fixed Phase 3 → 1 → 2 → 4 → 5 order, and emits a plan only. The runtime wrapper uses one queue snapshot.
3. **Plan → assignment package:** `orchestration_coordinator.py` packages selected and deferred tasks. Every package explicitly remains undispatched and unexecuted.
4. **Worker return → review:** `assignment_return.py` binds a return to an independently retained package digest, then calls the structural/evidence review pipeline. Passing is human-review-only.
5. **Review → artifact:** `review_artifact.py` builds a provenance-checked, in-memory three-file report bundle. It does not write or upload files.
6. **Event/recovery primitives:** `event_ledger.py`, `persistence_contract.py`, and `recovery_policy.py` provide pure in-memory validation/classification. They are not wired to a store, dispatcher, or queue-state mutation.

## Integration gates and consequences

### A. Current preflight is intentionally deny-only while execution switches are off

The checked-in agent configuration keeps agent execution disabled and queue execution disabled; the trusted allowlist is empty. The safety controller checks these switches before it can return `ALLOW_READ_ONLY`. Consequently, the current runtime preflight cannot produce an allowed task under the checked-in configuration. The planner will therefore not produce a dispatch-ready batch; it can only report blocked/deferred work.

This is safe and consistent with the current inactive state. It does mean the first manual validation should be described as a **blocked/preflight-only readiness artifact**, not as proof that an approved task can pass. If a later activation design needs positive preflight evidence while task execution remains disabled, introduce a separately specified non-authorizing readiness evaluation; do not simply turn on execution switches or reinterpret a DENY.

### B. Assignment binding has no trusted digest-retention channel yet

`assignment_package_digest()` calculates the exact package digest, and return review requires an independently retained expected digest. The coordinator currently returns `package_digest_stored: false`. No trusted dispatcher or protected handoff channel retains the digest. A future dispatcher must store it independently of worker-controlled data and bind it to the exact task, package, run, and delivery identity before accepting a return.

### C. Event history is not durable or authenticated

The event ledger validates a local hash chain and exact replay facts, but it does not authenticate the source, protect the chain head, or persist atomically. The trusted-store document correctly requires an authenticated source namespace and delivery ID, protected checkpoint, uniqueness constraints, and atomic append/checkpoint update. Do not treat an artifact, worker submission, or caller-supplied ledger as the trusted event store.

### D. Recovery classifications are advisory only

Recovery observations passed to the coordinator are explicitly unauthenticated. The recovery policy cannot determine whether a delivery really occurred. A future adapter must authenticate delivery receipts and reconcile uncertain outcomes before any retry. Automatic dispatch/retry must remain disabled.

### E. Artifact provenance is a caller/workflow responsibility

The report and artifact builders accept runtime facts from their caller. Their verifiers check consistency against independently supplied expected values, but do not themselves authenticate GitHub event context, checkout cleanliness, the artifact service, or the uploader. A future workflow must derive repository/ref/SHA/run identifiers from trusted workflow context, verify the checkout is clean at the exact expected commit, derive file manifests from that checkout, upload the complete three-file bundle, then download and verify it against trusted run/task context.

### F. Manual workflow activation remains blocked by repository topology

The agent workflow exists only on the isolated agent branch. GitHub manual `workflow_dispatch` requires the workflow file on the repository default branch (`main`). No approved activation bridge or separate agent repository exists. Do not use a push trigger as a workaround, and do not modify `main`, create a repository, change permissions/secrets, enable schedules, or touch the VPS without explicit user approval.

### G. Independent review is still pending

GitHub issue #3 contains the prepared read-only Copilot instruction, but the issue has no Copilot findings comment. The independent Phase 3 G0-05 review is therefore not complete and must not be represented as assigned, running, or finished.

## Required order before unattended operation

1. Obtain the independent G0-05 review and reconcile its findings without violating the controlling handoff.
2. Resolve the activation topology with explicit owner approval: reviewed minimal default-branch dispatcher or separate agent repository.
3. Define a non-authorizing readiness/preflight mode if positive readiness evidence is required while execution remains disabled.
4. Approve a trusted persistence backend and threat model; implement source authentication, protected checkpoint, atomic append, and delivery idempotency.
5. Implement a trusted dispatcher that retains assignment-package digests independently and verifies current task/handoff/phase/allowlist at the operation boundary.
6. Implement a least-privilege manual-only workflow that verifies checkout provenance and artifact round-trip integrity.
7. Wait until the controlling research handoff explicitly permits the exact validation scope; then run syntax, unit, integration, denial-path, and manual artifact checks.
8. Keep schedules and event triggers disabled until manual operation and recovery behavior have passed independent review.

## Current status

- Agent branch remains isolated; no research-branch merge is proposed.
- The current implementation is a non-executing foundation, not an operational unattended agent.
- No durable store, trusted dispatcher, active agent workflow, schedule, or event trigger is configured.
- No test or script has been executed; authored test counts are not runtime validation.
- No task execution, dispatch, research data/code change, candidate generation, backtest, PnL claim, gate closure, or phase advancement is authorized by this audit.
