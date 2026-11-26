"""Report-builder validation tests; authored but not executed under the active handoff."""
import tempfile
import unittest
from pathlib import Path

from research_agent.engine import report_builder


def valid_report():
    return {
        "schema_version": 1,
        "agent_name": "okx-research-agent",
        "task_id": "P3-RO-TEST",
        "phase": "phase3_sideways_range",
        "status": "preflight_only",
        "repository": "islamomanpk-boop/okxtester",
        "branch": "agent/okx-research-agent-v1",
        "commit_sha": "a" * 40,
        "run_id": "manual-test",
        "timestamp_utc": "2026-11-26T12:00:00Z",
        "input_manifest": [
            {"path": "docs/source.md", "sha256": "b" * 64}
        ],
        "findings": [],
        "blockers": [],
        "skipped_checks": [],
        "limitations": [],
    }


class ReportBuilderTests(unittest.TestCase):
    def test_rejects_completion_claim_statuses_without_executor(self):
        for status in ("completed", "success", "successful", "research_complete", "approved"):
            report = valid_report()
            report["status"] = status
            with self.subTest(status=status):
                with self.assertRaisesRegex(ValueError, "non-completion states"):
                    report_builder.validate_report(report)

    def test_accepts_only_supported_non_completion_statuses(self):
        for status in ("preflight_only", "blocked", "skipped", "not_run"):
            report = valid_report()
            report["status"] = status
            with self.subTest(status=status):
                report_builder.validate_report(report)

    def test_valid_report_renders_deterministically(self):
        report = valid_report()
        first = report_builder.render_json(report)
        second = report_builder.render_json(report)
        self.assertEqual(first, second)
        self.assertEqual(report_builder.report_digest(report), report_builder.report_digest(report))

    def test_rejects_duplicate_manifest_paths(self):
        report = valid_report()
        report["input_manifest"].append(dict(report["input_manifest"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate manifest"):
            report_builder.validate_report(report)

    def test_rejects_malformed_commit_sha(self):
        report = valid_report()
        report["commit_sha"] = "not-a-commit"
        with self.assertRaisesRegex(ValueError, "commit_sha"):
            report_builder.validate_report(report)

    def test_rejects_non_utc_timestamp(self):
        report = valid_report()
        report["timestamp_utc"] = "2026-11-26T12:00:00+04:00"
        with self.assertRaisesRegex(ValueError, "UTC"):
            report_builder.validate_report(report)

    def test_rejects_manifest_path_traversal(self):
        report = valid_report()
        report["input_manifest"][0]["path"] = "../outside.txt"
        with self.assertRaisesRegex(ValueError, "repository-relative"):
            report_builder.validate_report(report)

    def test_rejects_noncanonical_utc_timestamp(self):
        report = valid_report()
        report["timestamp_utc"] = "2026-11-26T12:00:00+00:00"
        with self.assertRaisesRegex(ValueError, "ending in Z"):
            report_builder.validate_report(report)

    def test_rejects_non_string_finding_entries(self):
        report = valid_report()
        report["findings"] = [{"unexpected": "object"}]
        with self.assertRaisesRegex(ValueError, "non-empty string"):
            report_builder.validate_report(report)

    def test_rejects_unsupported_report_fields(self):
        report = valid_report()
        report["unreviewed_metadata"] = "must not pass schema"
        with self.assertRaisesRegex(ValueError, "unsupported fields"):
            report_builder.validate_report(report)

    def test_rejects_boolean_schema_version(self):
        report = valid_report()
        report["schema_version"] = True
        with self.assertRaisesRegex(ValueError, "schema version"):
            report_builder.validate_report(report)

    def test_rejects_windows_style_manifest_paths(self):
        report = valid_report()
        report["input_manifest"][0]["path"] = r"docs\\source.md"
        with self.assertRaisesRegex(ValueError, "repository-relative"):
            report_builder.validate_report(report)

    def test_manifest_hashing_rejects_symlink_inputs(self):
        with tempfile.TemporaryDirectory(dir=report_builder.REPOSITORY_ROOT) as temporary:
            directory = Path(temporary)
            target = directory / "target.txt"
            target.write_text("stable bytes", encoding="utf-8")
            link = directory / "linked.txt"
            link.symlink_to(target)
            relative_link = link.relative_to(report_builder.REPOSITORY_ROOT)
            with self.assertRaisesRegex(ValueError, "symlinks"):
                report_builder.sha256_file(relative_link)

    def test_markdown_renderer_flattens_and_escapes_untrusted_findings(self):
        report = valid_report()
        report["findings"] = ["# Forged heading\n[click](https://example.invalid)"]
        rendered = report_builder.render_markdown(report)
        self.assertIn("Forged heading [click]", rendered)
        self.assertIn("\\#", rendered)
        self.assertNotIn("## Forged heading", rendered)
        self.assertNotIn("[click](", rendered)

    def test_manifest_hashing_rejects_paths_outside_repository(self):
        with tempfile.TemporaryDirectory() as temporary:
            outside = Path(temporary) / "outside.txt"
            outside.write_text("not repository data", encoding="utf-8")
            with self.assertRaises(ValueError):
                report_builder.sha256_file(outside)


if __name__ == "__main__":
    unittest.main()
