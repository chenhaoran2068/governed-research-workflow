"""Regression checks for the v1.19 Research Program registry guidance."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOUNDARY = ROOT / "system" / "03_workflows" / "RESEARCH_PROGRAM_BOUNDARY_AND_SHARED_MATERIALS_CONTROL.md"
RELEASE = ROOT / "system" / "11_distribution_installation_and_release"


class V119ResearchProgramRegistryTests(unittest.TestCase):
    def test_candidate_declares_exact_framework_contract_without_new_automation(self) -> None:
        manifest = (ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8")
        self.assertIn("system_version: 1.19.0", manifest)
        self.assertIn('supported_framework_versions: "0.5.0"', manifest)
        self.assertIn("neither moves Study roots", manifest)
        self.assertIn("no automation, data access, or authority transfer", manifest)

    def test_program_index_guidance_preserves_study_isolation_and_no_discovery(self) -> None:
        text = BOUNDARY.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "Research Program Index",
            "Registry/Research_Programs/<research-program-id>",
            "not a parent directory for member Studies",
            "does not scan a workspace or discover related Studies",
            "does not merge Studies",
            "does not transfer ethics",
            "does not grant access",
            "shared_material_references",
        ):
            self.assertIn(required, normalized)
        for forbidden in ("E:\\", "C:\\Users", "Research15", "Research16", "Research17"):
            self.assertNotIn(forbidden, text)

    def test_candidate_release_records_are_present_and_generic(self) -> None:
        paths = (
            RELEASE / "V1_19_RELEASE_GATE.md",
            RELEASE / "RELEASE_NOTES_v1.19.0.md",
            RELEASE / "PUBLIC_MATERIAL_RIGHTS_REVIEW_v1.19.0.md",
        )
        for path in paths:
            text = path.read_text(encoding="utf-8")
            self.assertTrue(path.is_file(), path.name)
            self.assertNotIn("E:\\", text)
            self.assertNotIn("Research15", text)


if __name__ == "__main__":
    unittest.main()
