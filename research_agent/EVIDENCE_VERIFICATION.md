# Worker Evidence Verification

The `engine.evidence_verifier` module compares each worker evidence declaration
with a path-to-SHA-256 manifest derived from one exact commit and the
corresponding file bytes obtained from that checkout.

## Required trusted inputs

The caller must supply the expected full commit SHA, a manifest containing
exactly `commit_sha` and `files` (a path-to-SHA-256 map), a path-to-bytes map
from the checkout at that commit, and the worker's evidence declarations.

The verifier checks commit identity consistency, safe paths, duplicate
references, missing files, worker-declared hashes, and actual checkout bytes.
An item is marked `verified` only when its declared hash and checkout bytes
both match the expected-commit manifest.

## Authority and limitations

This is an integrity check, not a research review. It does not authenticate
the caller, obtain Git data, read the filesystem, access GitHub, or establish
that the supplied manifest came from the claimed commit. A future workflow
must independently obtain the commit, verify checkout cleanliness, and derive
the manifest from that exact commit before invoking this module.

Even if every evidence item verifies, task completion and gate closure remain
unapproved and human review remains mandatory. No research files are modified.
