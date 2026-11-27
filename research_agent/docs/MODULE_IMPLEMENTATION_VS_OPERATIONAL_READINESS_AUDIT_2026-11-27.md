# Module implementation versus operational readiness audit — 2026-11-27

## Purpose and conclusion

This is a static, source-level readiness classification of the current `research_agent/engine/` modules and their corresponding authored test files. It distinguishes implemented deterministic logic from trusted operational capabilities. It is documentation-only and does not authorize tests, scripts, workflows, data access, dispatch, or activation.

**Conclusion:** the repository contains useful pure validation, planning, packaging, hashing, and review primitives. None of these modules constitutes a trusted end-to-end agent. The system remains non-operational. Current G0-05 restrictions continue to prohibit running the authored tests or other execution paths relevant to Phase 3.

## Readiness vocabulary

- **Implemented pure primitive:** deterministic local logic exists; no claim that it is independently validated or operational.
- **Composition only:** combines primitives in memory; does not create durable trust or authority.
- **Design contract only:** requirements are documented, but the external adapter/service is absent.
- **Not operational:** required trust root, persistence, authentication, runtime, or provider capability is absent.
- **Candidate for future synthetic validation:** code may be suitable for isolated synthetic-only testing after a controlling handoff permits it. This is not test approval.

## Module-by-module assessment

| Module | What source currently implements | What it does not establish | Readiness |
|---|---|---|---|
| `safety_controller.py` | Strict policy JSON parsing, task-contract checks, exact task digest/allowlist and phase checks, G0-05 deny lock, fail-closed decisions | Authenticated policy publication, independent approval identity, live handoff authentication, effective GitHub permissions, operation-bound transaction enforcement | Implemented pure/local authorization primitive; not a trusted authority service |
| `task_runner.py` | Fixed-path queue loading and per-task/all-task preflight; strict result envelopes; no executor | Queue authenticity/signature, durable queue state, worker execution, trusted workflow context, live policy/handoff recheck at action boundary | Implemented read-only preflight primitive |
| `batch_planner.py` | Bounded phase-ordered planning, exact queue/preflight ID matching, no phase skipping, non-authorizing plan | Assignment reservation, durable concurrency, authenticated preflight source, execution or queue mutation | Implemented pure planner |
| `assignment_package.py` | Exact task/preflight/planner binding, worker action declaration allowlist, non-dispatchable package and digest | Independent digest custody, authenticated dispatcher, package delivery receipt, live handoff enforcement | Implemented package builder; custody absent |
| `orchestration_coordinator.py` | In-memory composition of planning, packages and recovery guidance; explicitly reports no persistence/digest storage/dispatch | Authenticated recovery observations, durable assignment lifecycle, trusted digest retention, dispatch and receipt reconciliation | Composition only |
| `report_builder.py` | Strict report schemas, deterministic serialization/hash, manifest construction, report and artifact bundle verification helpers | Authenticated caller metadata, authoritative commit tree manifest, proof of clean checkout unless independently supplied, artifact-service uploader identity | Implemented report primitive; workflow trust absent |
| `artifact_preparation.py` | Fixed repository/branch checks, fixed-path task lookup, preflight report and in-memory bundle composition | Authentication of supplied run/commit/checkout metadata, file writes/upload, task execution, artifact service round-trip | Composition only |
| `supervisor_review.py` | Structural validation of worker-declared submission, allowed action labels, human-only completion boundary | Truth of claims, source correctness, reviewer authentication, raw return custody, actual dispatch/delivery proof | Implemented structural review primitive only |
| `evidence_verifier.py` | Byte hashes compared with a caller-supplied commit manifest and expected SHA | Manifest authenticity/completeness, independent checkout acquisition, source truth, provenance of the worker's bytes | Implemented hash-check primitive only |
| `review_pipeline.py` | Structural review followed by evidence-byte verification; downgrades invalid evidence to revision | Trusted inputs, durable review record, research correctness, authenticated reviewer and human disposition | Pure composition only |
| `assignment_return.py` | Exact canonical package comparison against independently supplied expected digest and trusted task; then review pipeline | Proof of dispatch/delivery, raw-byte transport authentication, durable receipt, return idempotency, late-return state, independently retained expected digest | Implemented binding/review primitive; trusted receiver absent |
| `review_artifact.py` | Converts assignment review into report bundle with fixed repo/branch and report/evidence SHA consistency | Authenticated workflow context, artifact upload/download, immutable artifact custody, actual human acceptance | Composition only |
| `event_ledger.py` | Append-only in-memory hash-chain validation and replay/conflict semantics | Durable atomic append, authenticated event source, external witness, anti-rollback, cross-runtime canonicalization guarantee | Implemented in-memory primitive |
| `persistence_contract.py` | Pure optimistic-concurrency preparation and stale-head detection | Atomic compare-and-swap, transaction isolation, persistence, idempotency index, concurrent writer exclusion | Contract/helper only; not a store |
| `recovery_policy.py` | Conservative classification of a limited delivery/review/human-disposition tuple | Full lifecycle state machine, authenticated observations, approval/cancellation/expiry/provider history, durable recovery | Limited advisory classifier |

## Important integration findings

### 1. The coordinator is not a dispatcher

`build_orchestration_snapshot()` composes a queue and preflight summary supplied by its caller. `build_runtime_orchestration_snapshot()` loads the repository queue and derives a preflight summary from that snapshot. Both return `SNAPSHOT_ONLY`; assignment digests are explicitly marked `package_digest_stored: false`; recovery observations are explicitly unauthenticated; persistence, scheduling, dispatch, execution, task completion, and gate closure are all false. This is a useful integration seam, not an operational lifecycle.

