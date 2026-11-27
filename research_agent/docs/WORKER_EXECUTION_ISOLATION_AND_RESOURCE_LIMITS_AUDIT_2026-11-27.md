# Worker execution isolation and resource-limits audit — 2026-11-27

## Scope and authority
Targeted static design audit of the threat model, security gap audit, trust-root architecture, dispatcher contract, and implementation-readiness criteria. Scope: future worker execution boundary, filesystem, process, network, credentials, resource exhaustion, and evidence export.

Documentation-only proposal. It does not select a worker provider/runtime, configure a sandbox, add executable code, alter permissions, or authorize execution. The active Phase 3 G0-05 handoff remains controlling.

## Executive assessment
The architecture places the worker outside the trusted registry boundary and prohibits worker credentials from writing approvals, registry state, protected checkpoints, research branches, or trusted evidence indexes. Identity separation alone is insufficient: a worker process could still read ambient files, inherit environment credentials, access cloud metadata, spawn unrestricted subprocesses, exfiltrate repository data, exhaust shared resources, or persist malicious state if its runtime boundary is weak.

A future worker must run in a disposable, per-assignment isolation boundary with no ambient authority. The control plane must prepare a minimal immutable input bundle and receive output through a separately authenticated, bounded return channel. The worker must never share a host, credential namespace, writable volume, network trust zone, or privileged control socket with the dispatcher, registry, reviewer, witness, VPS, or protected research environment.

## Findings

### WI-01 — Process and host isolation are not operationally specified (P0)
A container label alone is not proof of isolation. The selected runtime must document and demonstrate the kernel/VM boundary, tenant isolation, privilege model, host namespace exposure, runtime patching, and escape response.

Required:
- Prefer a disposable microVM or provider-managed strong tenant sandbox for untrusted code; if using containers, require a hardened isolated host/VM boundary and independently reviewed runtime configuration.
- Run as non-root and unprivileged UID/GID; drop all capabilities; prohibit privileged mode, host PID/IPC/network namespaces, host path mounts, device access, setuid escalation, and host control sockets.
- Enforce seccomp/AppArmor/SELinux or equivalent mandatory policy; read-only root filesystem; minimal writable scratch volume.
- No Docker/containerd socket, Kubernetes service-account token, cloud instance credentials, host agent socket, SSH agent, credential helper, or host proc/sys exposure beyond safe virtualized views.
- One assignment per sandbox. Destroy sandbox and ephemeral writable state after verified output capture; do not reuse a potentially compromised worker image/container.

### WI-02 — Filesystem and data minimization (P0)
The worker receives only exact task inputs needed for the approved assignment. It must not mount the full repository, user home, runner workspace, secrets directory, SSH configuration, cloud config, Git credential store, database files, or research VPS paths.

Required:
- Construct a content-addressed, read-only input bundle from an explicit path allowlist and exact commit; independently verify every path and digest before delivery.
- Reject symlinks, hardlinks, path traversal, absolute paths, device/FIFO/socket entries, case-collision ambiguity, alternate data streams, and archive extraction escapes.
- Keep scratch output separate from inputs; impose per-file and total output byte limits; reject unexpected paths and file types.
- No writable mount of the research repository or Git metadata. No worker push credentials, GitHub write token, or ability to alter branch refs.
- Export only declared output/evidence paths through a bounded receiver that computes its own digest and records provenance; worker-declared hashes remain claims.
- Treat archives, notebooks, scripts, PDFs, and returned files as untrusted; scan/parse in a separate non-privileged verifier sandbox.

### WI-03 — Secrets and identity isolation (P0)
No long-lived or broad credentials may enter the worker environment. A worker must not receive dispatcher, registry, approval, artifact-administration, witness, repository-write, cloud-admin, VPS, exchange, or research-data credentials.

Required:
- No secrets by default. If a task genuinely requires an external read-only capability, broker it through a narrow, short-lived, audience-restricted proxy/token with exact resource and operation scope; never expose reusable master credentials.
- Keep approval and registry service identities in separate control-plane services inaccessible from worker network and filesystem.
- Scrub inherited environment variables; pass a closed minimal environment allowlist. Disable shell startup files, user-site packages, credential helpers, and implicit cloud SDK discovery.
- Block instance metadata endpoints and local credential services at network and runtime layers, not merely by omitting environment variables.
- Ensure logs, crash dumps, process listings, temporary files, notebook outputs, and error messages cannot disclose secrets.
- Credential compromise triggers independent deny-only hold and out-of-band credential/session containment; no worker can clear the hold or rotate trusted roots.

