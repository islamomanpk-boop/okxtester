# Handoff binding and phase-policy enforcement audit — 2026-11-27

## Scope and method

Static comparison of agent_config.json, phase_permissions.json, task_queue.json, task_allowlist.json and engine/safety_controller.py. The audit asks whether the active handoff identity and phase-policy metadata are enforced as invariants, rather than merely present in the current queue.

No code was executed or modified. No tests, scripts, workflows, research data, provider services, or infrastructure were accessed.

## Current checked-in posture

The current configuration is multiply deny-only:
- agent_config.execution.enabled=false and scheduling.enabled=false.
- execution.current_g0_05_execution_lock=true.
- Phase 3 execution_override=deny and its G0-05 restrictions are marked prohibited.
- task_queue.queue_policy.execution_enabled=false.
- task_allowlist.approved_tasks is empty.
- Later phases remain blocked until prior phases are human-authorized closed.

The queue contains two Phase 3 tasks marked workstream=g0_05 and bound to PHASE3_G0_05_RECONCILIATION_TASK_02; later-phase tasks are blocked. These facts mean the gaps below do not create a current execution path: multiple independent deny conditions remain active.

## Findings

### HBP-01 — G0-05 workstream is not structurally required to carry the exact handoff ID

_validate_task_contract() (approximately lines 40–75) treats both workstream and handoff_id as optional fields. It validates that either optional value is a non-empty string when present, but does not require handoff_id whenever workstream == g0_05.

Later, _authorize_task_impl() (approximately lines 506–529) recognizes a G0-05 task when either its workstream equals g0_05 or its handoff ID equals the current handoff. It then checks the G0-05 policy restriction values. It does not require the task handoff ID to equal the exact active handoff identifier.

Consequently, if the global G0-05 lock and other deny controls were deliberately lifted in a future authorized change, a newly allowlisted task could be marked workstream=g0_05 while omitting or changing handoff_id and still satisfy the current conditional G0-05 restriction check. Exact queue equality and task hashing protect approved task bytes, but do not prove those bytes are bound to the currently authoritative handoff.

Recommended hardening before any future Phase 3 authorization: make handoff identity a required, exact policy binding for every task in a handoff-governed workstream. Require the exact current handoff ID in the task contract and compare it with an independently configured expected handoff ID at authorization time. Missing, stale, mismatched, or ambiguous handoff identity must deny. Keep the global lock independent and fail-closed.

### HBP-02 — phase_permissions.task_scope is schema-required but not semantically enforced

The Phase 3 rule exact-key schema includes task_scope (approximately lines 246–258), but the phase-rule validation loop only checks priority, status and execution_override types/values (approximately lines 264–268). The authorization path does not compare task_scope with the task scope or a handoff-derived scope.

The current value follow_current_handoff_and_gate_status is therefore descriptive metadata, not an enforced scope constraint. Actual task scope is carried in the exact queued task and protected by the task hash, but that is not equivalent to proving it remains within the active handoff's permitted scope.

Recommended hardening: either rename/document this field as non-authorizing metadata, or define and enforce a versioned scope-policy contract that intersects task scope with the exact active handoff's allowed scope. Do not treat the current field as a security control.

### HBP-03 — Current deny controls are effective in configuration, but not a substitute for the missing binding

The current lock (current_g0_05_execution_lock=true), Phase 3 execution_override=deny, disabled global/queue execution, and empty allowlist prevent authorization now. This audit does not recommend changing any of them. It records latent contract gaps to resolve before a future owner-approved policy transition, not an instruction to unlock or run anything.

## Required future acceptance evidence

Before any future Phase 3 authorization is considered, an independently reviewed change should demonstrate:
1. Every handoff-governed task has a mandatory exact handoff identifier.
2. The authorization policy independently supplies the expected active handoff identifier; task content cannot choose or replace it.
3. Missing, stale, mismatched and wrong-workstream handoff combinations all deny.
4. Effective scope is constrained by both task scope and authoritative handoff scope.
5. Existing global G0-05 lock, phase override, execution-disabled state and empty allowlist remain unchanged unless separately approved through the owner/security decision process.
6. Tests are run only after the authoritative research handoff explicitly permits the exact validation activity and required owner authorization exists.

## Disposition

This is a static design/code-contract finding, not evidence of a current bypass or execution. Current configuration remains deny-only. The recommendations are future hardening requirements; no code change is made under the active G0-05 handoff.

No tests, scripts, workflows, task execution, dispatch, provider calls, research-data operations, or infrastructure changes were performed. No agent workflow is active and no unattended worker is running.


## Source-location precision follow-up

The source-level boundary is more specific than the approximate references above:

- In `research_agent/engine/safety_controller.py`, lines 246–258 require the Phase 3 rule to contain a `task_scope` key, but do not validate its value or type.
- Lines 264–268 validate only `priority`, `status`, and `execution_override` in the phase-rule loop. No `task_scope` check occurs there.
- Lines 463–486 retrieve the selected phase rule and enforce active-phase status plus `execution_override`; they do not read `phase_rule["task_scope"]` or intersect it with `queued_task["scope"]`.
- Lines 506–530 enforce the independent global G0-05 lock and conditional G0-05 restriction values. The current checked-in `agent_config.json` keeps `current_g0_05_execution_lock=true`, while `phase_permissions.json` keeps Phase 3 `execution_override="deny"`; the queue also has execution disabled and the allowlist is empty.

Accordingly, `task_scope="follow_current_handoff_and_gate_status"` is not merely missing an intersection operation: it is not validated as a meaningful policy value by the controller at all. This remains a latent future authorization-contract gap, not a current execution path. The hard lock must not be weakened to test it.


## Static test-coverage observation

A read-only inspection of `research_agent/tests/test_safety_controller.py` found that `task_scope` is supplied as a fixture default (lines 28–50), but no test in that file directly mutates it to an unknown, malformed, or out-of-scope value and asserts denial. The Phase 3 lock tests at lines 253–265 and 453–467 verify denial while the global lock is active; they do not establish future scope-intersection behavior when the lock is lifted. This is a source-level coverage observation only. No test was run, and no claim is made about tests outside this file.
