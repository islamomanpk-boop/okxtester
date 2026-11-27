# Security architecture contradiction audit — 2026-11-27

## Scope and method

Targeted static comparison of the current agent-branch contracts for the unified lifecycle, assignment registry, backend/store adapter, approval lifecycle, restore/witness reconciliation, trust-root separation, emergency suspension/break-glass, and implementation readiness.

This audit checks whether the same operation has one compatible meaning across documents. It does not inspect a deployed identity provider, database, witness, worker provider, cloud account, workflow, or permission set. It does not execute code or tests.

## Executive result

**The architecture is substantially aligned on core lifecycle invariants, but the emergency-denial and resume-authority boundary needed a normative reconciliation.** The principal issue was not that emergency revocation should be allowed to mutate a frozen registry. It was that the documents did not distinguish immediate out-of-band credential containment from durable registry approval revocation while protected writes are frozen.

Two further ambiguities were corrected: the approval record's revocation-state wording, and a registry-design phrase that could conflate assignment cancellation with approval revocation. The resume quorum is now defined by identity and administrative independence, not merely by counting two accounts.

## Findings and resolutions

### CA-01 — Emergency credential containment versus frozen registry writes (P0)

**Observed ambiguity**
- The emergency protocol allowed a security authority to revoke an approval through the normal authenticated append-only path.
- The same protocol's emergency freeze stops protected registry writes.
- The restore protocol also freezes approval consumption/revocation processing while history and witness state are reconciled.

A reader could infer that emergency approval revocation must either violate the freeze or wait without any independent deny control.

**Resolution**
- Emergency freeze is an independent, deny-only security-plane hold. It blocks affected protected operations without changing registry history or creating a positive authorization.
- Credential/session/key containment is performed through the independent identity/security control plane and recorded in its independently retained incident audit.
- While the hold is active, approvals in the affected trust domain/incident scope are unusable; if compromise scope is uncertain, affected approval status is UNKNOWN and denied.
- No approval-revocation event is appended to a frozen or witness-pending registry.
- After the registry chain and witness are reconciled, but before any affected capability resumes, the trusted registry appends the exact approval revocation/invalidation facts, commits the matching outbox, obtains the external witness receipt, and verifies the resulting checkpoint. If this cannot be completed, the affected capability stays frozen.
- The security-plane hold remains active until the required registry events and independent resume authorization are verified. The hold cannot itself authorize an operation or replace the registry event.

### CA-02 — “Two people” did not define an independent resume quorum (P0)

**Observed ambiguity**
The prior protocol required two distinct principals for break-glass activation and multi-party resume, but did not specify which roles could sign resume or how to handle shared identity-provider/root recovery.

**Resolution**
- Resume requires two distinct human approvers with stable authenticated subject IDs and independently controlled credentials/authentication recovery.
- Both sign the exact registry ID, checkpoint epoch/sequence/digest, recovery-report digest, service scope, and expiry.
- Neither signer may be the freeze requester, break-glass activator, recovery operator, witness administrator/verifier, independent reviewer, or recovery-code deployer.
- The two approvers must not share an administrator or recovery path capable of unilaterally taking over both identities. Separate accounts in one commonly controlled tenant do not prove independence.
- The independent reviewer records a separate evidence-based recommendation; reviewer and approvers are not interchangeable.
- If distinct administrative/recovery control cannot be evidenced, remain suspended or obtain an additional genuinely independent trust root; do not weaken the quorum by counting aliases or service accounts.

### CA-03 — Approval record field wording could imply mutable revocation state (P1)

**Observed ambiguity**
The registry design described the immutable approval record as binding “expiry/revocation state,” then correctly stated that revocation and consumption are separate append-only facts and derived status.

**Resolution**
The approval record contains immutable issuance facts, including expiry. It contains no mutable revocation or consumption state. Current status is derived from immutable issuance plus authenticated ordered lifecycle events and trusted service time.

### CA-04 — Assignment cancellation and approval revocation were grouped in one phrase (P1)

**Observed ambiguity**
The registry design used “cancellation/revocation” in a single transition sentence, which could blur assignment cancellation, approval revocation, credential revocation, and provider-side cancellation.

**Resolution**
These are separate facts and operations:
- assignment cancellation blocks future assignment attempts;
- approval revocation blocks future use of that approval;
- credential/session revocation disables an identity credential through the identity/security plane;
- provider-side cancellation is a separate provider operation with its own authorization and authenticated receipt;
- none erases a committed dispatch attempt or proves provider execution stopped.

## Cross-document invariants after correction

1. A freeze is deny-only, monotonic for its incident scope, and independent of registry mutation.
2. Emergency credential containment may proceed out of band; authoritative approval revocation remains an append-only registry fact.
3. The registry cannot accept protected writes while witness-pending. The witness publisher may reconcile only the exact pending checkpoint; it cannot process unrelated revocation events or authorize service resume.
4. Affected approvals remain unusable under the external hold/UNKNOWN rule until revocation history is durably appended and witnessed.
5. Assignment cancellation, approval revocation, credential revocation, and provider cancellation are never conflated.
6. Two independent human resume approvers are required, distinct from incident/recovery/review/witness/deployment roles and independent in their administrative recovery paths.
7. Resume restores only the exact named service scope. Dispatch remains separately gated by fresh operation-bound approval.
8. No emergency mechanism can create approval, accept a worker return, approve task completion, close a phase gate, advance a phase, or bypass G0-05.

## Evidence still required before implementation

- An independently administered emergency hold/deny control with authenticated monotonic incident records.
- Effective identity-provider, MFA/passkey recovery, tenant/root, and security-admin permission exports.
- Proof that the two resume approvers have independent administrative and credential-recovery paths.
- A registry protocol for appending and witnessing incident-driven approval revocations before releasing the external hold.
- Negative tests for freeze, out-of-band credential containment, delayed registry revocation, witness-pending behavior, quorum separation, common-root compromise, and replayed resume authorization.
- Independent review of the actual deployed control plane and audit-retention boundary.

## Status and limitations

This audit and its resolutions are documentation-only. No emergency hold service, identity provider, registry, witness, approval channel, external audit sink, or recovery process is implemented or provisioned. No tests, scripts, workflows, dispatch, scheduling, VPS operations, or research operations were run. The agent remains non-operational. The Phase 3 G0-05 handoff remains controlling. All edits are confined to `research_agent/` on `agent/okx-research-agent-v1`.
