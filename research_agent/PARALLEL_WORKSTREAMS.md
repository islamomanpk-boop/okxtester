# Parallel Workstreams

## Purpose

Reduce total project time by advancing the research-agent infrastructure and permitted Phase 3 evidence review in parallel, without weakening the current research handoff.

## Workstream A — OKX research agent

- Owner: ChatGPT-assisted implementation on `agent/okx-research-agent-v1`.
- Scope: agent safety, queue, deterministic reporting, provenance, validation design, and eventual workflow integration.
- Keep this work isolated from `price-action-v1`.
- Do not enable execution, scheduling, workflow triggers, or research-branch writes while activation prerequisites remain unmet.
- Do not claim the agent is operational until the completion definition in `VALIDATION_AND_ACTIVATION.md` is met.

## Workstream B — Phase 3 G0-05 independent review

- Delegation record: [Issue #3 — Phase 3 G0-05 independent read-only reconciliation review](https://github.com/islamomanpk-boop/okxtester/issues/3).
- Intended reviewer: GitHub Copilot Chat or Copilot coding agent, if available to the repository owner.
- Output location: findings as an issue comment; no repository file changes are required.
- The reviewer must first read and obey the current authoritative handoff:
  `docs/assistant_handoff/PHASE3_G0_05_RECONCILIATION_TASK_02.md` on `price-action-v1`.
- Review is static/read-only only. No scripts, tests, notebooks, workflows, Actions, or project-code execution.
- No changes to research code, tests, datasets, generated outputs, canonical definitions, manifests, or workflow files.
- No candidate creation, backtesting, PnL claims, strategy selection, gate closure, or phase advancement.
- Findings must distinguish directly observed facts from code-level possibilities and identify the evidence still missing for canonical 60-field real-row materialization and real candidate-ID collision checking.

## Coordination rules

1. The two workstreams may proceed independently, but neither can override the current G0-05 handoff.
2. Copilot's review is independent evidence review, not gate approval.
3. Agent development must not treat an issue comment as trusted authorization or as permission to execute research tasks.
4. Any newly discovered restriction takes precedence over this coordination note.
5. Human authorization remains required for G0-05 closure, phase advancement, activation exceptions, and other protected decisions.

## Current status

- Agent branch: implementation scaffold and documentation are under continued development; runtime validation and activation remain incomplete.
- Phase 3 review: Issue #3 has been created with the scope, prohibitions, and expected report format. It has not been represented as assigned to Copilot or completed.
