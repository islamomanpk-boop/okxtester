# Worker-return lifecycle, replay, and late-arrival audit — 2026-11-27

## Status and authority

Targeted static review of the assignment-return module and the unified lifecycle, registry, backend-interface, and dispatcher contracts. No tests, scripts, workflows, dispatch, scheduling, VPS access, or research operations were run. No research code/data or protected branch was changed. The current Phase 3 G0-05 handoff remains controlling; this audit grants no execution or validation authority.

## Executive result

The design documents already state the essential high-level rules: raw returns are untrusted, the receiver computes the digest, delivery and assignment bindings come from trusted records, late returns are preserved, and review/task acceptance/gate closure are separate. The targeted review found that these statements need a more precise, interoperable transaction contract for duplicate returns, changed-payload replay, parse ordering, late-return handling, and review/disposition uniqueness.

The current implementation is intentionally much narrower. `engine/assignment_return.py` accepts a Python dictionary that has already been parsed, a caller-supplied assignment package, and a caller-supplied expected package digest. It does not accept raw bytes, authenticate a transport, resolve a delivery receipt, allocate a receiver-owned return ID, persist a raw payload, or enforce return/review idempotency. It explicitly reports that dispatch/delivery is not verified. This is not a defect in the current pure review helper; it is a missing future receiver/registry layer and must not be mistaken for an operational return path.

## Findings

### WR-01 — Raw-byte capture and digest-before-parse need an exact protocol (P0)

The unified lifecycle and backend interface say to store raw bytes before parsing, but do not fully define how a receiver handles malformed bytes, size limits, encoding, duplicate JSON keys, or the boundary between raw receipt and normalized submission.

Required future rule:
1. Authenticate the return transport and derive source namespace, provider delivery ID, dispatch attempt, assignment revision, and receipt time from trusted transport metadata.
2. Enforce a configured byte-size limit before parsing; preserve the exact received byte sequence in immutable storage and compute SHA-256 over those exact bytes at the receiver.
3. Commit the raw receipt and its idempotency record before any parser or reviewer processes it. If persistence outcome is uncertain, reconcile by the same authenticated return-delivery identity.
4. Parse only the retained bytes using strict UTF-8 and strict JSON rules (duplicate keys, non-finite numbers, unsupported values, and schema drift rejected). Never reserialize parsed JSON and call that the raw-payload digest.
5. Preserve malformed raw receipts with a bounded parse-error classification; do not discard or overwrite the original bytes. A malformed receipt cannot enter structural/evidence review.
6. Store any normalized representation separately and bind it to the raw digest, parser/schema version, and normalization version.

### WR-02 — Return identity and duplicate/conflicting replay need durable uniqueness (P0)

A receiver-generated `return_id` is already required, but the contracts do not fully specify the unique transport identity and replay facts for return receipts.

Required future rule:
- Use an authenticated return-delivery key such as `(return_source_namespace, return_delivery_id)`, scoped to the provider's documented delivery semantics. Enforce a durable unique constraint.
- The immutable facts digest must cover dispatch attempt, assignment ID/revision, expected package digest, authenticated source identity, raw byte digest, byte length, and transport receipt facts that affect meaning.
- Same key + same complete facts returns the original receipt and original `return_id`; it must not append a second receive event or create a second review/disposition path.
- Same key + different facts is a changed-replay security conflict. Preserve the first receipt, quarantine the conflicting arrival as separate incident evidence, and do not overwrite the original.
- A different delivery key carrying identical bytes is a separately observed transport arrival, not automatically an exact replay. Link it to the same raw-payload digest and mark it as a duplicate-content arrival; require an explicit policy decision before creating another review.
- Never deduplicate solely by worker-supplied return ID, payload digest, task ID, or timestamp. Worker values are untrusted declarations.

### WR-03 — Delivery and assignment binding must precede eligibility (P0)

The receiver must resolve the authenticated delivery identity against a committed dispatch attempt and protected assignment revision. It must load the retained canonical package bytes and digest from the registry, verify those bytes, and compare all worker-claimed assignment/task/package identifiers only as untrusted consistency checks.

