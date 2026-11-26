"""Deterministic report formatting helpers for okx-research-agent.

This module formats supplied findings. It does not run research tasks, inspect
GitHub, write files, or make claims beyond the data passed by its caller.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

REPORT_SCHEMA_VERSION = 1
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


def validate_report(report: dict[str, Any]) -> None:
    """Reject incomplete or malformed reports instead of inventing metadata."""
    required = {
        "schema_version", "agent_name", "task_id", "phase", "status",
        "repository", "branch", "commit_sha", "run_id", "timestamp_utc",
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
                  "branch", "commit_sha", "run_id", "timestamp_utc"):
        if not isinstance(report[field], str) or not report[field].strip():
            raise ValueError(f"Report field {field!r} must be a non-empty string.")
    if not _COMMIT_RE.fullmatch(report["commit_sha"]):
        raise ValueError("Report commit_sha must be a 40- or 64-character lowercase hexadecimal SHA.")
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
        f"- `{_markdown_safe(entry['path'])}` — SHA-256 `{_markdown_safe(entry['sha256'])}`"
        for entry in report["input_manifest"]
    ]
    if not manifest_lines:
        manifest_lines = ["- No input files recorded."]

    sections = [
        "# OKX Research Agent Report",
        "",
        f"- **Task:** `{_markdown_safe(report['task_id'])}`",
        f"- **Phase:** `{_markdown_safe(report['phase'])}`",
        f"- **Status:** {_markdown_safe(report['status'])}",
        f"- **Agent:** `{_markdown_safe(report['agent_name'])}`",
        f"- **Repository:** `{_markdown_safe(report['repository'])}`",
        f"- **Branch:** `{_markdown_safe(report['branch'])}`",
        f"- **Commit SHA:** `{_markdown_safe(report['commit_sha'])}`",
        f"- **Run ID:** `{_markdown_safe(report['run_id'])}`",
        f"- **Timestamp (UTC):** `{_markdown_safe(report['timestamp_utc'])}`",
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
        "## Input provenance",
        *manifest_lines,
        "",
    ]
    return "\n".join(sections)


def report_digest(report: dict[str, Any]) -> str:
    """Hash the canonical JSON representation of a report."""
    return hashlib.sha256(render_json(report).encode("utf-8")).hexdigest()
