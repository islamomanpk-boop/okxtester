"""Deterministic report formatting helpers for okx-research-agent.

This module formats supplied findings. It does not run research tasks, inspect
GitHub, write files, or make claims beyond the data passed by its caller.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

REPORT_SCHEMA_VERSION = 1
ALLOWED_REPORT_STATUSES = {"preflight_only", "blocked", "skipped", "not_run"}
REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_COMMIT_RE = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
_UTC_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")


def _repository_file(path: str | Path) -> Path:
    """Resolve a report input and reject paths outside the repository."""
    supplied = Path(path)
    if supplied.is_absolute() or ".." in supplied.parts:
        raise ValueError("Report input paths must be safe repository-relative paths.")
    # Reject symlinks at every path component, including links that happen
    # to resolve back inside the repository. This keeps provenance paths
    # stable and prevents a later link retarget from changing the input.
    candidate = REPOSITORY_ROOT
    for part in supplied.parts:
        candidate = candidate / part
        if candidate.is_symlink():
            raise ValueError("Report input paths must not contain symlinks.")
    resolved = candidate.resolve(strict=True)
    try:
        resolved.relative_to(REPOSITORY_ROOT.resolve())
    except ValueError as exc:
        raise ValueError("Report input resolves outside the repository.") from exc
    if not resolved.is_file():
        raise ValueError(f"Report input is not a regular file: {supplied}")
    return resolved


def sha256_file(path: str | Path) -> str:
    """Return SHA-256 for a repository-relative file's exact bytes."""
    resolved = _repository_file(path)
    digest = hashlib.sha256()
    with resolved.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_input_manifest(paths: Iterable[str | Path]) -> list[dict[str, str]]:
    """Create a sorted path/hash manifest for repository-contained inputs."""
    manifest = []
    seen: set[str] = set()
    for item in paths:
        raw_path = str(item)
        relative = Path(item)
        if (
            relative.is_absolute()
            or not relative.parts
            or ".." in relative.parts
            or "\\" in raw_path
            or any(ord(character) < 32 or ord(character) == 127 for character in raw_path)
        ):
            raise ValueError("Manifest paths must be safe repository-relative paths.")
        canonical_path = relative.as_posix()
        if canonical_path in seen:
            raise ValueError(f"Duplicate manifest input path: {canonical_path}")
        seen.add(canonical_path)
        digest = sha256_file(relative)
        manifest.append({"path": canonical_path, "sha256": digest})
    return sorted(manifest, key=lambda row: row["path"])


def _validate_utc_timestamp(value: str) -> None:
    # Require one canonical UTC representation so equivalent offsets or
    # unusual ISO-8601 spellings cannot produce inconsistent audit records.
    if not _UTC_TIMESTAMP_RE.fullmatch(value):
        raise ValueError("Report timestamp must use canonical ISO-8601 UTC form ending in Z.")
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError("Report timestamp must be a valid ISO-8601 UTC timestamp.") from exc