### WI-04 — Network egress and lateral movement (P0)
Default worker network policy is deny-all. A task's need for network access is not implied by its scope text.

Required:
- Disable inbound connectivity and arbitrary outbound Internet access by default.
- If a task is explicitly approved for network reads, use a controlled egress proxy with domain/IP policy, DNS protections, TLS validation, request/response size caps, rate limits, and auditable destination logs.
- Deny private, loopback, link-local, multicast, reserved, and cloud metadata ranges; revalidate resolved addresses at connection time to resist DNS rebinding and redirects.
- Deny access to GitHub write APIs, registry, approval channel, witness, internal databases, VPS, exchange accounts, runner control plane, and other workers.
- No port forwarding, reverse tunnels, peer discovery, arbitrary webhook listener, or inbound callback endpoint inside the worker.
- Enforce network policy outside the worker process so it remains effective if worker code is compromised.

### WI-05 — Command execution and software supply chain (P0)
A generic shell with ambient host tools is excessive authority. The task contract must specify permitted operations, not merely expected output.

Required:
- Use a closed command/tool allowlist and fixed executable paths; reject arbitrary shell, dynamic package installation, privileged helpers, unneeded interpreters, and unreviewed plugins.
- Pin worker image by immutable digest, dependencies by lockfile/hash, and external actions/tools by immutable revision; independently review updates and attest build provenance.
- Disable package-manager/network installation at runtime. Prebuild a minimal image from reviewed dependencies.
- Set no_new_privs, prohibit ptrace and process injection, restrict executable memory where supported, and block kernel/module/device operations.
- Record image digest, runtime version, policy digest, task digest, exact input manifest, and effective sandbox configuration from trusted platform context, not worker claims.
- Worker action declaration is not proof that only those actions occurred; enforce at runtime and preserve platform audit evidence.

### WI-06 — Resource exhaustion and denial of service (P0)
No resource limits are currently demonstrated. An untrusted task may consume CPU, memory, disk, PIDs, file descriptors, bandwidth, or provider quota.

Required hard ceilings per assignment:
- CPU quota and wall-clock deadline, with supervisor-enforced termination.
- Memory and swap limits; kill on out-of-memory without host-wide impact.
- PID/process/thread count, open-file descriptor count, and process-tree limits.
- Scratch disk, inode count, temporary storage, input/output bytes, log volume, and artifact count.
- Network bandwidth, request count, concurrency, and egress bytes where network is approved.
- Provider invocation count, workflow minutes, retries, and monetary spend ceiling enforced by the control plane.
- Limits are set outside worker control; worker cannot raise them. Record actual usage and termination reason from trusted runtime telemetry.
- Timeouts and resource kills produce incomplete/failed execution evidence, never successful task completion. No automatic retry without a new operation-bound approval.

### WI-07 — Persistence, cache and cross-assignment contamination (P0)
Reused workspaces, caches, home directories, package caches, and writable image layers can leak data or carry compromise between assignments.

Required:
- Fresh ephemeral sandbox, filesystem, process namespace, credentials, and network identity per assignment/attempt.
- No shared writable caches or volumes between workers. Any shared cache must contain only public, content-addressed immutable objects and be mounted read-only.
- No persistent user home, browser profile, shell history, notebook kernel state, environment cache, or background daemon.
- Destroy scratch data after output capture under documented retention policy; preserve only approved evidence bytes and trusted provenance metadata.
- Verify cleanup through platform evidence; if destruction cannot be established, quarantine worker host/tenant and do not schedule another assignment there.

### WI-08 — Artifact and output boundary (P0)
Worker output can contain active content, malicious archives, oversized payloads, path tricks, secrets, or misleading provenance.

