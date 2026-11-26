# Trusted backend selection decision framework

## Status and decision authority

**Evaluation framework only; no provider or backend selected.** This document converts the registry interface, dispatcher, store-adapter and threat-model requirements into a reviewable selection process. It does not authorize procurement, account creation, secrets, repository permissions, deployment, tests, workflow changes, dispatch or research execution.

The current Phase 3 G0-05 handoff remains controlling. No candidate may be activated until a separate approval and a then-current handoff explicitly permit the exact implementation and validation scope.

## 1. Non-negotiable qualification gates

A candidate is disqualified if it cannot demonstrate every applicable gate:

1. **Atomic multi-record transaction:** assignment state, event, idempotency index, global checkpoint and per-assignment version commit together.
2. **Concurrency correctness:** conditional writes/transactions protect both global registry version and assignment version; concurrent first-delivery races produce one winner.
3. **Replay semantics:** exact replay returns the original receipt before stale-check rejection; changed facts are rejected.
4. **Independent identity:** authenticated service identities and least privilege; worker cannot write protected registry, approval, package-digest or checkpoint records.
5. **Approval separation:** human approval/revocation is authenticated independently of worker input and revalidated at the operation boundary.
6. **Immutable evidence:** package bytes, raw worker returns, receipts and lifecycle events are retained with independently checked digests.
7. **Queryable delivery:** provider supports durable idempotency and queryable outcome, or an equivalent reconciliation contract; otherwise unattended delivery stays disabled.
8. **Anti-rollback:** a checkpoint witness exists outside the mutable registry's rollback/admin domain.
9. **Recovery:** consistent backups, point-in-time recovery or equivalent, restore verification and documented recovery ownership.
10. **Auditability:** authenticated audit logs, exportable receipts, access history, retention and incident response.
11. **Bounded operation:** quotas, rate limits, concurrency limits, cost visibility and safe pause controls.
12. **Operational fit:** approved hosting boundary, data residency/retention fit, manageable maintenance and no dependency on the research VPS or self-hosted runner.

A vendor feature page or marketing claim is not evidence. Each gate needs documentation and a disposable proof-of-capability plan before selection.

## 2. Candidate architecture classes

| Candidate class | Potential strengths | Critical questions / risks | Preliminary disposition |
|---|---|---|---|
| Managed relational database with strong transactions | Natural representation of immutable records, unique constraints, transactional event/index/checkpoint updates, consistent reads and SQL audit queries | Does the chosen service expose true atomic transactions at required scale? Can global and per-assignment versions be checked together? How are admin roles, backups and external checkpoint protected? | **Best initial class to evaluate**, subject to proof and independent identity/checkpoint services |
| Managed transactional key-value/document store | Conditional writes, managed scaling and service identity integration may suit a narrow command API | Can it atomically update all records and indexes across required partitions? Are transaction limits, isolation, retry semantics and queryability adequate? Can the event log remain globally ordered? | Viable only if full transaction and ordering proof passes |
| GitHub repository commits as registry | Familiar audit history and source-adjacent access controls | Repository writes are not automatically an atomic registry transaction; branch protection and API race semantics may not satisfy dual-version CAS; workflow/token compromise can collapse trust roots; unsuitable for mutable provider state | **Do not use as sole authoritative registry** |
| GitHub Actions artifacts as registry | Convenient immutable run outputs and easy report handoff | No transactional append, uniqueness index, compare-and-swap checkpoint or reliable queryable mutable state | **Reject as authoritative registry**; retain only as report/export channel |
| Local SQLite or research VPS filesystem | Simple local prototype and low setup overhead | Single-host availability, credential/admin separation, backup rollback, runner compromise and concurrent writer guarantees become difficult; conflicts with VPS isolation policy | **Do not select for unattended trusted control plane** |
| Custom registry service plus transactional store | Can centralize authentication, policy checks, command semantics and audit receipts | Larger implementation/security burden; service becomes high-value trust root; needs deployment, key management, monitoring and independent review | Consider only if managed primitives cannot meet requirements |

This table compares architecture classes, not named vendors or current product plans. No provider capability is asserted as verified.

## 3. Required logical topology

The preferred evaluation topology separates authority domains:

