# Provider delivery idempotency and receipt audit — 2026-11-27

## Scope and method

Targeted static review of:
- `docs/TRUSTED_DISPATCHER_CONTRACT.md`
- `docs/UNIFIED_TRUSTED_LIFECYCLE_TRANSACTION_SPEC.md`
- `docs/TRUSTED_REGISTRY_BACKEND_INTERFACE_SPEC.md`
- `docs/TRUSTED_STORE_ADAPTER_DESIGN.md`
- `docs/TRUSTED_ASSIGNMENT_REGISTRY_DESIGN.md`
- `docs/DISPATCH_CANCELLATION_AND_REVOCATION_RACE_AUDIT_2026-11-27.md`
- `docs/WORKER_RETURN_LIFECYCLE_REPLAY_AUDIT_2026-11-27.md`
- `docs/IMPLEMENTATION_READINESS_AND_EXIT_CRITERIA.md`

This is a documentation-only protocol audit. No provider, account, credentials, code, tests, scripts, workflow, network request, dispatch, or research operation was used.

## Executive result

The architecture already has the correct fundamental boundary: the durable `dispatch_started` transaction precedes the external provider call; provider acceptance is not implied by request submission; ambiguous delivery stays pending/unknown; and no fresh delivery identity or automatic retry is allowed.

The review identified missing provider-contract precision. “Durable idempotency” and “authenticated, queryable receipt” were named as requirements but not fully qualified. Provider idempotency may be scoped to an account/endpoint and retained only for a finite window. A key may also be bound to a request body, and a provider may return stale or non-terminal status observations. Reusing a key after its provider retention expires can create a second job. A successful HTTP response or unsigned webhook may not prove the intended provider-side state.

## Findings and required resolutions

### PD-01 — Provider idempotency scope and retention were not bounded (P0)

**Risk:** A provider may deduplicate a key only within one account, endpoint, region, or finite retention interval. If reconciliation is delayed beyond that interval, resubmitting the same key may create another delivery.

**Required contract:**
- Qualify key uniqueness by provider identity, tenant/account, API operation/endpoint, region where relevant, and provider-defined key namespace.
- Persist the exact provider idempotency key and all scope components in the immutable dispatch attempt before any provider call.
- Provider documentation/evidence must establish key retention duration, exact replay behavior, and what happens when the same key is reused with a changed request.
- The maximum automated reconciliation horizon must be strictly shorter than the proven provider retention window, with a safety margin.
- Once the retention window may have expired, never resubmit the request—even with the same key. Use authoritative provider lookup or independent provider support/reconciliation. If outcome cannot be proven, keep it UNKNOWN and require human resolution; do not create another key or attempt.
- If retention, scope, or replay behavior is undocumented or cannot be independently verified, provider is not qualified and dispatch remains disabled.

### PD-02 — Idempotency key was not explicitly bound to immutable request bytes (P0)

**Risk:** A stable key reused with a modified package, endpoint, headers, or semantic request may be rejected, misinterpreted, or treated as a new operation by the provider.

**Required contract:**
- Before dispatch, canonicalize and retain the exact provider request envelope (method/operation, endpoint identity, account/tenant scope, semantic headers, canonical body bytes, content type, API/schema version) and its digest.
- Bind the envelope digest, package digest, assignment revision, attempt ID, approval ID, provider scope, and idempotency key into the immutable dispatch attempt.
- Retries/reconciliation may refer only to the exact same retained request envelope. Any change requires a new authorized assignment revision and approval; it must not be smuggled under an existing attempt/key.
- Exclude ephemeral transport-only headers from the semantic digest only when explicitly documented; preserve enough raw request/response evidence to audit what was sent.

### PD-03 — “Prepare channel” versus “call provider” ordering was ambiguous (P1)

The dispatcher sequence said to use an authenticated delivery channel before the `dispatch_started` commit, while later stating that the provider call occurs after that commit. This can be read as permitting a pre-commit side effect.

**Resolution:** Before commit, the dispatcher may only resolve provider configuration, authenticate locally, validate endpoint/account identity, construct the immutable request envelope, and prepare a call without sending it. The atomic `dispatch_started` commit must persist the exact attempt and key. No provider request bytes may leave the trusted dispatcher before commit succeeds. Only after commit may the exact prepared envelope be submitted once using the recorded key. A crash after commit but before the call leaves an unresolved committed attempt; recovery must reconcile provider state and may submit only under the proven idempotency contract and same exact envelope. It may not mark the attempt unsent or mint another key.

### PD-04 — Provider receipt authenticity and semantic status were underspecified (P0)

**Risk:** HTTP success, an unverified callback, or a provider job ID alone may not establish acceptance, rejection, or terminal completion.

