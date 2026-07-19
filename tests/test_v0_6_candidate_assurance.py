"""Historical assurance checks for the released v0.6 capability scope."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = REPOSITORY_ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"
MANIFEST_PATH = REPOSITORY_ROOT / "SYSTEM_MANIFEST.yaml"
README_PATH = REPOSITORY_ROOT / "README.md"
ROADMAP_PATH = REPOSITORY_ROOT / "ROADMAP.md"
SKILL_PATH = REPOSITORY_ROOT / "SKILL.md"
FRAMEWORK_PLAN_PATH = REPOSITORY_ROOT / "system" / "00_manifest_and_profiles" / "FRAMEWORK_INTEGRATION_PLAN.md"
WORKFLOW_PATH = REPOSITORY_ROOT / ".github" / "workflows" / "test-bootstrap.yml"
EVIDENCE_MAP_PATH = REPOSITORY_ROOT / "system" / "10_assurance_evaluation_and_audit" / "V0_6_CANDIDATE_EVIDENCE_MAP.md"
RELEASE_ROOT = REPOSITORY_ROOT / "system" / "11_distribution_installation_and_release"
SYNTHETIC_ASSURANCE_PATH = REPOSITORY_ROOT / "system" / "12_synthetic_examples" / "V0_6_SYNTHETIC_ASSURANCE.md"


class V06CandidateAssuranceTests(unittest.TestCase):
    def test_v08_source_retains_the_historical_v06_capability_scope(self) -> None:
        manifest = MANIFEST_PATH.read_text(encoding="utf-8")
        readme = README_PATH.read_text(encoding="utf-8")
        roadmap = ROADMAP_PATH.read_text(encoding="utf-8")
        self.assertIn("system_version: 0.8.0-portability-role-helper-admission-candidate-source", manifest)
        self.assertIn("Status: v0.8 candidate source", readme)
        self.assertIn("retaining the released v0.4-v0.7 control scopes", " ".join(readme.split()))
        self.assertIn("## v0.8.0 (candidate portability, role-contract, and helper-admission source)", roadmap)
        self.assertIn("## v0.7.1 (release-state and control-hardening maintenance source)", roadmap)
        self.assertIn("## v0.7.0 (historical human-reviewed lesson-promotion release source)", roadmap)
        self.assertIn("## v0.6.0 (workflow/evidence-control release source)", roadmap)
        self.assertIn("## v0.5.1 (published release-state maintenance)", roadmap)

    def test_release_source_scope_is_admitted_but_not_an_installation_claim(self) -> None:
        ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        record = next(record for record in ledger["capabilities"] if record["capability_id"] == "GRW-CAP-060-01")
        self.assertEqual(record["implementation_status"], "verified")
        self.assertEqual(record["release_disposition"], "admitted")
        self.assertEqual(record["public_claim_status"], "permitted")
        self.assertEqual(record["version"]["target_release"], "v0.6.0")
        self.assertEqual(record["version"]["last_verified_release"], "v0.6.0")
        self.assertIn("not an installation target", record["limitations_and_next_action"].lower())
        self.assertIn("installed-runtime claim", record["limitations_and_next_action"].lower())
        evidence_map = EVIDENCE_MAP_PATH.read_text(encoding="utf-8").lower()
        self.assertIn("verified and admitted", evidence_map)
        normalized_evidence_map = " ".join(EVIDENCE_MAP_PATH.read_text(encoding="utf-8").lower().split())
        self.assertIn("neither this map nor any source file establishes public availability", normalized_evidence_map)
        self.assertIn("not the canonical capability", EVIDENCE_MAP_PATH.read_text(encoding="utf-8").replace("\n", " "))

    def test_release_source_interfaces_are_present_and_metadata_only(self) -> None:
        required_paths = (
            "system/09_schemas_records_and_templates/workflow_evidence_control_bundle.schema.json",
            "system/09_schemas_records_and_templates/workflow_evidence_control_baseline.schema.json",
            "assets/workflow-evidence-control-bundle.template.json",
            "assets/workflow-evidence-control-baseline.template.json",
            "scripts/validate_workflow_evidence_control_bundle.py",
            "references/workflow-evidence-control-records.md",
            "tests/test_workflow_evidence_control_bundle.py",
            "system/12_synthetic_examples/V0_6_SYNTHETIC_ASSURANCE.md",
        )
        for relative_path in required_paths:
            self.assertTrue((REPOSITORY_ROOT / relative_path).is_file(), relative_path)
        reference = (REPOSITORY_ROOT / "references" / "workflow-evidence-control-records.md").read_text(encoding="utf-8").lower()
        self.assertIn("metadata-only", reference)
        self.assertIn("does not", reference)

    def test_release_and_runtime_boundaries_remain_separate(self) -> None:
        source_records = (
            "V0_6_RELEASE_GATE.md",
            "V0_6_RELEASE_EVIDENCE.md",
            "V0_6_CAPABILITY_ADMISSION.md",
            "PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.6.0.md",
            "RELEASE_NOTES_v0.6.0.md",
        )
        source_text = "\n".join((RELEASE_ROOT / name).read_text(encoding="utf-8") for name in source_records).lower()
        normalized_source_text = " ".join(source_text.split())
        self.assertIn("does not itself establish publication", normalized_source_text)
        self.assertIn("not a public-release claim", source_text)
        self.assertIn("not authorize", source_text)
        self.assertIn("runtime-installation", source_text)

    def test_current_framework_validation_target_is_v012_and_historical_v04_evidence_is_not_rewritten(self) -> None:
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
        plan = FRAMEWORK_PLAN_PATH.read_text(encoding="utf-8")
        historical_v04 = (REPOSITORY_ROOT / "system" / "12_synthetic_examples" / "V0_4_SYNTHETIC_ASSURANCE.md").read_text(encoding="utf-8")
        self.assertIn("FRAMEWORK_RELEASE_TAG: v0.1.2", workflow)
        self.assertIn("FRAMEWORK_EXPECTED_COMMIT: 97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8", workflow)
        self.assertIn("Workspace Framework `v0.1.2`", plan)
        self.assertIn("framework tag: `v0.1.1`", historical_v04)

    def test_v06_release_source_assurance_remains_a_frozen_historical_snapshot(self) -> None:
        assurance = SYNTHETIC_ASSURANCE_PATH.read_text(encoding="utf-8")
        match = re.search(r"source snapshot SHA-256: `([0-9a-f]{64})`", assurance)
        self.assertIsNotNone(match)
        self.assertEqual(len(match.group(1)), 64)
        self.assertIn("This assurance file is excluded from its own digest", " ".join(assurance.split()))
        self.assertNotIn("v0.7.0", assurance)

    def test_release_source_surfaces_have_no_private_path_or_release_claim(self) -> None:
        source_paths = (
            README_PATH,
            ROADMAP_PATH,
            SKILL_PATH,
            EVIDENCE_MAP_PATH,
            REPOSITORY_ROOT / "references" / "workflow-evidence-control-records.md",
            REPOSITORY_ROOT / "system" / "12_synthetic_examples" / "V0_6_SYNTHETIC_ASSURANCE.md",
        )
        source_text = "\n".join(path.read_text(encoding="utf-8") for path in source_paths)
        self.assertIsNone(re.search(r"(?i)(?:[a-z]:\\|/(?:home|users)/)", source_text))
        self.assertNotIn("v0.6.0 is published", source_text.lower())
        self.assertNotIn("v0.6.0 provides an agent runtime", source_text.lower())

    def test_current_source_docs_do_not_make_dynamic_public_version_claims(self) -> None:
        current_paths = (
            README_PATH,
            ROADMAP_PATH,
            SKILL_PATH,
            MANIFEST_PATH,
            REPOSITORY_ROOT / "system" / "INDEX.md",
            RELEASE_ROOT / "CURRENT_RELEASE_STATUS.md",
            RELEASE_ROOT / "RELEASE_CONTROL.md",
            RELEASE_ROOT / "MODULE.md",
            RELEASE_ROOT / "V0_6_1_RELEASE_STATE_MAINTENANCE.md",
            RELEASE_ROOT / "RELEASE_NOTES_v0.6.1.md",
        )
        source_text = "\n".join(path.read_text(encoding="utf-8").lower() for path in current_paths)
        for prohibited in (
            "current published patch is",
            "current published version is",
            "current public baseline is",
            "current stable release is",
            "current release is",
            "currently published version is",
            "latest published tag is",
            "latest published version is",
            "latest release is",
        ):
            self.assertNotIn(prohibited, source_text)
        self.assertIn("does not declare a current published version", ROADMAP_PATH.read_text(encoding="utf-8"))
        release_control = (RELEASE_ROOT / "RELEASE_CONTROL.md").read_text(encoding="utf-8")
        self.assertIn("Current-State Assertion Control", release_control)
        self.assertIn("Candidate Snapshot Completeness", release_control)
        self.assertIn("git ls-files", release_control)


if __name__ == "__main__":
    unittest.main()
