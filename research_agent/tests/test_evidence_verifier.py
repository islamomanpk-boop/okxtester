"""Evidence-verifier tests; authored, not executed."""
import hashlib
import unittest

from research_agent.engine.evidence_verifier import verify_worker_evidence


class EvidenceVerifierTests(unittest.TestCase):
    def setUp(self):
        self.commit = "1" * 40
        self.content = b"authoritative handoff content\n"
        self.digest = hashlib.sha256(self.content).hexdigest()
        self.path = "docs/assistant_handoff/example.md"
        self.evidence = [{"path": self.path, "sha256": self.digest,
                          "source_ref": self.commit, "description": "Handoff evidence"}]
        self.manifest = {"commit_sha": self.commit, "files": {self.path: self.digest}}

    def verify(self, evidence=None, manifest=None, contents=None, commit=None):
        return verify_worker_evidence(
            self.evidence if evidence is None else evidence,
            expected_commit_sha=self.commit if commit is None else commit,
            commit_manifest=self.manifest if manifest is None else manifest,
            file_contents={self.path: self.content} if contents is None else contents,
        )

    def test_matching_evidence_is_verified_but_not_approved(self):
        result = self.verify()
        self.assertTrue(result["all_evidence_verified"])
        self.assertEqual(result["verified_count"], 1)
        self.assertFalse(result["task_completion_approved"])
        self.assertFalse(result["gate_closure_approved"])
        self.assertTrue(result["human_review_required"])

    def test_rejects_worker_hash_mismatch(self):
        result = self.verify(evidence=[dict(self.evidence[0], sha256="a" * 64)])
        self.assertIn("worker_hash_does_not_match_commit_manifest", result["results"][0]["reasons"])

    def test_rejects_checkout_byte_mismatch(self):
        result = self.verify(contents={self.path: b"changed"})
        self.assertIn("checkout_bytes_do_not_match_commit_manifest", result["results"][0]["reasons"])

    def test_rejects_missing_checkout_file(self):
        result = self.verify(contents={})
        self.assertIn("file_missing_from_checkout", result["results"][0]["reasons"])

    def test_rejects_path_not_in_commit_manifest(self):
        result = self.verify(manifest={"commit_sha": self.commit, "files": {}})
        self.assertIn("path_absent_from_expected_commit", result["results"][0]["reasons"])

    def test_rejects_commit_manifest_for_different_commit(self):
        with self.assertRaises(ValueError):
            self.verify(manifest={"commit_sha": "2" * 40, "files": {self.path: self.digest}})

    def test_rejects_traversal_and_duplicate_evidence_paths(self):
        unsafe = [dict(self.evidence[0], path="../outside.md")]
        self.assertIn("unsafe_repository_path", self.verify(evidence=unsafe)["results"][0]["reasons"])
        result = self.verify(evidence=self.evidence + [dict(self.evidence[0])])
        self.assertIn("duplicate_evidence_path", result["results"][1]["reasons"])

    def test_rejects_malformed_commit_manifest_hash(self):
        with self.assertRaises(ValueError):
            self.verify(manifest={"commit_sha": self.commit, "files": {self.path: "bad"}})

    def test_empty_evidence_is_not_vacuously_verified(self):
        result = self.verify(evidence=[])
        self.assertFalse(result["all_evidence_verified"])
        self.assertEqual(result["evidence_count"], 0)


if __name__ == "__main__":
    unittest.main()
