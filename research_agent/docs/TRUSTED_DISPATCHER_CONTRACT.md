# Trusted dispatcher contract (design only)

## Status and authority

This is a design contract, not an implementation or authorization. No dispatcher, worker-delivery channel, durable assignment registry, or workflow is currently active. The current Phase 3 G0-05 handoff remains authoritative and prohibits the relevant execution, test, and workflow activity. This document does not permit dispatch, execution, scheduling, repository writes, or research work.

The purpose is to specify the missing trust boundary between the existing pure planning/review modules and any future worker delivery mechanism. It deliberately separates planning, approval, preparation, dispatch, return, review, and human disposition. A successful earlier stage never implies authorization for a later stage.

## Existing components and missing links

The current code provides exact task-definition hashing and fail-closed permission evaluation; fixed-path queue preflight and a non-authorizing phase-ordered batch plan; immutable-in-memory assignment package construction; package digest calculation; assignment-return binding against an independently supplied expected digest; structural worker-submission review and evidence-byte verification; report/artifact construction; and pure event-ledger/persistence decision primitives.

The missing trusted dispatcher must supply authenticated human approval for the exact run scope; authenticated current workflow/repository/ref/commit context; live handoff and policy revalidation at the operation boundary; protected retention of the assignment-package digest before delivery; authenticated delivery identity and receipt; durable event/checkpoint persistence with atomic idempotency; and controlled receipt of worker output without treating worker claims as trusted facts.

## Required approval envelope

Before any future dispatch-capable operation, the approval record should bind:
- approving human identity from an authenticated platform context;
- exact repository and isolated working branch;
- exact workflow definition identity (path plus immutable commit SHA);
- exact task ID and canonical task-definition SHA-256;
- exact phase, operation, handoff ID/revision, declared scope and prohibitions;
- exact operation class being approved (readiness report, worker delivery, or evidence review);
- permitted input commit SHA and expected output/report class;
- approval timestamp and expiry or revocation mechanism.

The approval must be retained independently of the task, workflow inputs, worker package, and worker return. A task allowlist hash alone is not approval to run a workflow or deliver work. Approval for one operation class must not be widened into another. Any change to the task digest, handoff revision, workflow SHA, branch, operation, or scope invalidates the approval and requires a new decision.

Approval issuance is immutable: never extend expiry, clear revocation, reset consumption, or renew in place. Any renewal requires a fresh authenticated human decision with a new approval ID and nonce, bound to the complete current scope. The approval issuer must enforce unique IDs/nonces and exact-replay-versus-conflicting-replay semantics. Revocation is monotonic; it blocks future use but does not recall a dispatch attempt whose `dispatch_started` transaction already committed. Such an attempt is reconciled using its original provider key. If stopping provider-side work is required, use a separate authenticated cancellation operation and receipt.


For the current stage, the only conceivable first run is a non-executing, preflight/readiness report after the controlling handoff permits it. No worker delivery should be enabled as part of that first check.

## Dispatch transaction — future only

A future dispatcher must follow this order and fail closed on any missing or ambiguous fact:

1. Authenticate the triggering human/platform event. Derive actor, repository, workflow identity, run ID, run attempt, ref, and event identity from trusted platform context, never from dispatch inputs or report content.
2. Resolve the exact task from the trusted queue at a pinned commit. Reject unknown, duplicate, non-queued, malformed, or phase-ineligible tasks.
3. Independently load and verify the current task hash, task allowlist, phase permission, global execution switches, branch policy, current handoff, predecessor-gate state, and all applicable prohibitions. Revalidate immediately before the protected operation, not only when planning.
4. Verify the exact approval envelope for this run, task, operation, workflow SHA, handoff revision, and input commit. Reject expired, revoked, mismatched, or replayed approvals. Revalidate expiry/revocation atomically again in the `start_dispatch` transaction; consume a single-use approval in that same transaction.
5. Produce the canonical assignment package from the trusted task and exact preflight/planner result. Do not accept worker-supplied scope, instructions, allowed actions, schema, or handoff metadata.
6. Calculate the package digest using the declared versioned canonicalization contract. Persist the complete package (or immutable package reference), digest, task digest, workflow/run identity, approval identity, and expected delivery identity to a protected registry before attempting delivery. The worker must not be able to alter this registry.
7. Use an authenticated delivery channel and a stable upstream delivery ID. The delivery request must be idempotent. Never interpret “request sent” as proof of delivery or receipt.
8. Atomically commit `dispatch_started`, consuming the single-use approval and recording the stable provider idempotency key before the external call. This commit is the authorization/attempt linearization point. Then invoke the provider with that exact key. Record provider acceptance/rejection only from authenticated provider evidence; a timeout/lost response remains pending/unknown, not permission for a second delivery.
9. On ambiguous delivery, reconcile against the authenticated delivery receipt/registry before retrying. Never auto-retry an uncertain delivery. A duplicate request must resolve to the original delivery identity and package digest.
10. Persist the event, delivery index, and protected checkpoint atomically using the trusted-store contract. If persistence outcome is uncertain, reconcile by delivery ID before any further action.
11. Return a receipt that identifies the task digest, package digest, workflow/run, delivery identity, and committed event/checkpoint. The receipt proves only the recorded delivery state, not worker execution or task completion.

