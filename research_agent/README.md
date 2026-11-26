# OKX Research Agent

`okx-research-agent` is a free-first, deterministic research-operations agent for the OKX Price Action V1 repository. It is designed to organize approved work, inspect permitted evidence, and produce reproducible reports through GitHub Actions.

## Current status

- Foundation configuration, fail-closed safety controller, phase-ordered task queue, and empty trusted allowlist are present.
- Agent execution and scheduling remain disabled.
- Repository inspection is read-only by default.
- No unattended general-purpose LLM is assumed or required.
- Reports are intended for GitHub Actions artifacts.
- Work is organized in the agreed order: Phase 3, Phase 1, Phase 2, Phase 4, Phase 5.
- No automatic merge or write to the research branch is permitted.
- The safety controller, task queue, and report builder have not been runtime-tested; no scripts, tests, or workflows have been run as part of this setup.
- The safety controller binds approvals to the SHA-256 hash of the exact queued task definition; changing its phase, operation, scope, or restrictions invalidates that approval.
- The public runtime authorization function loads policy only from fixed repository configuration paths; policy injection is isolated to a private test seam.
- Markdown report rendering flattens line breaks and escapes Markdown control characters in untrusted findings and metadata.
- Report validation enforces a strict top-level schema, string-only narrative lists, canonical UTC timestamps ending in `Z`, normalized safe manifest paths, and finite JSON values.
- While the current G0-05 lock is active, all Phase 3 task authorization is denied, regardless of task labels.
- Only tasks marked `queued` in the currently active phase are eligible for future evaluation; later phases remain blocked.

## Hard safety boundary: Phase 3 G0-05

The current G0-05 handoff requires read-only reconciliation and explicitly prohibits running scripts, tests, or workflows, changing code or data, generating candidates, backtesting, making PnL claims, selecting strategies, or closing G0-05. This restriction takes precedence over general agent permissions. The agent must not bypass it through another workflow, task, or trigger.

## Permission model

Every proposed task must pass all of these checks before it can be considered for execution:

1. The task ID is explicitly present in the trusted task allowlist.
2. Its phase is recognized and has the relevant permission.
3. No current handoff or gate restriction prohibits the operation.
4. The operation is in the controller's narrow read-only allowlist.
5. The agent execution master switch is enabled.

A missing, ambiguous, malformed, or conflicting permission means **deny**. The task itself cannot grant its own permission. The current trusted allowlist is intentionally empty.

## Components

- `config/agent_config.json` — identity, operating mode, scheduling defaults, and global prohibitions.
- `config/phase_permissions.json` — phase order and operation-level permission boundaries.
- `config/task_queue.json` — initial phase-ordered task definitions and dependencies.
- `config/task_allowlist.json` — trusted task-definition hash approvals; currently empty.
- `engine/safety_controller.py` — fail-closed evaluator that requires an exact queue match, a trusted SHA-256 approval, an active phase, and read-only permission; it never executes tasks.
- `engine/task_runner.py` — preflight-only queue dispatcher; it selects an exact queue entry and asks the safety controller for a decision, but has no subprocess, script, test, workflow, or research executor.
- `engine/report_builder.py` — deterministic JSON/Markdown report formatting, repository-contained input SHA-256 manifests with symlink rejection, escaped untrusted Markdown values, strict report validation, and report digest; not runtime-tested.
- Regression coverage authored but not executed: 9 safety-controller tests, 13 report-builder tests, and 5 task-runner tests (27 total).
- `.github/workflows/` — no agent-specific workflow is installed yet. The first future workflow must be manual-dispatch only and preflight/report-only; event-driven and scheduled triggers require separate validation and approval.

## Validation and activation gates

See [VALIDATION_AND_ACTIVATION.md](VALIDATION_AND_ACTIVATION.md) for completed setup, deferred runtime checks, and conditions for safe activation. Static review does not count as runtime validation.

## Activation policy

Creating this scaffold does not authorize running it. Do not add or enable any agent workflow until the safety controller, task allowlist, and independent validation are complete and the applicable research handoffs permit execution. The G0-05 handoff remains authoritative even if a future agent configuration is changed.
