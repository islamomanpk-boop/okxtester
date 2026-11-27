# Agent documentation consistency audit — 2026-11-27

## Status and authority

Static documentation and repository-metadata review only. This audit does not authorize code changes, tests, scripts, workflows, dispatch, scheduling, backend provisioning, research execution, gate closure, or phase advancement. The Phase 3 G0-05 handoff remains controlling.

## Scope

Reviewed the current agent-branch snapshot and compared the following cross-document contracts:

- agent identity, branch isolation, default-branch activation constraint, and workflow status;
- research phase order and G0-05 restrictions;
- assignment/package digest custody and dispatch/delivery trust boundaries;
- event identity/idempotency and canonicalization versioning;
- task acceptance versus phase-gate closure;
- test-count reporting and the distinction between authored and executed tests.

Inspected the current README, workflow design, activation decision, implementation-readiness checklist, trusted registry interface, dispatcher contract, unified lifecycle specification, trust-root architecture, threat model, and trust-boundary crosswalk. This is a targeted consistency pass, not an exhaustive line-by-line audit of every source file or every document.

## Findings

### C-01 — stale agent-file count in workflow design

**Severity:** Low; documentation accuracy only.

`research_agent/WORKFLOW_DESIGN.md` described the agent implementation as “all 13 agent files” on the isolated branch. The current GitHub compare of `price-action-v1...agent/okx-research-agent-v1` reports 66 changed files, all under `research_agent/`. The statement is now stale because the agent scaffold and its documentation expanded substantially.

**Disposition:** Corrected in this commit to describe the branch/path isolation without embedding a stale file count. The branch comparison is a snapshot, not a permanent file-count guarantee.

### C-02 — authored-test count is internally consistent, but remains unexecuted

The README and validation document both report 236 authored regression tests, with the same 15 component counts. Neither claims they passed; both explicitly state that none were executed. This is consistent with the current G0-05 prohibition. No test was run during this audit.

**Disposition:** No change required.

### C-03 — workflow activation and default-branch constraint are consistent

The workflow design, activation decision, implementation-readiness checklist, and trust-root architecture consistently identify `main` as the repository default branch and the agent branch as isolated. They correctly state that an agent-only `workflow_dispatch` file is not a usable manual entrypoint under this repository topology, and that a separate agent repository or explicitly approved default-branch bridge would be required.

**Disposition:** No activation workaround introduced. No `main` change, repository creation, workflow installation, or trigger change was made.

### C-04 — package digest custody remains a design blocker, not an implemented control

The assignment-return code can verify against an independently supplied expected package digest, but the documents consistently state that no trusted dispatcher/registry currently retains that digest. The registry and dispatcher documents define future requirements; the current pure modules do not provide durable custody or authenticated delivery.

**Disposition:** No implementation claim elevated. Keep activation blocked until an independently trusted retention path exists and is validated.

### C-05 — event identity levels and canonicalization boundaries remain explicit

The crosswalk and registry interface distinguish provider-delivery identity `(source_namespace, delivery_id)` from lifecycle-event idempotency identity `(source_namespace, delivery_id, event_role)`. The event-ledger implementation remains Python-serialization-specific; future cross-runtime writers/verifiers require a versioned canonicalization contract and shared test vectors. Existing v1 hashes must not be silently migrated.

**Disposition:** No schema/hash migration or code change made.

### C-06 — human task disposition remains separate from research phase-gate closure

The reviewed lifecycle, registry, dispatcher, threat, and readiness documents consistently reserve task acceptance/rejection/revision for a human disposition and keep phase-gate closure as a separate authority and evidence decision. Current G0-05 restrictions continue to prohibit closure.

**Disposition:** No authority boundary changed.

### C-07 — provider-delivery lookup and event-receipt lookup were conflated

**Severity:** Moderate; future backend-interface ambiguity.

The registry interface named a read port `lookup_delivery(source_namespace, delivery_id, event_role)`, which returns an event-role receipt. The store-adapter design used the same `lookup_delivery(source_namespace, delivery_id)` name for the complete provider-delivery aggregate. The underlying identity model was correct—delivery pair versus event-role triple—but the interface names and signatures did not express the distinction consistently.

**Disposition:** Corrected both specifications. The provider-level read is now `lookup_provider_delivery(source_namespace, delivery_id)` and returns the complete aggregate with linked per-role receipts. The event-level read is `lookup_event_receipt(source_namespace, delivery_id, event_role)` and resolves one closed-schema event-role idempotency record. The unified transaction protocol continues to perform replay using the event-level tuple. No implementation or backend was created.

## Current verified snapshot

- Repository: `islamomanpk-boop/okxtester`.
- Compared refs: `price-action-v1...agent/okx-research-agent-v1`.
- Historical compare recorded when this audit was first written: 489 commits ahead, 0 behind; 66 changed files, all under `research_agent/`. This is a dated snapshot, not the current branch state; obtain a fresh compare before relying on counts.
- Agent-specific workflow: none installed or active.
- Agent workflow runs: none reported in the latest inspected state.
- Runtime validation: not performed; the authored regression suite remains unexecuted.
- Research authority: G0-05 remains controlling; no scripts, tests, workflows, dispatch, scheduling, or research operations were performed.

## Conclusion

The targeted cross-document review found one stale numeric description and corrected it. The principal safety and activation boundaries reviewed here remain aligned: no trusted backend or dispatcher is operational, no independent package-digest custody exists, no agent workflow is active, and the default-branch activation constraint is unresolved. The audit does not certify the system or authorize the next implementation stage.
