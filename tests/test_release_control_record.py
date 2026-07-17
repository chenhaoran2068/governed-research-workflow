"""Synthetic validation and refusal checks for release-control records."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPOSITORY_ROOT / "system" / "11_distribution_installation_and_release" / "release_control_record.schema.json"
TEMPLATE_PATH = REPOSITORY_ROOT / "assets" / "release-control-record.template.json"
GUIDANCE_PATH = REPOSITORY_ROOT / "system" / "11_distribution_installation_and_release" / "RELEASE_CONTROL.md"
LEDGER_PATH = REPOSITORY_ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"
CURRENT_RELEASE_PATH = REPOSITORY_ROOT / "system" / "11_distribution_installation_and_release" / "CURRENT_RELEASE_STATUS.md"


def release_claim_refusal_reasons(record: dict) -> list[str]:
    """Test-only claim gate; it does not create a tag, release, or permission."""
    reasons: list[str] = []
    if record["material_reviews"]["public_material_rights_review"] != "pass":
        reasons.append("public material and rights review is not passed")
    if record["material_reviews"]["private_material_secret_review"] != "pass":
        reasons.append("private material and secret review is not passed")
    if not record["candidate_review_acceptance_reference"]:
        reasons.append("candidate review acceptance is absent")
    if not record["c4_release_authorization_reference"]:
        reasons.append("C4 release authorization is absent")
    if record["c4_release_authorization_reference"] == record["candidate_review_acceptance_reference"]:
        reasons.append("candidate review acceptance cannot substitute for C4 authorization")
    if not record["post_release_verification_reference"]:
        reasons.append("post-release verification is absent")
    if record["candidate_identity"]["branch_state"] != "exact_release_commit":
        reasons.append("candidate is not identified as an exact release commit")
    if not record["capability_set"]["admitted_capability_ids"]:
        reasons.append("no exact-release admitted capability set is recorded")
    dependency = record["dependency_and_source_authority"]
    if dependency["framework_integrated_behavior_claimed"] and not (
        dependency["framework_tag"] and dependency["framework_commit"]
    ):
        reasons.append("framework-integrated claim lacks exact framework tag and commit")
    return reasons


class ReleaseControlRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.template = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())

    def assert_valid(self, record: dict) -> None:
        errors = sorted(self.validator.iter_errors(record), key=lambda error: list(error.absolute_path))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))

    def assert_invalid(self, record: dict) -> None:
        self.assertTrue(list(self.validator.iter_errors(record)), "record unexpectedly validated")

    def test_schema_and_synthetic_template_validate(self) -> None:
        self.assertTrue(SCHEMA_PATH.is_file())
        self.assertTrue(TEMPLATE_PATH.is_file())
        self.assertTrue(GUIDANCE_PATH.is_file())
        self.assert_valid(self.template)

    def test_missing_exact_candidate_identity_is_refused(self) -> None:
        record = copy.deepcopy(self.template)
        record["candidate_identity"]["exact_commit"] = "not-a-commit"
        self.assert_invalid(record)

    def test_candidate_review_requires_passed_material_reviews(self) -> None:
        record = copy.deepcopy(self.template)
        record["material_reviews"]["public_material_rights_review"] = "unknown"
        self.assert_invalid(record)

    def test_framework_integrated_claim_requires_exact_framework_identity(self) -> None:
        record = copy.deepcopy(self.template)
        record["dependency_and_source_authority"]["framework_integrated_behavior_claimed"] = True
        self.assert_invalid(record)

        record["dependency_and_source_authority"]["framework_tag"] = "v0.1.1"
        record["dependency_and_source_authority"]["framework_commit"] = "b0e32d7710b70299e633df1316b6924cd87b647b"
        self.assert_valid(record)

    def test_candidate_review_cannot_be_used_as_c4_or_post_release_evidence(self) -> None:
        candidate_reasons = release_claim_refusal_reasons(self.template)
        self.assertIn("C4 release authorization is absent", candidate_reasons)
        self.assertIn("post-release verification is absent", candidate_reasons)
        self.assertIn("candidate is not identified as an exact release commit", candidate_reasons)

        conflated = copy.deepcopy(self.template)
        conflated["status"] = "c4_authorized"
        conflated["candidate_identity"]["branch_state"] = "exact_release_commit"
        conflated["c4_release_authorization_reference"] = conflated["candidate_review_acceptance_reference"]
        self.assert_valid(conflated)
        self.assertIn("candidate review acceptance cannot substitute for C4 authorization", release_claim_refusal_reasons(conflated))

    def test_admitted_scope_record_is_valid_but_still_not_c4_authorization(self) -> None:
        record = copy.deepcopy(self.template)
        record["capability_set"]["candidate_outcome"] = "admitted_exact_release_scope"
        record["capability_set"]["admitted_capability_ids"] = ["GRW-CAP-031-01", "GRW-CAP-040-05"]
        self.assert_valid(record)
        reasons = release_claim_refusal_reasons(record)
        self.assertIn("C4 release authorization is absent", reasons)
        self.assertIn("post-release verification is absent", reasons)

    def test_record_hierarchy_and_current_release_are_not_conflated(self) -> None:
        guidance = GUIDANCE_PATH.read_text(encoding="utf-8")
        ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        current_release = CURRENT_RELEASE_PATH.read_text(encoding="utf-8")
        r4005 = next(record for record in ledger["capabilities"] if record["capability_id"] == "GRW-CAP-040-05")

        self.assertIn("Candidate-review acceptance is not C4 authorization", guidance)
        self.assertIn("C4 authorization is not\npost-release verification", guidance)
        self.assertIn("Current public release: `v0.3.1`", current_release)
        self.assertEqual(r4005["implementation_status"], "verified")
        self.assertEqual(r4005["release_disposition"], "admitted")
        self.assertEqual(r4005["public_claim_status"], "permitted")
        self.assertIn("no C4 release authorization", r4005["approval_reference"])


if __name__ == "__main__":
    unittest.main()
