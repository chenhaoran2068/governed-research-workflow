"""Release-preparation checks for the v1.21 source scope."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "system" / "11_distribution_installation_and_release"
CONTROL = RELEASE / "V1_21_RELEASE_CONTROL_CANDIDATE.json"
REQUIRED = (
    "RELEASE_NOTES_v1.21.0.md",
    "PUBLIC_MATERIAL_RIGHTS_REVIEW_v1.21.0.md",
    "V1_21_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
    "V1_21_RELEASE_GATE.md",
    "V1_21_RELEASE_EVIDENCE.md",
    "V1_21_RELEASE_CONTROL_CANDIDATE.json",
)
PRIVATE_MARKERS = (r"(?i)[a-z]:\\", r"(?i)paco2", r"(?i)research[0-9]+", r"(?i)crs_dev", r"(?i)99sai")


class V121ReleasePreparationTests(unittest.TestCase):
    def test_source_identity_and_release_records_are_present(self) -> None:
        manifest = (ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8")
        self.assertIn("system_version: 1.21.1", manifest)
        for name in REQUIRED:
            self.assertTrue((RELEASE / name).is_file(), name)

    def test_control_record_is_structurally_valid_and_keeps_release_unresolved(self) -> None:
        schema = json.loads((RELEASE / "release_control_record.schema.json").read_text(encoding="utf-8"))
        record = json.loads(CONTROL.read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))
        self.assertEqual(record["status"], "candidate_reviewed")
        self.assertEqual(record["candidate_identity"]["candidate_version"], "1.21.0")
        self.assertEqual(record["candidate_identity"]["exact_commit"], "0" * 40)
        self.assertIsNone(record["c4_release_authorization_reference"])
        self.assertIsNone(record["post_release_verification_reference"])

    def test_release_source_is_generic_and_does_not_preclaim_publication(self) -> None:
        content = "\n".join((RELEASE / name).read_text(encoding="utf-8") for name in REQUIRED)
        for pattern in PRIVATE_MARKERS:
            with self.subTest(pattern=pattern):
                self.assertIsNone(re.search(pattern, content), pattern)
        lowered = content.lower()
        self.assertIn("does not establish", lowered)
        self.assertIn("release remains blocked", lowered)
        self.assertNotIn("v1.21.0 is published", lowered)
        self.assertNotIn("v1.21.0 is installed", lowered)

    def test_release_scope_retains_existing_boundaries(self) -> None:
        notes = (RELEASE / "RELEASE_NOTES_v1.21.0.md").read_text(encoding="utf-8").lower()
        gate = (RELEASE / "V1_21_RELEASE_GATE.md").read_text(encoding="utf-8").lower()
        self.assertIn("not a new capability identifier", notes)
        self.assertIn("read-only", notes)
        self.assertIn("matching github release", gate)


if __name__ == "__main__":
    unittest.main()
