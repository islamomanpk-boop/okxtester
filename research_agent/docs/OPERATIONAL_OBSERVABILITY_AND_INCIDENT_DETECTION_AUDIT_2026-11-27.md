# Operational observability and incident-detection audit — 2026-11-27

## Status and authority

Targeted documentation-only audit of the future agent lifecycle, trusted registry/backend, provider dispatch and reconciliation, worker isolation, evidence custody, control-plane authorization, and emergency response contracts.

This document grants no monitoring, notification, incident-response, dispatch, cancellation, permission, credential, workflow, scheduling, test, or research authority. It does not configure a monitoring provider, notification destination, on-call rotation, webhook, dashboard, alert rule, log sink, or credential. The active Phase 3 G0-05 handoff remains controlling. No scripts, tests, workflows, network requests, provider calls, VPS access, dispatch, or research operations were performed. The agent remains non-operational.

## Executive result

The architecture has substantial lifecycle and recovery requirements, but no operational observability plane is implemented. Existing event, provider-observation, witness, worker-telemetry, and incident-response documents define evidence that a future system should preserve; they do not provide deployed collection, alert evaluation, notification delivery, acknowledgement, escalation, or monitoring-integrity proof.

The future observability plane must be **read-only with respect to protected control-plane state**. It may collect, correlate, classify, retain, and notify. It must not approve, dispatch, retry, cancel, revoke, change task state, clear holds, alter policy, close gates, or resume operations. Emergency freeze remains a separately authenticated deny-only capability, not an alert action. Human incident responders use independently authenticated procedures and separate authority.

## Findings and required resolutions

### OBS-01 — No end-to-end telemetry ownership or deployed monitoring plane (P0)

No active service currently proves that lifecycle events, workflow outcomes, provider observations, worker telemetry, evidence receipts, witness acknowledgments, and security events are collected into a durable, independently protected monitoring system.

Before activation, define an inventory for every critical component: producer, event schema/version, source identity, sequence/cursor, timestamp semantics, delivery guarantee, retention, owner, health signal, and failure behavior. Monitoring must distinguish source silence from a healthy system with no events. Every critical producer needs an independently observable heartbeat or a documented reason it cannot provide one. Missing telemetry is UNKNOWN, never evidence of healthy operation.

### OBS-02 — Closed event taxonomy and severity semantics are needed (P0)

Use a versioned, closed alert taxonomy with stable alert type and rule version. Severity is based on impact and uncertainty, not the producer's own claimed severity:

- **SEV-0 / critical security or integrity incident:** suspected trust-root compromise, unauthorized protected action, broken/forked registry or witness chain, unverified rollback, approval/identity compromise, evidence tampering, or an emergency hold that cannot be independently confirmed.
- **SEV-1 / urgent operational safety:** dispatch outcome uncertain beyond its bounded reconciliation window; provider acceptance without recoverable receipt; callback signature or binding conflict; witness pending beyond its service objective; critical producer/monitoring blind spot; sandbox escape or kill/fence failure.
- **SEV-2 / degraded or blocked:** repeated workflow failures, stuck assignment, missing expected evidence, provider outage, callback/history gap, resource ceiling approached, artifact verification failure, backup/restore reconciliation pending.
- **SEV-3 / informational:** expected task transitions, routine completion of non-authorizing checks, recoverable transient errors, and policy-approved maintenance notices.

Rules must define objective thresholds, evaluation windows, confidence, required evidence, false-positive handling, and escalation. Severity may be raised by verified impact; it may not be silently lowered by a worker, provider callback, or untrusted payload. An alert is not itself a finding of wrongdoing.

### OBS-03 — Correlation must use trusted lifecycle identities, not names or arrival order (P0)

Correlate signals using immutable IDs and versions: repository/workflow/run/attempt, task ID and task digest, assignment ID/revision, package digest, dispatch attempt, provider namespace/account/job/event identity, raw receipt digest, worker-return receipt, review digest, registry sequence/checkpoint, witness receipt, and policy/handoff revision.

Preserve source event time and receiver observation time separately. Do not infer order from arrival timestamps. Deduplicate exact replays by authenticated source identity plus stable event ID/role and immutable facts digest. Same identity with changed facts is a security conflict, not an update. Keep separate alerts when identities cannot safely be joined; never use fuzzy task titles, filenames, or dashboard labels to attach evidence to an assignment.

### OBS-04 — Stuck work and missing evidence need explicit bounded expectations (P1)

