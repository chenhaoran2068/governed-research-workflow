"""Regression checks for the v1.14 Results-first manuscript guidance."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
GUIDANCE_PATH = ROOT / "references" / "manuscript-and-submission-control.md"
PROHIBITED_PATTERNS = (
    r"(?i)[a-z]:\\",
    r"(?i)researchx_",
    r"(?i)src-[a-z0-9]",
    r"(?i)xvt-[0-9]",
    r"(?i)m[0-9]{2}",
)


class V114ManuscriptWorkSequenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.guidance = GUIDANCE_PATH.read_text(encoding="utf-8")
        cls.lower_guidance = cls.guidance.lower()

    def test_default_work_order_is_results_first(self) -> None:
        expected = (
            "1. Results;",
            "2. Methods;",
            "3. Discussion and Conclusion;",
            "4. Introduction;",
            "5. Abstract or Summary;",
            "6. declarations, supplements, cover letter, response material, and the",
        )
        positions = [self.guidance.index(item) for item in expected]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("not a required final manuscript layout", self.lower_guidance)

    def test_results_review_moves_from_structure_to_evidence_and_back(self) -> None:
        expected = (
            "Results-section purpose;",
            "subsection order;",
            "paragraph function;",
            "factual sentence and claim;",
            "result artifact and matching table or figure;",
            "sentence-to-display and claim-to-evidence alignment;",
            "paragraph, display, and subsection coherence;",
            "whole-Results coherence;",
            "whole-manuscript claim consistency.",
        )
        positions = [self.guidance.index(item) for item in expected]
        self.assertEqual(positions, sorted(positions))

    def test_results_assembly_modes_preserve_completion_boundary(self) -> None:
        for expected in ("display-first", "parallel", "provisional prose"):
            self.assertIn(expected, self.lower_guidance)
        self.assertIn("This is the default", self.guidance)
        self.assertIn("completed evidence cycle", self.lower_guidance)
        self.assertIn("not ready to support", self.lower_guidance)

    def test_guidance_allows_documented_exceptions_without_weakening_evidence(self) -> None:
        self.assertIn("### Exceptions", self.guidance)
        self.assertIn("why an exception is needed", self.lower_guidance)
        self.assertIn("No exception permits changing result truth", self.guidance)
        self.assertIn("pre-specified confirmation", self.lower_guidance)

    def test_guidance_is_generic_and_does_not_claim_execution_or_authority(self) -> None:
        for expected in (
            "write a manuscript",
            "read project material",
            "establish a result or claim",
            "approve a package",
            "submit material",
        ):
            self.assertIn(expected, self.lower_guidance)
        self.assertRegex(self.lower_guidance, r"does not\s+write a manuscript")
        for pattern in PROHIBITED_PATTERNS:
            self.assertIsNone(re.search(pattern, self.guidance), pattern)


if __name__ == "__main__":
    unittest.main()