- **Human approval channel:** authenticates the project owner/reviewer and records exact operation-bound decisions and revocations.
- **Dispatcher identity:** short-lived, narrowly scoped identity that can request only approved commands.
- **Registry API:** validates transitions and performs atomic transactions; workers never receive direct database credentials.
- **Transactional store:** holds immutable records, lifecycle events, indexes and materialized state.
- **External checkpoint witness:** independently retains monotonic sequence/hash or signed checkpoint so a stale restore is detectable.
- **Worker provider:** receives only the approved assignment package and returns through an authenticated channel.
- **Evidence/report store:** stores report artifacts and raw evidence references; it is not the lifecycle authority.
- **Independent reviewer:** can read and verify records but cannot silently rewrite them.

A single vendor may host multiple components only if identity, permissions, administrative roles and rollback domains remain meaningfully separated. Nominally separate services sharing one administrator credential are not independent trust roots.

## 4. Evaluation scorecard

Score only after a candidate passes all mandatory gates. Use 0–5 per criterion: 0 = absent, 1 = weak/undocumented, 3 = demonstrated with limitations, 5 = independently demonstrated. Mark unknown as **U**, not zero, and do not compute a final score while mandatory criteria are unknown.

| Criterion | Weight | Evidence required |
|---|---:|---|
| Atomic transaction and dual concurrency | 20 | Transaction documentation plus concurrent proof-of-capability |
| Identity and separation of duties | 15 | Role matrix, service identity model, audit evidence |
| Approval/revocation integration | 10 | Authenticated approval source and boundary recheck design |
| Replay and idempotency | 10 | Durable unique constraints and replay race proof |
| Checkpoint/anti-rollback | 10 | Independent witness, restore/rollback proof |
| Backup and recovery | 10 | RPO/RTO, point-in-time restore and recovery drill design |
| Delivery provider semantics | 5 | Idempotent/queryable delivery contract |
| Audit and evidence retention | 5 | Immutable export, retention, integrity verification |
| Operational safety and limits | 5 | Quotas, cost controls, pause, alerting |
| Hosting, privacy and maintainability | 10 | Region/data handling, ownership, maintenance burden |
| **Total** | **100** | Mandatory gates still override score |

No score is assigned in this document because no provider has been evaluated or tested.

## 5. Questions that must be answered before provider comparison

1. Is a separate repository/organization boundary approved, or must the agent remain inside the existing repository?
2. Which hosting/account boundary may hold registry records and approval metadata?
3. Who can approve, revoke, administer the store, and verify recovery? Can those roles be separated?
4. What region, retention, privacy and data-export requirements apply?
5. What is the acceptable monthly cost and operational maintenance burden?
6. Which worker-delivery provider is intended, and can its delivery be queried by a stable idempotency key?
7. What independent checkpoint witness is acceptable, and who controls its credentials?
8. What recovery point and recovery time objectives are acceptable?
9. Which workflow identity and immutable workflow revision can be trusted?
10. Which canonical JSON/hash version will be used for future lifecycle events? Event v1 must remain unchanged.

These are future owner decisions. No credentials, account access or sensitive values should be posted into the repository or chat.

## 6. Recommended evaluation sequence

1. Freeze this decision framework and the existing backend interface contract.
2. Resolve repository topology and hosting boundary before comparing individual products.
3. Select at most two candidate classes/providers for documentary review; do not create accounts.
4. For each, map every mandatory gate to a specific documented capability and identify unknowns.
5. Design a disposable proof-of-capability using synthetic records only, with no research data or live worker.
6. Independently review transaction, identity, approval, idempotency and anti-rollback evidence.
7. Obtain explicit project-owner approval for one backend and trust-root topology.
8. Only after a separate controlling handoff permits it, implement a minimal adapter on the isolated agent branch.
9. Validate in an isolated disposable environment before any manual workflow readiness exercise.
10. Treat scheduled/event-driven dispatch and production use as later, separate approvals.

## 7. Stop conditions

Keep the system inactive if any of the following is unresolved: no independent approval identity; worker can mutate trusted records; no atomic update across event/index/state/checkpoint; no dual concurrency control; ambiguous replay behavior; no package digest retained before delivery; provider outcome cannot be queried; checkpoint can be rolled back with the database; restore has not been verified; or the current handoff prohibits the proposed work.

## 8. Current project status

- No backend, vendor, hosting region, account or database is selected.
- No credentials, secrets, service identities or external resources were created.
- No registry API, dispatcher, delivery channel or independent checkpoint witness exists.
- Current ledger/persistence modules remain pure in-memory primitives.
- Existing GitHub artifacts remain report outputs only, not a trusted mutable registry.
- No tests, scripts, workflows, dispatch, scheduling, VPS access or research execution were performed.
- The agent is not operational.
- The Phase 3 G0-05 handoff remains authoritative.

This document is a decision aid, not an implementation authorization.
