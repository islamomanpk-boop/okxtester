# Engine side-effect and execution-boundary audit — 2026-11-27

## Scope

Static inspection of the current agent engine source on `agent/okx-research-agent-v1`, focused on filesystem effects, network/provider calls, task execution, dispatch, scheduling, persistence, and the meaning of `ALLOW_READ_ONLY`. Inspected: `safety_controller.py`, `task_runner.py`, `assignment_package.py`, `assignment_return.py`, `recovery_policy.py`, `event_ledger.py`, `persistence_contract.py`, `review_pipeline.py`, `review_artifact.py`, `artifact_preparation.py`, `batch_planner.py`, `evidence_verifier.py`, `supervisor_review.py`, `report_builder.py`, and `orchestration_coordinator.py`.

No source was imported or executed. No tests, scripts, workflows, research datasets, provider APIs, network probes, or live infrastructure were used.

## Findings

### 1. No operational worker dispatcher or task executor exists in the inspected engine

The public runtime path composes preflight, planning, assignment packaging, and recovery guidance. `orchestration_coordinator.py` explicitly returns `mode=orchestration_snapshot_only`, `decision=SNAPSHOT_ONLY`, `dispatch_permitted=False`, `execution_performed=False`, `queue_state_changed=False`, `persistence_performed=False`, and `scheduling_enabled=False`; package digests are marked `package_digest_stored=False`. Its module docstring says it has no filesystem, network, GitHub, dispatch, persistence, scheduling, or task-execution side effects.

`task_runner.py` loads the fixed queue file and returns preflight results. Its CLI description at lines 253–255 says it never executes tasks; `preflight_all_tasks()` at lines 234–250 returns a non-authorizing summary. The word “dispatcher” in some descriptive labels should not be confused with a worker/provider dispatcher.

### 2. `ALLOW_READ_ONLY` is a preflight decision, not execution authority

`safety_controller.py` returns `authorized=True`, `decision=ALLOW_READ_ONLY`, and `execution_performed=False` in the eligible read-only case (around lines 540–548). The Phase 3 global G0-05 lock is checked independently of task labels at lines 506–516 and denies every Phase 3 task while active. The controller's runtime entrypoint at lines 577–584 loads policy from fixed paths in the checkout, but this does not authenticate who published the checkout or prove effective GitHub permissions.

Therefore, `ALLOW_READ_ONLY` means only that the local policy evaluator's preflight checks passed for the exact queued task. It does not authorize an external worker, prove current handoff validity at a future dispatch boundary, or establish operational trust.

### 3. Existing filesystem interactions are read-only input access

- `task_runner.py:34–42` reads the queue using `Path.read_text()` and strict JSON parsing.
- `safety_controller.py:125–132` reads policy JSON files using `Path.read_text()`.
- `report_builder.py:48–55` opens repository-contained input files in binary read mode to compute SHA-256.
- `report_builder.py:425–443` builds an in-memory artifact bundle and explicitly states it never writes or uploads files.
- `artifact_preparation.py` composes queue/preflight/report/bundle inputs and is documented as no task work, queue update, filesystem write, upload, or scheduling.

No file-write, delete, subprocess, shell, socket, HTTP client, provider call, artifact upload, or scheduling call was identified in the inspected engine modules. This is a bounded static inspection, not a runtime sandbox proof or a guarantee about uninspected dependencies and future changes.

### 4. In-memory contracts are not durable or independently authenticated

`event_ledger.py` provides hash-chain primitives, while `persistence_contract.py` prepares an append against a supplied head; neither persists state or performs an atomic compare-and-swap. `assignment_package.py` creates a package but does not dispatch it. `orchestration_coordinator.py` calculates a package digest but explicitly marks it not independently stored. `assignment_return.py` depends on an independently retained expected package digest and does not prove delivery. `evidence_verifier.py` consumes caller-supplied commit/manifest/bytes and does not authenticate their source. `report_builder.py:535–539` says artifact verification does not authenticate the artifact service or uploader.

These are intentional pure/in-memory building blocks, not an end-to-end control plane.

### 5. Terminology should remain precise

Use these distinct terms in future documentation and UI:

- **Preflight:** local policy evaluation; no task work.
- **Plan:** proposed phase-ordered work; non-authorizing.
- **Assignment package:** prepared instructions and constraints; not delivered.
- **Dispatch attempt:** a future authenticated, durable operation at the provider boundary; not implemented.
- **Delivery receipt:** future authenticated evidence of provider acceptance/delivery; not implemented.
- **Worker execution:** future isolated task execution; not implemented.
- **Report artifact:** currently an in-memory bundle; no uploader or artifact-service trust is implemented in this engine.

## Disposition

Static review supports the conclusion that the inspected engine is a non-operational preflight/planning/review scaffold. No hidden task executor or provider dispatcher was identified in the inspected module set. This does not prove the entire repository, third-party dependencies, GitHub Actions environment, or future workflow is safe; those require separate review and authorized validation.

## Restrictions and next step

The active `docs/assistant_handoff/PHASE3_G0_05_RECONCILIATION_TASK_02.md` on `price-action-v1` remains authoritative and prohibits relevant scripts/tests/workflows and research-code/data changes. This audit does not relax that boundary. The smallest safe next step remains obtaining the independent read-only G0-05 review requested in issue #3, without issuing another Copilot task while the first remains outstanding.

No tests, scripts, workflows, research data, provider calls, deployments, or infrastructure changes were performed. No agent workflow is active; no unattended worker is running; no task was dispatched or executed.
