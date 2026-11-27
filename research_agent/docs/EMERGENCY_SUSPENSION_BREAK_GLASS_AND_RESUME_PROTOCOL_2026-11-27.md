# Emergency suspension, break-glass, and recovery authority protocol — 2026-11-27

## Status and authority

Design-only protocol derived from the trust-root separation, administrative independence, approval lifecycle, and restore requirements. No identity provider, emergency channel, registry, witness, account, key, or recovery service is selected or provisioned. This document authorizes no implementation, workflow, dispatch, scheduling, or research execution.

No tests, scripts, workflows, provider calls, or VPS operations were performed. The Phase 3 G0-05 handoff remains authoritative.

## 1. Core rule: emergency suspension is easy; privileged resumption is hard

Any authenticated designated incident reporter may request an immediate deny-only suspension. Suspension may stop dispatch, approval consumption, assignment transitions, return acceptance, human disposition writes, and protected registry writes. It must not create approval, accept work, alter history, bypass the witness, or resume service.

A suspension request is not proof of compromise and need not wait for a second approver before taking the system offline. The system should fail closed on a credible emergency signal. False-positive suspension is an availability incident; failing to suspend during compromise is an authority-integrity incident.

Resumption is a separate operation. No person who requested suspension, invoked break-glass, executed restore, administered the witness, or deployed the recovery code may unilaterally authorize resume.

## 2. Separate emergency capabilities

| Capability | Permitted effect | Explicitly prohibited |
|---|---|---|
| Emergency freeze requester | Trigger deny-only freeze and incident record | Resume, approve dispatch, rewrite registry/witness |
| Incident commander | Coordinate incident, assign roles, maintain timeline | Self-approve restore or alter immutable evidence |
| Credential/security custodian | Revoke or disable affected credentials; rotate under approved process | Create task approval or erase prior identity history |
| Recovery operator | Restore isolated copy and perform documented repair | Dispatch, approve own actions, alter witness history |
| Witness verifier | Independently query/verify witness and checkpoint lineage | Write registry events or approve task execution |
| Independent reviewer | Review evidence, verify role separation and report | Execute restore or alter source evidence |
| Resume authority | Approve narrowly scoped return to service after evidence review | Change historical records or grant research/gate approval |
| Provider cancellation operator | Request provider-side cancellation with separate authenticated receipt | Rewrite dispatch history or assume cancellation succeeded without receipt |

The same human may hold more than one role only if an explicit threat assessment proves no self-approval path and independent controls remain. For high-impact recovery, the recovery operator, witness verifier, and resume authority must be distinct authenticated principals under independently administered credentials. If that separation cannot be demonstrated, remain suspended.

## 3. Break-glass credential design

Break-glass access is a narrowly scoped, short-lived emergency capability, not a superuser account.

Mandatory properties:
- separately enrolled emergency identity and hardware-backed strong authentication where supported;
- dual authorization to activate privileged recovery access, with two distinct principals;
- time-limited grant, one operation scope, one incident ID, and automatic expiry;
- no standing access; no reusable shared password or recovery code;
- no authority to modify approval policy, create/renew approval, rewrite event history, change witness checkpoints, delete audit records, alter branch protections, or resume dispatch;
- independent out-of-band notification at activation and use;
- every privileged action recorded to an independently administered append-only audit destination;
- emergency credential rotation/revocation and post-incident review;
- inability of the break-glass administrator to suppress alerts or administer the only audit destination.

If the identity provider, MFA recovery, root account, or signing key may be compromised, do not trust approvals authenticated solely through that domain after the earliest plausible compromise time. Freeze, revoke affected credentials through an independent path, and re-establish identity trust before resumption.

## 4. Approval and revocation under incident conditions

