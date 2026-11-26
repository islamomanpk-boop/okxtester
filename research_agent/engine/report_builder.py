"""Deterministic report formatting helpers for okx-research-agent.

This module formats supplied findings. It does not run research tasks, inspect
GitHub, write files, or make claims beyond the data passed by its caller.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

REPORT_SCHEMA_VERSION = 1


def sha256_file(path: str | Path) -> str:
    """Return the SHA-256 digest of a file's exact bytes."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_input_manifest(paths: Iterable[str | Path]) -> list[dict[str, str]]:
    """Create a sorted path/hash manifest; missing inputs raise an error."""
    manifest = []
    for item in paths:
        path = Path(item)
        if not path.is_file():
            raise FileNotFoundError(f"Required report input is missing: {path}")
        manifest.append({"path": path.as_posix(), "sha256": sha256_file(path)})
    return sorted(manifest, key=lambda row: row["path"])


def validate_report(report: dict[str, Any]) -> None:
    """Reject incomplete reports instead of silently inventing metadata."""
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
    for field in ("findings", "blockers", "skipped_checks", "limitations", "input_manifest"):
        if not isinstance(report[field], list):
            raise TypeError(f"Report field {field!r} must be a list.")
    for field in ("agent_name", "task_id", "phase", "status", "repository",
                  "branch", "commit_sha", "run_id", "timestamp_utc"):
        if not isinstance(report[field], str) or not report[field].strip():
            raise ValueError(f"Report field {field!r} must be a non-empty string.")


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
        f"- {entry['path']} — SHA-256 {entry['sha256']}"
        for entry in report["input_manifest"]
    ]
    if not manifest_lines:
        manifest_lines = ["- No input files recorded."]

    sections = [
        "# OKX Research Agent Report",
        "",
        f"- **Task:** {report['task_id']}",
        f"- **Phase:** {report['phase']}",
        f"- **Status:** {report['status']}",
        f"- **Agent:** {report['agent_name']}",
        f"- **Repository:** {report['repository']}",
        f"- **Branch:** {report['branch']}",
        f"- **Commit SHA:** {report['commit_sha']}",
        f"- **Run ID:** {report['run_id']}",
        f"- **Timestamp (UTC):** {report['timestamp_utc']}",
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
