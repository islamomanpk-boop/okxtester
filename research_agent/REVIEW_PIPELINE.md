# Integrated Supervisor Review Pipeline

`engine.review_pipeline.review_submission_with_verified_evidence` connects
structural worker-submission review with the evidence-integrity verifier.

## Order of checks

1. Validate the submission against the exact trusted queue task and reject
   unsupported actions, mismatched task identity/digest, malformed evidence,
   or gate-closure claims.
2. If structural review fails, stop; evidence verification is not attempted.
3. If structural review passes, compare each evidence declaration and supplied
   checkout bytes with a manifest for the expected commit.
4. Downgrade the disposition to `return_for_revision` if any evidence item
   fails integrity verification.

## Authority boundary

A passing result means only that the submission is structurally valid and its
referenced bytes match the supplied commit manifest. It does not establish
research correctness, task completion, or gate closure. Every result requires
human review.

The pipeline itself does not authenticate the caller or obtain the expected
commit, manifest, or checkout bytes. A future workflow must independently
verify checkout cleanliness and commit identity and derive the manifest from
that exact commit. The module performs no filesystem, GitHub, network, task,
or research operations.

Regression tests are authored but not executed under the current G0-05
handoff restrictions.