Unknown, unconfirmed, mismatched, or ambiguous delivery identity must not be promoted into an eligible submission. A transport-authenticated return does not itself prove the worker received the exact package. The registry must bind the return to the exact delivery attempt and package digest.

### WR-04 — Late, cancelled, revoked, or expired returns need a terminal eligibility classification (P0)

The documents require late returns to be preserved and excluded from valid completion, but the receiver contract should distinguish at least:
- `eligible_for_review`: delivery confirmed, assignment revision matches, and no applicable cancellation/expiry/revocation rule bars acceptance;
- `received_late_after_cancel`;
- `received_after_expiry`;
- `received_after_revocation`;
- `delivery_binding_unknown`;
- `assignment_or_package_mismatch`;
- `malformed_payload`.

These classifications are immutable receipt facts/derived review eligibility, not worker-controlled fields. Late or ineligible returns remain preserved with their raw digest. They cannot advance the normal `submission_received` → `review_completed` → human disposition path. If any inspection is later permitted, it must be a separate, explicitly authorized incident/forensic review that cannot silently convert the return into task completion evidence. A committed dispatch attempt is not erased by later cancellation; the return remains linked to that attempt.

### WR-05 — Review idempotency and disposition uniqueness need explicit keys (P1)

A repeated return must not produce multiple independent reviews or allow a second review to overwrite the first. Define:
- review identity bound to `(return_id, raw_payload_sha256, assignment_revision, reviewer_policy_version)`;
- exact replay returns the original immutable review receipt;
- changed review facts under the same identity are rejected and preserved as a conflict;
- a corrected/new review is a new linked review record with a new review ID and explicit supersedes/revision relation;
- human disposition binds to one exact review digest and assignment revision, with durable idempotency and an explicit rule for whether a later human decision supersedes an earlier disposition. No worker or automated review may create or alter disposition;
- phase-gate disposition remains a separate authority and event.

### WR-06 — Current helper is not a receiver and does not implement these guarantees (P0)

Static inspection of `engine/assignment_return.py` confirms:
- input `submission` is already a dictionary; raw bytes and parse provenance are outside the interface;
- expected package digest is passed by the caller, and no trusted registry currently retains it;
- the helper rebuilds and compares the assignment package before review;
- it does not authenticate transport, prove dispatch/delivery, bind a provider delivery ID, create a return ID, persist a receipt, detect duplicate returns, or apply cancellation/expiry/revocation eligibility;
- it returns `dispatch_or_delivery_verified=False`, `task_completion_approved=False`, and `gate_closure_approved=False`.

The integrated review pipeline also accepts caller-supplied commit/manifest/bytes and explicitly says those are not authenticated by the orchestration layer. Therefore no current module should be described as a complete worker-return lifecycle implementation.

## Required design updates

The unified lifecycle specification, assignment registry design, and dispatcher contract now need to carry the above raw-byte, identity, replay, eligibility, review-idempotency, and human-disposition rules. The detailed requirements are recorded in the updated contracts and this audit.

## Prioritized blockers

| Priority | Blocker | Required evidence before implementation |
|---|---|---|
| P0 | Authenticated return transport and delivery-attempt binding | Provider contract, identity derivation, exact delivery receipt verification |
| P0 | Immutable raw-byte receipt and digest-before-parse | Receiver API/schema, bounded raw object storage, strict parser contract |
| P0 | Return idempotency and changed-replay quarantine | Unique constraints, complete facts digest, atomic receipt/event/checkpoint transaction |
| P0 | Late/cancelled/revoked/expired eligibility | Trusted service-time and assignment-state transition rules |
| P0 | Trusted package custody | Independently retained canonical bytes and digest, not caller/worker input |
| P1 | Review and disposition idempotency | Immutable review identity, supersession, exact human decision binding |
| P1 | Cross-runtime raw/normalized representation | Versioned parser/normalizer and shared fixtures |

## Stop conditions and current status

No receiver, registry, authenticated return channel, durable raw-payload store, provider integration, or human-disposition service exists. The package digest is not independently persisted. No tests or failure injections were executed. The agent remains non-operational; G0-05 remains authoritative. These requirements are design findings only and do not authorize implementation or workflow activity.