Required:
- Return data through an authenticated provider channel bound to assignment revision and attempt ID.
- Enforce strict size, file-count, path, MIME/type, encoding, nesting, and decompression-ratio limits before parsing.
- Store raw bytes immutably; compute receiver-side digest/length before inspection.
- Parse or render outputs in a separate sandbox with no credentials/network and read-only inputs.
- Never execute returned scripts, macros, notebooks, binaries, HTML, or embedded active content as part of review.
- Verify evidence against independently derived checkout manifests; do not accept worker-supplied commit identity, file hash, or path as authoritative.
- Quarantine malformed, duplicate, late, mismatched, or over-limit returns without altering trusted task state.

### WI-09 — Monitoring, termination and incident response (P1)
A sandbox policy without independent enforcement telemetry cannot prove containment.

Required:
- Collect trusted runtime events for image digest, policy digest, identity, assignment, start/end, resource usage, process termination, network destinations/bytes, denied syscalls, output digest, and cleanup result.
- Separate worker-visible logs from security audit logs; worker cannot delete, alter, or suppress the latter.
- Detect sandbox escape indicators, unexpected egress, metadata access attempts, privilege changes, resource-limit abuse, and cross-assignment access.
- Provide immediate out-of-band kill/fence for worker and separate deny-only hold for dispatch/registry operations.
- Preserve forensic evidence without allowing compromised worker to write to evidence store.
- Define incident ownership, notification, credential containment, host quarantine/rebuild, and independent resume criteria before activation.

## Required future isolation profile
1. One disposable sandbox per assignment/attempt, preferably a provider-managed microVM/strong tenant boundary.
2. Non-root, no capabilities, no privileged mode, no host mounts/sockets/devices, read-only root.
3. Minimal immutable input bundle; separate bounded scratch/output channel.
4. No secrets or credentials by default; no dispatcher/registry/approval/repository/VPS access.
5. Deny-all network by default; controlled proxy only for explicitly approved read-only needs.
6. Fixed reviewed image and dependencies; no runtime installation or arbitrary command escalation.
7. Hard external CPU, memory, PID, disk, time, bandwidth, output, concurrency and cost limits.
8. Independent trusted telemetry, kill switch, host quarantine, and verified cleanup.
9. Returned artifacts inspected in a separate unprivileged sandbox and never executed during review.
10. Exact runtime/image/policy/input/attempt provenance retained outside worker control.

## Required synthetic validation matrix
Before any worker execution is authorized, independently test:
- Attempts to read host files, home directories, SSH keys, cloud config, environment secrets, Git credentials, registry credentials, and mounted research data.
- Access to Docker/containerd sockets, Kubernetes tokens, host namespaces, devices, proc/sys, metadata endpoints, loopback, link-local, private networks, and internal services.
- Privilege escalation, setuid, capabilities, ptrace, process injection, kernel/module operations, symlink/hardlink/path traversal, archive extraction escapes, and case-collision paths.
- Arbitrary shell, unapproved binaries, dynamic package installation, malicious dependency updates, mutable image tags, and worker-controlled policy changes.
- DNS rebinding, redirects to blocked IPs, IPv6 bypass, proxy bypass, raw sockets, reverse tunnels, inbound listeners, and unauthorized API calls.
- CPU/memory/PID/fd/disk/inode/log/network/output exhaustion; process fork bombs; infinite loops; decompression bombs; oversized files and archive bombs.
- Cross-assignment cache/workspace/credential leakage, background process survival, incomplete cleanup, and host reuse after suspected compromise.
- Malformed/active artifacts, macros, notebooks, HTML/JS, binaries, polyglot files, and false worker-declared hashes.
- Kill-switch races, control-plane outage, telemetry loss, and host quarantine behavior.

Oracles must prove worker compromise cannot reach trusted services or protected data, limits are enforced outside worker control, no assignment can access another assignment's state, no secret is exposed, all egress is policy-mediated, and cleanup/termination are independently evidenced. Use synthetic fixtures and disposable infrastructure only.

## Current status and blockers
- No worker runtime/provider, image, sandbox, network policy, credential broker, telemetry system, or resource quota is selected or configured.
- No runtime isolation or resource-limit claim is currently proven. These controls are UNKNOWN/BLOCKED, not PASS.
- No tests, scripts, workflows, sandbox executions, network probes, provider calls, or failure injections were run.
- No credentials, permissions, repositories, default branch, protected research branch, VPS, runner, or research artifacts were changed.
- The agent remains non-operational. Phase 3 G0-05 remains controlling; this audit does not authorize worker execution, research execution, task completion, gate closure, or phase advancement.