### 2. Caller-supplied inputs remain a trust boundary

Several pure functions intentionally accept caller-supplied queue/preflight, task/package, expected commit, manifest/file bytes, run identity, checkout cleanliness, timestamps, recovery observations, or expected package digest. Their local consistency checks do not authenticate the source of those values. A future workflow/service must acquire these values independently from trusted sources and bind them to one authenticated transaction. Do not treat a caller-provided `expected_*` parameter as proof of trust.

### 3. Package digest custody is still missing

The assignment builder calculates a digest, but the coordinator marks it not stored. Return review correctly requires an independently retained expected digest; however, there is no trusted dispatcher/registry currently retaining and later retrieving it. Therefore the assignment-return function is not yet end-to-end usable as an authenticated worker-return path.

### 4. Evidence integrity is narrower than evidence validity

The verifier establishes that supplied bytes match a supplied manifest. It does not prove that the manifest is authentic, complete, independently derived from the intended commit tree, or that the evidence supports the research claim. Structural review, byte integrity, research correctness, task acceptance, and phase-gate closure must remain distinct decisions.

### 5. Report provenance helpers are not workflow authentication

Report and artifact verification can check exact content, declared run identity, commit identity, and expected context. But callers must independently obtain and protect those expected values; the module does not authenticate GitHub event metadata, prove artifact uploader identity, or itself upload/download artifacts. The future workflow must provide the trusted acquisition and round-trip evidence.

### 6. In-memory concurrency preparation is not atomic persistence

`persistence_contract.py` can identify a stale expected head and prepare an append. It cannot prevent two concurrent callers from preparing against the same head. The future backend must perform authenticated read, full-chain validation, conditional atomic append, uniqueness/index/checkpoint update, and witness outbox commit in one transaction.

## Authored test inventory and validation status

The test directory contains 15 module-level test files corresponding to the engine primitives. These are authored tests, not executed validation. Under the active G0-05 handoff, no test suite or test file should be run as a shortcut or alternate route. The presence of tests does not establish pass status, coverage, runtime compatibility, or integration correctness.

After a future controlling handoff explicitly permits synthetic-only validation, the recommended sequence is:

1. Validate pure schema/hash/path helpers with synthetic fixtures only.
2. Validate safety controller and preflight against temporary synthetic config/queue fixtures, preserving fixed-path runtime policy.
3. Validate planner, assignment package, coordinator and recovery classifier with adversarial malformed and cross-phase fixtures.
4. Validate structural review, byte verifier, assignment binding and artifact builder using independently generated synthetic manifests/bytes.
5. Validate event-ledger and persistence helper invariants, then test a real backend adapter separately under concurrent synthetic transactions.
6. Validate complete workflow artifact round-trip only after workflow identity and activation topology are approved.

No sequence above is currently authorized by this audit.

## Future acceptance classification

**Suitable first for isolated synthetic unit validation, once authorized:** strict JSON/task digests, path safety, planner ordering, package exact-match logic, pure recovery classifications, report schema/rendering, hash-chain and byte-comparison helpers.

**Require adapter/integration design before meaningful end-to-end validation:** assignment return custody, artifact preparation/round-trip, event persistence, trusted package digest retention, authenticated human disposition, provider delivery/reconciliation, worker isolation, monitoring and recovery.

**Must never be promoted to authority based solely on local tests:** G0-05 closure, phase advancement, provider delivery, research correctness, human task acceptance, or production activation.

## Required next implementation dependencies

1. Finish the current G0-05 read-only reconciliation and obtain the independent review/disposition required by the controlling handoff.
2. Resolve owner decisions on repository topology, hosting, identity, backend, witness, canonicalization, provider, retention, and recovery objectives.
3. Qualify supply-chain and data/evidence foundations.
4. Implement and independently verify the trusted transactional registry, event/idempotency/checkpoint/witness protocol, and package-digest custody.
5. Implement operation-bound authorization and provider-qualified dispatcher/receipt reconciliation.
6. Implement disposable worker isolation and authenticated raw-byte return receiver.
7. Complete evidence completeness, research correctness review, and immutable human task/gate disposition.
8. Add trusted workflow context, artifact round-trip, monitoring/incident controls, and backup/restore proof.
9. Only then consider a separately authorized manual synthetic preflight; unattended automation remains a later approval.

## Current status and non-claims

This audit was performed by static source inspection only. No modules or tests were executed. No scripts, workflows, provider calls, research-data access, VPS actions, deployments, permission changes, credentials, services, or infrastructure were performed or changed. No operational readiness or test pass is claimed. The agent remains non-operational; no unattended work is running; Phase 3 G0-05 remains controlling.


## Follow-up — cross-platform path identity is not yet enforced

Static review of `report_builder.build_input_manifest()` and `evidence_verifier._safe_path()` confirms that both reject traversal and exact duplicate evidence paths, but neither enforces a portable collision policy for case-fold-equivalent names or Unicode-normalization-equivalent names. The evidence verifier's dictionary keys and duplicate tracking are exact-string based. A manifest containing distinct paths such as `Data.csv` and `data.csv` can therefore pass these local path checks even though a case-insensitive checkout or extraction target may not represent both objects distinctly. Unicode normalization differences can create a similar portability ambiguity.

This does not establish that the current repository contains such colliding paths, nor that a current checkout was corrupted. It is a helper-boundary limitation. A future trusted Git-tree manifest builder must preserve raw tree path identity and mode semantics, declare the target filesystem/platform policy, detect case-fold and Unicode-normalization collisions before materialization, and fail closed rather than silently renaming, overwriting, or merging objects. Tests for this behavior remain authored/future work and must not be run under the active G0-05 handoff.
