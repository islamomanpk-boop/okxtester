# Software supply-chain and build-provenance audit — 2026-11-27

## Status and authority

Targeted documentation-only audit of the future worker image, Python dependencies, GitHub Actions workflows/actions, build process, artifact provenance, and update lifecycle.

This audit does not add or change dependencies, lockfiles, package sources, workflow files, action references, container images, build scripts, permissions, secrets, or credentials. It does not install packages, resolve dependencies, build images, generate an SBOM, scan vulnerabilities, verify signatures, run tests, execute workflows, or contact registries. The active Phase 3 G0-05 handoff remains controlling. No scripts, tests, workflows, network requests, provider calls, VPS access, dispatch, or research operations were performed. The agent remains non-operational.

## Executive assessment

The worker-isolation design correctly requires fixed reviewed images, pinned dependencies, no runtime installation, and trusted runtime provenance. Those requirements are not yet backed by a selected build system, dependency lock, approved package/index policy, artifact-signing identity, SBOM, provenance attestation, vulnerability process, or independent verification service.

A version string or lockfile alone is insufficient. The future system must establish the complete chain from reviewed source and dependency resolution through a controlled builder, immutable image/artifact digest, signed provenance, deployment-time verification, and runtime observation. The worker must not choose, install, update, or attest its own executable supply chain.

## Findings and required resolutions

### SC-01 — No authoritative dependency inventory or complete lock is established (P0)

No reviewed, authoritative inventory currently establishes every direct and transitive runtime, build, test, workflow, and tooling dependency for the agent.

Before activation:
- Inventory direct and transitive packages, build backends, compilers, system libraries, base images, GitHub Actions, reusable workflows, downloaded binaries, plugins, and external tools.
- Separate runtime, build, test, documentation, and developer-only dependency groups. A package needed only for tests must not silently enter the worker runtime.
- Use a lock format that captures exact package versions and artifact hashes for every supported platform/interpreter combination; reject unlocked or floating transitive dependencies in production builds.
- Record package name, normalized ecosystem identity, version, source/index, artifact filename, platform tags, cryptographic digest, license metadata, and dependency edge.
- Detect dependency confusion, namespace collisions, typosquatting, unexpected new maintainers, and unapproved alternate indexes.
- Pin the interpreter, OS/base image, system packages, build tools, and package manager—not only Python application libraries.

A declared version range, requirements file without complete transitive hashes, or current package metadata page is not a reproducible dependency lock.

### SC-02 — Package source and resolution policy are unspecified (P0)

A future build must use an owner-approved, controlled package-source policy. Define trusted registries/mirrors, namespace ownership, TLS and certificate validation, repository/index precedence, immutable artifact retention, and behavior when an artifact disappears or is replaced.

Do not allow arbitrary extra indexes, per-task package URLs, VCS branches, editable installs, direct local paths, mutable Git tags, or unverified wheel/source archives in production builds. If source distributions are required, build them in a separate hardened builder and retain the exact source archive, build recipe, build dependencies, and resulting wheel digest. Prefer reviewed wheels where their provenance is established.

Never resolve or install packages at worker runtime. Network egress denial and package-manager disablement must be enforced outside the worker process.

### SC-03 — Build process and builder identity are not established (P0)

No trusted build service, builder identity, isolation profile, or build provenance is configured.

Require:
- A disposable, isolated, least-privilege builder with no production secrets, registry write credentials, deployment authority, or access to protected research data.
- Exact source commit/tree digest, dependency lock digest, build recipe digest, base-image digest, toolchain versions, build parameters, and environment identity recorded by the trusted builder.
- Network disabled during the build where feasible; otherwise use a controlled, logged, content-addressed dependency fetch stage separated from the build stage.
- No unreviewed build hooks, arbitrary shell sourced from package metadata, mutable remote scripts, or task-controlled build arguments.
- Build outputs written to a quarantine location before independent verification and promotion.
- Independent review of build definition changes and protected builder configuration.

The build process must not share credentials, writable caches, hosts, or administrative trust roots with the worker runtime, registry, dispatcher, reviewer, or witness.

### SC-04 — GitHub Actions and reusable workflow references require immutable pinning (P0)

The earlier bounded workflow inventory found tag-based action references and inherited workflows with varied triggers and permission declarations. That inventory was not an exhaustive dependency or workflow audit. Effective permissions depend on repository and organization configuration.