Define per-state service objectives only after owner-approved workflow/provider capabilities and time budgets are known. Candidate monitored conditions include:
- prepared assignment with no authenticated dispatch decision;
- committed dispatch attempt without delivery resolution;
- provider acceptance without receipt or query/history reconciliation;
- callback receipt remaining unprocessed;
- provider sequence/cursor gap or incomplete history;
- worker execution exceeding its approved wall-clock/resource envelope;
- worker completion without an authenticated return receipt or expected artifact;
- return received but evidence objects, manifest, or review remain incomplete;
- review waiting for an authorized human disposition;
- witness outbox awaiting external acknowledgment;
- backup/restore or credential-revocation reconciliation remaining unresolved.

Each timer must state its start event, trusted clock, pause conditions, deadline, and response. A timeout creates an alert and preserves UNKNOWN; it never authorizes retry, cancellation, task completion, or a new provider attempt. Do not invent SLAs before the owner selects provider/runtime and service objectives.

### OBS-05 — Alert routing and escalation require independent ownership (P0)

For each severity and signal family, document primary owner, backup owner, security escalation, research supervisor, and external escalation path. Routes must not depend solely on the component being monitored or on credentials that component can control. SEV-0/SEV-1 must have a tested path to an independently administered destination. If no human coverage is available, record that fact and keep protected operations disabled; an alert queue is not on-call coverage.

The eventual routing matrix must specify delivery channels, authenticated recipients, acknowledgement deadline, escalation deadline, fallback channel, duplicate suppression, and evidence of successful delivery. No destination or recipient is selected in this audit.

### OBS-06 — Acknowledgement, silence, and alert closure must not mutate protected state (P0)

Acknowledgement means a named authenticated responder has seen an alert; it does not mean the incident is resolved. Closure requires an immutable incident record, cited evidence, disposition, reviewer, and reason. Suppression/silence must be scoped by exact alert fingerprint, owner, start/end time, justification, and policy version. Expired silences automatically stop suppressing notifications. Security/integrity alerts cannot be silenced by the worker, dispatcher, provider, or the identity under investigation.

Alert acknowledgement, suppression, escalation, and closure are monitoring records only. None may clear an emergency hold, restore approval validity, authorize dispatch, retry delivery, or close a research gate. Any protected response uses its own independent, authenticated, operation-bound authorization protocol.

### OBS-07 — Monitoring itself is a high-value trust boundary (P0)

Protect monitoring configuration, alert rules, routing, suppression lists, log retention, clocks, signing keys, and administrator access from worker and dispatcher control. Use least-privilege write paths; workers may emit bounded telemetry but cannot delete, rewrite, downgrade, or suppress it. Prefer append-only or immutable storage with independent retention and access audit. Alert-rule changes require versioned review, two-person approval for security-critical rules, staged rollout, and a rollback record that does not erase prior history.

Monitor the monitor: heartbeat and ingestion lag, dropped/invalid events, queue depth, clock drift, retention failures, destination delivery failures, rule-evaluation failures, unauthorized configuration changes, and missing independent audit receipts. A monitoring outage or integrity uncertainty must produce an independently observable SEV-1/SEV-0 signal where possible and force the system into a documented degraded/read-only posture. Do not claim full coverage when the monitoring root shares the same administrative failure domain as the system it observes.

### OBS-08 — Logs and alerts must be useful without leaking secrets or sensitive data (P1)

Define an owner-approved telemetry data classification and minimization policy. Never log access tokens, private keys, raw credentials, full authorization headers, session cookies, secret environment values, or unnecessary personal information. Avoid copying complete market datasets or worker payloads into alert text. Prefer immutable IDs, digests, bounded status fields, source references, and access-controlled evidence links. Preserve raw evidence in the separately governed evidence store, not in chat/email notification bodies.

Specify encryption in transit/at rest, key ownership and rotation, region/data residency, access logging, retention/deletion schedules, legal hold, export controls, and incident access. Redaction must be deterministic and tested without destroying evidence needed for forensic verification. Alerts should contain enough context to act but not enough data to become a secondary secret store.

### OBS-09 — Independent time, sequence, and retention are required for trustworthy detection (P1)

Record trusted receiver time, producer time, source sequence/cursor, monotonic registry sequence, and ingestion time as separate fields. Detect clock drift, timestamp regression, sequence gaps, duplicate IDs, stale events, and late arrivals. Alert windows must use trusted service time and tolerate documented provider delivery delay without assuming that delay proves absence.

Retention must cover the maximum approved investigation, provider reconciliation, backup/restore, and legal requirements with an owner-approved margin. If source history expires before reconciliation, alert and preserve UNKNOWN; do not infer a terminal outcome. Monitoring retention and evidence retention are separate policies and must be linked by immutable references.

### OBS-10 — Incident response needs evidence-preserving playbooks and role separation (P0)

