# Agent activation decision record

## Decision status

**Activation remains blocked. No workflow is installed, enabled, or dispatched by this record.**

The agent implementation is isolated on `agent/okx-research-agent-v1`. The repository default branch is `main`. GitHub's `workflow_dispatch` trigger requires the workflow file to exist on the default branch before it can be manually dispatched. Therefore, adding a manual workflow only to the agent branch does not make that workflow manually runnable.

This is a repository activation constraint, not a defect in the task engine.

## Options

### Option A — separate agent repository (preferred isolation)

Create a dedicated repository whose default branch contains the agent workflow and agent code. The workflow would check out the research repository at an explicitly pinned, read-only ref and would publish only bounded artifacts.

Advantages:
- Keeps agent workflow and permissions separate from the research repository's default branch.
- Avoids introducing an agent activation bridge on `main`.
- Makes the workflow's own default-branch dispatch semantics straightforward.

Requirements:
- Repository owner must explicitly create/authorize the new repository.
- Configure least-privilege installation and Actions permissions.
- Pin all third-party actions to immutable commit SHAs.
- Check out research inputs read-only at an explicit commit/ref.
- Do not expose research write tokens, VPS credentials, or self-hosted runners.
- Start with manual preflight/report-only operation after the active research handoff permits validation.

### Option B — minimal dispatcher on `main`

Add a narrowly scoped manual-only dispatcher workflow to `main`, which calls a reviewed reusable workflow stored on the isolated agent branch. The caller's `uses:` reference must pin the reusable workflow to an immutable full commit SHA.

Advantages:
- Reuses the existing repository and its artifact storage.
- Can preserve the agent implementation on its isolated branch.

Risks and requirements:
- This is a deliberate exception to the current no-change-to-`main` boundary and requires explicit owner approval.
- The dispatcher must have minimal explicit permissions and no broad write token.
- The caller on `main` must declare `workflow_dispatch` only; the reusable callee must declare `workflow_call` only. The callee must not expose direct manual, push, pull-request, schedule, or other event triggers.\n- The caller's reusable-workflow reference must use an immutable full commit SHA; a branch name or mutable tag is insufficient.
- The workflow must not call inherited research workflows or execute research scripts.
- It must start as manual preflight/report-only; no scheduling, event triggers, queue execution, or research writes.

### Option C — push-trigger workaround

Do not use a push trigger on the agent branch as a substitute for a controlled manual activation path. It would make ordinary branch updates trigger automation and would not resolve the desired explicit activation and review boundary.

## Recommendation

Prefer **Option A**, a separate agent repository, if the owner is willing to create one. It provides the cleanest separation between research data/workflows and the operations agent. If a second repository is not acceptable, Option B can be reconsidered only after explicit approval for the smallest possible `main`-branch dispatcher change.

No option is authorized merely by being documented here. Do not create a repository, change `main`, add or enable workflows, change permissions/secrets, or dispatch any workflow without the required owner authorization and research-handoff permission.

## Current research lock

The active Phase 3 G0-05 handoff remains controlling. It prohibits the relevant script, test, and workflow execution and prohibits research code/data changes. This activation design does not override that handoff. Even after the repository activation constraint is resolved, the first permitted run must wait until the applicable handoff allows it and the deferred validation gates can be completed safely.

## Minimum first-run trust boundary

Before any future first run, the workflow must independently:
1. Resolve the exact task from the trusted queue at a pinned commit.
2. Re-check the current handoff, task digest, phase gate, allowlist, and operation permissions at the operation boundary.
3. Use a clean, isolated hosted runner with no VPS/self-hosted access.
4. Run only the explicitly permitted preflight/report-only path.
5. Retain the assignment-package digest in a trusted channel independent of worker-return content.
6. Verify checkout identity, clean state, input hashes, downloaded artifact name, run ID/attempt, and complete artifact bundle.
7. Preserve human-only task acceptance and phase-gate closure.

The current implementation contains pure decision and verification components for several of these steps, but no trusted dispatcher, authenticated delivery channel, atomic persistent event store, or workflow integration exists yet. Those are not to be inferred from the presence of the corresponding pure modules.
