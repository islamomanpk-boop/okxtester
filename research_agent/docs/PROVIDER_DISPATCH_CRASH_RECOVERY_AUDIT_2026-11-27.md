# Provider dispatch crash-recovery audit — 2026-11-27

## Scope and method

Targeted static review of the trusted dispatcher contract, unified lifecycle transaction specification, backend interface, store adapter, provider idempotency audit, restore/witness protocol, and cancellation/revocation race audit.

This is a documentation-only protocol review. No provider, credentials, account, code, tests, scripts, workflow, network request, dispatch, scheduling, VPS access, or research operation was used.

## Executive result

The design already establishes the essential distributed-systems boundary: the registry's atomic dispatch_started commit precedes provider submission; the external provider call cannot be part of the registry transaction; uncertain delivery cannot be treated as non-delivery; and an unresolved attempt cannot be replaced with a new delivery identity.

The review makes crash recovery more explicit. The most dangerous window is provider acceptance followed by process/host failure before the authenticated response is durably committed. Recovery must query the original provider identity and reconstruct the provider outcome. A local dispatch_started row, timeout, absent receipt, or missing callback cannot establish whether the request was sent or accepted.

## Crash-point matrix

| Crash point | What is durably known | Required restart behavior |
|---|---|---|
| Before dispatch-start transaction begins | No committed attempt; provider side effects are forbidden | Revalidate current policy/approval and retry only the same authenticated command identity |
| During dispatch-start transaction; commit outcome unknown to caller | The transaction may have committed or rolled back | Query registry by the exact triggering idempotency identity before doing anything else. Exact committed facts return the original receipt; confirmed absence permits a fresh transaction only after current preconditions are revalidated. Never infer rollback from a lost response |
| After dispatch-start commit, before provider submission | Immutable attempt/key/request envelope exist; provider submission may not yet have happened, but restart cannot infer that from local process state alone | Reconcile/query by the original provider key and scope. If authoritative absence is proven after documented visibility delay, and the original key remains within its proven retention window, submit only the exact retained envelope/key. Otherwise query/escalate and preserve UNKNOWN |
| During request transmission or after bytes leave, before response | Provider may have accepted, rejected, or not received the request | Query the original provider identity. Never create a new key/attempt. Same-key resubmission only under the qualified exact-replay contract and within retention |
| Provider accepted request; process crashes before response is received | Provider may be running the work; registry may still show dispatch-started/pending | Recover authenticated status by original key/job ID. Persist the authenticated provider observation. No second logical job |
| Response received in memory; crash before receipt transaction commits | The process once observed bytes, but there is no durable evidence of them | Do not claim receipt persistence. Query provider for an authenticated observation; if query cannot reconstruct the state, preserve UNKNOWN and escalate. A provider that offers only an unqueryable, losable callback is not qualified for unattended dispatch |
| Provider observation transaction commits; response to dispatcher is lost | Receipt/observation and checkpoint may already be committed | Resolve by the provider-observation idempotency identity and exact facts digest. Return original committed receipt on exact replay; changed facts are a conflict |
| Registry DB commits observation plus witness outbox; crash before external witness acknowledgment | Registry state is one checkpoint ahead and witness-pending | Freeze protected writes. Publish/replay the exact outbox checkpoint identity; persist authenticated witness acknowledgment. Do not create a new lifecycle event or sequence |
| Witness accepts checkpoint; publisher crashes before recording acknowledgment | External witness may be ahead of local acknowledgment state | Re-submit/reconcile the exact same witness tuple/idempotency identity; witness returns original receipt. Record acknowledgment in the registry; do not advance another sequence |
| Witness acknowledgment is recorded; dispatcher crashes before returning its API response | Full registry/witness state is committed | Exact command replay returns the original receipt; no provider call, event, or sequence is duplicated |
| Crash during cancellation or approval revocation race | Cancellation/revocation and dispatch attempt may have committed in either order | Read authoritative ordered events. If cancellation/revocation preceded dispatch-start, deny. If dispatch-start committed first, preserve and reconcile that attempt; cancellation does not prove non-delivery |

## Findings

### CR-01 — dispatch_started is intentionally ambiguous about external submission (P0)

This is not a defect: the registry cannot atomically commit with an external provider. But restart logic must never interpret dispatch_started as either “provider definitely not called” or “provider definitely accepted.” It means only that an authorized attempt was durably recorded.

**Resolution:** Every nonterminal attempt is reconciled against the provider by its original scoped key/job identity. The provider's authoritative query semantics and visibility horizon determine whether absence can be established. If not, remain UNKNOWN.

### CR-02 — Provider acceptance before local receipt persistence is the critical lost-response case (P0)

A process can receive provider acceptance and crash before its receipt/observation transaction commits. The in-memory response is lost; the registry cannot reconstruct it from local logs or a worker claim.

**Resolution:** Provider qualification must require authenticated query/reconciliation by original key or job ID, including sufficient history to recover accepted/running/terminal state after a dispatcher restart. If a provider supports only a callback and does not provide durable queryable state or a separately proven durable callback inbox, it is not qualified for unattended dispatch.

### CR-03 — Provider observations need their own replay identity and immutable facts digest (P0)

The provider delivery identity identifies the logical provider job; it is not the same as each provider receipt, callback, or query observation.

