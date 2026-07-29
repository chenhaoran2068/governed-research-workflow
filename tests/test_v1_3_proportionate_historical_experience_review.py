"""Public-contract and release-preparation checks for the v1.3.0 source scope."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "system" / "09_schemas_records_and_templates"
ASSETS = ROOT / "assets" / "experience-vocabulary"
RELEASE = ROOT / "system" / "11_distribution_installation_and_release"
LEDGER_PATH = ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"


class V13ProportionateHistoricalExperienceReviewTests(unittest.TestCase):
    def test_generic_contract_surfaces_and_template_validate(self) -> None:
        schema = json.loads((SCHEMAS / "experience_review_decision_register.schema.json").read_text(encoding="utf-8"))
        template = json.loads((ASSETS / "experience-review-decision-register.template.json").read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema).iter_errors(template))
        self.assertEqual([], errors, "\n".join(error.message for error in errors))
        for path in (
            ROOT / "scripts" / "validate_experience_review_decision_register.py",
            ROOT / "scripts" / "validate_experience_reference_index.py",
            ROOT / "tests" / "test_experience_review_decision_register.py",
            ROOT / "references" / "controlled-experience-vocabulary.md",
        ):
            self.assertTrue(path.is_file(), path)

    def test_capability_is_unique_and_keeps_per_source_human_boundary(self) -> None:
        ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        matching = [item for item in ledger["capabilities"] if item["capability_id"] == "GRW-CAP-140-01"]
        self.assertEqual(1, len(matching))
        self.assertEqual(len(ledger["capabilities"]), len({item["capability_id"] for item in ledger["capabilities"]}))
        record = matching[0]
        self.assertEqual("verified", record["implementation_status"])
        self.assertEqual("admitted", record["release_disposition"])
        self.assertEqual({"metadata_only", "synthetic_only", "no_data_access", "no_external_service_action"}, set(record["data_and_external_boundary"]))
        self.assertIn("human", record["promise"].lower())
        self.assertIn("does not read", record["non_promise"].lower())
        self.assertIn("promotion", record["non_promise"].lower())

    def test_release_preparation_records_are_generic_and_pre_c4(self) -> None:
        required = (
            "V1_3_CAPABILITY_ADMISSION.md",
            "V1_3_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
            "V1_3_RELEASE_CONTROL_CANDIDATE.json",
            "V1_3_RELEASE_EVIDENCE.md",
            "V1_3_RELEASE_GATE.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v1.3.0.md",
            "RELEASE_NOTES_v1.3.0.md",
        )
        for name in required:
            self.assertTrue((RELEASE / name).is_file(), name)
        record = json.loads((RELEASE / "V1_3_RELEASE_CONTROL_CANDIDATE.json").read_text(encoding="utf-8"))
        schema = json.loads((RELEASE / "release_control_record.schema.json").read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema).iter_errors(record))
        self.assertEqual([], errors, "\n".join(error.message for error in errors))
        self.assertEqual("1.3.0", record["candidate_identity"]["candidate_version"])
        self.assertEqual("v1.3.0", record["candidate_identity"]["intended_tag"])
        self.assertIsNone(record["c4_release_authorization_reference"])
        text = "\n".join((RELEASE / name).read_text(encoding="utf-8") for name in required if name.endswith(".md"))
        self.assertIn("pre-C4", text)
        self.assertNotIn("Release has been created", text)

    def test_current_surfaces_are_time_neutral_and_do_not_leak_private_markers(self) -> None:
        paths = (
            ROOT / "README.md",
            ROOT / "ROADMAP.md",
            ROOT / "SKILL.md",
            ROOT / "system" / "06_memory_and_learning" / "MODULE.md",
            ROOT / "references" / "controlled-experience-vocabulary.md",
            SCHEMAS / "experience_review_decision_register.schema.json",
            SCHEMAS / "experience_reference_index.schema.json",
            ASSETS / "experience-review-decision-register.template.json",
            ROOT / "scripts" / "validate_experience_review_decision_register.py",
            ROOT / "scripts" / "validate_experience_reference_index.py",
            RELEASE / "V1_3_CAPABILITY_ADMISSION.md",
            RELEASE / "V1_3_DEPENDENCY_AND_WORKFLOW_REVIEW.md",
            RELEASE / "V1_3_RELEASE_EVIDENCE.md",
            RELEASE / "V1_3_RELEASE_GATE.md",
            RELEASE / "PUBLIC_MATERIAL_RIGHTS_REVIEW_v1.3.0.md",
            RELEASE / "RELEASE_NOTES_v1.3.0.md",
        )
        text = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        lowered = text.lower()
        self.assertIn("grw-cap-140-01", lowered)
        self.assertIn("metadata-only", lowered)
        self.assertIn("mapped", lowered)
        self.assertNotIn("v1.3.0 is released", lowered)
        self.assertNotIn("v1.3.0 is installed", lowered)
        self.assertIsNone(re.search(r"(?i)(?:[a-z]:\\|/(?:home|users)/)", text))
        for prohibited in ("src-gm-", "src-lcr-", "src-pq-", "src-study-", "chenhaoran\\shared", "source_inventory.json"):
            self.assertNotIn(prohibited, lowered)


if __name__ == "__main__":
    unittest.main()
