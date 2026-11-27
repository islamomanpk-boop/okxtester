# Provider status reconciliation and terminal consistency audit — 2026-11-27

## Scope and method

Targeted static review of provider delivery idempotency, crash recovery, callback ingestion/ordering, unified lifecycle, dispatcher contract, and backend interface. This review addresses disagreement among provider query APIs, callback streams, provider dashboards/history, local registry projections, and terminal outcomes.

Documentation-only. No provider, account, credentials, code, tests, scripts, workflow, network request, dispatch, scheduling, VPS access, or research operation was used.

## Executive result

The existing contracts correctly require authenticated observations, immutable raw evidence, provider-specific ordering, query-based recovery, and fail-closed UNKNOWN states. A remaining design gap is the absence of a single explicit precedence and reconciliation protocol when independent provider evidence sources disagree or when a provider revises a previously reported status.

There must be no simplistic global source ranking such as "query beats webhook" or "dashboard beats callback." Authority depends on provider-documented semantics, authentication, scope, freshness, resource version, completeness, and the exact attempt binding. A dashboard screenshot or operator statement is not equivalent to an authenticated machine-readable receipt. Local projection is a derived view, not an independent source of provider truth.

## Findings and required resolutions

### SR-01 — No universal source precedence (P0)

**Risk:** Treating one channel as always authoritative can discard newer or stronger evidence. A query can be eventually consistent; a callback can be delayed; a dashboard may be manually curated or show a different account/region.

**Required protocol:**
- Qualify each provider's source semantics separately: authenticated query API, callback/event stream, immutable job history, dashboard/UI, support/operator statement.
- Record source class, provider account/tenant/region, endpoint, authentication provenance, observation time, provider event time, resource version/cursor/sequence, consistency model, and completeness.
- Machine-authenticated evidence with documented semantics may drive a projection only when bound to the exact attempt and ordering model. UI observations and human statements are corroborative evidence only unless independently captured and authenticated under a separately approved procedure.
- Do not resolve conflicts by fixed channel rank or latest local arrival. Compare the provider-defined version/order and documented consistency horizon.
- If the provider supplies no trustworthy ordering or conflict-resolution semantics, retain all observations and mark the delivery UNKNOWN pending reconciliation.

### SR-02 — Query "not found" is not authoritative absence by default (P0)

A query result can be stale, scoped incorrectly, delayed by indexing, or omit archived jobs. "Not found" may be treated as absence only when provider documentation establishes the exact lookup key/scope, visibility horizon, archival behavior, consistency guarantee, and response authenticity. Before the horizon expires, re-query with bounded backoff. After key/history retention expires or the guarantee cannot be established, query only/escalate; never resubmit or declare non-delivery.

### SR-03 — Status is not a single linear enum (P0)

Provider lifecycle facts must be represented as immutable observations and orthogonal dimensions, not overwritten by one mutable status string. At minimum distinguish:
- submission/delivery evidence: not attempted, attempt committed, outcome unknown, provider job identified;
- execution: queued, running, terminal success, terminal failure, terminal cancellation, or unknown;
- cancellation: not requested, requested, provider accepted cancellation request, terminal cancellation proven, cancellation outcome unknown;
- evidence quality: authenticated, stale, incomplete, conflicting, quarantined;
- reconciliation: current, pending visibility, sequence gap, source conflict, history expired;
- local task disposition and phase-gate disposition, which remain separate human-controlled facts.

A provider's "cancel requested" is not terminal cancellation. A provider's "completed" is not automatically successful research/task completion. A provider execution failure does not automatically imply safe retry.

### SR-04 — Terminal status needs provider-specific finality semantics (P0)

A terminal label is authoritative only if provider documentation defines it as final for that job and the observation is authenticated, correctly bound, and sufficiently ordered. Some providers may revise, retract, or append later billing/termination/administrative events. Preserve every observation. A later nonterminal observation never regresses a proven terminal projection; contradictory later terminal evidence, explicit provider correction, or higher resource revision creates a conflict requiring documented provider history reconciliation and human review. Do not silently rewrite the terminal fact.

### SR-05 — Multiple sources may refer to different attempts/jobs (P0)

Every observation must bind to exact provider account/region, job ID, idempotency key/scope, dispatch attempt ID, request-envelope digest, package digest, assignment revision, and provider qualification version. A dashboard may show a prior attempt, retry, similarly named job, or another tenant. Ambiguous identity, missing attempt linkage, or mismatched request digest is quarantined and cannot change the current attempt projection.

