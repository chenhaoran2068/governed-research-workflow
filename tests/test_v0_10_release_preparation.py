"""Release-preparation checks for the bounded v0.10 candidate."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "system" / "11_distribution_installation_and_release"
LEDGER = ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"
SCHEMA = ROOT / "system" / "09_schemas_records_and_templates" / "voluntary_experience_package.schema.json"
PUBLIC_FILES = (
    "system/09_schemas_records_and_templates/voluntary_experience_package.schema.json",
    "assets/voluntary-experience-package.template.json",
    "references/voluntary-experience-package.md",
    "scripts/validate_voluntary_experience_package.py",
    "tests/fixtures/voluntary_experience_package/valid/experience-package.json",
)
FORBIDDEN_MARKERS = ("E:" + chr(92) + "Chen" + "haoran", "C:" + chr(92) + "Us" + "ers", "99" + "sai", "gh" + "p_", "github" + "_pat_", "BEGIN" + " PRIVATE" + " KEY")


class V010ReleasePreparationTests(unittest.TestCase):
    def test_current_candidate_identity_and_historical_baseline_are_separate(self) -> None:
        manifest = (ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8")
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.assertIn("system_version: 0.10.0-voluntary-experience-package-candidate", manifest)
        self.assertEqual(ledger["release_context"]["source_release_version"], "v0.10.0")
        self.assertEqual(ledger["release_context"]["historical_public_baseline"], "v0.9.0")
        self.assertNotIn("v0.10.0 is published", "\n".join((manifest, json.dumps(ledger))).lower())

    def test_capability_admission_is_single_and_not_c4(self) -> None:
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        record = next(item for item in ledger["capabilities"] if item["capability_id"] == "GRW-CAP-100-01")
        self.assertEqual(record["implementation_status"], "verified")
        self.assertEqual(record["release_disposition"], "admitted")
        self.assertEqual(record["version"]["target_release"], "v0.10.0")
        self.assertIsNone(record["version"]["last_verified_release"])
        self.assertIn("does not collect", record["non_promise"].lower())
        admission = " ".join((RELEASE / "V0_10_CAPABILITY_ADMISSION.md").read_text(encoding="utf-8").lower().split())
        self.assertIn("not c3-remote evidence", admission)
        self.assertIn("does not prove a hosted release", admission)

    def test_release_control_is_valid_and_leaves_final_identity_unresolved(self) -> None:
        schema = json.loads((RELEASE / "release_control_record.schema.json").read_text(encoding="utf-8"))
        record = json.loads((RELEASE / "V0_10_RELEASE_CONTROL_CANDIDATE.json").read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))
        self.assertEqual(record["candidate_identity"]["exact_commit"], "0" * 40)
        self.assertEqual(record["candidate_identity"]["branch_state"], "local_candidate_only")
        self.assertIsNone(record["c4_release_authorization_reference"])

    def test_public_surface_is_generic_and_validator_has_no_network_or_write_executor(self) -> None:
        for relative in PUBLIC_FILES:
            content = (ROOT / relative).read_text(encoding="utf-8")
            for marker in FORBIDDEN_MARKERS:
                self.assertNotIn(marker, content, f"{relative} contains {marker!r}")
        validator = (ROOT / "scripts" / "validate_voluntary_experience_package.py").read_text(encoding="utf-8")
        for forbidden in ("requests", "urllib", "http.client", "subprocess", "os.walk", "rglob", "write_text", "write_bytes", "unlink", "mkdir"):
            self.assertNotIn(forbidden, validator)
        reference = " ".join((ROOT / "references" / "voluntary-experience-package.md").read_text(encoding="utf-8").lower().split())
        self.assertIn("outside its view", reference)
        self.assertIn("not a computer b test", reference)

    def test_schema_has_no_identity_or_attachment_property(self) -> None:
        schema_text = SCHEMA.read_text(encoding="utf-8")
        for forbidden in ('"email"', '"account"', '"attachment"', '"raw_transcript"', '"project_identifier"'):
            self.assertNotIn(forbidden, schema_text)


if __name__ == "__main__":
    unittest.main()