**Resolution:** Define a closed observation-source identity:
- callbacks/events: (provider_source_namespace, provider_account_scope, provider_event_id, event_role);
- synchronous response: bind to the immutable local dispatch attempt and a receiver-generated response-observation ID, with raw response digest and authenticated transport/request context;
- query result: bind to the attempt, provider query request/receipt identity or provider status version/cursor where supplied, and the exact raw response digest.

For each identity, store a complete immutable facts digest covering attempt ID, assignment revision, package/request digest, provider key/scope, source identity, raw bytes digest/length, authentication provenance, provider status/version, and provider/receiver timestamps. Exact replay returns the original receipt. Same identity with changed facts is a security conflict; never overwrite the first observation. Distinct observation IDs with identical bytes remain separately auditable and may be linked by content digest.

Where the provider supplies no stable event/version identity for query responses, the adapter must use a deterministic, documented observation identity scoped to the exact query request and raw response digest; it must not collapse materially different statuses or treat repeated polls as new delivery attempts.

### CR-04 — Provider observation and checkpoint persistence must be one registry transaction (P0)

A verified provider response cannot be treated as confirmed until its raw evidence, authentication result, immutable observation, provider-event idempotency index, derived delivery projection, event-chain update, assignment/global versions, internal checkpoint, and witness outbox are committed atomically.

If this transaction times out or its result is unknown, resolve the exact observation identity before retry. Never write a second event based only on the caller's uncertainty.

### CR-05 — External witness acknowledgment creates a second crash boundary (P0)

The database transaction and independent witness cannot be assumed to commit atomically. A crash after database commit but before witness acknowledgment leaves a legitimate witness-pending state.

**Resolution:** Retain the established one-outstanding-outbox rule. On restart reconcile the exact tuple and predecessor, replay the same witness identity, persist the authenticated acknowledgment, and keep all protected writes frozen until complete. If witness is ahead, local DB is more than one sequence ahead, outbox is missing/mismatched, or history forks, fail closed.

### CR-06 — Exact retry must distinguish command replay from provider resubmission (P1)

A client retry after losing a dispatcher API response is not permission to repeat the external provider call. The dispatcher first resolves the already committed command/attempt and returns its existing state. Provider resubmission is a separate recovery decision constrained by provider key retention, exact envelope identity, and authoritative query evidence.

**Resolution:** Separate command idempotency, provider-delivery idempotency, provider-observation idempotency, and witness-checkpoint idempotency. Do not reuse one identifier across these domains or infer one domain's success from another.

## Normative restart algorithm

1. Enter recovery mode; do not dispatch, consume approvals, accept returns, complete reviews, record dispositions, or advance protected state.
2. Authenticate registry identity and current independent witness. Verify event chain, global and assignment versions, all idempotency indexes, exact package/request objects, and the single pending witness-outbox rule.
3. Reconcile any pending witness outbox by exact tuple/predecessor and same witness identity. If any discrepancy exists, remain read-only and fail closed.
4. Enumerate every nonterminal dispatch attempt from authoritative registry history. Do not infer the set from worker artifacts, workflow inputs, process memory, or log lines.
5. For each attempt, retrieve the exact retained request envelope, digest, provider qualification version, provider scope, key, approval/assignment bindings, cancellation/revocation facts, and provider retention deadline/evidence.
6. Query the provider using the original key/job identity and authenticated provider account scope. Respect documented consistency/visibility delays and bounded backoff. Preserve raw query evidence and authenticate it before interpreting status.
7. If provider reports accepted/running/terminal, commit the authenticated observation through the atomic observation transaction. If it reports authoritative absence, revalidate the provider retention window and exact request binding before any same-key submission; never mint a new key for an unresolved attempt.
8. If query is unavailable, ambiguous, expired, unauthenticated, stale, or outside retention, preserve UNKNOWN and escalate to independent human/provider reconciliation. Do not infer non-delivery.
9. Resolve exact replay/conflicting replay by the appropriate command, provider-delivery, provider-observation, or witness identity. Never convert a lost client response into a second logical operation.
10. Resume protected writes only after all pending witness state and nonterminal delivery attempts are reconciled or explicitly held under an approved recovery decision, and the separate human resume protocol is satisfied.

## Required synthetic crash-injection cases

Before any provider dispatch capability is enabled, test at least:
- crash before dispatch transaction; during commit; after commit before provider call;
- crash after request bytes are sent but before response;
- provider accepts then drops response;
- response received then process crashes before observation commit;
- observation commit succeeds but client loses response;
- DB commit succeeds but witness publish does not;
- witness accepts but publisher loses acknowledgment;
- exact duplicate callback; same callback ID with changed body; out-of-order/stale callback;
- query returns transient not-found, delayed accepted status, expired history, or unavailable provider;
- provider key retention expires during outage;
- cancellation/revocation races with each dispatch crash point;
- duplicate client command after every crash point.

The test oracle must prove no second logical provider job, no lost committed event, no false non-delivery, no receipt fabricated from local state, and no protected write while witness-pending. Tests must use a synthetic provider/account and must not contact a real worker or execute research tasks.

## Current status

This audit resolves protocol/documentation requirements only. No provider is selected or qualified; no dispatcher, registry, provider inbox, or witness is implemented. No tests, scripts, workflows, network requests, provider calls, dispatch, or research operations were run. The agent remains non-operational and the Phase 3 G0-05 handoff remains controlling.