### SR-06 — Provider history pagination and gaps can hide evidence (P1)

For paginated history, persist query parameters, cursor chain, page identity, retrieval time, raw page bytes/digests, and completeness result. Detect cursor loops, repeated pages, missing sequence ranges, truncation, retention boundary, and pagination errors. A partial history cannot prove absence or finality. Reconciliation remains pending until all required ranges are obtained or provider limits force UNKNOWN/escalation.

### SR-07 — Reconciliation itself needs a stable transaction identity (P1)

A reconciliation run must be bound to exact attempt, source set, query window/cursors, provider qualification version, policy version, and expected checkpoint. Preserve raw source observations and an immutable reconciliation decision with cited observation IDs and explicit unresolved conflicts. Exact replay returns the original decision; changed inputs/policy produce a new linked reconciliation revision, never overwrite history. Reconciliation output is a technical projection recommendation, not human task acceptance or gate closure.

### SR-08 — Provider outage and retention expiry must not create false certainty (P0)

If query API is unavailable, callback history is incomplete, provider retention expired, source authenticity cannot be verified, or sources disagree without documented resolution, preserve UNKNOWN. No new provider attempt/key, no automatic retry, no inferred success/failure/cancellation, and no task completion. Escalate to independently authenticated provider support/history or human review. If evidence cannot be recovered, record the unresolved limitation permanently.

## Normative reconciliation algorithm

1. Freeze new dispatch and state-changing recovery operations for the affected attempt; preserve independent emergency-hold semantics.
2. Verify registry chain, witness state, attempt identity, retained request envelope, package digest, approval/cancellation/revocation facts, and provider qualification version.
3. Enumerate all known observations by exact provider account/region and job/key identity, including callbacks, synchronous receipts, query results, and history pages.
4. Authenticate each raw observation using its recorded source/key/policy version; reject unverifiable evidence from authoritative projection while preserving it as quarantined evidence.
5. Verify every observation binds to exactly one dispatch attempt and exact request/package digests.
6. Apply provider-specific ordering/version semantics; separate provider event time from receiver observation time. Identify stale events, duplicate/conflicting IDs, sequence gaps, pagination gaps, and contradictory terminal observations.
7. Query authenticated provider status/history using the original job/key and exact scope; honor documented visibility delay, retention, pagination, and consistency semantics.
8. Treat not-found as absence only if the provider's documented authoritative-absence conditions are all satisfied. Otherwise retain UNKNOWN.
9. Build an immutable reconciliation record referencing all observation IDs, query cursors, policy/qualification versions, and each resolved/unresolved conflict. Do not overwrite observations or prior reconciliation records.
10. Atomically append reconciliation evidence, derived projection, idempotency index, checkpoint, and witness outbox. Unknown transaction outcome is resolved by the same reconciliation identity/digest.
11. Keep protected writes frozen while witness acknowledgment is pending. A witness-pending or conflicted projection cannot authorize dispatch, completion, or retry.
12. Require independent human review for unresolved/contradictory terminal evidence, lost history, expired retention, provider support statements, or any proposed new attempt. Human task disposition and phase-gate disposition remain separate.

## Required synthetic conformance cases

- Query API says not-found while a delayed authenticated callback later reports accepted/running.
- Callback reports completed while an eventually consistent query reports running.
- Dashboard and API show different jobs or accounts with similar labels.
- Same provider resource version reports conflicting terminal statuses.
- Higher version retracts or corrects a previous terminal result.
- Cancellation request accepted but job continues/runs/completes.
- Query returns partial paginated history, repeated cursor, cursor gap, or retention truncation.
- Provider history expires during outage; query unavailable across visibility horizon.
- A provider status observation has correct job ID but wrong account, key, attempt, or request digest.
- Exact reconciliation replay, conflicting replay, policy-version change, and transaction timeout.
- Reconciliation commits but external witness acknowledgment is lost.
- Provider says success while worker artifact is missing, or worker artifact exists while provider history is unavailable.

Oracles must prove no false absence, no silent terminal rewrite, no cross-attempt attribution, no automatic retry from ambiguity, no task/gate completion from provider status alone, and no protected action while witness-pending. Synthetic data only.

## Current status

Protocol and documentation clarification only. No provider or source semantics have been qualified; no provider, account, API, dashboard integration, registry, reconciliation service, or witness is implemented. No tests, scripts, workflows, network requests, provider calls, dispatch, scheduling, VPS access, or research operations were run. The agent remains non-operational and Phase 3 G0-05 remains controlling.
