"""Report-builder validation tests; authored but not executed under the active handoff."""
import hashlib
import json
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
        "task_definition_sha256": "d" * 64,
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

    def test_checkout_manifest_verification_accepts_matching_bytes(self):
        with tempfile.TemporaryDirectory(dir=report_builder.REPOSITORY_ROOT) as temporary:
            path = Path(temporary) / "evidence.txt"
            path.write_text("original evidence", encoding="utf-8")
            relative = path.relative_to(report_builder.REPOSITORY_ROOT).as_posix()
            report = valid_report()
            report["input_manifest"] = report_builder.build_input_manifest([relative])
            self.assertEqual(
                report_builder.verify_input_manifest_against_checkout(report), []
            )

    def test_checkout_manifest_verification_detects_changed_bytes(self):
        with tempfile.TemporaryDirectory(dir=report_builder.REPOSITORY_ROOT) as temporary:
            path = Path(temporary) / "evidence.txt"
            path.write_text("original evidence", encoding="utf-8")
            relative = path.relative_to(report_builder.REPOSITORY_ROOT).as_posix()
            report = valid_report()
            report["input_manifest"] = report_builder.build_input_manifest([relative])
            path.write_text("modified evidence", encoding="utf-8")
            mismatches = report_builder.verify_input_manifest_against_checkout(report)
            self.assertEqual(len(mismatches), 1)
            self.assertIn("does not match", mismatches[0])

    def test_checkout_manifest_verification_reports_missing_input(self):
        report = valid_report()
        report["input_manifest"] = [
            {"path": "research_agent/nonexistent-evidence.txt", "sha256": "b" * 64}
        ]
        mismatches = report_builder.verify_input_manifest_against_checkout(report)
        self.assertEqual(len(mismatches), 1)
        self.assertIn("unavailable", mismatches[0])

    def test_markdown_states_provenance_and_metadata_limits(self):
        rendered = report_builder.render_markdown(valid_report())
        self.assertIn("Declared input manifest", rendered)
        self.assertIn("not cryptographically authenticated", rendered)
        self.assertIn("does not prove the checkout is clean", rendered)
        self.assertIn("not task-completion evidence", rendered)

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


    def test_markdown_metadata_and_manifest_cannot_break_inline_code_context(self):
        report = valid_report()
        report["task_id"] = "task`\n## forged heading"
        report["branch"] = "branch` [click](https://example.invalid)"
        report["input_manifest"] = [
            {"path": "docs/`[x].md", "sha256": "c" * 64}
        ]
        rendered = report_builder.render_markdown(report)
        self.assertEqual(rendered.count("`"), 0)
        self.assertIn("\\`", rendered)
        self.assertNotIn("[click](", rendered)
        self.assertNotIn("## forged heading", rendered)


    def test_rejects_malformed_task_definition_hash(self):
        report = valid_report()
        report["task_definition_sha256"] = "not-a-hash"
        with self.assertRaisesRegex(ValueError, "task_definition_sha256"):
            report_builder.validate_report(report)

    def test_task_definition_digest_is_stable_and_order_independent(self):
        first = {"task_id": "P3-RO-001", "phase": "phase3", "scope": ["a", "b"]}
        second = {"scope": ["a", "b"], "phase": "phase3", "task_id": "P3-RO-001"}
        self.assertEqual(
            report_builder.task_definition_digest(first),
            report_builder.task_definition_digest(second),
        )

    def test_task_definition_digest_rejects_non_string_object_keys(self):
        with self.assertRaisesRegex(TypeError, "keys must be strings"):
            report_builder.task_definition_digest({"task_id": "x", 1: "ambiguous"})

    def test_task_definition_digest_rejects_python_only_values(self):
        with self.assertRaisesRegex(TypeError, "not JSON-compatible"):
            report_builder.task_definition_digest({"task_id": "x", "scope": ("a", "b")})

    def test_task_definition_digest_rejects_non_finite_numbers(self):
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "non-finite"):
                    report_builder.task_definition_digest({"task_id": "x", "weight": value})

    def test_task_definition_digest_accepts_nested_json_values(self):
        task = {"task_id": "x", "policy": {"enabled": True, "thresholds": [1, 2.5, None]}}
        digest = report_builder.task_definition_digest(task)
        self.assertRegex(digest, r"^[0-9a-f]{64}$")

    def test_report_task_binding_accepts_exact_trusted_task(self):
        task = {"task_id": "P3-RO-TEST", "phase": "phase3_sideways_range", "scope": ["inspect"]}
        report = valid_report()
        report["task_definition_sha256"] = report_builder.task_definition_digest(task)
        report_builder.verify_report_task_binding(report, task)

    def test_report_task_binding_rejects_changed_task_definition(self):
        task = {"task_id": "P3-RO-TEST", "phase": "phase3_sideways_range", "scope": ["inspect"]}
        report = valid_report()
        report["task_definition_sha256"] = report_builder.task_definition_digest(task)
        changed = dict(task, scope=["inspect", "extra"])
        with self.assertRaisesRegex(ValueError, "hash does not match"):
            report_builder.verify_report_task_binding(report, changed)

    def test_report_task_binding_rejects_task_id_or_phase_mismatch(self):
        task = {"task_id": "P3-RO-TEST", "phase": "phase3_sideways_range", "scope": ["inspect"]}
        report = valid_report()
        report["task_definition_sha256"] = report_builder.task_definition_digest(task)
        with self.assertRaisesRegex(ValueError, "task_id"):
            report_builder.verify_report_task_binding(report, dict(task, task_id="P3-OTHER"))
        with self.assertRaisesRegex(ValueError, "phase"):
            report_builder.verify_report_task_binding(report, dict(task, phase="phase1"))

    def test_report_provenance_accepts_matching_clean_checkout(self):
        with tempfile.TemporaryDirectory(dir=report_builder.REPOSITORY_ROOT) as temporary:
            path = Path(temporary) / "evidence.txt"
            path.write_text("commit-bound evidence", encoding="utf-8")
            relative = path.relative_to(report_builder.REPOSITORY_ROOT).as_posix()
            task = {"task_id": "P3-RO-TEST", "phase": "phase3_sideways_range", "scope": ["inspect"]}
            report = valid_report()
            report["task_definition_sha256"] = report_builder.task_definition_digest(task)
            report["input_manifest"] = report_builder.build_input_manifest([relative])
            report_builder.verify_report_provenance(
                report, task,
                expected_repository=report["repository"],
                expected_branch=report["branch"],
                expected_commit_sha=report["commit_sha"],
                actual_head_sha=report["commit_sha"],
                checkout_clean=True,
            )

    def test_report_provenance_rejects_head_commit_mismatch(self):
        task = {"task_id": "P3-RO-TEST", "phase": "phase3_sideways_range", "scope": ["inspect"]}
        report = valid_report()
        report["task_definition_sha256"] = report_builder.task_definition_digest(task)
        with self.assertRaisesRegex(ValueError, "HEAD does not match"):
            report_builder.verify_report_provenance(
                report, task,
                expected_repository=report["repository"],
                expected_branch=report["branch"],
                expected_commit_sha=report["commit_sha"],
                actual_head_sha="c" * 40,
                checkout_clean=True,
            )

    def test_report_provenance_rejects_dirty_checkout(self):
        task = {"task_id": "P3-RO-TEST", "phase": "phase3_sideways_range", "scope": ["inspect"]}
        report = valid_report()
        report["task_definition_sha256"] = report_builder.task_definition_digest(task)
        with self.assertRaisesRegex(ValueError, "confirmed clean"):
            report_builder.verify_report_provenance(
                report, task,
                expected_repository=report["repository"],
                expected_branch=report["branch"],
                expected_commit_sha=report["commit_sha"],
                actual_head_sha=report["commit_sha"],
                checkout_clean=False,
            )

    def test_report_provenance_rejects_untrusted_branch_claim(self):
        task = {"task_id": "P3-RO-TEST", "phase": "phase3_sideways_range", "scope": ["inspect"]}
        report = valid_report()
        report["task_definition_sha256"] = report_builder.task_definition_digest(task)
        with self.assertRaisesRegex(ValueError, "branch does not match"):
            report_builder.verify_report_provenance(
                report, task,
                expected_repository=report["repository"],
                expected_branch="price-action-v1",
                expected_commit_sha=report["commit_sha"],
                actual_head_sha=report["commit_sha"],
                checkout_clean=True,
            )

    def test_artifact_bundle_contains_complete_hashed_outputs(self):
        with tempfile.TemporaryDirectory(dir=report_builder.REPOSITORY_ROOT) as temporary:
            path = Path(temporary) / "evidence.txt"
            path.write_text("artifact evidence", encoding="utf-8")
            relative = path.relative_to(report_builder.REPOSITORY_ROOT).as_posix()
            task = {"task_id": "P3-RO-TEST", "phase": "phase3_sideways_range", "scope": ["inspect"]}
            report = valid_report()
            report["run_id"] = "12345"
            report["task_definition_sha256"] = report_builder.task_definition_digest(task)
            report["input_manifest"] = report_builder.build_input_manifest([relative])
            bundle = report_builder.build_artifact_bundle(
                report, task,
                expected_repository=report["repository"],
                expected_branch=report["branch"],
                expected_commit_sha=report["commit_sha"],
                actual_head_sha=report["commit_sha"],
                checkout_clean=True,
                run_id="12345",
                run_attempt="2",
            )
            self.assertEqual(
                set(bundle["files"]),
                {"report.json", "report.md", "artifact_manifest.json"},
            )
            self.assertEqual(bundle["artifact_name"], "okx-research-agent-12345-2")
            manifest = json.loads(bundle["files"]["artifact_manifest.json"])
            self.assertEqual(
                {row["path"] for row in manifest["files"]},
                {"report.json", "report.md"},
            )
            for row in manifest["files"]:
                actual = hashlib.sha256(bundle["files"][row["path"]].encode("utf-8")).hexdigest()
                self.assertEqual(actual, row["sha256"])
            self.assertTrue(bundle["files"]["artifact_manifest.json"].endswith("\n"))

    def test_artifact_verifier_accepts_complete_bundle(self):
        with tempfile.TemporaryDirectory(dir=report_builder.REPOSITORY_ROOT) as temporary:
            path = Path(temporary) / "evidence.txt"
            path.write_text("artifact evidence", encoding="utf-8")
            relative = path.relative_to(report_builder.REPOSITORY_ROOT).as_posix()
            task = {"task_id": "P3-RO-TEST", "phase": "phase3_sideways_range", "scope": ["inspect"]}
            report = valid_report()
            report["run_id"] = "12345"
            report["task_definition_sha256"] = report_builder.task_definition_digest(task)
            report["input_manifest"] = report_builder.build_input_manifest([relative])
            bundle = report_builder.build_artifact_bundle(
                report, task,
                expected_repository=report["repository"],
                expected_branch=report["branch"],
                expected_commit_sha=report["commit_sha"],
                actual_head_sha=report["commit_sha"],
                checkout_clean=True,
                run_id="12345",
                run_attempt="2",
            )
            report_builder.verify_artifact_files(
                bundle["files"], bundle["manifest"],
                actual_artifact_name=bundle["artifact_name"],
                expected_run_id="12345",
                expected_run_attempt="2",
            )

    def test_artifact_verifier_binds_repository_branch_and_task_hash(self):
        with tempfile.TemporaryDirectory(dir=report_builder.REPOSITORY_ROOT) as temporary:
            path = Path(temporary) / "evidence.txt"
            path.write_text("artifact identity binding", encoding="utf-8")
            relative = path.relative_to(report_builder.REPOSITORY_ROOT).as_posix()
            task = {"task_id": "P3-RO-TEST", "phase": "phase3_sideways_range", "scope": ["inspect"]}
            report = valid_report()
            report["run_id"] = "12345"
            report["task_definition_sha256"] = report_builder.task_definition_digest(task)
            report["input_manifest"] = report_builder.build_input_manifest([relative])
            bundle = report_builder.build_artifact_bundle(
                report, task,
                expected_repository=report["repository"],
                expected_branch=report["branch"],
                expected_commit_sha=report["commit_sha"],
                actual_head_sha=report["commit_sha"],
                checkout_clean=True,
                run_id="12345",
                run_attempt="1",
            )
            tampered_manifest = dict(bundle["manifest"])
            tampered_manifest["repository"] = "attacker/other-repo"
            tampered_files = dict(bundle["files"])
            tampered_files["artifact_manifest.json"] = (
                json.dumps(tampered_manifest, sort_keys=True, indent=2) + "\\n"
            )
            with self.assertRaisesRegex(ValueError, "identity does not match"):
                report_builder.verify_artifact_files(
                    tampered_files, tampered_manifest,
                    actual_artifact_name=bundle["artifact_name"],
                    expected_run_id="12345",
                    expected_run_attempt="1",
                    expected_repository=report["repository"],
                    expected_branch=report["branch"],
                    expected_commit_sha=report["commit_sha"],
                    expected_task_id=report["task_id"],
                    expected_phase=report["phase"],
                    expected_task_definition_sha256=report["task_definition_sha256"],
                )

    def test_artifact_verifier_rejects_downloaded_name_mismatch(self):
        with tempfile.TemporaryDirectory(dir=report_builder.REPOSITORY_ROOT) as temporary:
            path = Path(temporary) / "evidence.txt"
            path.write_text("artifact evidence", encoding="utf-8")
            relative = path.relative_to(report_builder.REPOSITORY_ROOT).as_posix()
            task = {"task_id": "P3-RO-TEST", "phase": "phase3_sideways_range", "scope": ["inspect"]}
            report = valid_report()
            report["run_id"] = "12345"
            report["task_definition_sha256"] = report_builder.task_definition_digest(task)
            report["input_manifest"] = report_builder.build_input_manifest([relative])
            bundle = report_builder.build_artifact_bundle(
                report, task,
                expected_repository=report["repository"],
                expected_branch=report["branch"],
                expected_commit_sha=report["commit_sha"],
                actual_head_sha=report["commit_sha"],
                checkout_clean=True,
                run_id="12345",
                run_attempt="1",
            )
            with self.assertRaisesRegex(ValueError, "Artifact name"):
                report_builder.verify_artifact_files(
                    bundle["files"], bundle["manifest"],
                    actual_artifact_name="wrong-artifact-name",
                    expected_run_id="12345",
                    expected_run_attempt="1",
                    expected_repository=report["repository"],
                    expected_branch=report["branch"],
                    expected_commit_sha=report["commit_sha"],
                    expected_task_id=report["task_id"],
                    expected_phase=report["phase"],
                    expected_task_definition_sha256=report["task_definition_sha256"],
                )

    def test_artifact_verifier_rejects_tampered_report_bytes(self):
        with tempfile.TemporaryDirectory(dir=report_builder.REPOSITORY_ROOT) as temporary:
            path = Path(temporary) / "evidence.txt"
            path.write_text("artifact evidence", encoding="utf-8")
            relative = path.relative_to(report_builder.REPOSITORY_ROOT).as_posix()
            task = {"task_id": "P3-RO-TEST", "phase": "phase3_sideways_range", "scope": ["inspect"]}
            report = valid_report()
            report["run_id"] = "12345"
            report["task_definition_sha256"] = report_builder.task_definition_digest(task)
            report["input_manifest"] = report_builder.build_input_manifest([relative])
            bundle = report_builder.build_artifact_bundle(
                report, task,
                expected_repository=report["repository"],
                expected_branch=report["branch"],
                expected_commit_sha=report["commit_sha"],
                actual_head_sha=report["commit_sha"],
                checkout_clean=True,
                run_id="12345",
                run_attempt="1",
            )
            tampered = dict(bundle["files"])
            tampered["report.md"] += "\\nInjected content"
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                report_builder.verify_artifact_files(
                    tampered, bundle["manifest"],
                    actual_artifact_name=bundle["artifact_name"],
                    expected_run_id="12345",
                    expected_run_attempt="1",
                    expected_repository=report["repository"],
                    expected_branch=report["branch"],
                    expected_commit_sha=report["commit_sha"],
                    expected_task_id=report["task_id"],
                    expected_phase=report["phase"],
                    expected_task_definition_sha256=report["task_definition_sha256"],
                )

    def test_artifact_verifier_rejects_missing_or_unexpected_files(self):
        files = {
            "report.json": "{}",
            "report.md": "report",
            "artifact_manifest.json": "{}",
            "extra.txt": "unexpected",
        }
        with self.assertRaisesRegex(ValueError, "exactly the three"):
            report_builder.verify_artifact_files(
                files, {}, actual_artifact_name="okx-research-agent-1-1",
                expected_run_id="1", expected_run_attempt="1"
            )

    def test_artifact_verifier_rejects_untrusted_run_identifier_claim(self):
        with tempfile.TemporaryDirectory(dir=report_builder.REPOSITORY_ROOT) as temporary:
            path = Path(temporary) / "evidence.txt"
            path.write_text("artifact evidence", encoding="utf-8")
            relative = path.relative_to(report_builder.REPOSITORY_ROOT).as_posix()
            task = {"task_id": "P3-RO-TEST", "phase": "phase3_sideways_range", "scope": ["inspect"]}
            report = valid_report()
            report["run_id"] = "12345"
            report["task_definition_sha256"] = report_builder.task_definition_digest(task)
            report["input_manifest"] = report_builder.build_input_manifest([relative])
            bundle = report_builder.build_artifact_bundle(
                report, task,
                expected_repository=report["repository"],
                expected_branch=report["branch"],
                expected_commit_sha=report["commit_sha"],
                actual_head_sha=report["commit_sha"],
                checkout_clean=True,
                run_id="12345",
                run_attempt="2",
            )
            with self.assertRaisesRegex(ValueError, "trusted workflow context"):
                report_builder.verify_artifact_files(
                    bundle["files"], bundle["manifest"],
                    actual_artifact_name=bundle["artifact_name"],
                    expected_run_id="99999",
                    expected_run_attempt="2",
                    expected_repository=report["repository"],
                    expected_branch=report["branch"],
                    expected_commit_sha=report["commit_sha"],
                    expected_task_id=report["task_id"],
                    expected_phase=report["phase"],
                    expected_task_definition_sha256=report["task_definition_sha256"],
                )

    def test_artifact_verifier_rejects_duplicate_manifest_json_keys(self):
        files = {
            "report.json": "{}",
            "report.md": "report",
            "artifact_manifest.json": '{"schema_version":1,"schema_version":1}',
        }
        with self.assertRaisesRegex(ValueError, "strict JSON"):
            report_builder.verify_artifact_files(
                files, {}, actual_artifact_name="okx-research-agent-1-1",
                expected_run_id="1", expected_run_attempt="1",
            )

    def test_artifact_verifier_rejects_nonstandard_json_constants(self):
        files = {
            "report.json": '{"value":NaN}',
            "report.md": "report",
            "artifact_manifest.json": "{}",
        }
        with self.assertRaisesRegex(ValueError, "strict JSON"):
            report_builder.verify_artifact_files(
                files, {}, actual_artifact_name="okx-research-agent-1-1",
                expected_run_id="1", expected_run_attempt="1",
            )

    def test_artifact_bundle_rejects_run_id_mismatch(self):
        task = {"task_id": "P3-RO-TEST", "phase": "phase3_sideways_range", "scope": ["inspect"]}
        report = valid_report()
        report["task_definition_sha256"] = report_builder.task_definition_digest(task)
        with self.assertRaisesRegex(ValueError, "run_id"):
            report_builder.build_artifact_bundle(
                report, task,
                expected_repository=report["repository"],
                expected_branch=report["branch"],
                expected_commit_sha=report["commit_sha"],
                actual_head_sha=report["commit_sha"],
                checkout_clean=True,
                run_id="99999",
                run_attempt="1",
            )

    def test_artifact_bundle_rejects_non_numeric_run_attempt(self):
        task = {"task_id": "P3-RO-TEST", "phase": "phase3_sideways_range", "scope": ["inspect"]}
        report = valid_report()
        report["run_id"] = "12345"
        report["task_definition_sha256"] = report_builder.task_definition_digest(task)
        with self.assertRaisesRegex(ValueError, "run_attempt"):
            report_builder.build_artifact_bundle(
                report, task,
                expected_repository=report["repository"],
                expected_branch=report["branch"],
                expected_commit_sha=report["commit_sha"],
                actual_head_sha=report["commit_sha"],
                checkout_clean=True,
                run_id=report["run_id"],
                run_attempt="latest",
            )

    def test_markdown_report_displays_task_definition_hash(self):
        rendered = report_builder.render_markdown(valid_report())
        self.assertIn("Task definition SHA-256", rendered)
        self.assertIn("d" * 64, rendered)

if __name__ == "__main__":
    unittest.main()