def _validate_json_value(value: Any, location: str = "task") -> None:
    """Reject Python-only values so task hashes have unambiguous JSON meaning."""
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"{location} contains a non-finite number.")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate_json_value(item, f"{location}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError(f"{location} object keys must be strings.")
            _validate_json_value(item, f"{location}.{key}")
        return
    raise TypeError(f"{location} contains a value that is not JSON-compatible.")


def task_definition_digest(task: dict[str, Any]) -> str:
    """Hash a strict JSON task object using canonical JSON serialization."""
    if not isinstance(task, dict) or not task:
        raise TypeError("Task definition must be a non-empty JSON object.")
    _validate_json_value(task)
    canonical = json.dumps(
        task, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def verify_report_task_binding(report: dict[str, Any], trusted_task: dict[str, Any]) -> None:
    """Require report identity and digest to match the exact trusted queue task."""
    validate_report(report)
    if not isinstance(trusted_task, dict):
        raise TypeError("Trusted task definition must be a JSON object.")
    task_id = trusted_task.get("task_id")
    phase = trusted_task.get("phase")
    if task_id != report["task_id"]:
        raise ValueError("Report task_id does not match the trusted task definition.")
    if phase != report["phase"]:
        raise ValueError("Report phase does not match the trusted task definition.")
    if task_definition_digest(trusted_task) != report["task_definition_sha256"]:
        raise ValueError("Report task-definition hash does not match the trusted task definition.")


def validate_report(report: dict[str, Any]) -> None:
    """Reject incomplete or malformed reports instead of inventing metadata."""
    required = {
        "schema_version", "agent_name", "task_id", "phase", "status",
        "repository", "branch", "commit_sha", "task_definition_sha256", "run_id", "timestamp_utc",
        "input_manifest", "findings", "blockers", "skipped_checks", "limitations",
    }
    if not isinstance(report, dict):
        raise TypeError("Report must be a JSON object.")
    missing = sorted(required.difference(report))
    if missing:
        raise ValueError("Report is missing required fields: " + ", ".join(missing))
    unexpected = sorted(set(report).difference(required))
    if unexpected:
        raise ValueError("Report contains unsupported fields: " + ", ".join(unexpected))
    if type(report["schema_version"]) is not int or report["schema_version"] != REPORT_SCHEMA_VERSION:
        raise ValueError("Unsupported report schema version.")
    list_fields = ("findings", "blockers", "skipped_checks", "limitations", "input_manifest")
    for field in list_fields:
        if not isinstance(report[field], list):
            raise TypeError(f"Report field {field!r} must be a list.")
    for field in ("findings", "blockers", "skipped_checks", "limitations"):
        if not all(isinstance(item, str) and item.strip() for item in report[field]):
            raise ValueError(f"Every item in report field {field!r} must be a non-empty string.")
    for field in ("agent_name", "task_id", "phase", "status", "repository",
                  "branch", "commit_sha", "task_definition_sha256", "run_id", "timestamp_utc"):
        if not isinstance(report[field], str) or not report[field].strip():
            raise ValueError(f"Report field {field!r} must be a non-empty string.")
    if report["status"] not in ALLOWED_REPORT_STATUSES:
        raise ValueError(
            "Report status must be one of the explicitly supported non-completion states."
        )
    if not _COMMIT_RE.fullmatch(report["commit_sha"]):
        raise ValueError("Report commit_sha must be a 40- or 64-character lowercase hexadecimal SHA.")
    if not _SHA256_RE.fullmatch(report["task_definition_sha256"]):
        raise ValueError("Report task_definition_sha256 must be 64 lowercase hexadecimal characters.")
    _validate_utc_timestamp(report["timestamp_utc"])

    seen_paths: set[str] = set()
    for entry in report["input_manifest"]:
        if not isinstance(entry, dict):
            raise TypeError("Each input manifest entry must be an object.")
        if set(entry) != {"path", "sha256"}:
            raise ValueError("Each input manifest entry must contain only path and sha256.")
        path_value = entry["path"]
        if not isinstance(path_value, str) or not path_value.strip():
            raise ValueError("Manifest path must be a non-empty string.")
        relative = Path(path_value)
        if (
            relative.is_absolute()
            or not relative.parts
            or ".." in relative.parts
            or "\\" in path_value
            or any(ord(character) < 32 or ord(character) == 127 for character in path_value)
        ):
            raise ValueError("Manifest paths must be safe repository-relative paths.")
        if relative.as_posix() != path_value:
            raise ValueError("Manifest paths must use normalized POSIX relative paths.")
        if path_value in seen_paths:
            raise ValueError(f"Duplicate manifest input path: {path_value}")
        seen_paths.add(path_value)
        if not isinstance(entry["sha256"], str) or not _SHA256_RE.fullmatch(entry["sha256"]):
            raise ValueError("Manifest SHA-256 must be 64 lowercase hexadecimal characters.")


def verify_input_manifest_against_checkout(report: dict[str, Any]) -> list[str]:
    """Compare declared input hashes with files in the current checkout.

    This verifies current working-tree bytes only. It does not prove that the
    files came from report['commit_sha'] or that the checkout is clean.
    Returns an empty list when every declared input matches.
    """
    validate_report(report)
    mismatches: list[str] = []
    for entry in report["input_manifest"]:
        try:
            actual = sha256_file(entry["path"])
        except (OSError, ValueError) as exc:
            mismatches.append(f"{entry['path']}: unavailable ({exc})")
            continue
        if actual != entry["sha256"]:
            mismatches.append(f"{entry['path']}: SHA-256 does not match current checkout.")
    return mismatches


def verify_report_provenance(
    report: dict[str, Any],
    trusted_task: dict[str, Any],
    *,
    expected_repository: str,
    expected_branch: str,
    expected_commit_sha: str,
    actual_head_sha: str,
    checkout_clean: bool,
) -> None:
    """Verify report claims against trusted task and independently supplied checkout facts.

    The caller must obtain these runtime facts from the workflow/checkout boundary,
    not from report fields or task-controlled input. A clean checkout at the exact
    expected commit makes the declared file hashes attributable to that commit.
    """
    verify_report_task_binding(report, trusted_task)
    for name, value in (
        ("expected_repository", expected_repository),
        ("expected_branch", expected_branch),
        ("expected_commit_sha", expected_commit_sha),
        ("actual_head_sha", actual_head_sha),
    ):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must be a non-empty trusted runtime value.")
    if not _COMMIT_RE.fullmatch(expected_commit_sha):
        raise ValueError("expected_commit_sha must be a valid lowercase Git SHA.")
    if not _COMMIT_RE.fullmatch(actual_head_sha):
        raise ValueError("actual_head_sha must be a valid lowercase Git SHA.")
    if report["repository"] != expected_repository:
        raise ValueError("Report repository does not match trusted workflow context.")
    if report["branch"] != expected_branch:
        raise ValueError("Report branch does not match trusted workflow context.")
    if report["commit_sha"] != expected_commit_sha:
        raise ValueError("Report commit SHA does not match trusted workflow context.")
    if actual_head_sha != expected_commit_sha:
        raise ValueError("Checked-out HEAD does not match the expected commit SHA.")
    if checkout_clean is not True:
        raise ValueError("Checkout must be independently confirmed clean.")
    mismatches = verify_input_manifest_against_checkout(report)
    if mismatches:
        raise ValueError("Input manifest verification failed: " + "; ".join(mismatches))


def render_json(report: dict[str, Any]) -> str:
    """Return stable, human-readable JSON with deterministic key ordering."""
    validate_report(report)
    return json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def _markdown_safe(value: Any) -> str:
    """Flatten untrusted values and escape Markdown control characters."""
    rendered = value if isinstance(value, str) else json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)
    rendered = " ".join(rendered.split())
    for character in (chr(92), chr(96), "*", "_", "{", "}", "[", "]", "<", ">", "#", "+", "-", ".", "!", "|"):
        rendered = rendered.replace(character, chr(92) + character)
    return rendered


def _as_bullets(items: list[Any]) -> str:
    if not items:
        return "- None recorded."
    return "\n".join("- " + _markdown_safe(item) for item in items)


def render_markdown(report: dict[str, Any]) -> str:
    """Render a concise audit report from validated report data."""
    validate_report(report)
    manifest_lines = [
        f"- Path: {_markdown_safe(entry['path'])} — SHA-256: {_markdown_safe(entry['sha256'])}"
        for entry in report["input_manifest"]
    ]
    if not manifest_lines:
        manifest_lines = ["- No input files recorded."]

    sections = [
        "# OKX Research Agent Report",
        "",
        f"- **Task:** {_markdown_safe(report['task_id'])}",
        f"- **Phase:** {_markdown_safe(report['phase'])}",
        f"- **Status:** {_markdown_safe(report['status'])}",
        f"- **Agent:** {_markdown_safe(report['agent_name'])}",
        f"- **Repository:** {_markdown_safe(report['repository'])}",
        f"- **Branch:** {_markdown_safe(report['branch'])}",
        f"- **Commit SHA:** {_markdown_safe(report['commit_sha'])}",
        f"- **Task definition SHA-256:** {_markdown_safe(report['task_definition_sha256'])}",
        f"- **Run ID:** {_markdown_safe(report['run_id'])}",
        f"- **Timestamp (UTC):** {_markdown_safe(report['timestamp_utc'])}",
        "",
        "## Findings",
        _as_bullets(report["findings"]),
        "",
        "## Blockers",
        _as_bullets(report["blockers"]),
        "",
        "## Skipped checks",
        _as_bullets(report["skipped_checks"]),
        "",
        "## Limitations",
        _as_bullets(report["limitations"]),
        "",
        "## Declared input manifest",
        "The paths and SHA-256 values below are declarations whose format was validated. "
        "The renderer does not re-read these files or authenticate their relationship to the reported commit.",
        *manifest_lines,
        "",
        "## Verification boundaries",
        "- Report metadata (repository, branch, commit SHA, task-definition hash, run ID, and timestamp) is supplied by the caller and is not cryptographically authenticated by schema validation.",
        "- The task-definition hash identifies the canonical task object only when produced with task_definition_digest() from the exact trusted queue entry; the schema validates its format, not its origin.",
        "- Input hashes are declarations until verify_input_manifest_against_checkout() is run against the intended checkout.",
        "- Checkout hash matching alone does not prove the checkout is clean or that its bytes belong to the reported commit.",
        "- This report is an audit record, not task-completion evidence or human gate approval.",
        "",
    ]
    return "\n".join(sections)


def build_artifact_bundle(
    report: dict[str, Any],
    trusted_task: dict[str, Any],
    *,
    expected_repository: str,
    expected_branch: str,
    expected_commit_sha: str,
    actual_head_sha: str,
    checkout_clean: bool,
    run_id: str,
    run_attempt: str,
) -> dict[str, Any]:
    """Build a complete in-memory artifact bundle after provenance verification.

    This function never writes or uploads files. The caller must publish the
    returned files atomically as one artifact and fail the workflow if any
    expected file is absent. Run identifiers must come from trusted workflow
    context, not task or report content.
    """
    for name, value in (("run_id", run_id), ("run_attempt", run_attempt)):
        if not isinstance(value, str) or not re.fullmatch(r"[1-9][0-9]*", value):
            raise ValueError(f"{name} must be a positive decimal workflow identifier.")
    if report.get("run_id") != run_id:
        raise ValueError("Report run_id does not match trusted workflow context.")

    verify_report_provenance(
        report,
        trusted_task,
        expected_repository=expected_repository,
        expected_branch=expected_branch,
        expected_commit_sha=expected_commit_sha,
        actual_head_sha=actual_head_sha,
        checkout_clean=checkout_clean,
    )
    report_json = render_json(report)
    report_markdown = render_markdown(report)
    files = {
        "report.json": report_json,
        "report.md": report_markdown,
    }
    manifest = {
        "schema_version": 1,
        "artifact_name": f"okx-research-agent-{run_id}-{run_attempt}",
        "task_id": report["task_id"],
        "phase": report["phase"],
        "run_id": run_id,
        "run_attempt": run_attempt,
        "commit_sha": expected_commit_sha,
        "files": [
            {"path": name, "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest()}
            for name, content in sorted(files.items())
        ],
        "limitations": [
            "Bundle generated in memory; this function does not write or upload files.",
            "Artifact integrity hashes detect later byte changes but do not authenticate the uploader or GitHub artifact service.",
            "The caller must upload the complete bundle as one artifact and verify the uploaded artifact contains every declared file.",
        ],
    }
    files["artifact_manifest.json"] = (
        json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"
    )
    return {
        "artifact_name": manifest["artifact_name"],
        "files": files,
        "manifest": manifest,
    }


def report_digest(report: dict[str, Any]) -> str:
    """Hash the canonical JSON representation of a report."""
    return hashlib.sha256(render_json(report).encode("utf-8")).hexdigest()
