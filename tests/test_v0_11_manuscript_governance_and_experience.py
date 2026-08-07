"""Regression checks for the bounded v0.11 manuscript-governance source scope."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIRECTORY = REPOSITORY_ROOT / "assets" / "manuscript-governance"
EXPERIENCE_COLLECTION = (
    REPOSITORY_ROOT
    / "system"
    / "06_memory_and_learning"
    / "knowledge_governance_experience_collection"
    / "README.md"
)
EXPERIENCE_REFERENCE = REPOSITORY_ROOT / "references" / "knowledge-governance-experience-collection.md"
MANUSCRIPT_REFERENCE = REPOSITORY_ROOT / "references" / "manuscript-governance-templates.md"
SYNTHETIC_EXAMPLE = REPOSITORY_ROOT / "system" / "12_synthetic_examples" / "V0_11_SYNTHETIC_MANUSCRIPT_GOVERNANCE_EXAMPLE.md"
LEDGER_PATH = REPOSITORY_ROOT / "system" / "00_manifest_and_profiles" / "v1_capability_truth_ledger.json"

TEMPLATES = {
    "manuscript-assembly-claim-display-review.template.md": "does not establish a scientific fact",
    "reviewer-response-revision-trace.template.md": "does not decide whether a response is adequate",
    "declaration-ai-use-fact-boundary.template.md": "does not determine authorship",
    "submission-route-package-provenance.template.md": "does not verify a portal",
    "decision-ready-human-review-packet.template.md": "does not grant authority",
}

FORBIDDEN_COLLECTION_MARKERS = (
    "e:\\",
    "c:\\",
    "99sai",
    "research1",
    "research2",
    "crs_dev",
    "sepsis",
    "paco2",
    "prisma",
    "strobe",
    "equator",
    "sha256",
    "receipt",
    "run trace",
)


class V011ManuscriptGovernanceAndExperienceTests(unittest.TestCase):
    def test_five_blank_templates_have_required_human_boundaries(self) -> None:
        self.assertEqual(
            {path.name for path in TEMPLATE_DIRECTORY.glob("*.template.md")},
            set(TEMPLATES),
        )
        for name, refusal in TEMPLATES.items():
            text = (TEMPLATE_DIRECTORY / name).read_text(encoding="utf-8").lower()
            self.assertIn("blank generic template", text)
            self.assertIn("accountable human", text)
            self.assertIn(refusal, text)
            self.assertIn("unknown", text)

    def test_experience_collection_is_a_legacy_entrypoint_after_v16_supersession(self) -> None:
        text = EXPERIENCE_COLLECTION.read_text(encoding="utf-8")
        self.assertIn("Historical KGE Public Collection Entry Point", text)
        self.assertIn("KGE-001` through `KGE-038", text)
        self.assertIn("public-safe-shared-experience-derivatives.md", text)
        self.assertNotIn("| KGE-001", text)

    def test_legacy_entrypoint_preserves_non_authority_boundary(self) -> None:
        text = EXPERIENCE_COLLECTION.read_text(encoding="utf-8").lower()
        self.assertIn("not a\nknowledge content package", text)
        self.assertIn("not a\nknowledge content package, source library", text)
        self.assertIn("current-source\nchecker, approval, promotion mechanism", text)
        self.assertIn("older immutable\nreleases", text)

    def test_references_and_synthetic_example_preserve_the_non_authority_boundary(self) -> None:
        experience_reference = EXPERIENCE_REFERENCE.read_text(encoding="utf-8").lower()
        manuscript_reference = MANUSCRIPT_REFERENCE.read_text(encoding="utf-8").lower()
        synthetic_example = SYNTHETIC_EXAMPLE.read_text(encoding="utf-8").lower()
        self.assertIn("historical public identifiers", experience_reference)
        self.assertIn("public-safe-shared-experience-derivatives.md", experience_reference)
        self.assertIn("current official sources", manuscript_reference)
        self.assertIn("not a scientific conclusion", manuscript_reference)
        self.assertIn("synthetic-only illustration", synthetic_example)
        self.assertIn("not a manuscript", synthetic_example)
        self.assertIn("pending", synthetic_example)

    def test_v011_content_is_retained_by_the_later_v013_source(self) -> None:
        manifest = (REPOSITORY_ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8")
        readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        roadmap = (REPOSITORY_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        self.assertIn("system_version: 1.8.0", manifest)
        self.assertIn("Status: v1.1.0 versioned source scope", readme)
        self.assertIn("does not itself prove the\nrelease or installation identity", readme)
        self.assertIn("## v0.11.0", roadmap)
        self.assertEqual(ledger["ledger_schema_version"], "1.6.0")
        self.assertEqual(ledger["release_context"]["source_release_version"], "v1.0.0")
        capability_ids = {record["capability_id"] for record in ledger["capabilities"]}
        self.assertEqual(
            {f"GRW-CAP-110-{number:02d}" for number in range(1, 7)}.intersection(capability_ids),
            {f"GRW-CAP-110-{number:02d}" for number in range(1, 7)},
        )

    def test_v011_adds_no_script_or_validator(self) -> None:
        self.assertEqual(list((REPOSITORY_ROOT / "scripts").glob("*v0_11*")), [])
        self.assertEqual(
            list((REPOSITORY_ROOT / "system" / "09_schemas_records_and_templates").glob("*v0_11*")),
            [],
        )


if __name__ == "__main__":
    unittest.main()
