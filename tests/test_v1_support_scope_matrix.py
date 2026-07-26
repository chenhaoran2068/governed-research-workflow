"""Structural support-contract checks for the frozen V1 Support Scope Matrix."""

from __future__ import annotations

import copy
import json
import re
import unittest
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "system" / "00_manifest_and_profiles" / "v1_support_scope_matrix.json"
SCHEMA_PATH = ROOT / "system" / "09_schemas_records_and_templates" / "v1_support_scope_matrix.schema.json"
LEDGER_PATH = ROOT / "system" / "00_manifest_and_profiles" / "v1_capability_truth_ledger.json"
MODULE_IDS = tuple(f"{index:02d}" for index in range(13))
FORBIDDEN_SUPPORT_WORDS = (
    "data access",
    "source corpus",
    "retrieval service",
    "agent runtime",
    "generic writer",
    "automatic push",
    "automatic release",
)


def is_safe_relative_path(value: str) -> bool:
    normalized = value.replace("\\", "/")
    return not normalized.startswith("/") and not re.match(r"^[A-Za-z]:", normalized) and ".." not in PurePosixPath(normalized).parts


class V1SupportScopeMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))

    def test_matrix_validates_and_has_exact_public_identity(self) -> None:
        errors = list(Draft202012Validator(self.schema).iter_errors(self.matrix))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))
        self.assertEqual(self.matrix["matrix_schema_version"], "2.0.0")
        self.assertEqual(self.matrix["matrix_id"], "governed-research-workflow-v1-support-scope-matrix")
        self.assertEqual(self.matrix["matrix_status"], "interface_frozen")
        self.assertEqual(self.matrix["package_contract"]["source_version"], "v1.0.0")
        self.assertEqual(self.matrix["package_contract"]["historical_public_baseline"], "v0.13.0")
        self.assertEqual(set(self.matrix["package_contract"]["public_profiles"]), {"standalone", "framework_integrated"})
        self.assertTrue(any("frozen V1 contract maturity" in limitation for limitation in self.matrix["matrix_limitations"]))

    def test_matrix_covers_each_module_once(self) -> None:
        module_ids = [module["module_id"] for module in self.matrix["modules"]]
        self.assertEqual(module_ids, list(MODULE_IDS))
        self.assertEqual(len(module_ids), len(set(module_ids)))
        self.assertEqual({module["posture"] for module in self.matrix["modules"]}, {"active_bounded"})

    def test_every_active_module_has_existing_references_and_explicit_boundaries(self) -> None:
        ledger_ids = {record["capability_id"] for record in self.ledger["capabilities"]}
        for module in self.matrix["modules"]:
            self.assertTrue(module["bounded_surfaces"], module["module_id"])
            self.assertTrue(module["external_boundaries"], module["module_id"])
            self.assertTrue(module["v1_exclusions"], module["module_id"])
            self.assertTrue(module["known_limitations"], module["module_id"])
            self.assertTrue(module["refusal_statement"], module["module_id"])
            self.assertEqual(module["compatibility_and_migration"]["v012_user_action"], "no_action_required")
            self.assertEqual(module["compatibility_and_migration"]["migration_action"], "none")
            for surface in module["bounded_surfaces"]:
                for path in surface["interface_paths"]:
                    self.assertTrue(is_safe_relative_path(path), path)
                    target = ROOT / path
                    self.assertTrue(target.exists(), path)
                for capability_id in surface["capability_ids"]:
                    self.assertIn(capability_id, ledger_ids, capability_id)
            for evidence in module["evidence_references"]:
                self.assertTrue(is_safe_relative_path(evidence["path"]), evidence["path"])
                self.assertTrue((ROOT / evidence["path"]).is_file(), evidence["path"])

    def test_schema_refuses_missing_duplicate_or_unsupported_module_disposition(self) -> None:
        missing = copy.deepcopy(self.matrix)
        missing["modules"].pop()
        self.assertTrue(list(Draft202012Validator(self.schema).iter_errors(missing)))

        invalid_posture = copy.deepcopy(self.matrix)
        invalid_posture["modules"][0]["posture"] = "fully_supported"
        self.assertTrue(list(Draft202012Validator(self.schema).iter_errors(invalid_posture)))

        missing_surface = copy.deepcopy(self.matrix)
        missing_surface["modules"][0]["bounded_surfaces"] = []
        self.assertTrue(list(Draft202012Validator(self.schema).iter_errors(missing_surface)))

        duplicate = copy.deepcopy(self.matrix)
        duplicate["modules"][1]["module_id"] = "00"
        identifiers = [module["module_id"] for module in duplicate["modules"]]
        self.assertNotEqual(len(identifiers), len(set(identifiers)))

    def test_matrix_cannot_turn_named_exclusions_into_supported_claims(self) -> None:
        combined = "\n".join(
            "\n".join(item["non_claim"] for item in module["v1_exclusions"])
            + "\n"
            + "\n".join(item["non_claim"] for item in module["external_boundaries"])
            for module in self.matrix["modules"]
        ).lower()
        for phrase in FORBIDDEN_SUPPORT_WORDS:
            self.assertIn(phrase, combined, phrase)

        active_surface_text = "\n".join(
            surface["summary"] for module in self.matrix["modules"] for surface in module["bounded_surfaces"]
        ).lower()
        self.assertNotIn("agent runtime", active_surface_text)
        self.assertNotIn("generic writer", active_surface_text)
        self.assertNotIn("automatic release", active_surface_text)

    def test_matrix_preserves_separate_authority_layers(self) -> None:
        authority = self.matrix["authority_boundary"]
        self.assertIn("sole machine-readable authority for module-level", authority["module_support_owner"])
        self.assertIn("capability_truth_ledger.json", authority["capability_claim_owner"])
        self.assertIn("Git tag", authority["release_identity_owner"])
        self.assertIn("installation receipt", authority["installation_identity_owner"])
        self.assertIn("accountable human", authority["project_decision_owner"])
        guidance = (ROOT / "system" / "00_manifest_and_profiles" / "V1_SUPPORT_SCOPE.md").read_text(encoding="utf-8")
        self.assertIn("not public-release", guidance)

    def test_module_boundaries_do_not_retain_a_superseded_current_matrix_label(self) -> None:
        for module_id in MODULE_IDS:
            matches = list((ROOT / "system").glob(f"{module_id}_*/MODULE.md"))
            self.assertEqual(len(matches), 1, module_id)
            content = matches[0].read_text(encoding="utf-8")
            self.assertIn("The V1 Support Scope Matrix", content)
            self.assertNotIn("The v0.13 V1 Support Scope Matrix", content)


if __name__ == "__main__":
    unittest.main()
