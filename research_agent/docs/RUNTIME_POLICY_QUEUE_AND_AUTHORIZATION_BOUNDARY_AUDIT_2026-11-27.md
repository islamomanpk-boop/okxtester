# Runtime policy, queue and authorization-boundary static audit — 2026-11-27

## Scope and conclusion

This is a static inspection of the agent configuration, task queue, allowlist, phase permissions, safety controller, and task-runner entry points. It does not execute preflight or any project code.

**Conclusion:** the current configuration is intentionally non-authorizing at several independent layers. The repository contains a fail-closed local authorization design, but its configuration is not enabled for operation and its policy files are not authenticated by an external trust service. This is a sound development hold, not evidence of operational authorization.

## Static facts from the current configuration

| Control | Current configured value | Effect |
|---|---|---|
| `agent_config.execution.enabled` | `false` | Controller denies before any read-only allowance can be returned. |
| `agent_config.scheduling.enabled` | `false` | No scheduled or event-driven operation is enabled. |
| `agent_config.execution.current_g0_05_execution_lock` | `true` | All Phase 3 task authorization is denied by a global phase lock. |
| `task_queue.queue_policy.execution_enabled` | `false` | Queue-level execution is disabled. |
| `phase_permissions.phases.phase3_sideways_range.execution_override` | `deny` | Phase 3 has no explicit read-only authorization override. |
| `task_allowlist.approved_tasks` | empty list | No task has an exact hash approval. |
| `phase_permissions` later phases | `queued`, override `deny` | Later phases remain non-active and denied. |

The task queue contains two Phase 3 G0-05 read-only documentation/reconciliation tasks marked `queued`, followed by one task for each later phase marked `blocked_until_prior_phases_complete`. The task queue policy also requires human-authorized prior gate closure and prohibits phase skipping and handoff override.

## Authorization path inspected

1. `task_runner.load_queue()` parses the fixed repository queue path and rejects duplicate JSON keys and non-standard numeric constants.
2. `_preflight_task_with_queue()` requires exactly one matching task ID and delegates authorization to `safety_controller.authorize_task()`; malformed or inconsistent responses become DENY.
3. `safety_controller.authorize_task()` uses the runtime policy-loading path, which reads fixed checkout policy files rather than accepting caller-provided policy or allowlist arguments.
4. `_authorize_task_impl()` validates exact policy schemas, branch isolation, scheduling state, execution flags, queue policy, queue IDs, exact task equality, task contract, allowlist identity/hash, phase order/status, prior human gate state, operation class, and Phase 3 G0-05 lock.
5. The controller returns an identity-bound `ALLOW_READ_ONLY` result only after all checks pass. The current static configuration reaches earlier deny conditions and cannot return that allowance.

## Independent deny conditions currently present

- Agent execution is disabled.
- Queue execution is disabled.
- The Phase 3 execution override is `deny`.
- The global G0-05 execution lock is `true`.
- The exact task allowlist has no approved entries.
- Phase 1, 2, 4 and 5 are not active and their execution overrides are `deny`.
- Scheduling is disabled.

These are independent configuration gates. Changing a task label, moving a task to another queue status, or supplying a different task object does not satisfy the fixed policy checks. The controller requires exact equality with the separately loaded queue definition and exact task digest approval.

## What this audit does and does not prove

**Confirmed by static source/config inspection:** the checked-in settings are disabled/deny-only as listed; the queue has two active-phase G0-05 task definitions and four blocked later-phase task definitions; the allowlist is empty; the controller's runtime path loads fixed policy documents; the task runner converts malformed controller results to DENY; the G0-05 lock explicitly denies every Phase 3 task.

**Not established:** authenticity or tamper resistance of policy files in Git; independent identity of a policy approver; actual GitHub effective token permissions; protection against an actor who can modify the branch and workflow together; atomic policy revalidation at a future external dispatch transaction; service availability; runtime behavior; or any successful task preflight.

The fixed repository paths are trusted only relative to the checkout supplied to the process. A future workflow must independently bind the exact checkout commit, clean state, protected branch policy, and policy-file digests to trusted workflow context. Local code cannot authenticate its own deployment or its own policy publisher.

## Recommendations

1. Preserve the current disabled/deny settings while G0-05 remains controlling. Do not add allowlist entries or change phase overrides as a convenience.
2. Keep the runtime controller's fixed-path policy loading separate from private test seams; do not expose caller-controlled policy inputs in a future production API.
3. Before any future activation, require independently authenticated policy release/version and protected-branch provenance, not merely a matching file hash supplied by the same job.
4. Make the future dispatcher re-check the live handoff, phase gate, task digest, allowlist revision and emergency hold inside the same trusted transaction that records dispatch start.
5. Keep queue status descriptive rather than authoritative; status alone must never confer execution permission.
6. Add adversarial synthetic tests for task substitution, duplicate queue IDs, empty/duplicate allowlist entries, changed policy revision, relabelled Phase 3 tasks, stale phase gate, malformed controller response and concurrent revocation—but only after a controlling handoff explicitly permits test execution.

## Current status and non-claims

Static review only. No preflight, tests, scripts, workflows, provider calls, research-data access, VPS operations, deployments, credentials, services, permissions or infrastructure were executed, changed, or configured. No task was authorized or dispatched. The agent remains non-operational; Phase 3 G0-05 remains controlling.
