"""Deterministic report formatting helpers for okx-research-agent.

This module formats supplied findings. It does not run research tasks, inspect
GitHub, write files, or make claims beyond the data passed by its caller.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

REPORT_SCHEMA_VERSION = 1
REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _repository_file(path: str | Path) -> Path:
    """Resolve a report input and reject paths outside the repository."""
    supplied = Path(path)
    if supplied.is_absolute():
        raise ValueError("Report input paths must be repository-relative.")
    resolved = (REPOSITORY_ROOT / supplied).resolve(strict=True)
    try:
        resolved.relative_to(REPOSITORY_ROOT)
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
    for item in paths:
        relative = Path(item)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("Manifest paths must be safe repository-relative paths.")
        digest = sha256_file(relative)
        manifest.append({"path": relative.as_posix(), "sha256": digest})
    return sorted(manifest, key=lambda row: row["path"])


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
    if report["schema_version"] != REPORT_SCHEMA_VERSION:
        raise ValueError("Unsupported report schema version.")
    list_fields = ("findings", "blockers", "skipped_checks", "limitations", "input_manifest")
    for field in list_fields:
        if not isinstance(report[field], list):
            raise TypeError(f"Report field {field!r} must be a list.")
    for field in ("agent_name", "task_id", "phase", "status", "repository",
                  "branch", "commit_sha", "run_id", "timestamp_utc"):
        if not isinstance(report[field], str) or not report[field].strip():
            raise ValueError(f"Report field {field!r} must be a non-empty string.")
    for entry in report["input_manifest"]:
        if not isinstance(entry, dict):
            raise TypeError("Each input manifest entry must be an object.")
        if set(entry) != {"path", "sha256"}:
            raise ValueError("Each input manifest entry must contain only path and sha256.")
        if not isinstance(entry["path"], str) or not entry["path"].strip():
            raise ValueError("Manifest path must be a non-empty string.")
        if Path(entry["path"]).is_absolute() or ".." in Path(entry["path"]).parts:
            raise ValueError("Manifest paths must be repository-relative.")
        if not isinstance(entry["sha256"], str) or not _SHA256_RE.fullmatch(entry["sha256"]):
            raise ValueError("Manifest SHA-256 must be 64 lowercase hexadecimal characters.")


def render_json(report: dict[str, Any]) -> str:
    """Return stable, human-readable JSON with deterministic key ordering."""
    validate_report(report)
    return json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _as_bullets(items: list[Any]) -> str:
    if not items:
        return "- None recorded."
    return "\n".join(
        "- " + (item if isinstance(item, str) else json.dumps(item, sort_keys=True, ensure_ascii=False))
        for item in items
    )


def render_markdown(report: dict[str, Any]) -> str:
    """Render a concise audit report from validated report data."""
    validate_report(report)
    manifest_lines = [
        f"- \`{entry['path']}\` — SHA-256 \`{entry['sha256']}\`"
        for entry in report["input_manifest"]
    ]
    if not manifest_lines:
        manifest_lines = ["- No input files recorded."]

    sections = [
        "# OKX Research Agent Report",
        "",
        f"- **Task:** \`{report['task_id']}\`",
        f"- **Phase:** \`{report['phase']}\`",
        f"- **Status:** {report['status']}",
        f"- **Agent:** \`{report['agent_name']}\`",
        f"- **Repository:** \`{report['repository']}\`",
        f"- **Branch:** \`{report['branch']}\`",
        f"- **Commit SHA:** \`{report['commit_sha']}\`",
        f"- **Run ID:** \`{report['run_id']}\`",
        f"- **Timestamp (UTC):** \`{report['timestamp_utc']}\`",
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
