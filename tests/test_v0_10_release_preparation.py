"""Release-state and preparation checks for the bounded v0.10 source."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "system" / "11_distribution_installation_and_release"
LEDGER = ROOT / "system" / "00_manifest_and_profiles" / "v1_capability_truth_ledger.json"
SCHEMA = ROOT / "system" / "09_schemas_records_and_templates" / "voluntary_experience_package.schema.json"
PUBLIC_FILES = (
    "system/09_schemas_records_and_templates/voluntary_experience_package.schema.json",
    "assets/voluntary-experience-package.template.json",
    "references/voluntary-experience-package.md",
    "scripts/validate_voluntary_experience_package.py",
    "tests/fixtures/voluntary_experience_package/valid/experience-package.json",
)
V101_PUBLIC_FILES = (
    "system/09_schemas_records_and_templates/synthetic_experience_exchange_pilot_receipt.schema.json",
    "assets/synthetic-experience-exchange-pilot-receipt.template.json",
    "references/synthetic-experience-exchange-pilot.md",
    "scripts/validate_synthetic_experience_exchange_pilot.py",
    "tests/fixtures/synthetic_experience_exchange_pilot/valid/exchange-pilot-receipt.json",
)
FORBIDDEN_MARKERS = ("E:" + chr(92) + "Chen" + "haoran", "C:" + chr(92) + "Us" + "ers", "99" + "sai", "gh" + "p_", "github" + "_pat_", "BEGIN" + " PRIVATE" + " KEY")


class V010ReleasePreparationTests(unittest.TestCase):
    def test_v010_history_is_retained_while_later_source_moves_forward(self) -> None:
        manifest = (ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        index = (ROOT / "system" / "INDEX.md").read_text(encoding="utf-8")
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        current_surface = "\n".join((manifest, readme, roadmap, index, json.dumps(ledger))).lower()
        self.assertIn("system_version: 1.15.0", manifest)
        self.assertIn("Status: v1.1.0 versioned source scope", readme)
        self.assertIn("does not itself prove the\nrelease or installation identity", readme)
        self.assertIn("## v0.10.0 (voluntary metadata-only experience package)", roadmap)
        self.assertIn("## v0.10.1 (self-controlled synthetic experience-exchange pilot)", roadmap)
        self.assertIn("## v0.10.2 (human-mediated experience-curation maintenance source)", roadmap)
        self.assertIn("Status: v1.15.0 joint-review-profile source", index)
        self.assertEqual(ledger["release_context"]["source_release_version"], "v1.0.0")
        self.assertEqual(ledger["release_context"]["historical_public_baseline"], "v0.13.0")
        self.assertIn("human-specified channel", readme.lower())
        self.assertIn("no user-facing intake", roadmap.lower())
        self.assertIn("## v0.11.0 (manuscript-governance and public-experience source)", roadmap)
        self.assertIn("## v0.12.0 (synthetic integration-assurance maintenance source)", roadmap)
        self.assertNotIn("voluntary-experience-package candidate", current_surface)
        self.assertNotIn("v0.10.1 is published", current_surface)

    def test_v0102_is_maintenance_only_with_no_new_capability_admission(self) -> None:
        contract = (RELEASE / "V0_10_2_HUMAN_MEDIATED_EXPERIENCE_CURATION_MAINTENANCE.md").read_text(encoding="utf-8").lower()
        rights = (RELEASE / "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.10.2.md").read_text(encoding="utf-8").lower()
        dependency = (RELEASE / "V0_10_2_DEPENDENCY_AND_WORKFLOW_REVIEW.md").read_text(encoding="utf-8").lower()
        evidence = (RELEASE / "V0_10_2_RELEASE_EVIDENCE.md").read_text(encoding="utf-8").lower()
        notes = (RELEASE / "RELEASE_NOTES_v0.10.2.md").read_text(encoding="utf-8").lower()
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

        self.assertIn("zero-new-capability maintenance source", contract)
        self.assertIn("no `grw-cap-*` item is", contract)
        self.assertIn("no contributor submission", rights)
        self.assertIn("new dependency or lockfile | none", dependency)
        self.assertIn("new admitted capability identifiers | none", evidence)
        self.assertIn("does not add external contributor support", notes)
        self.assertFalse(any(item["version"]["target_release"] == "v0.10.2" for item in ledger["capabilities"]))

    def test_capability_admission_is_single_and_not_c4(self) -> None:
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        record = next(item for item in ledger["capabilities"] if item["capability_id"] == "GRW-CAP-100-01")
        self.assertEqual(record["implementation_status"], "verified")
        self.assertEqual(record["release_disposition"], "admitted")
        self.assertEqual(record["version"]["target_release"], "v0.10.0")
        self.assertIsNone(record["version"]["last_verified_release"])
        self.assertIn("does not collect", record["non_promise"].lower())
        admission = " ".join((RELEASE / "V0_10_CAPABILITY_ADMISSION.md").read_text(encoding="utf-8").lower().split())
        self.assertIn("historical accountable-human c2 scope-admission snapshot", admission)
        self.assertIn("not c3-remote evidence", admission)
        self.assertIn("does not prove a hosted release", admission)

    def test_release_control_is_valid_and_records_only_c3_remote_identity(self) -> None:
        schema = json.loads((RELEASE / "release_control_record.schema.json").read_text(encoding="utf-8"))
        record = json.loads((RELEASE / "V0_10_RELEASE_CONTROL_CANDIDATE.json").read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))
        self.assertEqual(record["candidate_identity"]["exact_commit"], "3edf684a94ab8becc958ea451e3b1f1e5a565990")
        self.assertEqual(record["candidate_identity"]["branch_state"], "remote_candidate_branch")
        self.assertIsNone(record["c4_release_authorization_reference"])

    def test_local_evidence_is_bound_to_the_reviewed_implementation_not_a_release(self) -> None:
        evidence = (ROOT / "system" / "10_assurance_evaluation_and_audit" / "V0_10_CANDIDATE_EVIDENCE_MAP.md").read_text(encoding="utf-8")
        release_evidence = (RELEASE / "V0_10_RELEASE_EVIDENCE.md").read_text(encoding="utf-8")
        dependency_review = (RELEASE / "V0_10_DEPENDENCY_AND_WORKFLOW_REVIEW.md").read_text(encoding="utf-8")
        self.assertIn("c3095d0bab9da8ddf3ae8c86dc93b9cc28fa2d5c", evidence)
        self.assertIn("203", evidence)
        self.assertIn("204", evidence)
        self.assertIn("29738250097", evidence)
        self.assertIn("historical c3-remote candidate", release_evidence.lower())
        self.assertIn("29738250097", dependency_review)
        self.assertNotIn("ci must be repeated after c3-remote push", dependency_review.lower())

    def test_current_notes_are_time_neutral_and_pre_c4_records_are_historical(self) -> None:
        release_notes = (RELEASE / "RELEASE_NOTES_v0.10.0.md").read_text(encoding="utf-8").lower()
        gate = (RELEASE / "V0_10_RELEASE_GATE.md").read_text(encoding="utf-8").lower()
        rights_review = (RELEASE / "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.10.0.md").read_text(encoding="utf-8").lower()
        current_status = (RELEASE / "CURRENT_RELEASE_STATUS.md").read_text(encoding="utf-8").lower()
        module_paths = (
            "system/06_memory_and_learning/MODULE.md",
            "system/07_tools_and_integrations/MODULE.md",
            "system/09_schemas_records_and_templates/MODULE.md",
            "system/10_assurance_evaluation_and_audit/MODULE.md",
            "system/12_synthetic_examples/MODULE.md",
        )
        module_text = "\n".join((ROOT / path).read_text(encoding="utf-8").lower() for path in module_paths)
        release_control = json.loads((RELEASE / "V0_10_RELEASE_CONTROL_CANDIDATE.json").read_text(encoding="utf-8"))
        self.assertNotIn("release notes candidate", release_notes)
        self.assertIn("versioned release-source notes", release_notes)
        self.assertIn("historical pre-c4 candidate gate", gate)
        self.assertIn("historical local candidate material-review snapshot", rights_review)
        self.assertIn("v0.10 release-source scope", current_status)
        self.assertIn("v0_10_release_control_candidate.json", current_status)
        self.assertNotIn("the v0.10 candidate", module_text)
        self.assertIn("historical pre-c4 c3-remote candidate", release_control["candidate_identity"]["intended_github_release"].lower())
        self.assertIn("historical pre-c4 record", release_control["residual_risks"][-1].lower())

    def test_public_surface_is_generic_and_validator_has_no_network_or_write_executor(self) -> None:
        for relative in PUBLIC_FILES:
            content = (ROOT / relative).read_text(encoding="utf-8")
            for marker in FORBIDDEN_MARKERS:
                self.assertNotIn(marker, content, f"{relative} contains {marker!r}")
        validator = (ROOT / "scripts" / "validate_voluntary_experience_package.py").read_text(encoding="utf-8")
        for forbidden in ("requests", "urllib", "http.client", "subprocess", "os.walk", "rglob", "write_text", "write_bytes", "unlink", "mkdir"):
            self.assertNotIn(forbidden, validator)
        reference = " ".join((ROOT / "references" / "voluntary-experience-package.md").read_text(encoding="utf-8").lower().split())
        self.assertIn("outside its view", reference)
        self.assertIn("not a computer b test", reference)

    def test_schema_has_no_identity_or_attachment_property(self) -> None:
        schema_text = SCHEMA.read_text(encoding="utf-8")
        for forbidden in ('"email"', '"account"', '"attachment"', '"raw_transcript"', '"project_identifier"'):
            self.assertNotIn(forbidden, schema_text)

    def test_v101_public_surface_is_synthetic_only_and_has_no_network_or_writer(self) -> None:
        for relative in V101_PUBLIC_FILES:
            content = (ROOT / relative).read_text(encoding="utf-8")
            for marker in FORBIDDEN_MARKERS:
                self.assertNotIn(marker, content, f"{relative} contains {marker!r}")
        validator = (ROOT / "scripts" / "validate_synthetic_experience_exchange_pilot.py").read_text(encoding="utf-8")
        for forbidden in ("requests", "urllib", "http.client", "subprocess", "os.walk", "rglob", "write_text", "write_bytes", "unlink", "mkdir"):
            self.assertNotIn(forbidden, validator)
        reference = " ".join((ROOT / "references" / "synthetic-experience-exchange-pilot.md").read_text(encoding="utf-8").lower().split())
        self.assertIn("do not call it computer b evidence", reference)
        self.assertIn("external contributor intake", reference)


if __name__ == "__main__":
    unittest.main()
