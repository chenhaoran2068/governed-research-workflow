"""Structural checks for the versioned v1.1 future-Study support matrix."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "system" / "00_manifest_and_profiles" / "v1_1_support_scope_matrix.json"
SCHEMA_PATH = ROOT / "system" / "00_manifest_and_profiles" / "v1_1_support_scope_matrix.schema.json"
LEDGER_PATH = ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"


def is_safe_relative_path(value: str) -> bool:
    normalized = value.replace("\\", "/")
    return not normalized.startswith("/") and not re.match(r"^[A-Za-z]:", normalized) and ".." not in PurePosixPath(normalized).parts


class V11SupportScopeMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.ledger_ids = {item["capability_id"] for item in json.loads(LEDGER_PATH.read_text(encoding="utf-8"))["capabilities"]}

    def test_versioned_matrix_validates_and_has_13_modules(self) -> None:
        errors = list(Draft202012Validator(self.schema).iter_errors(self.matrix))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))
        self.assertEqual(self.matrix["matrix_schema_version"], "1.1.0")
        self.assertEqual(self.matrix["matrix_status"], "release_source_prepared")
        self.assertEqual(self.matrix["package_contract"]["historical_public_baseline"], "v1.0.0")
        self.assertEqual([module["module_id"] for module in self.matrix["modules"]], [f"{index:02d}" for index in range(13)])

    def test_surfaces_are_safe_and_new_capability_is_limited_to_relevant_modules(self) -> None:
        containing_modules = set()
        for module in self.matrix["modules"]:
            self.assertEqual(module["compatibility_and_migration"]["v1_user_action"], "no_action_required")
            for surface in module["bounded_surfaces"]:
                for path in surface["interface_paths"]:
                    self.assertTrue(is_safe_relative_path(path), path)
                    self.assertTrue((ROOT / path).exists(), path)
                for capability_id in surface["capability_ids"]:
                    self.assertIn(capability_id, self.ledger_ids)
                if "GRW-CAP-111-01" in surface["capability_ids"]:
                    containing_modules.add(module["module_id"])
        self.assertEqual(containing_modules, {"02", "03", "09"})


if __name__ == "__main__":
    unittest.main()