- Existing approvals remain immutable historical facts. Emergency suspension does not rewrite them as revoked; it makes protected operations unavailable while incident status is unresolved.
- A designated security authority may revoke a specific approval or credential through the normal authenticated append-only path. Revocation is monotonic and does not cancel an already committed provider attempt.
- A new or renewed approval must never be issued by break-glass. It requires the ordinary independent human approval channel, current policy/handoff checks, a fresh ID and nonce, exact operation/scope, and trusted expiry.
- If the approval channel or issuer is compromised or uncertain, approvals from the affected interval are UNKNOWN and cannot authorize operations.
- Provider-side cancellation is a separate provider operation with its own identity, approval requirements, and authenticated receipt. A local freeze is not proof that provider execution stopped.

## 5. Recovery and resume sequence

1. **Freeze:** record incident ID, trigger identity, trusted timestamp, affected systems, and freeze receipt. Deny new protected operations immediately.
2. **Preserve:** isolate failed instances, logs, backups, workflow artifacts, raw returns, and provider receipts as immutable evidence. Do not clean up or rotate away evidence before capture.
3. **Scope compromise:** identify earliest plausible compromise time and every common administrator, identity issuer, key, workflow, runner, billing, support, and recovery dependency.
4. **Contain credentials:** revoke/disable affected credentials and sessions through a separately controlled path. Preserve revocation receipts and identity/key versions.
5. **Assign independent roles:** name incident commander, recovery operator, witness verifier, independent reviewer, and resume authority. Reject self-review and shared-root conflicts.
6. **Restore in isolation:** apply the restore/witness outbox reconciliation protocol. No protected writes or dispatch while witness-pending, divergent, or unverifiable.
7. **Reconcile lifecycle:** verify approval issuance/revocation/consumption/nonces, assignment revisions, all dispatch attempts and provider receipts, cancellations, raw return bytes/digests/bindings, reviews, human dispositions, and phase-gate state. Unknown or missing authoritative history blocks the affected operation.
8. **Review evidence:** independent reviewer verifies exact checkpoint, witness receipt, restore report, credential containment, administrative dependency graph, audit completeness, unresolved deliveries, and residual risk.
9. **Authorize narrow resume:** two distinct authorized principals approve the exact registry ID, checkpoint digest/epoch/sequence, restore report digest, service scope, and expiry. This restores only the explicitly named service capability; dispatch remains separately gated by fresh operation-bound approval.
10. **Monitor and close:** retain elevated monitoring, verify revocation propagation and audit export, record post-incident review, expire break-glass grants, and rotate emergency credentials.

Any UNKNOWN critical identity, checkpoint, approval, delivery, or audit fact means no resume for the affected capability. A human risk acceptance cannot manufacture missing cryptographic history or override the active research handoff.

## 6. Dual-control and anti-self-approval invariants

- No single principal or common credential root may request privileged break-glass access, execute recovery, verify the witness, and authorize resume.
- The recovery operator cannot approve their own restore report.
- The witness verifier must obtain evidence directly from the witness trust domain, not solely from the restored registry.
- The resume authorization must be signed/recorded outside the compromised registry and bound to exact recovery evidence.
- Emergency freeze is deny-only and may be triggered without dual approval; emergency unfreeze/resume always requires independent multi-party authorization.
- Break-glass never grants task completion, phase-gate closure, strategy selection, research execution, or permission to bypass G0-05.

## 7. Required synthetic validation before deployment

In an approved synthetic environment, independently validate:
1. one-person freeze succeeds but one-person resume fails;
2. recovery operator cannot self-approve;
3. shared identity-provider/root compromise marks affected approvals UNKNOWN;
4. break-glass grant expires and cannot be reused or expanded;
5. break-glass cannot modify witness, approval policy, event history, or audit retention;
6. independent audit export survives registry-admin compromise;
7. credential revocation blocks new protected operations within documented maximum latency;
8. provider-side cancellation uncertainty remains unresolved until authenticated receipt;
9. witness-pending, witness-ahead, forked, and stale restore cases remain frozen;
10. resume authorization is bound to exact checkpoint/report and cannot be replayed for another restore or service scope.

These are future test requirements, not tests performed.

## 8. Current status

All controls above are design requirements only. No emergency identity, dual-control channel, independent audit sink, registry, witness, provider, or recovery service exists. No permissions, secrets, workflows, or infrastructure were changed. The agent remains non-operational; G0-05 remains controlling.
