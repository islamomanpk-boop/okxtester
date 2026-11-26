# Append-only Task Event Ledger

## Purpose

The event ledger provides a deterministic, append-only audit format for task lifecycle observations. It is separate from `config/task_queue.json`: the queue remains the static source of task definitions and phase order, while the ledger records what an external trusted process says happened.

## Event format and integrity

Each event has an upstream stable `event_id`, an allowlisted event type, exact task ID and task-definition SHA-256, canonical UTC occurrence time (shortest fractional representation, with zero fractions omitted), source category/reference, JSON payload, previous-event SHA-256, and its own SHA-256. The current implementation hashes UTF-8 bytes of Python `json.dumps(sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)` output. This is deterministic for the supported Python implementation, but it is not a claim of RFC 8785/JCS cross-language canonicalization.

Duplicate delivery IDs with identical event facts are idempotent; reuse of an ID for different facts is rejected.

Supported observations are `task_observed`, `assignment_prepared`, `worker_submission_received`, `review_completed`, and `human_disposition_recorded`. Source categories are `github_workflow`, `human_review`, and `worker_return`.

## Canonicalization interoperability gate

Before any non-Python writer or verifier is introduced, select and version one cross-language canonicalization contract (preferably RFC 8785 JSON Canonicalization Scheme, with its number and Unicode rules), then add independent test vectors shared by every implementation. Alternatively, explicitly constrain all ledger creation and verification to one pinned Python serialization implementation and version. Do not assume that sorting JSON keys alone makes Python, JavaScript, and other runtimes produce identical bytes. The current schema permits finite floating-point values, making numeric serialization behavior particularly important. A canonicalization migration must be versioned and must not silently reinterpret existing event hashes.

## Critical trust limits

- Hash chaining detects accidental or unauthenticated modification relative to a trusted retained head hash; it does **not** authenticate who created an event.
- A hash chain can be rewritten from genesis by an actor who can replace the entire ledger. A future store must retain a trusted checkpoint/head independently (for example, protected workflow-run metadata or a separately permissioned append-only record).
- Event source references and payloads are declarations until a future verifier independently checks them against trusted GitHub run context, worker-return bytes, or a human review record.
- The ledger does not authorize execution, mutate task queue status, prove dispatch/delivery, approve task completion, or close phase gates.
- A `human_disposition_recorded` event is only a record of a human decision claimed by its source; the future integration must authenticate the human actor and decision through an independently trusted channel.
- The module is pure: it performs no file I/O, network calls, GitHub operations, scheduling, or workflow dispatch. It returns a new list; it never overwrites the caller's ledger. Strict JSON validation rejects non-string object keys, tuples, non-finite numbers, and other values that serializers might otherwise coerce.

`engine/persistence_contract.py` adds a pure optimistic-concurrency preparation step: it accepts a new event only when an independently trusted expected head matches the validated ledger head, reports stale-checkpoint conflicts without changing the ledger, and recognizes exact delivery replays. It does not provide atomic compare-and-swap or persistence; see [docs/PERSISTENCE_CONTRACT.md](docs/PERSISTENCE_CONTRACT.md).

## Future persistence requirements

Before this ledger can support unattended operation, a separately reviewed workflow/store must:

1. Obtain event IDs and source context from authenticated upstream events, never worker-controlled payload fields.
2. Load and validate the complete ledger and independently retained head checkpoint.
3. Use the selected, versioned canonicalization contract consistently across every writer and verifier.
4. Append one event using optimistic concurrency against the expected head hash; fail closed if the head changed.
5. Persist atomically and preserve prior events; no in-place event edits or deletion.
6. Retain a separately permissioned checkpoint or signed/otherwise authenticated record of the current head.
7. Make retries idempotent and reconcile interrupted runs without losing pending tasks.
8. Re-check the current handoff, task digest, phase gate, allowlist, and all safety switches at the moment of any future permitted operation.

The current repository has no trusted persistence adapter or dispatcher. This module is an integrity primitive only, not a durable queue and not evidence that the agent is running.

## Validation

Thirteen regression tests are authored in `tests/test_event_ledger.py`; they have not been executed. Runtime validation remains deferred while the current Phase 3 G0-05 handoff prohibits relevant code/test execution.
