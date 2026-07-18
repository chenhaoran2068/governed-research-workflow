"""Synthetic structure and boundary tests for the metadata-only provenance register."""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPOSITORY_ROOT / "system" / "09_schemas_records_and_templates" / "data_provenance_register.schema.json"
TEMPLATE_PATH = REPOSITORY_ROOT / "assets" / "data-provenance-register.template.json"
GUIDANCE_PATH = REPOSITORY_ROOT / "references" / "data-provenance-register.md"
PRIVATE_PATH_PATTERN = r"(?i)(?:[a-z]:\\|/(?:home|users)/)"


def data_action_refusal_reasons(record: dict, requested_action: str) -> list[str]:
    """Test-only interpretation of record boundaries; not a data-access helper."""
    reasons: list[str] = []
    access = record["access_and_sharing"]
    unknown_fields = (
        access["access_status"],
        access["restriction_status"],
        access["sharing_status"],
        access["online_service_condition_status"],
    )
    if requested_action in {"copy", "upload", "share", "publish", "release", "process"} and "unknown" in unknown_fields:
        reasons.append("critical data status is unknown")
    if access["status_claimed"] and not access["data_access_or_share_evidence_reference"]:
        reasons.append("claimed status lacks data-access/share evidence")
    if record["source"]["contains_credentials_or_sensitive_identifiers"]:
        reasons.append("record declares credentials or sensitive identifiers")
    return reasons


class DataProvenanceRegisterTests(unittest.TestCase):
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

    def test_template_is_valid_metadata_only_synthetic_pointer(self) -> None:
        self.assert_valid(self.template)
        self.assertTrue(self.template["metadata_only"])
        self.assertEqual(self.template["object_class"], "external_source_pointer")
        self.assertEqual(self.template["source"]["contains_credentials_or_sensitive_identifiers"], False)
        self.assertIn("example.invalid", self.template["source"]["source_pointer_or_redacted_locator"])

    def test_claimed_data_status_requires_evidence_reference(self) -> None:
        claimed = copy.deepcopy(self.template)
        claimed["access_and_sharing"].update(
            {
                "access_status": "documented_access_available",
                "restriction_status": "documented_restricted",
                "sharing_status": "documented_sharing_restricted",
                "online_service_condition_status": "documented_conditions_apply",
                "status_claimed": True,
                "data_access_or_share_evidence_reference": None,
            }
        )
        self.assert_invalid(claimed)
        claimed["access_and_sharing"]["data_access_or_share_evidence_reference"] = "SYNTHETIC-SOURCE-TERMS-0001"
        self.assert_valid(claimed)

    def test_unknown_status_refuses_consequential_data_actions_without_forbidding_planning(self) -> None:
        record = copy.deepcopy(self.template)
        self.assertEqual(data_action_refusal_reasons(record, "plan"), [])
        self.assertIn("critical data status is unknown", data_action_refusal_reasons(record, "process"))
        self.assertIn("critical data status is unknown", data_action_refusal_reasons(record, "share"))
        self.assertTrue(record["access_and_sharing"]["verification_hypothesis"]["not_an_authorization"])

    def test_optional_restricted_or_clinical_awareness_requires_explicit_non_compliance_boundary(self) -> None:
        extended = copy.deepcopy(self.template)
        extended["optional_restricted_or_clinical_awareness"] = {"applies": True}
        self.assert_invalid(extended)

        extended["optional_restricted_or_clinical_awareness"] = {
            "applies": True,
            "context_categories": ["clinical_database", "other_restricted"],
            "credentialed_access_may_be_required": True,
            "governance_status": "unknown",
            "not_a_compliance_determination": True,
        }
        self.assert_valid(extended)

    def test_record_cannot_declare_sensitive_content(self) -> None:
        unsafe = copy.deepcopy(self.template)
        unsafe["source"]["contains_credentials_or_sensitive_identifiers"] = True
        self.assert_invalid(unsafe)

    def test_public_template_and_guidance_have_no_private_workspace_markers(self) -> None:
        text = TEMPLATE_PATH.read_text(encoding="utf-8") + "\n" + GUIDANCE_PATH.read_text(encoding="utf-8")
        self.assertIsNone(re.search(PRIVATE_PATH_PATTERN, text))
        self.assertIsNone(re.search(r"(?i)(password\s*[=:]|api[_-]?key\s*[=:]|authorization:\s*bearer)", text))

    def test_guidance_separates_metadata_from_task_authorization_and_compliance(self) -> None:
        guidance = GUIDANCE_PATH.read_text(encoding="utf-8")
        normalized_guidance = re.sub(r"\s+", " ", guidance)
        self.assertIn("Neither record substitutes for the other", normalized_guidance)
        self.assertIn("Unknown Is Not Approval", normalized_guidance)
        self.assertIn("not an ethics, consent, DUA, privacy", normalized_guidance)
        self.assertIn("does not import, read, copy, hash, clean, analyze", normalized_guidance)


if __name__ == "__main__":
    unittest.main()
