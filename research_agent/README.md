# OKX Research Agent

`okx-research-agent` is a free-first, deterministic research-operations agent for the OKX Price Action V1 repository. It is designed to organize approved work, inspect permitted evidence, and produce reproducible reports through GitHub Actions.

## Current status

- Foundation configuration only; automation is not enabled.
- Repository inspection is read-only by default.
- No unattended general-purpose LLM is assumed or required.
- Reports are intended for GitHub Actions artifacts.
- Work is organized across all five research phases in the agreed order: Phase 3, Phase 1, Phase 2, Phase 4, Phase 5.
- No automatic merge or write to the research branch is permitted.

## Hard safety boundary: Phase 3 G0-05

The current G0-05 handoff requires read-only reconciliation and explicitly prohibits running scripts, tests, or workflows, changing code or data, generating candidates, backtesting, making PnL claims, selecting strategies, or closing G0-05. This restriction takes precedence over general agent permissions. The agent must not bypass it through another workflow, task, or trigger.

## Permission model

Every future task must pass all of these checks before execution:

1. The task is explicitly present in the task allowlist.
2. Its phase is enabled for that exact operation.
3. No current handoff or gate restriction prohibits the operation.
4. The operation is within the free-only budget and repository scope.
5. The operation does not require human approval that has not been granted.

A missing, ambiguous, or conflicting permission means **deny**.

## Planned components

- `config/agent_config.json` — identity, operating mode, scheduling defaults, and global prohibitions.
- `config/phase_permissions.json` — phase order and operation-level permission boundaries.
- `engine/safety_controller.py` — planned fail-closed enforcement (not yet implemented).
- `engine/task_runner.py` — planned allowlisted task execution (not yet implemented).
- `engine/report_builder.py` — planned reproducible report generation (not yet implemented).
- `.github/workflows/` — planned event-driven orchestration; must remain disabled until separately reviewed and approved.

## Activation policy

Creating this scaffold does not authorize running it. Do not add or enable scheduled/event-triggered workflows until the safety controller, task allowlist, and independent validation are complete and the applicable research handoffs permit execution.
