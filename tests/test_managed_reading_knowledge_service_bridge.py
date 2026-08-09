"""Source-free structural and refusal checks for GRW-CAP-220-01."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"
SCHEMA_PATH = ROOT / "system" / "09_schemas_records_and_templates" / "study_knowledge_handoff.schema.json"
TEMPLATE_PATH = ROOT / "assets" / "managed-reading-knowledge-service" / "study-knowledge-handoff.template.json"
BRIDGE_PATH = ROOT / "references" / "managed-reading-knowledge-service-bridge.md"
MANIFEST_PATH = ROOT / "SYSTEM_MANIFEST.yaml"


class ManagedReadingKnowledgeServiceBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.template = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
        cls.bridge = BRIDGE_PATH.read_text(encoding="utf-8")
        cls.manifest = MANIFEST_PATH.read_text(encoding="utf-8")
        cls.validator = Draft202012Validator(cls.schema)

    def test_optional_consumer_capability_is_explicit_and_source_free(self) -> None:
        record = next(item for item in self.ledger["capabilities"] if item["capability_id"] == "GRW-CAP-220-01")
        self.assertEqual("routing", record["capability_class"])
        self.assertEqual("v1.12.0", record["version"]["target_release"])
        self.assertIn("metadata-only", record["promise"])
        self.assertIn("Does not discover", record["non_promise"])
        self.assertIn("no_data_access", record["data_and_external_boundary"])
        self.assertIn("no_external_service_action", record["data_and_external_boundary"])
        self.assertIn("optional_shared_services:\n  - scholarly-reading-knowledge", self.manifest)

    def test_blank_template_validates_as_metadata_only(self) -> None:
        self.assertEqual([], list(self.validator.iter_errors(self.template)))
        self.assertFalse(self.template["source_content_transferred"])
        self.assertFalse(self.template["source_reading_authorized"])
        self.assertEqual("non_authoritative", self.template["authority_status"])

    def test_schema_refuses_content_paths_and_unauthorized_states(self) -> None:
        cases = []
        content_case = copy.deepcopy(self.template)
        content_case["source_content_transferred"] = True
        cases.append(content_case)
        path_case = copy.deepcopy(self.template)
        path_case["approved_metadata"]["pdf_path"] = "C:\\private\\paper.pdf"
        cases.append(path_case)
        authorization_case = copy.deepcopy(self.template)
        authorization_case["source_reading_authorized"] = True
        cases.append(authorization_case)
        authority_case = copy.deepcopy(self.template)
        authority_case["authority_status"] = "source_supported"
        cases.append(authority_case)

        for candidate in cases:
            self.assertTrue(list(self.validator.iter_errors(candidate)))

    def test_bridge_keeps_service_ownership_and_refusal_boundaries(self) -> None:
        for required in (
            "optional consumer",
            "reading Skill owns",
            "metadata-only handoff",
            "Do not use this bridge",
            "source_content_transferred",
        ):
            self.assertIn(required, self.bridge)
        for prohibited in ("E:" + "\\Chenhaoran", "C:" + "\\Users"):
            self.assertNotIn(prohibited, self.bridge)


if __name__ == "__main__":
    unittest.main()
