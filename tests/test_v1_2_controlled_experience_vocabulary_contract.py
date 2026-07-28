"""Public-contract checks for the v1.2 controlled vocabulary source scope."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "system" / "09_schemas_records_and_templates"
ASSETS = ROOT / "assets" / "experience-vocabulary"
LEDGER = ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"


class V12ControlledExperienceVocabularyContractTests(unittest.TestCase):
    def test_all_generic_contract_surfaces_exist_and_templates_validate(self) -> None:
        pairs = (
            ("controlled_experience_vocabulary.schema.json", "controlled-experience-vocabulary.template.json"),
            ("experience_source_inventory.schema.json", "experience-source-inventory.template.json"),
            ("experience_mapping_decision.schema.json", "experience-mapping-decision.template.json"),
            ("experience_reference_index.schema.json", "experience-reference-index.template.json"),
        )
        for schema_name, template_name in pairs:
            schema = json.loads((SCHEMAS / schema_name).read_text(encoding="utf-8"))
            template = json.loads((ASSETS / template_name).read_text(encoding="utf-8"))
            errors = list(Draft202012Validator(schema).iter_errors(template))
            self.assertEqual(errors, [], "\n".join(error.message for error in errors))

        self.assertTrue((ROOT / "references" / "controlled-experience-vocabulary.md").is_file())
        self.assertTrue((ROOT / "scripts" / "validate_controlled_experience_vocabulary.py").is_file())
        self.assertTrue((ROOT / "scripts" / "validate_experience_reference_index.py").is_file())

    def test_capability_ledger_and_current_surfaces_keep_generic_metadata_only_boundary(self) -> None:
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        record = next(item for item in ledger["capabilities"] if item["capability_id"] == "GRW-CAP-120-01")
        self.assertEqual(record["implementation_status"], "verified")
        self.assertEqual(record["release_disposition"], "admitted")
        self.assertEqual(record["profile_scope"], "both")
        self.assertEqual(
            set(record["data_and_external_boundary"]),
            {"metadata_only", "synthetic_only", "no_data_access", "no_external_service_action"},
        )
        self.assertIn("read source bodies or pointers", record["non_promise"])
        self.assertIn("tag, map, promote, or integrate an experience", record["non_promise"])

        current_paths = (
            ROOT / "README.md",
            ROOT / "ROADMAP.md",
            ROOT / "SKILL.md",
            ROOT / "system" / "06_memory_and_learning" / "MODULE.md",
            ROOT / "references" / "controlled-experience-vocabulary.md",
        )
        text = "\n".join(path.read_text(encoding="utf-8").lower() for path in current_paths)
        for marker in ("grw-cap-120-01", "metadata-only", "does not", "mapping"):
            self.assertIn(marker, text)
        self.assertIn("caller to name", (ROOT / "SKILL.md").read_text(encoding="utf-8").lower())
        self.assertNotIn("v1.2.0 is released", text)
        self.assertNotIn("v1.2.0 is installed", text)

    def test_public_candidate_has_no_private_workspace_marker_or_real_source_claim(self) -> None:
        paths = (
            SCHEMAS / "controlled_experience_vocabulary.schema.json",
            SCHEMAS / "experience_source_inventory.schema.json",
            SCHEMAS / "experience_mapping_decision.schema.json",
            SCHEMAS / "experience_reference_index.schema.json",
            *ASSETS.glob("*.json"),
            ROOT / "references" / "controlled-experience-vocabulary.md",
            ROOT / "scripts" / "validate_controlled_experience_vocabulary.py",
            ROOT / "scripts" / "validate_experience_reference_index.py",
        )
        text = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        self.assertIsNone(re.search(r"(?i)(?:[a-z]:\\|/(?:home|users)/)", text))
        lowered = text.lower()
        for required_boundary in ("metadata-only", "source pointer", "automatic"):
            self.assertTrue(required_boundary in lowered, required_boundary)


if __name__ == "__main__":
    unittest.main()
