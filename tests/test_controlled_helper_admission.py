"""Structural and boundary tests for the v0.8 helper-admission record."""

from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPOSITORY_ROOT / "system" / "09_schemas_records_and_templates" / "controlled_helper_admission.schema.json"
TEMPLATE_PATH = REPOSITORY_ROOT / "assets" / "controlled_helper_admission.template.json"
RECORD_PATH = REPOSITORY_ROOT / "system" / "07_tools_and_integrations" / "bootstrap_empty_workspace_helper_admission.json"
SCRIPT_PATH = REPOSITORY_ROOT / "scripts" / "bootstrap_empty_workspace.py"
REFERENCE_PATH = REPOSITORY_ROOT / "references" / "controlled-helper-admission.md"
CANONICAL_TEXT_HASH_ALGORITHM = "sha256_utf8_lf_v1"


def canonical_utf8_lf_source_bytes(raw_bytes: bytes) -> bytes:
    """Return the declared cross-platform source-text identity bytes."""
    try:
        decoded = raw_bytes.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise ValueError("sha256_utf8_lf_v1 requires strict UTF-8 source text.") from error
    return decoded.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def source_identity_digest(raw_bytes: bytes) -> str:
    return hashlib.sha256(canonical_utf8_lf_source_bytes(raw_bytes)).hexdigest()


class ControlledHelperAdmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema)
        cls.template = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
        cls.record = json.loads(RECORD_PATH.read_text(encoding="utf-8"))

    def assert_valid(self, record: dict[str, object]) -> None:
        errors = sorted(self.validator.iter_errors(record), key=lambda error: list(error.absolute_path))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))

    def test_schema_template_and_candidate_record_are_valid(self) -> None:
        self.assertEqual(self.schema["$id"], "https://github.com/chenhaoran2068/governed-research-workflow/schemas/controlled_helper_admission.schema.json")
        self.assert_valid(self.template)
        self.assert_valid(self.record)
        self.assertEqual(self.record["helper_id"], "bootstrap_empty_workspace")
        self.assertEqual(self.record["admission_status"], "candidate")
        self.assertEqual(self.record["accountable_human_admission"], {"status": "not_granted", "reference": None})

    def test_source_identity_matches_canonical_bootstrap_source_text(self) -> None:
        digest = source_identity_digest(SCRIPT_PATH.read_bytes())
        identity = self.record["source_identity"]
        self.assertEqual(identity["repository_relative_path"], "scripts/bootstrap_empty_workspace.py")
        self.assertEqual(identity["content_hash_algorithm"], CANONICAL_TEXT_HASH_ALGORITHM)
        self.assertEqual(identity["sha256"], digest)
        self.assertIn("not a public Release", identity["identity_scope"])

    def test_canonical_source_identity_is_stable_across_text_line_endings(self) -> None:
        lf = b"def example():\n    return 'stable'\n"
        crlf = lf.replace(b"\n", b"\r\n")
        self.assertNotEqual(hashlib.sha256(lf).hexdigest(), hashlib.sha256(crlf).hexdigest())
        self.assertEqual(source_identity_digest(lf), source_identity_digest(crlf))
        with self.assertRaisesRegex(ValueError, "strict UTF-8"):
            source_identity_digest(b"\xff\xfe")

    def test_admission_preserves_preview_write_and_recovery_controls(self) -> None:
        confirmation = self.record["confirmation_boundary"]
        write = self.record["write_boundary"]
        recovery = self.record["recovery_boundary"]
        self.assertTrue(confirmation["exact_plan_id_required"])
        self.assertTrue(confirmation["nonempty_accountable_human_approval_reference_required"])
        self.assertTrue(confirmation["filesystem_identity_rechecked_before_write"])
        self.assertTrue(write["no_write_preview_required"])
        self.assertFalse(write["overwrite_permitted"])
        self.assertFalse(write["resume_permitted"])
        self.assertFalse(write["delete_permitted"])
        self.assertTrue(recovery["final_receipt_required"])
        self.assertTrue(recovery["generated_file_hashes_required"])
        for action, allowed in self.record["data_credential_network_boundary"].items():
            self.assertFalse(allowed, action)

    def test_schema_rejects_privileged_boundary_or_unverifiable_identity(self) -> None:
        privileged = copy.deepcopy(self.record)
        privileged["data_credential_network_boundary"]["network_access"] = True
        self.assertNotEqual(list(self.validator.iter_errors(privileged)), [])

        invalid_hash = copy.deepcopy(self.record)
        invalid_hash["source_identity"]["sha256"] = "not-a-sha256"
        self.assertNotEqual(list(self.validator.iter_errors(invalid_hash)), [])

        unsupported_hash_algorithm = copy.deepcopy(self.record)
        unsupported_hash_algorithm["source_identity"]["content_hash_algorithm"] = "sha256_any_bytes"
        self.assertNotEqual(list(self.validator.iter_errors(unsupported_hash_algorithm)), [])

        missing_confirmation = copy.deepcopy(self.record)
        del missing_confirmation["confirmation_boundary"]
        self.assertNotEqual(list(self.validator.iter_errors(missing_confirmation)), [])

    def test_admission_is_not_per_run_or_runtime_authority(self) -> None:
        combined = " ".join(self.record["explicit_non_claims"]).lower() + " " + REFERENCE_PATH.read_text(encoding="utf-8").lower()
        for required in ("not a per-run", "not m53", "not a generic writer", "not a public release", "not a per-run approval"):
            self.assertIn(required, combined)


if __name__ == "__main__":
    unittest.main()