**Required receipt evidence:**
- authenticated provider namespace and account/tenant/endpoint scope;
- provider delivery/job ID and the exact local dispatch attempt ID;
- provider idempotency key and request-envelope digest;
- provider status and whether it is provisional, accepted, rejected, running, cancelled, or terminal;
- provider event/receipt ID, provider timestamp and receiver observation time;
- authenticated raw receipt/callback bytes and receiver-computed digest;
- signature/MAC or authenticated API response provenance, with key identity/version and verification result where applicable;
- query consistency/version/cursor information where provider status is eventually consistent.

A receipt must be verified against provider documentation and a trusted key/transport. Webhook/callback events need signature verification, replay protection, unique event IDs, and monotonic transition handling. Out-of-order or stale status must not overwrite a later verified state. Transport-level 2xx means only that the transport endpoint responded unless provider semantics explicitly define it as durable acceptance.

### PD-05 — Provider query/reconciliation capability needed exact semantics (P0)

A queryable outcome must support lookup by the original provider idempotency key and/or provider delivery ID within the qualified scope, and return enough authenticated evidence to distinguish:
- no matching request, with documented authoritative absence semantics;
- request accepted/queued/running;
- request rejected before execution;
- terminal success/failure/cancelled;
- unknown, expired, or unavailable history.

A “not found” response is not proof of non-delivery unless the provider documents consistency guarantees and a bounded visibility delay. Re-query according to documented bounded backoff while preserving the same attempt. Once the visibility horizon or idempotency retention limit is exceeded, stop automatic reconciliation and escalate to human/provider support. Never infer non-delivery from timeout, missing callback, worker silence, or missing artifact.

### PD-06 — Provider cancellation and late observations

Provider-side cancellation remains a separate authenticated command bound to the provider job, original attempt, package/request digest, cancellation approval, and idempotency identity. Its accepted response is not proof that execution stopped; require an authenticated terminal cancellation observation. A cancellation request racing with success/failure must preserve all immutable observations and derive current state without overwriting history. Late receipts/callbacks are retained and reconciled; they cannot be discarded because local assignment cancellation occurred.

## Normative provider-delivery protocol

1. Qualify provider capabilities before enabling dispatch: key scope, key retention, exact replay semantics, request-body binding, lookup semantics, receipt authenticity, status consistency, cancellation behavior, rate/size limits, and support escalation.
2. Construct the exact immutable provider request envelope from the protected assignment/package. Compute and retain its digest and the provider scope.
3. Authenticate dispatcher and provider configuration. This stage may prepare but must not send request bytes.
4. In one registry transaction, revalidate the current handoff/policy, emergency hold, assignment revision, approval scope/expiry/revocation/consumption, cancellation state, provider qualification version, provider scope, and expected checkpoint. Persist immutable attempt ID, exact provider key, key scope, request-envelope digest/reference, package digest, approval ID, and `dispatch_started` event/checkpoint. This is the authorization/attempt linearization point.
5. Only after commit, submit the exact retained request envelope once with the recorded key. No pre-commit provider side effect is permitted.
6. Verify and persist authenticated provider receipt/response bytes, digest, signature/transport provenance, provider event ID, provider job ID, key, scope, request digest, and status as a separate observation.
7. If the call times out or the response is lost, record pending/unknown if possible and query the original provider identity. Never mint a new key or attempt.
8. Re-submit only if provider documentation proves that the exact same key and exact same request are still within the provider's deduplication window and exact replay cannot create a second logical job. Otherwise query only; if unresolved, stop and escalate.
9. If key retention may have expired or provider lookup cannot prove absence/presence, mark unresolved UNKNOWN. Do not resubmit, even with the same key. Require independent human/provider reconciliation before any new assignment or attempt.
10. A new dispatch attempt requires a new assignment revision where applicable, fresh exact human approval, and a new provider key only after the prior attempt is conclusively resolved and policy permits a new attempt. A new key is never a workaround for uncertainty.

## Required provider qualification evidence

Before any provider is selected, obtain:
- versioned official provider documentation for idempotency scope, retention, replay, and body mismatch;
- documented lookup/query API and consistency/visibility guarantees;
- receipt and webhook authentication specification, signing-key rotation, replay protections;
- cancellation semantics and terminal-state evidence;
- rate limits, payload limits, timeout behavior, and support/escalation path;
- synthetic conformance evidence for duplicate requests, changed body under same key, delayed callback, expired key, stale query, timeout after acceptance, provider restart, and cancellation races.

Provider feature claims must be tested in an approved synthetic environment. Documentation alone is not proof that a particular account/API version has the capability.

## Current status

Provider, provider account, API version, endpoint, idempotency retention, query semantics, receipt verification, cancellation API, and support path are all unselected/unverified. The design therefore remains **BLOCKED: do not dispatch**. No code/tests/scripts/workflows/provider calls or research operations were run. The agent remains non-operational and the Phase 3 G0-05 handoff remains controlling.
