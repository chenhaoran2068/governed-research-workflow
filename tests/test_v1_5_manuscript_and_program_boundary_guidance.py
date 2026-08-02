"""Regression checks for generic v1.5 manuscript and boundary guidance."""

from pathlib import Path
import re
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_ROOT = REPOSITORY_ROOT / "system" / "03_workflows"
MANUSCRIPT_PATH = WORKFLOW_ROOT / "MANUSCRIPT_OPERATIONAL_CHECKLISTS.md"
BOUNDARY_PATH = WORKFLOW_ROOT / "RESEARCH_PROGRAM_BOUNDARY_AND_SHARED_MATERIALS_CONTROL.md"
PROHIBITED_PATTERNS = (
    r"(?i)[a-z]:\\",
    r"(?i)four_layer_ocedm",
    r"(?i)researchx_",
    r"(?i)papers/",
    r"(?i)src-[a-z0-9]",
    r"(?i)xvt-[0-9]",
    r"(?i)m[0-9]{2}",
)


class V15ManuscriptAndProgramBoundaryGuidanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manuscript = MANUSCRIPT_PATH.read_text(encoding="utf-8")
        cls.boundary = BOUNDARY_PATH.read_text(encoding="utf-8")
        cls.combined = "\n".join((cls.manuscript, cls.boundary))

    def test_documents_are_generic_human_review_guidance(self) -> None:
        self.assertIn("requirement uncertainty", self.manuscript.lower())
        self.assertIn("section, display, and paragraph boundaries", self.manuscript.lower())
        self.assertIn("claim, evidence, and citation visibility", self.manuscript.lower())
        self.assertIn("revision and response traceability", self.manuscript.lower())
        self.assertIn("declarations and ai-use facts", self.manuscript.lower())
        self.assertIn("human review boundary", self.manuscript.lower())
        self.assertIn("default isolation", self.boundary.lower())
        self.assertIn("human-reviewed grouping", self.boundary.lower())
        self.assertIn("limited stable shared material", self.boundary.lower())
        self.assertIn("narrow explicit references", self.boundary.lower())

    def test_documents_refuse_authority_access_and_submission_inference(self) -> None:
        text = self.combined.lower()
        for expected in (
            "does not write a manuscript",
            "does not prove",
            "does not merge work units",
            "grant access",
            "never permission to read",
            "does not automatically promote",
        ):
            self.assertIn(expected, text)

    def test_documents_contain_no_private_or_historical_identifiers(self) -> None:
        for pattern in PROHIBITED_PATTERNS:
            self.assertIsNone(re.search(pattern, self.combined), pattern)

    def test_documents_do_not_create_an_executable_surface(self) -> None:
        for pattern in (
            r"(?i)\bpython\b",
            r"(?i)\bjsonschema\b",
            r"(?i)\bvalidator\b",
            r"(?i)\bhelper\b",
            r"(?i)\bagent runtime\b",
            r"(?i)\bexecutable script\b",
            r"(?i)\bscripts/",
            r"(?i)\.py\b",
        ):
            self.assertIsNone(re.search(pattern, self.combined), pattern)


if __name__ == "__main__":
    unittest.main()
