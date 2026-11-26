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
- The safety controller, task queue, report builder, and artifact-preparation layer have not been runtime-tested; no scripts, tests, or workflows have been run as part of this setup.
- The safety controller binds approvals to the SHA-256 hash of the exact queued task definition; changing its phase, operation, scope, or restrictions invalidates that approval.
- Trusted policy JSON loading rejects duplicate object keys rather than accepting the parser's last-value-wins behavior.
- The safety controller validates every queue entry's full contract (including blocked future-phase tasks) and rejects duplicate queue IDs, malformed allowlist hashes, duplicate allowlist approvals, phase-priority mismatches (with strict integer typing), boolean-type confusion, missing human-gate advancement rules, unsupported or missing policy keys, schema-version drift, and weakened global operation defaults, incomplete task contracts, duplicate scope/prohibition entries, unsupported task fields, missing mandatory prohibitions, and non-human completion authority. It also enforces read-only repository access, the exact isolated branch policy, no automatic merge/research-branch commits, and disabled scheduling.
- The public runtime authorization function loads policy only from fixed repository configuration paths; policy injection is isolated to a private test seam.
- Markdown report rendering flattens line breaks and escapes Markdown control characters in untrusted findings and metadata; untrusted values are not placed inside Markdown code spans, preventing delimiter breakout.
- Report validation enforces a strict top-level schema, the fixed `okx-research-agent` identity, string-only narrative lists, canonical UTC timestamps ending in `Z`, normalized safe manifest paths, finite JSON values, and only allowlisted non-completion statuses (`preflight_only`, `blocked`, `skipped`, `not_run`). Task-definition hashing additionally rejects non-string object keys, non-finite numbers, and Python-only values before canonical JSON serialization. The safety controller and report builder now use the same digest function; a report-task binding verifier checks task ID, phase, and digest against the exact trusted task object.
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
- `engine/task_runner.py` — preflight-only queue dispatcher with exact single-task checks and a bounded whole-queue visibility summary; it has no subprocess, script, test, workflow, or research executor.
- `engine/report_builder.py` — deterministic JSON/Markdown reports, safe input manifests, provenance checks, in-memory artifact bundle creation, and downloaded-artifact verification. It performs no filesystem writes or uploads.
- `engine/artifact_preparation.py` — joins the trusted queue, one task's preflight result, the preflight-only report factory, and in-memory artifact bundling. It is restricted to this repository and isolated agent branch. A denial becomes a blocked audit artifact; the module performs no task work, queue updates, filesystem writes, uploads, or scheduling. Runtime workflow metadata must be independently supplied and verified by a future workflow. See [ARTIFACT_PREPARATION.md](ARTIFACT_PREPARATION.md).
- `engine/batch_planner.py` — creates a bounded phase-ordered assignment plan from exact preflight results and carries forward the full task scope, prohibited actions, handoff ID, and task-definition digest. It never skips an earlier blocked phase, never treats a plan as authorization, and never executes or changes task state. See [BATCH_PLANNER.md](BATCH_PLANNER.md).
- `engine/supervisor_review.py` — validates untrusted worker submissions against the exact trusted task, including task digest, a fail-closed allowlist of declared read-only actions, evidence-reference shape (including Windows drive-path rejection), and safety claims. A valid submission is only marked ready for human review; evidence bytes and research correctness remain unverified, and task/gate completion are never approved. See [SUPERVISOR_REVIEW.md](SUPERVISOR_REVIEW.md).
- `engine/evidence_verifier.py` — compares worker-declared evidence hashes and checkout bytes against a caller-supplied manifest for one exact commit. It is pure/read-only and does not authenticate the caller or obtain Git data; a future workflow must supply trusted commit context. Passing integrity checks never approves task completion or gate closure. See [EVIDENCE_VERIFICATION.md](EVIDENCE_VERIFICATION.md).
- `engine/review_pipeline.py` — joins structural supervisor review with independent evidence-integrity checks. Structural/safety failures stop before evidence verification; hash or byte mismatches return the submission for revision. A passing result remains human-review-only. See [REVIEW_PIPELINE.md](REVIEW_PIPELINE.md).
- `engine/assignment_package.py` — binds the exact trusted task, preflight outcome, and batch-planner entry into a complete worker handoff. It carries the handoff ID, scope, prohibitions, digest, and submission schema; it never dispatches a worker or grants execution authority. Under the active G0-05 lock it records a blocked package. See [ASSIGNMENT_PACKAGE.md](ASSIGNMENT_PACKAGE.md).
- `engine/assignment_return.py` — verifies a returned submission against the exact prepared assignment and a separately retained trusted package SHA-256 before supervisor/evidence review. A worker-returned digest is not trusted; the future dispatcher must retain and supply the expected digest independently. It rejects blocked or tampered packages; it does not prove dispatch or delivery and never approves completion.
- `engine/review_artifact.py` — converts an assignment-bound supervisor/evidence review into the existing provenance-checked, in-memory report bundle. Worker claims remain labelled declarations, report status stays `not_run`, and human-only completion authority is preserved. See [REVIEW_ARTIFACT.md](docs/REVIEW_ARTIFACT.md).
- Regression coverage authored but not executed: 32 safety-controller tests, 50 report-builder tests, 27 task-runner tests, 7 artifact-preparation tests, 9 batch-planner tests, 17 supervisor-review tests, 10 evidence-verifier tests, 6 integrated-review tests, 9 assignment-package tests, 11 assignment-return tests, and 6 review-artifact tests (184 total). None have been executed because the active G0-05 handoff prohibits the relevant validation.
- `.github/workflows/` — no agent-specific workflow is installed yet. The first future workflow must be manual-dispatch only and preflight/report-only; event-driven and scheduled triggers require separate validation and approval.

## Full-project phase coverage

See [PHASE_SUPPORT_MATRIX.md](PHASE_SUPPORT_MATRIX.md) for the shared operating model and queue coverage across all five phases in the agreed order: Phase 3, Phase 1, Phase 2, Phase 4, Phase 5. The agent is reusable across the full project; Phase 3 is only the current active phase. Later phases remain blocked until predecessor gates are human-authorized closed and their own handoffs permit work.

## Validation and activation gates

See [VALIDATION_AND_ACTIVATION.md](VALIDATION_AND_ACTIVATION.md) for completed setup, deferred runtime checks, and conditions for safe activation. Static review does not count as runtime validation.

## Activation policy

Creating this scaffold does not authorize running it. Do not add or enable any agent workflow until the safety controller, task allowlist, and independent validation are complete and the applicable research handoffs permit execution. The G0-05 handoff remains authoritative even if a future agent configuration is changed.
