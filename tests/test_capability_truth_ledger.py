"""Structural and refusal checks for the local v0.4 capability truth ledger."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path, PurePosixPath


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = REPOSITORY_ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"
SCHEMA_PATH = REPOSITORY_ROOT / "system" / "09_schemas_records_and_templates" / "capability_truth_ledger.schema.json"
EVIDENCE_MATRIX_PATH = REPOSITORY_ROOT / "system" / "10_assurance_evaluation_and_audit" / "CAPABILITY_EVIDENCE_MATRIX.md"
ADMISSION_RECORD_PATH = REPOSITORY_ROOT / "system" / "11_distribution_installation_and_release" / "V0_4_CAPABILITY_ADMISSION.md"

EXPECTED_CAPABILITY_IDS = {
    "GRW-CAP-031-01",
    "GRW-CAP-031-02",
    "GRW-CAP-031-03",
    "GRW-CAP-031-04",
    "GRW-CAP-040-00",
    "GRW-CAP-040-01",
    "GRW-CAP-040-02",
    "GRW-CAP-040-03",
    "GRW-CAP-040-04",
    "GRW-CAP-040-05",
    "GRW-CAP-040-06",
}
REQUIRED_RECORD_FIELDS = {
    "capability_id",
    "public_name",
    "capability_class",
    "implementation_status",
    "release_disposition",
    "public_claim_status",
    "promise",
    "non_promise",
    "approval_owner",
    "interface",
    "profile_scope",
    "data_and_external_boundary",
    "evidence",
    "version",
    "prior_release_history",
    "approval_reference",
    "claim_surfaces",
    "contradiction_refusal",
    "limitations_and_next_action",
}
def is_safe_relative_path(value: str) -> bool:
    normalized = value.replace("\\", "/")
    if normalized.startswith("/") or re.match(r"^[A-Za-z]:", normalized):
        return False
    return ".." not in PurePosixPath(normalized).parts


class CapabilityTruthLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.records = cls.ledger["capabilities"]

    def test_canonical_ledger_and_schema_have_expected_identity(self) -> None:
        self.assertEqual(self.ledger["ledger_schema_version"], "1.0.0")
        self.assertEqual(self.ledger["ledger_id"], "governed-research-workflow-capability-truth-ledger")
        self.assertEqual(self.ledger["ledger_status"], "local_candidate")
        self.assertEqual(self.ledger["release_context"]["target_release_version"], "v0.4.0")
        self.assertEqual(self.ledger["release_context"]["current_public_baseline"], "v0.3.1")
        self.assertEqual(self.ledger["release_context"]["candidate_branch"], "v0.4.0-capability-truth-ledger-candidate")
        self.assertFalse(self.ledger["release_context"]["public_release_exists"])
        self.assertIn("only to v0.4.0", self.ledger["target_claim_scope"])
        self.assertIn("prior_release_history", self.ledger["target_claim_scope"])
        self.assertEqual(
            self.schema["$id"],
            "https://github.com/chenhaoran2068/governed-research-workflow/schemas/capability_truth_ledger.schema.json",
        )
        self.assertIn("capability", self.schema["$defs"])

    def test_records_are_complete_unique_and_use_controlled_values(self) -> None:
        identifiers = [record["capability_id"] for record in self.records]
        self.assertEqual(set(identifiers), EXPECTED_CAPABILITY_IDS)
        self.assertEqual(len(identifiers), len(set(identifiers)))

        capability_classes = {"routing", "helper", "record", "profile", "role_card", "assurance", "release_control"}
        implementation_statuses = {"planned", "implemented", "verified", "deferred", "retired"}
        release_dispositions = {"candidate", "admitted", "excluded", "superseded"}
        profile_scopes = {"standalone", "framework_integrated", "both", "not_profile_specific"}
        evidence_statuses = {"unverified", "verified", "expired", "not_applicable"}

        for record in self.records:
            self.assertEqual(set(record), REQUIRED_RECORD_FIELDS)
            self.assertTrue(record["public_name"])
            self.assertTrue(record["promise"])
            self.assertTrue(record["non_promise"])
            self.assertTrue(record["contradiction_refusal"])
            self.assertTrue(record["limitations_and_next_action"])
            self.assertIn(record["capability_class"], capability_classes)
            self.assertIn(record["implementation_status"], implementation_statuses)
            self.assertIn(record["release_disposition"], release_dispositions)
            self.assertIn(record["profile_scope"], profile_scopes)
            self.assertIn(record["evidence"]["status"], evidence_statuses)
            self.assertEqual(record["approval_owner"], "accountable_human")
            self.assertEqual(record["version"]["target_release"], "v0.4.0")

    def test_public_claim_requires_verified_admitted_human_approved_evidence(self) -> None:
        for record in self.records:
            if record["public_claim_status"] == "permitted":
                self.assertEqual(record["implementation_status"], "verified")
                self.assertEqual(record["release_disposition"], "admitted")
                self.assertEqual(record["evidence"]["status"], "verified")
                self.assertIsInstance(record["approval_reference"], str)
                self.assertTrue(record["approval_reference"])
                self.assertTrue(record["evidence"]["references"])
            else:
                self.assertEqual(record["public_claim_status"], "forbidden")

        self.assertFalse(
            any(record["public_claim_status"] == "permitted" for record in self.records),
            "No v0.4.0 capability is admitted while this is a local candidate.",
        )

    def test_interface_and_evidence_references_are_safe_and_exist_when_verified(self) -> None:
        for record in self.records:
            interface = record["interface"]
            self.assertIn(interface["status"], {"present", "planned"})
            self.assertTrue(interface["identifiers"])
            for relative_path in interface["paths"]:
                self.assertTrue(is_safe_relative_path(relative_path), relative_path)
                if interface["status"] == "present":
                    self.assertTrue((REPOSITORY_ROOT / relative_path).is_file(), relative_path)

            for relative_path in record["claim_surfaces"]:
                self.assertTrue(is_safe_relative_path(relative_path), relative_path)
                self.assertTrue((REPOSITORY_ROOT / relative_path).is_file(), relative_path)

            evidence = record["evidence"]
            if evidence["status"] == "verified":
                self.assertTrue(evidence["references"])
                for reference in evidence["references"]:
                    self.assertTrue(is_safe_relative_path(reference["path"]), reference["path"])
                    self.assertTrue((REPOSITORY_ROOT / reference["path"]).is_file(), reference["path"])
                    self.assertTrue(reference["identifier"])
            else:
                self.assertEqual(record["public_claim_status"], "forbidden")

    def test_r4001_is_verified_candidate_but_not_admitted_or_publicly_claimable(self) -> None:
        record = next(record for record in self.records if record["capability_id"] == "GRW-CAP-040-01")
        self.assertEqual(record["implementation_status"], "verified")
        self.assertEqual(record["release_disposition"], "candidate")
        self.assertEqual(record["public_claim_status"], "forbidden")
        self.assertEqual(record["interface"]["status"], "present")
        self.assertEqual(record["evidence"]["status"], "verified")
        self.assertTrue(record["approval_reference"])

    def test_all_reviewed_r40_records_have_local_acceptance_and_no_c4_authorization(self) -> None:
        reviewed_r40_ids = {
            "GRW-CAP-040-00",
            "GRW-CAP-040-01",
            "GRW-CAP-040-02",
            "GRW-CAP-040-03",
            "GRW-CAP-040-04",
            "GRW-CAP-040-05",
            "GRW-CAP-040-06",
        }
        for record in self.records:
            if record["capability_id"] not in reviewed_r40_ids:
                continue
            self.assertIsInstance(record["approval_reference"], str)
            self.assertIn("implementation review accepted", record["approval_reference"])
            self.assertIn("no C4 release authorization", record["approval_reference"])

    def test_r4002_is_verified_candidate_but_not_an_executor_or_public_claim(self) -> None:
        record = next(record for record in self.records if record["capability_id"] == "GRW-CAP-040-02")
        self.assertEqual(record["implementation_status"], "verified")
        self.assertEqual(record["release_disposition"], "candidate")
        self.assertEqual(record["public_claim_status"], "forbidden")
        self.assertEqual(record["interface"]["status"], "present")
        self.assertEqual(record["evidence"]["status"], "verified")
        self.assertIn("does not grant autonomy", record["non_promise"].lower())
        self.assertTrue(record["approval_reference"])

    def test_r4004_is_verified_candidate_but_not_data_processing_or_compliance_claim(self) -> None:
        record = next(record for record in self.records if record["capability_id"] == "GRW-CAP-040-04")
        self.assertEqual(record["implementation_status"], "verified")
        self.assertEqual(record["release_disposition"], "candidate")
        self.assertEqual(record["public_claim_status"], "forbidden")
        self.assertEqual(record["interface"]["status"], "present")
        self.assertEqual(record["evidence"]["status"], "verified")
        self.assertIn("will not access", record["non_promise"].lower())
        self.assertIn("does not access data", record["limitations_and_next_action"].lower())
        self.assertTrue(record["approval_reference"])

    def test_r4005_is_verified_candidate_but_not_c4_or_release_claim(self) -> None:
        record = next(record for record in self.records if record["capability_id"] == "GRW-CAP-040-05")
        self.assertEqual(record["implementation_status"], "verified")
        self.assertEqual(record["release_disposition"], "candidate")
        self.assertEqual(record["public_claim_status"], "forbidden")
        self.assertEqual(record["interface"]["status"], "present")
        self.assertEqual(record["evidence"]["status"], "verified")
        self.assertIn("not c4 authorization", record["limitations_and_next_action"].lower())
        self.assertTrue(record["approval_reference"])

    def test_r4006_is_verified_candidate_only_synthetic_assurance(self) -> None:
        record = next(record for record in self.records if record["capability_id"] == "GRW-CAP-040-06")
        self.assertEqual(record["implementation_status"], "verified")
        self.assertEqual(record["release_disposition"], "candidate")
        self.assertEqual(record["public_claim_status"], "forbidden")
        self.assertEqual(record["interface"]["status"], "present")
        self.assertEqual(record["evidence"]["status"], "verified")
        self.assertIn("local synthetic assurance", record["limitations_and_next_action"].lower())
        self.assertTrue(record["approval_reference"])

    def test_planned_r40_records_cannot_be_misrepresented_as_admitted(self) -> None:
        planned_records = [
            record
            for record in self.records
            if record["capability_id"].startswith("GRW-CAP-040-")
            and record["capability_id"] not in {"GRW-CAP-040-00", "GRW-CAP-040-01", "GRW-CAP-040-02", "GRW-CAP-040-03", "GRW-CAP-040-04", "GRW-CAP-040-05", "GRW-CAP-040-06"}
        ]
        self.assertEqual(len(planned_records), 0)
        for record in planned_records:
            self.assertEqual(record["implementation_status"], "planned")
            self.assertEqual(record["release_disposition"], "candidate")
            self.assertEqual(record["public_claim_status"], "forbidden")
            self.assertEqual(record["interface"]["status"], "planned")
            self.assertEqual(record["evidence"]["status"], "unverified")
            self.assertEqual(record["evidence"]["references"], [])
            self.assertIsNone(record["approval_reference"])

    def test_contradiction_brief_requires_options_tradeoffs_and_human_choice(self) -> None:
        required = {
            "conflicting_records_and_exact_locations",
            "known_evidence_and_unknowns",
            "safe_immediate_stop",
            "feasible_repair_options",
            "benefit_cost_compatibility_release_effect_and_residual_risk_per_option",
            "smallest_next_verification",
            "ai_recommendation_separate_from_accountable_human_choice",
        }
        self.assertEqual(set(self.ledger["contradiction_decision_brief_requirements"]), required)
        self.assertIn("forbid", self.ledger["contradiction_refusal_rule"].lower())
        self.assertIn("accountable-human", self.ledger["contradiction_refusal_rule"])

    def test_local_candidate_cannot_claim_a_release(self) -> None:
        text = LEDGER_PATH.read_text(encoding="utf-8")
        self.assertIn(
            "no `v0.4.0` capability is admitted",
            ADMISSION_RECORD_PATH.read_text(encoding="utf-8").lower(),
        )
        self.assertIn("not a public release", EVIDENCE_MATRIX_PATH.read_text(encoding="utf-8"))
        skill = (REPOSITORY_ROOT / "SKILL.md").read_text(encoding="utf-8")
        readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("capability_truth_ledger.json", skill)
        self.assertIn("capability_truth_ledger.json", readme)
        self.assertNotIn("v0.4.0 is released", "\n".join((text, skill, readme)))


if __name__ == "__main__":
    unittest.main()
