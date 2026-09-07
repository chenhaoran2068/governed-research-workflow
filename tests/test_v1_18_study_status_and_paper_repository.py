"""Release-facing checks for the bounded v1.18 source additions."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "system" / "11_distribution_installation_and_release"
SCHEMAS = ROOT / "system" / "09_schemas_records_and_templates"
PAPER_ASSETS = ROOT / "assets" / "paper-repository"


class V118StudyStatusAndPaperRepositoryTests(unittest.TestCase):
    def test_source_identity_and_capability_admission_are_explicit(self) -> None:
        manifest = (ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8")
        ledger = json.loads(
            (ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json").read_text(encoding="utf-8")
        )
        records = {item["capability_id"]: item for item in ledger["capabilities"]}

        self.assertIn("system_version: 1.18.1", manifest)
        self.assertEqual(ledger["release_context"]["historical_public_baseline"], "v1.18.0")
        for capability_id in ("GRW-CAP-250-01", "GRW-CAP-260-01"):
            self.assertEqual(records[capability_id]["release_disposition"], "admitted")
            self.assertEqual(records[capability_id]["version"]["target_release"], "v1.18.0")

    def test_release_control_names_scope_and_stays_unreleased(self) -> None:
        record = json.loads((RELEASE / "V1_18_RELEASE_CONTROL_CANDIDATE.json").read_text(encoding="utf-8"))
        self.assertEqual(record["status"], "source_prepared_not_released")
        self.assertEqual(record["release_version"], "v1.18.0")
        self.assertEqual(record["capability_ids"], ["GRW-CAP-250-01", "GRW-CAP-260-01"])
        self.assertIn("annotated_tag", record["required_before_release"])
        self.assertIn("matching_github_release", record["required_before_release"])

    def test_required_public_surfaces_and_templates_exist(self) -> None:
        paths = (
            ROOT / "assets" / "study-lifecycle-stage-catalog.v1.json",
            ROOT / "assets" / "study-status-snapshot.template.json",
            ROOT / "references" / "study-status-snapshot-contract.md",
            ROOT / "references" / "paper-repository-standard.md",
            SCHEMAS / "study_status_snapshot.schema.json",
            SCHEMAS / "paper_repository_release_manifest.schema.json",
            SCHEMAS / "paper_repository_public_export_scope.schema.json",
            PAPER_ASSETS / "paper-repository-release-manifest.template.json",
            PAPER_ASSETS / "public-export-scope.template.json",
            RELEASE / "GRW_CAP_250_01_PUBLIC_CAPABILITY_ADMISSION.md",
            RELEASE / "GRW_CAP_260_01_PUBLIC_CAPABILITY_ADMISSION.md",
            RELEASE / "RELEASE_NOTES_v1.18.0.md",
        )
        for path in paths:
            self.assertTrue(path.is_file(), str(path.relative_to(ROOT)))
        for path in paths:
            if path.suffix == ".json":
                json.loads(path.read_text(encoding="utf-8"))

    def test_paper_standard_declares_profiles_gates_and_non_authority(self) -> None:
        standard = (ROOT / "references" / "paper-repository-standard.md").read_text(encoding="utf-8")
        for profile in (
            "code_with_synthetic_demo",
            "code_with_redistributable_data",
            "code_with_access_instructions",
            "materials_only",
        ):
            self.assertIn(profile, standard)
        for gate in ("Gate A: Scope And Rights", "Gate B: Clean Candidate", "Gate C: Reproducibility", "Gate D: Independent Review", "Gate E: Release And Citation"):
            self.assertIn(gate, standard)
        self.assertIn("automated scanning is treated as supporting evidence, not proof", standard)
        self.assertIn("does not authorize", standard)

    def test_public_additions_exclude_private_project_material(self) -> None:
        roots = (
            ROOT / "assets" / "paper-repository",
            ROOT / "references" / "paper-repository-standard.md",
            ROOT / "references" / "study-status-snapshot-contract.md",
            ROOT / "scripts" / "build_paper_repository_candidate.py",
            ROOT / "scripts" / "validate_paper_repository_candidate.py",
        )
        files = []
        for root in roots:
            files.extend(root.rglob("*") if root.is_dir() else [root])
        content = "\n".join(path.read_text(encoding="utf-8") for path in files if path.is_file())
        self.assertIsNone(re.search(r"(?i)[a-z]:\\", content))
        self.assertNotIn("PaCO2", content)
        self.assertNotIn("Research1_", content)
        self.assertNotIn("BEGIN PRIVATE KEY", content)

    def test_tools_have_no_git_or_network_execution(self) -> None:
        sources = "\n".join(
            (ROOT / "scripts" / name).read_text(encoding="utf-8")
            for name in (
                "build_paper_repository_candidate.py",
                "paper_repository_release_common.py",
                "validate_paper_repository_candidate.py",
            )
        )
        for prohibited in ("subprocess", "requests", "urllib", "socket", "git push", "gh release"):
            self.assertNotIn(prohibited, sources)


if __name__ == "__main__":
    unittest.main()
