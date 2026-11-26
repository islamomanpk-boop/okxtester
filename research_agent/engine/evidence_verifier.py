"""Independent, read-only verification of worker evidence declarations.

The caller must obtain commit_manifest and file_contents from a trusted,
clean checkout at the expected commit. This module does not access GitHub,
the filesystem, or the network and cannot authenticate caller-supplied context.
"""
from __future__ import annotations

import hashlib
import re
from typing import Any

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_COMMIT_RE = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
_EVIDENCE_FIELDS = {"path", "sha256", "source_ref", "description"}


def _safe_path(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    if value.startswith(("/", "\\")) or "\\" in value:
        return False
    if re.match(r"^[A-Za-z]:", value):
        return False
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        return False
    return all(part not in {"", ".", ".."} for part in value.split("/"))


def verify_worker_evidence(
    evidence: list[dict[str, Any]],
    *,
    expected_commit_sha: str,
    commit_manifest: dict[str, Any],
    file_contents: dict[str, bytes],
) -> dict[str, Any]:
    """Compare declarations and checkout bytes with a manifest for one commit."""
    if not isinstance(expected_commit_sha, str) or not _COMMIT_RE.fullmatch(expected_commit_sha):
        raise ValueError("Expected commit SHA is malformed.")
    if not isinstance(commit_manifest, dict) or set(commit_manifest) != {"commit_sha", "files"}:
        raise ValueError("Commit manifest must contain exactly commit_sha and files.")
    if commit_manifest["commit_sha"] != expected_commit_sha:
        raise ValueError("Commit manifest does not match the expected commit.")
    manifest_files = commit_manifest["files"]
    if not isinstance(manifest_files, dict):
        raise TypeError("Commit manifest files must be a path-to-SHA-256 object.")
    for path, digest in manifest_files.items():
        if not _safe_path(path) or not isinstance(digest, str) or not _SHA256_RE.fullmatch(digest):
            raise ValueError("Commit manifest contains an unsafe path or malformed SHA-256.")
    if not isinstance(file_contents, dict):
        raise TypeError("Checkout file contents must be a path-to-bytes object.")
    for path, content in file_contents.items():
        if not _safe_path(path) or not isinstance(content, bytes):
            raise ValueError("Checkout file map contains an unsafe path or non-bytes content.")
    if not isinstance(evidence, list):
        raise TypeError("Worker evidence must be a list.")

    seen: set[str] = set()
    results: list[dict[str, Any]] = []
    for index, item in enumerate(evidence):
        result = {"index": index, "path": None, "status": "rejected", "reasons": []}
        if not isinstance(item, dict) or set(item) != _EVIDENCE_FIELDS:
            result["reasons"].append("invalid_evidence_schema")
            results.append(result)
            continue
        path = item["path"]
        result["path"] = path if isinstance(path, str) else None
        if not all(isinstance(item[key], str) and item[key].strip() for key in _EVIDENCE_FIELDS):
            result["reasons"].append("empty_or_non_string_evidence_field")
        if not _safe_path(path):
            result["reasons"].append("unsafe_repository_path")
        elif path in seen:
            result["reasons"].append("duplicate_evidence_path")
        else:
            seen.add(path)
        declared_hash = item["sha256"]
        if not isinstance(declared_hash, str) or not _SHA256_RE.fullmatch(declared_hash):
            result["reasons"].append("invalid_declared_sha256")
        if not result["reasons"]:
            expected_hash = manifest_files.get(path)
            if expected_hash is None:
                result["reasons"].append("path_absent_from_expected_commit")
            elif path not in file_contents:
                result["reasons"].append("file_missing_from_checkout")
            else:
                actual_hash = hashlib.sha256(file_contents[path]).hexdigest()
                if declared_hash != expected_hash:
                    result["reasons"].append("worker_hash_does_not_match_commit_manifest")
                if actual_hash != expected_hash:
                    result["reasons"].append("checkout_bytes_do_not_match_commit_manifest")
                if not result["reasons"]:
                    result["status"] = "verified"
                    result["verified_sha256"] = actual_hash
        results.append(result)

    all_verified = bool(results) and all(row["status"] == "verified" for row in results)
    return {
        "mode": "evidence_verification_only",
        "expected_commit_sha": expected_commit_sha,
        "evidence_count": len(results),
        "verified_count": sum(row["status"] == "verified" for row in results),
        "rejected_count": sum(row["status"] != "verified" for row in results),
        "all_evidence_verified": all_verified,
        "task_completion_approved": False,
        "gate_closure_approved": False,
        "human_review_required": True,
        "results": results,
        "limitations": [
            "Verification is only as trustworthy as the commit manifest and file bytes supplied by the caller.",
            "The caller must authenticate the checkout, verify its exact commit and cleanliness, and derive the manifest from that commit.",
            "Matching bytes prove integrity relative to the supplied manifest, not research correctness or source truth.",
            "This function performs no filesystem, GitHub, network, task, or research operations.",
        ],
    }