For each SEV-0/SEV-1 class, prepare a runbook that defines: trigger evidence; immediate read-only containment; independent deny-only emergency-hold criteria; credential/session/key containment outside a frozen registry; provider-side cancellation only where separately authorized; raw evidence preservation; registry/witness reconciliation; affected assignments and approvals; role-conflict checks; communications; recovery criteria; independent review; and post-incident actions.

The incident commander cannot unilaterally become security custodian, recovery operator, witness verifier, independent reviewer, or resume authority. Break-glass remains two-principal, short-lived, incident-bound, and unable to resume or grant authority. Resume returns only to read-only/non-dispatching state; normal activation requires a separate decision. Alerts never invoke break-glass or emergency controls automatically.

### OBS-11 — Detection coverage must be measurable and tested synthetically (P1)

Create a coverage matrix mapping each threat/lifecycle failure to producer, detection rule, alert route, retained evidence, responder, and synthetic validation case. At minimum cover unauthorized permission changes, policy drift, stale handoff, approval expiry/revocation, duplicate/conflicting dispatch, lost provider receipt, callback forgery/replay/gaps, provider outage/retention expiry, worker silence/resource abuse/isolation failure, missing/tampered artifacts, evidence-manifest mismatch, witness outage/rollback/fork, backup restore divergence, monitoring outage, alert-route failure, suppression abuse, and common-root compromise.

Measure event-ingestion completeness, detection latency, notification delivery/acknowledgement latency, unresolved alert age, false-positive rate, rule coverage, and time to establish monitoring health. Define synthetic test oracles and retain exact rule/config versions. No test execution is authorized by this document; validation remains blocked until the active handoff permits it.

## Required alert record

A future alert record should be immutable and versioned, with at least:
- alert ID and stable fingerprint;
- alert type, severity, rule ID/version, and policy version;
- first/last observed time and trusted receiver time;
- authenticated source namespace and source event IDs/digests;
- exact repository/workflow/run/task/assignment/attempt/provider/checkpoint identifiers where applicable;
- affected resource and evidence references;
- correlation confidence and unresolved identity/order conflicts;
- detection window, threshold, and rule explanation;
- routing attempts and authenticated delivery receipts;
- acknowledgement, escalation, suppression, and closure records as separate append-only facts;
- retention classification and integrity/provenance metadata.

The alert record is a monitoring artifact, not a registry command or authorization token.

## Required synthetic conformance cases

1. Critical producer heartbeat disappears while no lifecycle events are expected.
2. Ingestion queue drops or delays a valid event; source sequence exposes the gap.
3. Exact duplicate event is delivered repeatedly; one alert fingerprint remains stable.
4. Same source/event identity arrives with changed facts; security conflict is raised and original evidence retained.
5. Events arrive out of order across provider callback and query channels; no arrival-time overwrite occurs.
6. A dispatch attempt remains uncertain beyond its approved reconciliation window; alert raised, no retry.
7. Provider reports not-found before its documented visibility horizon; no false absence alert closure.
8. Worker exceeds resource/time budget; monitoring detects it without granting worker extra runtime.
9. Worker return claims success but authenticated receipt/artifact is missing or mismatched.
10. Evidence object or manifest hash changes after receipt; integrity alert is raised.
11. Witness outbox remains pending or external checkpoint regresses/forks; protected writes remain frozen.
12. Backup restore is behind/ahead of independent witness; incident is raised, no automatic resume.
13. Monitoring rule, silence, retention, or routing configuration changes without required approval.
14. Alert destination is unavailable; independent fallback and delivery failure are recorded.
15. Acknowledgement is recorded but alert remains unresolved; escalation continues on policy.
16. An alert is suppressed past expiry or a security alert is silenced by a conflicted identity; suppression is rejected.
17. Monitoring service loses its own heartbeat, clock integrity, audit sink, or retention proof.
18. Secret-bearing payloads are redacted from alert text while raw evidence remains in separately controlled custody.
19. SEV-0 alert occurs during registry freeze; monitoring can notify without writing to the frozen registry.
20. Incident response attempts to use alert acknowledgement as dispatch approval, hold clearance, task acceptance, or gate closure; all are denied.

Oracles must prove monitoring has no protected-action authority, no loss or rewrite of source evidence, no false certainty from silence/timeouts, no suppression by conflicted principals, and independent visibility of monitoring failure.

## Current status and non-claims

This is a targeted design audit, not a live observability assessment. No monitoring vendor, log store, metrics platform, alert manager, notification channel, on-call rotation, incident system, data region, retention policy, or recipient is selected or configured. No dashboards, alert rules, credentials, integrations, workflows, tests, scripts, network calls, provider calls, or incident notifications were created or run. No live telemetry was inspected. The agent remains non-operational; no unattended work is running; Phase 3 G0-05 remains controlling.
