"""Regression tests separating v0.8 role contracts from excluded runtimes."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = REPOSITORY_ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"


class RoleCardScopeTests(unittest.TestCase):
    def test_role_contract_records_exist_but_no_role_card_or_agent_runtime_is_present(self) -> None:
        agent_module = REPOSITORY_ROOT / "system" / "08_agent_contracts"
        self.assertTrue((agent_module / "role_contracts" / "record_validation_reviewer.json").is_file())
        self.assertTrue((agent_module / "role_contracts" / "audit_boundary_reviewer.json").is_file())
        self.assertFalse((agent_module / "role_cards").exists())
        self.assertFalse((agent_module / "runtime").exists())
        self.assertFalse((REPOSITORY_ROOT / "role_cards").exists())
        self.assertFalse((REPOSITORY_ROOT / "agent_runtime").exists())

    def test_public_scope_is_explicit_and_single_conversation_remains_the_model(self) -> None:
        readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        skill = (REPOSITORY_ROOT / "SKILL.md").read_text(encoding="utf-8")
        roadmap = (REPOSITORY_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        module = (REPOSITORY_ROOT / "system" / "08_agent_contracts" / "MODULE.md").read_text(encoding="utf-8")

        for text in (readme, skill, roadmap, module):
            self.assertIn("role contract", text.lower())
        self.assertIn("One Codex conversation", readme)
        self.assertIn("One Codex conversation", skill)
        self.assertIn("not a runnable", module)
        self.assertIn("agent runtime", module)

    def test_ledger_marks_role_cards_as_verified_excluded_and_not_publicly_claimable(self) -> None:
        ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        record = next(record for record in ledger["capabilities"] if record["capability_id"] == "GRW-CAP-040-03")
        self.assertEqual(record["implementation_status"], "verified")
        self.assertEqual(record["release_disposition"], "excluded")
        self.assertEqual(record["public_claim_status"], "forbidden")
        self.assertEqual(record["interface"]["status"], "present")
        self.assertEqual(record["evidence"]["status"], "verified")
        self.assertIn("separate named-role design", record["limitations_and_next_action"])

    def test_bounded_autonomy_record_does_not_create_a_role_card(self) -> None:
        schema = (REPOSITORY_ROOT / "system" / "09_schemas_records_and_templates" / "bounded_autonomy_authorization.schema.json").read_text(encoding="utf-8")
        self.assertIn("prohibited_v0_4", schema)
        self.assertNotIn('"role_card"', schema)


if __name__ == "__main__":
    unittest.main()
