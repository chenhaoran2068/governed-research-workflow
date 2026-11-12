"""Structural checks for the v1.21.1 new Study-root naming reference."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "references" / "study-root-naming.md"
SKILL = ROOT / "SKILL.md"
LEDGER = ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"


class V1211StudyRootNamingTests(unittest.TestCase):
    def test_reference_defines_only_the_new_root_convention(self) -> None:
        content = REFERENCE.read_text(encoding="utf-8")
        self.assertIn("Research<number>-<lowercase-hyphenated-slug>", content)
        self.assertIn("uppercase `R`", content)
        self.assertIn("study_id", content)
        self.assertIn("study_title", content)
        self.assertIn("research_program_id", content)

    def test_reference_refuses_automatic_workspace_operations(self) -> None:
        content = REFERENCE.read_text(encoding="utf-8").lower()
        for phrase in (
            "does not choose a number",
            "create a folder",
            "rename or move an existing folder",
            "do not rename them",
            "do not scan a directory",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_entrypoint_and_ledger_expose_the_bounded_reference(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        self.assertIn("references/study-root-naming.md", skill)
        self.assertIn("Do not choose a number, inspect folders", skill)

        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        capability = next(
            item for item in ledger["capabilities"] if item["capability_id"] == "GRW-CAP-190-01"
        )
        self.assertIn("references/study-root-naming.md", capability["interface"]["paths"])
        self.assertIn("new-study-root-naming-convention", capability["interface"]["identifiers"])
        self.assertIn("references/study-root-naming.md", capability["claim_surfaces"])

    def test_public_reference_has_no_private_workspace_markers(self) -> None:
        content = REFERENCE.read_text(encoding="utf-8").lower()
        for marker in ("e:\\", "c:\\", "paco2", "crs_dev", "99sai"):
            with self.subTest(marker=marker):
                self.assertNotIn(marker, content)


if __name__ == "__main__":
    unittest.main()