Before any future workflow activation:
- Pin every third-party action and reusable workflow to a full reviewed commit SHA. A version tag may be documented for human readability but must not be the executable reference.
- Record repository owner/name, action path, resolved commit SHA, release/tag reviewed, source commit, and review date in the dependency inventory.
- Audit nested/composite actions and every action's own downloaded tools, scripts, container images, and transitive dependencies.
- Pin container actions by immutable image digest where supported; do not rely on mutable tags.
- Set explicit least-privilege workflow and job permissions; use read-only contents by default, no secrets, no write tokens, and persist-credentials false unless a separately approved operation requires otherwise.
- Avoid self-hosted runners, persistent caches, privileged containers, untrusted PR execution, and broad event triggers.
- Treat action updates as code changes requiring review and fresh provenance—not routine tag refreshes.

No inherited workflow is authorized for dispatch by this audit; the current G0-05 handoff remains controlling.

### SC-05 — Immutable image and artifact identity must be verified independently (P0)

The worker image must be referenced by immutable digest, not a mutable tag. The deployment controller must independently verify the exact approved digest, platform/architecture, image signature, provenance, vulnerability policy, and runtime configuration before starting a sandbox.

The runtime must report its observed image digest and policy digest through trusted platform telemetry. Worker-reported environment details are untrusted claims. Image rebuilds, even from the same source version, create a new digest and require fresh review/promotion.

Use separate identities and repositories/registries for build, quarantine, approved release, and deployment where feasible. Worker processes must have no image-push, registry-admin, signing, or release-promotion credentials.

### SC-06 — SBOM and provenance attestations are not yet produced or authenticated (P0)

Require a machine-readable SBOM for each promoted image/artifact, including direct and transitive application packages, OS/system packages, build tools, and embedded binaries. Choose a supported format/version and define completeness, namespace, relationship, and license handling.

Require signed build provenance that binds at least:
- source repository and immutable commit/tree digest;
- exact build definition and builder identity;
- dependency lock and resolved artifact digests;
- base image and toolchain digests;
- build parameters and target platform;
- resulting image/artifact digest;
- SBOM digest;
- build timestamp and provenance schema version.

The verifier must authenticate the signer against an independently governed trust root and verify subject digest, builder identity, source, materials, and policy before promotion. A JSON provenance file, unsigned SBOM, worker assertion, or artifact hash alone is not an attestation.

### SC-07 — Signing keys and trust roots need lifecycle separation (P0)

No signing identity, key custody, rotation, revocation, or recovery process is selected.

Build provenance and release signatures must be produced by a narrowly scoped identity isolated from source contributors, workers, workflow dispatchers, repository administrators, and deployment operators. Prefer short-lived workload identity with verifiable issuer/subject claims and hardware-backed or managed key custody where available. Do not expose private signing keys to build steps or workers.

Define key creation, owner approval, permitted subjects, audience, expiry, rotation overlap, revocation, compromise response, transparency/audit evidence, backup/recovery, and verifier trust-bundle updates. A compromised signing identity must cause affected artifacts to become untrusted; do not silently re-sign or bless old artifacts. Emergency hold and credential containment remain independent, and recovery cannot itself authorize dispatch.

### SC-08 — Vulnerability and malicious-package response is not operationally defined (P1)

Define a repeatable process for vulnerability intelligence, package/image scanning, exploitability assessment, prioritization, exception handling, patch deadlines, and evidence retention. Scan the complete dependency graph and OS image, not only direct Python packages.

The policy must distinguish:
- known vulnerable component with reachable versus unreachable code;
- actively exploited or compromised dependency;
- malicious package, typosquat, maintainer/account takeover, or poisoned release;
- unsupported/end-of-life runtime or base image;
- license/policy violation;
- scanner unavailable, stale database, or incomplete coverage.

A scanner result is evidence, not automatic authorization to update or deploy. Unknown scanner state, stale feeds, unscanned artifacts, and unresolved critical/high-risk findings remain blocked according to owner-approved thresholds. Exceptions must be narrow, time-bounded, evidence-backed, independently approved, and expire automatically.

### SC-09 — Reproducibility, build cache and artifact retention need controls (P1)

Aim for reproducible builds from identical source, lock, builder image, and build parameters. Where bit-for-bit reproducibility is not feasible, document nondeterministic inputs and independently compare build attestations and output contents.

Caches are untrusted optimization inputs, not trust roots. Use content-addressed immutable cache objects; isolate cache namespaces by trust level; never share writable worker caches with builders or release pipelines. A cache hit must not bypass signature, digest, provenance, or policy verification.

Retain source snapshot identity, lockfiles, build recipes, SBOM, provenance, signatures, scanner results, promotion decisions, and released image digests for the approved investigation and rollback period. Define registry immutability, deletion protection, region, encryption, access logging, and legal hold. Retention expiry must not make an old artifact appear verified.

