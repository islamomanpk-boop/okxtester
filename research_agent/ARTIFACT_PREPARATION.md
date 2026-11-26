# Preflight Artifact Preparation

The `engine.artifact_preparation` module connects the trusted task queue,
single-task read-only preflight, deterministic preflight report factory, and
in-memory artifact bundle builder.

## Current capability

For one exact queue task, the module:
1. Loads the repository's trusted queue (not a caller-supplied task object).
2. requires the configured repository and isolated agent branch;
3. obtains that task's preflight decision through the existing safety controller;
4. builds an input hash manifest for explicitly supplied repository-relative paths;
5. creates a `preflight_only` or `blocked` report and validates checkout provenance;
6. returns exactly three artifact files in memory: `report.json`,
   `report.md`, and `artifact_manifest.json`.

A denied task can still produce a blocked audit artifact. This does not mean
that the task ran. The result explicitly reports that no task execution,
filesystem write, or artifact upload occurred.

## Important boundary

This is an orchestration seam, not an active worker. It does not perform
repository research, invoke Copilot, execute scripts or tests, update queue
status, write files, upload artifacts, or schedule itself. Runtime metadata
must be supplied independently by a future trusted workflow; the function
does not authenticate caller-supplied context. The current G0-05 lock remains
in force, so Phase 3 preflight is expected to be denied until an authoritative
handoff changes the permitted scope.

## Future workflow contract

A future workflow may call this module only after:
- the applicable handoff permits the exact operation;
- deferred tests and independent safety checks are authorized and pass;
- the default-branch activation constraint is resolved;
- task-specific authorization and phase permissions are explicitly approved;
- GitHub Actions permissions, checkout identity/cleanliness, artifact upload,
  and downloaded-artifact verification are independently established.

No scheduled or event-driven trigger is enabled by this module.
