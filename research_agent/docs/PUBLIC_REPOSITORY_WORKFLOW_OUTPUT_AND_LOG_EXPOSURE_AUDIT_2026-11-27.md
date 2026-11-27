# Public Repository Workflow Output and Log Exposure Audit — 2026-11-27

## Scope and status

Documentation-only review of GitHub Actions output exposure for `islamomanpk-boop/okxtester`, whose repository metadata was observed as public with default branch `main`.

No workflow was created, modified, enabled, or dispatched. No run logs or artifacts were downloaded. No repository settings, secrets, permissions, retention policies, or branch protections were changed. No scripts, tests, or research operations were run.

## Finding LOG-01 — workflow logs are an independent public-output channel

**Severity: P0 confidentiality gate for non-public runtime data.**

GitHub documents that repository read access is required to view and download workflow logs. For public resources, the REST API endpoint for downloading workflow-run logs can be used without authentication. The same public-resource rule is documented for job logs.

Sources:
- GitHub Docs, [Using workflow run logs](https://docs.github.com/en/actions/how-tos/monitor-workflows/use-workflow-run-logs).
- GitHub REST API, [Workflow runs — download workflow run logs](https://docs.github.com/en/rest/actions/workflow-runs).
- GitHub REST API, [Workflow jobs — download job logs](https://docs.github.com/en/rest/actions/workflow-jobs).

**Impact:** A future workflow on this public repository must treat stdout/stderr-derived logs, step summaries, annotations, failure messages, command echoes, and generated diagnostic output as public disclosures. Protecting or omitting the uploaded artifact does not protect information already printed to logs.

GitHub secret redaction is a useful defense but is not a data-classification boundary and must not be relied on to protect arbitrary credentials, private data, operational metadata, or research evidence. Never print secrets or rely on masking as permission to pass secrets through an untrusted workflow.

## Finding LOG-02 — UI visibility and API visibility have different access details

GitHub's UI documentation says a user must be signed in to view workflow run information, including for public repositories, and read access is required for logs. The REST API documentation separately states that the log-download endpoints can be used without authentication when only public resources are requested.

The safe policy is not to interpret the sign-in requirement for the UI as confidentiality. For this public repository, logs and artifacts must be classified as public repository outputs.

## Finding LOG-03 — output channels must be reviewed together

The public-output review must cover at least:

1. Workflow run names, job names, step names, and annotations.
2. Standard output and standard error, including exception traces and debug output.
3. Step summaries, job outputs, environment dumps, and command echoing.
4. Uploaded artifacts and artifact manifests.
5. Cache contents and cross-job artifact transfers.
6. Failure diagnostics, generated reports, and any URLs or identifiers printed by tools.
7. Commit statuses/check summaries and any other output rendered on the repository or pull request.

The current proposed three-file report bundle (`report.json`, `report.md`, `artifact_manifest.json`) is only one part of this surface.

## Required controls before any workflow run

- Define a public-output classification and allowlist covering logs, summaries, artifacts, metadata, and failure paths.
- Use synthetic fixtures to exercise success and failure logging and inspect every output channel before any real task is considered.
- Keep logs terse and structured; never dump environment variables, complete task payloads, raw worker returns, source evidence, credentials, tokens, private paths, or unrestricted exception objects.
- Ensure error handling does not leak request bodies, headers, credential-bearing URLs, or raw external responses.
- Do not treat secret masking, artifact expiry, or a non-obvious artifact name as confidentiality.
- If any required output is confidential, move the run and its outputs to a separately controlled private repository/service before activation, and independently verify its access policy.
- Retention settings must cover both artifacts and logs; retention limits deletion timing, not the audience during retention.

## Relationship to the prior activation audit

This finding supplements `ACTIVATION_TOPOLOGY_AND_ARTIFACT_CONFIDENTIALITY_AUDIT_2026-11-27.md`. Option B in the current public repository is unsuitable for confidential logs or artifacts. Option A only improves confidentiality if its repository is private and its Actions, logs, artifacts, and access controls are verified. A separate public agent repository does not solve this issue.

## Disposition

- Treat all logs and artifacts produced in the current public repository as public outputs.
- Do not emit sensitive runtime or research content into them.
- No workflow topology is approved by this audit.
- The active Phase 3 G0-05 handoff remains controlling; this document does not authorize preflight, workflow validation, execution, or phase advancement.
