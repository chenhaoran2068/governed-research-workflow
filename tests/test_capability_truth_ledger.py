"""Structural and refusal checks for the capability truth ledger."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = REPOSITORY_ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"
SCHEMA_PATH = REPOSITORY_ROOT / "system" / "09_schemas_records_and_templates" / "capability_truth_ledger.schema.json"
EVIDENCE_MATRIX_PATH = REPOSITORY_ROOT / "system" / "10_assurance_evaluation_and_audit" / "CAPABILITY_EVIDENCE_MATRIX.md"
ADMISSION_RECORD_PATH = REPOSITORY_ROOT / "system" / "11_distribution_installation_and_release" / "V0_4_CAPABILITY_ADMISSION.md"
V05_ADMISSION_RECORD_PATH = REPOSITORY_ROOT / "system" / "11_distribution_installation_and_release" / "V0_5_CAPABILITY_ADMISSION.md"
V06_ADMISSION_RECORD_PATH = REPOSITORY_ROOT / "system" / "11_distribution_installation_and_release" / "V0_6_CAPABILITY_ADMISSION.md"

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
    "GRW-CAP-050-01",
    "GRW-CAP-060-01",
    "GRW-CAP-070-01",
    "GRW-CAP-080-01",
    "GRW-CAP-080-02",
    "GRW-CAP-080-03",
    "GRW-CAP-090-01",
    "GRW-CAP-090-02",
    "GRW-CAP-090-03",
    "GRW-CAP-100-01",
    "GRW-CAP-101-01",
    "GRW-CAP-110-01",
    "GRW-CAP-110-02",
    "GRW-CAP-110-03",
    "GRW-CAP-110-04",
    "GRW-CAP-110-05",
    "GRW-CAP-110-06",
}
RELEASED_OR_ADMITTED_IDS = EXPECTED_CAPABILITY_IDS - {
    "GRW-CAP-040-03",
}
V08_RELEASE_SCOPE_IDS = {"GRW-CAP-080-01", "GRW-CAP-080-02", "GRW-CAP-080-03"}
V09_SCOPE_IDS = {"GRW-CAP-090-01", "GRW-CAP-090-02", "GRW-CAP-090-03"}
V10_SCOPE_IDS = {"GRW-CAP-100-01"}
V101_SCOPE_IDS = {"GRW-CAP-101-01"}
V011_SCOPE_IDS = {
    "GRW-CAP-110-01",
    "GRW-CAP-110-02",
    "GRW-CAP-110-03",
    "GRW-CAP-110-04",
    "GRW-CAP-110-05",
    "GRW-CAP-110-06",
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
        self.assertEqual(self.ledger["ledger_schema_version"], "1.4.0")
        self.assertEqual(self.ledger["ledger_id"], "governed-research-workflow-capability-truth-ledger")
        self.assertEqual(self.ledger["ledger_status"], "release_source_prepared")
        self.assertEqual(self.ledger["release_context"]["source_release_version"], "v0.12.0")
        self.assertEqual(self.ledger["release_context"]["historical_public_baseline"], "v0.11.0")
        self.assertIn("exact annotated tag", self.ledger["release_context"]["live_release_identity_rule"])
        self.assertIn("C2-admitted v0.11.0 source scope", self.ledger["target_claim_scope"])
        self.assertIn("v0.12.0 is no-new-interface synthetic integration assurance", self.ledger["target_claim_scope"])
        self.assertIn("Historical facts", self.ledger["target_claim_scope"])
        self.assertEqual(
            self.schema["$id"],
            "https://github.com/chenhaoran2068/governed-research-workflow/schemas/capability_truth_ledger.schema.json",
        )
        self.assertIn("capability", self.schema["$defs"])

    def test_canonical_ledger_validates_against_its_schema(self) -> None:
        errors = sorted(
            Draft202012Validator(self.schema).iter_errors(self.ledger),
            key=lambda error: list(error.absolute_path),
        )
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))

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
            expected_target = (
                "v0.11.0" if record["capability_id"] in V011_SCOPE_IDS
                else "v0.10.1" if record["capability_id"] in V101_SCOPE_IDS
                else "v0.10.0" if record["capability_id"] in V10_SCOPE_IDS
                else "v0.9.0" if record["capability_id"] in V09_SCOPE_IDS
                else
                "v0.8.0" if record["capability_id"] in V08_RELEASE_SCOPE_IDS
                else "v0.7.0" if record["capability_id"] == "GRW-CAP-070-01"
                else "v0.6.0" if record["capability_id"] == "GRW-CAP-060-01"
                else "v0.5.0" if record["capability_id"] == "GRW-CAP-050-01"
                else "v0.4.0"
            )
            self.assertEqual(record["version"]["target_release"], expected_target)

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

        permitted_ids = {
            record["capability_id"]
            for record in self.records
            if record["public_claim_status"] == "permitted"
        }
        self.assertEqual(permitted_ids, RELEASED_OR_ADMITTED_IDS)

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

    def test_r4001_is_verified_and_admitted_for_future_release_scope(self) -> None:
        record = next(record for record in self.records if record["capability_id"] == "GRW-CAP-040-01")
        self.assertEqual(record["implementation_status"], "verified")
        self.assertEqual(record["release_disposition"], "admitted")
        self.assertEqual(record["public_claim_status"], "permitted")
        self.assertEqual(record["interface"]["status"], "present")
        self.assertEqual(record["evidence"]["status"], "verified")
        self.assertTrue(record["approval_reference"])

    def test_all_reviewed_r40_records_preserve_option_a_and_no_c4_authorization(self) -> None:
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
            if record["capability_id"] == "GRW-CAP-040-03":
                self.assertEqual(record["release_disposition"], "excluded")
                self.assertIn("Option A exclusion retained", record["approval_reference"])
            else:
                self.assertEqual(record["release_disposition"], "admitted")
                self.assertIn("Option A capability-set admission accepted", record["approval_reference"])

    def test_r4002_is_admitted_but_not_an_executor_or_tool_grant(self) -> None:
        record = next(record for record in self.records if record["capability_id"] == "GRW-CAP-040-02")
        self.assertEqual(record["implementation_status"], "verified")
        self.assertEqual(record["release_disposition"], "admitted")
        self.assertEqual(record["public_claim_status"], "permitted")
        self.assertEqual(record["interface"]["status"], "present")
        self.assertEqual(record["evidence"]["status"], "verified")
        self.assertIn("does not grant autonomy", record["non_promise"].lower())
        self.assertTrue(record["approval_reference"])

    def test_r4004_is_admitted_but_not_data_processing_or_compliance_claim(self) -> None:
        record = next(record for record in self.records if record["capability_id"] == "GRW-CAP-040-04")
        self.assertEqual(record["implementation_status"], "verified")
        self.assertEqual(record["release_disposition"], "admitted")
        self.assertEqual(record["public_claim_status"], "permitted")
        self.assertEqual(record["interface"]["status"], "present")
        self.assertEqual(record["evidence"]["status"], "verified")
        self.assertIn("will not access", record["non_promise"].lower())
        self.assertIn("does not access data", record["limitations_and_next_action"].lower())
        self.assertTrue(record["approval_reference"])

    def test_r4005_is_admitted_but_not_c4_or_release_claim(self) -> None:
        record = next(record for record in self.records if record["capability_id"] == "GRW-CAP-040-05")
        self.assertEqual(record["implementation_status"], "verified")
        self.assertEqual(record["release_disposition"], "admitted")
        self.assertEqual(record["public_claim_status"], "permitted")
        self.assertEqual(record["interface"]["status"], "present")
        self.assertEqual(record["evidence"]["status"], "verified")
        self.assertIn("not c4 authorization", record["limitations_and_next_action"].lower())
        self.assertTrue(record["approval_reference"])

    def test_r4006_is_admitted_but_remains_synthetic_assurance_only(self) -> None:
        record = next(record for record in self.records if record["capability_id"] == "GRW-CAP-040-06")
        self.assertEqual(record["implementation_status"], "verified")
        self.assertEqual(record["release_disposition"], "admitted")
        self.assertEqual(record["public_claim_status"], "permitted")
        self.assertEqual(record["interface"]["status"], "present")
        self.assertEqual(record["evidence"]["status"], "verified")
        self.assertIn("release-source synthetic assurance", record["limitations_and_next_action"].lower())
        self.assertTrue(record["approval_reference"])

    def test_r5001_is_verified_and_admitted_for_the_published_scope(self) -> None:
        record = next(record for record in self.records if record["capability_id"] == "GRW-CAP-050-01")
        self.assertEqual(record["implementation_status"], "verified")
        self.assertEqual(record["release_disposition"], "admitted")
        self.assertEqual(record["public_claim_status"], "permitted")
        self.assertEqual(record["evidence"]["status"], "verified")
        self.assertEqual(record["version"]["target_release"], "v0.5.0")
        self.assertIn("does not access", record["non_promise"].lower())
        self.assertIn("published v0.5.0", record["limitations_and_next_action"].lower())
        self.assertIn("not an installed-runtime claim", record["limitations_and_next_action"].lower())
        admission = V05_ADMISSION_RECORD_PATH.read_text(encoding="utf-8").lower()
        self.assertIn("historical pre-c4 admission record", admission)
        self.assertIn("admitted", admission)
        self.assertIn("published at immutable `v0.5.0`", admission)

    def test_r6001_is_admitted_for_release_source_scope_without_release_or_runtime_claim(self) -> None:
        record = next(record for record in self.records if record["capability_id"] == "GRW-CAP-060-01")
        self.assertEqual(record["implementation_status"], "verified")
        self.assertEqual(record["release_disposition"], "admitted")
        self.assertEqual(record["public_claim_status"], "permitted")
        self.assertEqual(record["version"]["target_release"], "v0.6.0")
        self.assertEqual(record["version"]["last_verified_release"], "v0.6.0")
        self.assertIn("read-only", record["promise"].lower())
        self.assertIn("does not open data", record["non_promise"].lower())
        self.assertIn("not an installation target", record["limitations_and_next_action"].lower())
        self.assertIn("not an installed-runtime claim", record["limitations_and_next_action"].lower())
        admission = V06_ADMISSION_RECORD_PATH.read_text(encoding="utf-8").lower()
        self.assertIn("accountable-human release-scope admission record", admission)
        self.assertIn("admitted `grw-cap-060-01`", admission)
        self.assertIn("does not authorize a push", admission)

    def test_r7001_scope_and_selected_version_status_remain_distinct(self) -> None:
        record = next(record for record in self.records if record["capability_id"] == "GRW-CAP-070-01")
        self.assertEqual(record["implementation_status"], "verified")
        self.assertEqual(record["release_disposition"], "admitted")
        self.assertEqual(record["public_claim_status"], "permitted")
        self.assertEqual(record["version"]["target_release"], "v0.7.0")
        self.assertEqual(record["version"]["last_verified_release"], "v0.7.0")
        self.assertIn("automatically promote", record["non_promise"].lower())
        self.assertIn("exact immutable tag and matching github release", record["limitations_and_next_action"].lower())

    def test_v08_published_scope_remains_distinct_from_release_or_runtime_identity(self) -> None:
        records = {record["capability_id"]: record for record in self.records}
        self.assertEqual(set(records).intersection(V08_RELEASE_SCOPE_IDS), V08_RELEASE_SCOPE_IDS)
        for capability_id in V08_RELEASE_SCOPE_IDS:
            record = records[capability_id]
            self.assertEqual(record["implementation_status"], "verified")
            self.assertEqual(record["release_disposition"], "admitted")
            self.assertEqual(record["public_claim_status"], "permitted")
            self.assertEqual(record["evidence"]["status"], "verified")
            self.assertEqual(record["version"]["target_release"], "v0.8.0")
            self.assertEqual(record["version"]["last_verified_release"], "v0.8.0")
            self.assertIn("pull-request #10", record["approval_reference"])
            self.assertIn("subsequent C4 publication completed", record["approval_reference"])
            self.assertIn("exact annotated tag and matching GitHub Release", record["approval_reference"])
            self.assertIn("hosted", record["limitations_and_next_action"].lower())
            self.assertIn("c4", record["limitations_and_next_action"].lower())

    def test_v09_scope_is_admitted_but_not_a_release_or_runtime_claim(self) -> None:
        records = {record["capability_id"]: record for record in self.records}
        self.assertEqual(set(records).intersection(V09_SCOPE_IDS), V09_SCOPE_IDS)
        for capability_id in V09_SCOPE_IDS:
            record = records[capability_id]
            self.assertEqual(record["implementation_status"], "verified")
            self.assertEqual(record["release_disposition"], "admitted")
            self.assertEqual(record["public_claim_status"], "permitted")
            self.assertEqual(record["evidence"]["status"], "verified")
            self.assertTrue(record["evidence"]["references"])
            self.assertEqual(record["version"]["target_release"], "v0.9.0")
            self.assertIsNone(record["version"]["last_verified_release"])
            self.assertIn("three-item v0.9.0 scope", record["approval_reference"].lower())
            self.assertIn("does not establish c3-remote evidence", record["limitations_and_next_action"].lower())

    def test_v101_scope_is_synthetic_and_does_not_claim_a_transfer_or_computer_b(self) -> None:
        record = next(record for record in self.records if record["capability_id"] == "GRW-CAP-101-01")
        self.assertEqual(record["implementation_status"], "verified")
        self.assertEqual(record["release_disposition"], "admitted")
        self.assertEqual(record["public_claim_status"], "permitted")
        self.assertEqual(record["version"]["target_release"], "v0.10.1")
        self.assertIn("does not create public or external-contributor intake", record["non_promise"].lower())
        self.assertIn("independent computer b", record["non_promise"].lower())
        self.assertIn("cannot establish a hosted tag", record["limitations_and_next_action"].lower())

    def test_v102_maintenance_direction_is_human_mediated_and_not_an_intake(self) -> None:
        readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8").lower()
        roadmap = (REPOSITORY_ROOT / "ROADMAP.md").read_text(encoding="utf-8").lower()
        skill = (REPOSITORY_ROOT / "SKILL.md").read_text(encoding="utf-8").lower()
        for text in (readme, roadmap, skill):
            self.assertIn("human-specified channel", text)
            self.assertIn("automatic promotion", text)
        self.assertIn("v0.11.0 source scope", self.ledger["target_claim_scope"])

    def test_v011_scope_is_template_and_experience_only(self) -> None:
        records = {record["capability_id"]: record for record in self.records}
        self.assertEqual(set(records).intersection(V011_SCOPE_IDS), V011_SCOPE_IDS)
        for capability_id in V011_SCOPE_IDS:
            record = records[capability_id]
            self.assertEqual(record["implementation_status"], "verified")
            self.assertEqual(record["release_disposition"], "admitted")
            self.assertEqual(record["public_claim_status"], "permitted")
            self.assertEqual(record["version"]["target_release"], "v0.11.0")
            self.assertIsNone(record["version"]["last_verified_release"])
            self.assertIn("C2 accepted", record["approval_reference"])
            self.assertIn("hosted tag", record["limitations_and_next_action"].lower())

        experience = records["GRW-CAP-110-06"]
        self.assertIn("38", experience["promise"])
        self.assertIn("not provide a Knowledge package", experience["non_promise"])
        self.assertIn("retrieval", experience["non_promise"])

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

    def test_published_v050_capability_does_not_claim_a_runtime_installation(self) -> None:
        text = LEDGER_PATH.read_text(encoding="utf-8")
        admission_record = ADMISSION_RECORD_PATH.read_text(encoding="utf-8").lower()
        self.assertIn("option a", admission_record)
        self.assertIn("historical pre-c4 admission record", admission_record)
        self.assertIn("not by itself a public release", EVIDENCE_MATRIX_PATH.read_text(encoding="utf-8").lower())
        skill = (REPOSITORY_ROOT / "SKILL.md").read_text(encoding="utf-8")
        readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("capability_truth_ledger.json", skill)
        self.assertIn("capability_truth_ledger.json", readme)
        combined = "\n".join((text, skill, readme)).lower()
        self.assertIn("published v0.5.0", combined)
        self.assertIn("does not prove", combined)
        self.assertNotIn("no tag or github release exists", combined)


if __name__ == "__main__":
    unittest.main()
