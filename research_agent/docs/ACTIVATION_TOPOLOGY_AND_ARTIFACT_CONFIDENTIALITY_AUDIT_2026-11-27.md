# Activation Topology and Artifact Confidentiality Audit — 2026-11-27

## Status and scope

**Documentation-only static review. No workflow was created, enabled, dispatched, or modified. No artifact was uploaded or downloaded. No repository settings, permissions, secrets, branch protections, or Actions settings were changed.**

This audit examines the proposed activation topologies against the currently observed repository visibility and GitHub's documented artifact-access model. It does not authorize activation or override the active Phase 3 G0-05 handoff.

## Verified repository facts

- Repository: `islamomanpk-boop/okxtester`.
- Current repository metadata reports `visibility=public` and `default_branch=main`.
- The proposed Option B stores its caller on `main` and its reusable callee on the isolated agent branch, while workflow runs and uploaded artifacts remain associated with the same repository.
- The current design proposes an artifact containing `report.json`, `report.md`, and `artifact_manifest.json`; a seven-day retention period is a design proposal, not a configured setting.

These facts make artifact audience a first-order activation decision, not merely a retention setting.

## Finding ACT-ART-01 — same-repository artifacts inherit a public audience

**Severity: P0 confidentiality gate for any non-public report content.**

GitHub's documentation says people signed into GitHub with read access to a repository can download its workflow artifacts. Its REST documentation also says artifact listing/get endpoints can be used without authentication when only public resources are requested. Since this repository is public, repository read access is not a meaningful confidentiality boundary for artifacts stored here. A seven-day retention period limits duration; it does not restrict who can read an artifact during that period.

Sources:
- GitHub Docs, [Downloading workflow artifacts](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/download-workflow-artifacts).
- GitHub Docs, [REST API endpoints for GitHub Actions artifacts](https://docs.github.com/en/rest/actions/artifacts).

**Impact:** Option B's proposed three-file artifact must be treated as publicly readable if uploaded to this public repository. Hashes, provenance fields, task IDs, worker findings, evidence references, source paths, operational details, and any included evidence bytes may disclose information even when the report is labelled preflight-only. The current report schema and hash checks establish consistency/integrity properties; they do not provide confidentiality or access control.

**Required control before any artifact upload to this repository:**
1. Define and approve a public-output classification and field-level allowlist.
2. Exclude credentials, tokens, private operational details, personal data, restricted research data, raw source data, private evidence bytes, and any sensitive logs.
3. Treat filenames, task metadata, branch/commit identifiers, evidence paths, summaries, and hashes as potentially sensitive metadata; include them only after explicit classification.
4. Test the rendered JSON, Markdown, manifest, and workflow logs for accidental disclosure using synthetic fixtures before any real workflow run.
5. Do not rely on short retention, obscure artifact names, unguessable URLs, or SHA-256 hashes as confidentiality controls.

If the report cannot be made safe for public disclosure, do not upload it to this repository.

## Finding ACT-ART-02 — Option A is the safer artifact boundary only if the agent repository is private

Option A (a separate agent repository) was previously preferred for workflow and permission isolation. This review adds a necessary qualification: a separate repository only improves artifact confidentiality if its visibility and access controls are deliberately selected and verified.

- A **private** agent repository can restrict artifact downloads to authorized repository readers, subject to its actual access configuration.
- A **public** agent repository does not solve the artifact-audience problem; its artifacts should also be treated as public.
- The public research repository can remain a read-only input source. Do not copy sensitive research evidence into the agent repository merely because it is separate.

**Recommendation:** If reports may contain non-public operational or research metadata, evaluate a private agent repository with a narrowly scoped read-only path to the research repository. Repository creation and its access configuration require explicit owner authorization and are not performed by this audit.

## Finding ACT-ART-03 — caller/callee isolation does not isolate artifact storage

Under Option B, a reusable workflow pinned to an agent-branch commit still executes as part of a run initiated in the same repository. A separate workflow file location or branch does not create a separate artifact access-control domain. The caller/callee split protects code review and trigger topology only; it does not make same-repository artifacts private.

The caller and callee must therefore be reviewed for:
- exact immutable callee SHA and matching explicit checkout SHA;
- caller-granted token permissions and the callee's effective permission ceiling;
- all artifact names, paths, uploaded files, logs, and retention;
- any cross-job or cross-run artifact handoff;
- whether workflow inputs or untrusted repository content can influence report fields or log output.

## Finding ACT-ART-04 — retention and integrity are not substitutes for confidentiality or authenticity

The proposed seven-day retention period is a lifecycle limit, not an audience restriction. Artifact-manifest hashes and downloaded-file verification can detect certain mismatches, but do not authenticate the uploader, make a public artifact private, or prove that its content is safe to disclose. The workflow must not treat a valid hash as permission to publish the corresponding bytes.

## Required activation decision updates

Before any future workflow design is approved, the owner/security review must record:
1. Whether workflow artifacts are intentionally public or require restricted access.
2. The exact repository that stores workflow runs, logs, and artifacts, and its verified visibility.
3. A public-output data classification and allowlist if any artifact is stored in a public repository.
4. Whether raw evidence and detailed worker returns are prohibited from public artifacts.
5. Who may read, retain, delete, and export artifacts, and how those permissions are independently verified.

These decisions are additional to the existing default-branch, workflow SHA pinning, caller/callee permission, clean-checkout, task-binding, and G0-05 handoff requirements.

## Disposition

- Option B on the current public repository: **not suitable for non-public artifact content** unless the artifact is moved to an independently controlled private store or the complete artifact is explicitly classified safe for public release.
- Option A: **preferred for isolation, conditional on a private agent repository** if confidential artifacts are required.
- No topology is approved or activated by this audit.
- No workflow, script, test, or research task was executed.
- The current G0-05 handoff remains controlling; this audit does not authorize preflight, validation, research execution, or phase advancement.