### SC-10 — Update and emergency revocation lifecycle needs a governed process (P1)

Dependency, action, base-image, toolchain, and runtime updates must follow a staged process:
1. Observe an upstream release/advisory without changing production.
2. Resolve and inspect exact source and transitive changes.
3. Review maintainer, provenance, signatures, release history, licenses, and vulnerability impact.
4. Update lock and build definitions in an isolated review branch.
5. Build in the trusted isolated builder and generate fresh SBOM/provenance/signatures.
6. Run authorized synthetic and compatibility validation in a separate approved environment.
7. Obtain independent review and a versioned promotion decision.
8. Deploy only the exact approved digest after a fresh authorization check.
9. Monitor rollout and retain the previous known-good digest for controlled rollback.
10. Record revocation/withdrawal for compromised artifacts and prevent future starts.

A compromised dependency or image may require immediate deny-only quarantine of affected digests and runtime identities. Do not automatically replace a compromised artifact with an unreviewed latest version. Rollback to an older image is not automatically safe if that image shares the vulnerability or has stale trust status.

### SC-11 — Runtime drift and provenance-to-execution binding are not demonstrated (P0)

The system must bind each assignment execution to the approved software bill of materials, image digest, workflow/action revisions, runtime policy digest, task digest, input manifest, and assignment attempt. Trusted runtime telemetry—not worker output—must record the actually started image and policy.

Deny execution if observed digest, platform, action/workflow revision, dependency lock, or runtime policy differs from the approved release record. Detect unexpected package installation, executable changes, writable system paths, image pull substitution, mutable tag resolution, or runtime drift. Preserve evidence of denied starts and quarantine affected hosts/tenants where integrity is uncertain.

### SC-12 — Supply-chain controls need measurable synthetic conformance (P1)

Create a versioned coverage matrix from threats to preventive control, independent verifier, alert, owner, and retained evidence. At minimum test:
1. Lock omits a transitive dependency or platform-specific artifact.
2. Same package version resolves to different bytes; hash mismatch blocks build.
3. Dependency-confusion package appears on an unapproved index.
4. Typosquatted or namespace-colliding package is introduced.
5. VCS branch/tag or direct URL dependency is mutable.
6. Build hook attempts arbitrary command execution or network access.
7. Builder attempts to read deployment, registry, signing, or repository-write credentials.
8. Mutable action tag moves after review; immutable SHA remains fixed.
9. Nested action downloads an unpinned binary or image.
10. Base-image tag resolves to an unexpected digest.
11. SBOM omits an embedded binary or transitive package.
12. Provenance signer, subject digest, source commit, or builder identity is wrong.
13. Signature is revoked or trust root is compromised.
14. Vulnerability feed is stale/unavailable or scanner coverage incomplete.
15. Cache supplies poisoned or cross-tenant content.
16. Runtime image digest differs from the approved release.
17. Worker attempts package installation or executable modification.
18. Artifact is deleted/replaced or retention policy is bypassed.
19. Rollback selects a revoked or vulnerable image.
20. Supply-chain incident occurs while the control plane is frozen; alerting and quarantine do not grant dispatch/resume authority.

Oracles must prove fail-closed verification, no worker signing/promotion authority, immutable digest binding, independent trust-root validation, retained provenance, and no automatic deploy/retry/rollback on ambiguous evidence.

## Minimum release-verification record

A future release record should be immutable and include:
- release ID and status;
- source repository, commit and tree digest;
- build definition digest and trusted builder identity;
- dependency lock digest and complete resolved package manifest;
- base image, OS packages, interpreter, package manager and toolchain digests;
- action/reusable-workflow full commit SHAs and nested materials;
- SBOM format/version and digest;
- signed provenance and signature-verification result;
- resulting artifact/image digest and target platform;
- vulnerability scanner/version/feed timestamp/results and approved exceptions;
- policy version, reviewers, approval evidence, and promotion timestamp;
- revocation/withdrawal state and retained predecessor release references.

This record documents a release; it is not a dispatch approval or human research-gate decision.

## Current status and non-claims

This is a targeted static design audit, not a live software inventory, vulnerability scan, build, signature verification, or deployment assessment. No dependency was installed or changed. No lockfile, SBOM, provenance, signature, image, build, scanner, package registry, workflow, credential, or release process was configured. No tests, scripts, workflows, network requests, provider calls, or VPS operations were run. No inherited workflow was dispatched. The agent remains non-operational, no unattended work is running, and Phase 3 G0-05 remains controlling.
