"""Public-material checks for the v0.9 metadata-only implementation surface."""

from __future__ import annotations

import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
V09_PUBLIC_FILES = [
    "system/09_schemas_records_and_templates/integrity_audit_bundle.schema.json",
    "assets/integrity-audit-bundle.template.json",
    "references/integrity-audit-bundle.md",
    "scripts/validate_integrity_audit_bundle.py",
    "tests/fixtures/integrity_audit_bundle/valid/bundle.json",
]
FORBIDDEN_PUBLIC_MARKERS = [
    "E:" + chr(92) + "Chen" + "haoran",
    "C:" + chr(92) + "Us" + "ers",
    "99" + "sai",
    "gh" + "p_",
    "github" + "_pat_",
    "BEGIN" + " PRIVATE" + " KEY",
]


class V09SyntheticAssuranceTests(unittest.TestCase):
    def test_v09_public_surface_is_generic_and_free_of_local_identity_markers(self) -> None:
        for relative_path in V09_PUBLIC_FILES:
            content = (REPOSITORY_ROOT / relative_path).read_text(encoding="utf-8")
            for marker in FORBIDDEN_PUBLIC_MARKERS:
                self.assertNotIn(marker, content, f"{relative_path} contains forbidden marker {marker!r}")

    def test_v09_public_surface_describes_metadata_only_boundaries(self) -> None:
        schema = (REPOSITORY_ROOT / V09_PUBLIC_FILES[0]).read_text(encoding="utf-8")
        reference = (REPOSITORY_ROOT / V09_PUBLIC_FILES[2]).read_text(encoding="utf-8")
        self.assertIn('"metadata_only": {"const": true}', schema)
        self.assertIn("does not decide which record is true", reference)
        self.assertIn("does not enumerate a directory", reference)


if __name__ == "__main__":
    unittest.main()