## Worker return boundary

Treat all worker-return fields as untrusted declarations, including task ID, package digest, actions taken, timestamps, evidence paths, evidence hashes, completion status, and narrative findings.

The trusted receiver must authenticate the return transport and bind it to the recorded delivery identity; retrieve the expected package digest and exact package from the protected registry, never from the return body; reject returns for unknown or mismatched deliveries; and, where a delivery was already committed but the assignment was later cancelled, revoked, or expired, preserve the raw immutable return and digest, mark it late/revoked, and exclude it from valid task completion (any further review requires explicit human authority). It must verify the complete canonical package and task digest before parsing an eligible return as a submission; obtain expected repository, branch, commit, run and evidence manifest from trusted workflow/checkout context; verify actual evidence bytes against an independently generated commit manifest; run structural review before evidence review and fail closed on malformed inputs; record review output as a separate event; and leave human disposition and phase-gate closure as separate authenticated actions.

A passing structural/evidence review means only that the submission is eligible for human review. It does not prove the worker's narrative is true, that the research interpretation is correct, or that the task is accepted.

## State machine and replay rules

The minimum durable assignment lifecycle states are:
- prepared_not_dispatched
- dispatch_started
- delivery_pending_or_unknown
- delivery_confirmed
- submission_received
- review_completed
- human_disposition_recorded

Cancellation is a separate durable assignment flag/event, not a replacement for dispatch/delivery state. An assignment may be marked cancellation-requested/cancelled for future work while an earlier dispatch attempt remains `dispatch_started` or `delivery_pending_or_unknown`; the registry must retain both facts. A cancellation after `dispatch_started` cannot be represented as proof that the provider call did not occur.

Each transition requires an authenticated event and a valid prior state. Impossible transitions fail closed. Duplicate delivery events with identical authenticated facts are idempotent; the same delivery identity with changed package/task facts is rejected. A repeated worker return must resolve to the original receipt and must not create a second task completion. A revision request creates a new revision identity linked to the original assignment; it must not overwrite the original package or review record.

Human dispositions are limited to explicit, authenticated values such as accepted, rejected, or needs_revision. Task acceptance does not close a phase gate. Gate closure and phase advancement require their own separate human-authorized record.

## Least-privilege and containment requirements

- Use a fresh GitHub-hosted runner; never use self-hosted/VPS runners.
- Start with no repository secrets and no write token.
- Pin workflow and action identities immutably; do not select workflow refs or shell commands from task/worker data.
- Restrict checkouts to the exact isolated agent branch and pinned research input commit; never invoke inherited research workflows.
- Keep worker outputs as data; never execute files recovered from artifacts or worker submissions.
- Bound run time, task count, artifact size, retry count (zero automatic retries for uncertain delivery), and concurrency.
- Keep scheduling and event-driven triggers disabled until manual validation and independent review are complete.
- Do not commit to the research branch, mutate canonical research data/definitions, close gates, advance phases, or create candidates/backtests/PnL/strategy conclusions.

## Failure handling

| Failure | Required result |
|---|---|
| Approval missing, stale, revoked, or mismatched | Deny before package delivery |
| Handoff or phase state cannot be verified | Deny; require human investigation |
| Package digest cannot be stored before delivery | Do not dispatch |
| Delivery response times out | Keep the same attempt pending/unknown; reconcile with the same provider key, never retry with a new identity |
| Cancellation/revocation commits before `dispatch_started` | Deny the dispatch transaction; do not call provider |
| Cancellation/revocation commits after `dispatch_started` | Preserve the attempt; resolve it with the original provider key; cancellation blocks future attempts but does not assert non-delivery |
| Delivery identity replay with identical facts | Return original receipt; no duplicate delivery |
| Delivery identity replay with changed facts | Reject and preserve original record |
| Store/checkpoint integrity fails | Stop; preserve evidence; no reset/rebuild |
| Worker return lacks matching protected package | Reject return |
| Evidence bytes or commit provenance mismatch | Return for revision; no acceptance |
| Review service fails or returns malformed data | Fail closed; preserve raw return and report failure |
| Human disposition is absent | Keep task pending human review |
| Human accepts task | Record acceptance only; phase gate remains open |

## Implementation sequence and gates

1. Approve the repository topology and workflow activation route.
2. Approve a concrete trusted-store backend, identity model, retention, backup, and administrator threat model.
3. Produce a dispatcher threat model and failure-injection matrix.
4. Implement the protected assignment registry and atomic event-store adapter on the isolated agent branch.
5. Implement a non-dispatching readiness workflow only after the controlling handoff permits its exact validation scope.
6. Independently review the workflow, store, approval binding, and failure behavior.
7. Only after separate explicit approval, implement bounded worker delivery for a specifically authorized task.
8. Validate delivery, duplicate/replay, timeout, crash-before/after-commit, tampering, stale approval, changed handoff, and recovery cases.
9. Keep scheduled/event-driven operation disabled until manual operation is demonstrated and separately approved.

No backend, delivery provider, secret, workflow, schedule, or permission change is selected by this design. The current implementation remains non-operational and no task is authorized for dispatch.
