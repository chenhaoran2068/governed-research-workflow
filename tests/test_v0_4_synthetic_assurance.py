"""Release-source integration checks for the v0.4 governance-records route."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = REPOSITORY_ROOT / "system" / "00_manifest_and_profiles" / "capability_truth_ledger.json"
CURRENT_RELEASE_PATH = REPOSITORY_ROOT / "system" / "11_distribution_installation_and_release" / "CURRENT_RELEASE_STATUS.md"
ASSURANCE_PATH = REPOSITORY_ROOT / "system" / "12_synthetic_examples" / "V0_4_SYNTHETIC_ASSURANCE.md"
V05_ASSURANCE_PATH = REPOSITORY_ROOT / "system" / "12_synthetic_examples" / "V0_5_SYNTHETIC_ASSURANCE.md"
FRAMEWORK_PLAN_PATH = REPOSITORY_ROOT / "system" / "00_manifest_and_profiles" / "FRAMEWORK_INTEGRATION_PLAN.md"
AUTHORIZATION_TEMPLATE_PATH = REPOSITORY_ROOT / "assets" / "bounded-autonomy-authorization.template.json"
PROVENANCE_TEMPLATE_PATH = REPOSITORY_ROOT / "assets" / "data-provenance-register.template.json"
RELEASE_TEMPLATE_PATH = REPOSITORY_ROOT / "assets" / "release-control-record.template.json"
ASSURANCE_RELATIVE_PATH = ASSURANCE_PATH.relative_to(REPOSITORY_ROOT).as_posix().encode("utf-8")


def canonical_snapshot_bytes(source_bytes: bytes) -> bytes:
    """Normalize text line endings while preserving binary source bytes exactly."""
    if b"\0" in source_bytes:
        return source_bytes
    return source_bytes.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def source_snapshot_sha256(excluded_relative_path: bytes) -> str:
    """Hash tracked source while excluding one self-referential evidence file."""
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
    )
    digest = hashlib.sha256()
    for relative_path in sorted(path for path in result.stdout.split(b"\0") if path):
        if relative_path == excluded_relative_path:
            continue
        digest.update(relative_path)
        digest.update(b"\0")
        source_path = REPOSITORY_ROOT / relative_path.decode("utf-8")
        if not source_path.is_file() or source_path.is_symlink():
            raise RuntimeError(f"tracked source snapshot entry is not a regular file: {relative_path!r}")
        source_bytes = source_path.read_bytes()
        # This package contains text records and source code. Normalize only
        # non-binary files so a Windows checkout cannot invalidate the same
        # logical candidate snapshot solely because of CRLF conversion.
        digest.update(canonical_snapshot_bytes(source_bytes))
        digest.update(b"\0")
    return digest.hexdigest()


def current_source_snapshot_sha256() -> str:
    """Return the v0.4 historical-source snapshot representation."""
    return source_snapshot_sha256(ASSURANCE_RELATIVE_PATH)


class V04SyntheticAssuranceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        cls.records = {record["capability_id"]: record for record in cls.ledger["capabilities"]}

    def test_preceding_v04_outcomes_are_admitted_or_explicitly_excluded(self) -> None:
        expected = {
            "GRW-CAP-040-00": "admitted",
            "GRW-CAP-040-01": "admitted",
            "GRW-CAP-040-02": "admitted",
            "GRW-CAP-040-03": "excluded",
            "GRW-CAP-040-04": "admitted",
            "GRW-CAP-040-05": "admitted",
            "GRW-CAP-040-06": "admitted",
        }
        for capability_id, disposition in expected.items():
            record = self.records[capability_id]
            self.assertEqual(record["implementation_status"], "verified")
            self.assertEqual(record["release_disposition"], disposition)
            expected_claim = "forbidden" if capability_id == "GRW-CAP-040-03" else "permitted"
            self.assertEqual(record["public_claim_status"], expected_claim)

    def test_release_verification_runtime_and_source_identities_remain_separate(self) -> None:
        current_release = CURRENT_RELEASE_PATH.read_text(encoding="utf-8")
        skill = (REPOSITORY_ROOT / "SKILL.md").read_text(encoding="utf-8")
        normalized_release = re.sub(r"\s+", " ", current_release)
        self.assertIn("Release Status Verification", current_release)
        self.assertIn("matching GitHub Release", current_release)
        self.assertIn("does not prove that a private skill source or an installed Codex runtime has been updated", normalized_release)
        self.assertIn("Do not infer an installed runtime version", skill)

    def test_v04_framework_profile_evidence_remains_historical_while_current_candidate_targets_v012(self) -> None:
        assurance = ASSURANCE_PATH.read_text(encoding="utf-8")
        framework_plan = FRAMEWORK_PLAN_PATH.read_text(encoding="utf-8")
        self.assertIn("framework tag: `v0.1.1`", assurance)
        self.assertIn("framework resolved commit: `b0e32d7710b70299e633df1316b6924cd87b647b`", assurance)
        self.assertIn("unreleased v0.6 candidate", framework_plan)
        self.assertIn("Workspace Framework `v0.1.2`", framework_plan)
        self.assertIn("97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8", framework_plan)

    def test_synthetic_records_preserve_cross_record_refusal_boundaries(self) -> None:
        authorization = json.loads(AUTHORIZATION_TEMPLATE_PATH.read_text(encoding="utf-8"))
        provenance = json.loads(PROVENANCE_TEMPLATE_PATH.read_text(encoding="utf-8"))
        release = json.loads(RELEASE_TEMPLATE_PATH.read_text(encoding="utf-8"))

        self.assertEqual(authorization["status"], "draft")
        self.assertEqual(authorization["approval"]["status"], "not_granted")
        self.assertEqual(provenance["access_and_sharing"]["access_status"], "unknown")
        self.assertEqual(provenance["access_and_sharing"]["restriction_status"], "unknown")
        self.assertEqual(release["c4_release_authorization_reference"], None)
        self.assertEqual(release["post_release_verification_reference"], None)
        self.assertEqual(release["capability_set"]["admitted_capability_ids"], [])

    def test_assurance_evidence_is_release_source_only_and_synthetic(self) -> None:
        assurance = ASSURANCE_PATH.read_text(encoding="utf-8")
        normalized_assurance = re.sub(r"\s+", " ", assurance)
        self.assertIn("Status: release-source synthetic assurance evidence.", assurance)
        self.assertIn("assurance design baseline: `854d6d10910677ebd7988ee61c6ca6a35519e66f`", assurance)
        self.assertRegex(assurance, r"working-tree source snapshot SHA-256: `[0-9a-f]{64}`")
        self.assertIn("No C4 authorization, tag, GitHub\n  Release, merge, or runtime installation occurred", assurance)
        self.assertIn("does not prove scientific, clinical, ethics, DUA, legal, security, installation, or release correctness", normalized_assurance)
        self.assertNotIn("E:\\", assurance)
        self.assertNotIn("C:\\Users", assurance)

    def test_historical_v04_assurance_snapshot_is_well_formed_but_not_reused_for_v05(self) -> None:
        assurance = ASSURANCE_PATH.read_text(encoding="utf-8")
        match = re.search(r"working-tree source snapshot SHA-256: `([0-9a-f]{64})`", assurance)
        self.assertIsNotNone(match)
        self.assertRegex(match.group(1), r"^[0-9a-f]{64}$")
        self.assertIn("v0.4", assurance.lower())
        self.assertNotEqual(match.group(1), current_source_snapshot_sha256())

    def test_v05_historical_assurance_uses_its_own_tracked_source_snapshot(self) -> None:
        assurance = V05_ASSURANCE_PATH.read_text(encoding="utf-8")
        match = re.search(r"working-tree source snapshot SHA-256: `([0-9a-f]{64})`", assurance)
        self.assertIsNotNone(match)
        self.assertRegex(match.group(1), r"^[0-9a-f]{64}$")
        self.assertIn("Status: historical pre-C4 synthetic assurance evidence.", assurance)
        self.assertIn("historical candidate-source snapshot", re.sub(r"\s+", " ", assurance))

    def test_snapshot_ignores_an_untracked_ci_checkout_directory(self) -> None:
        baseline = current_source_snapshot_sha256()
        with tempfile.TemporaryDirectory(prefix="ci-framework-checkout-", dir=REPOSITORY_ROOT) as temporary_directory:
            temporary_path = Path(temporary_directory)
            (temporary_path / "framework-marker.txt").write_text("not candidate source\n", encoding="utf-8")
            self.assertEqual(current_source_snapshot_sha256(), baseline)

    def test_snapshot_normalizes_text_line_endings_without_altering_binary_inputs(self) -> None:
        text_crlf = b"first\r\nsecond\r\n"
        text_lf = b"first\nsecond\n"
        text_lone_cr = b"first\rsecond\r"
        binary = b"\x00\r\nbinary\rpayload"

        self.assertEqual(canonical_snapshot_bytes(text_crlf), text_lf)
        self.assertEqual(canonical_snapshot_bytes(text_lf), text_lf)
        self.assertEqual(canonical_snapshot_bytes(text_lone_cr), b"first\nsecond\n")
        self.assertEqual(canonical_snapshot_bytes(binary), binary)

    def test_no_role_card_or_agent_runtime_claim_is_introduced(self) -> None:
        public_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (REPOSITORY_ROOT / "system").rglob("*.md")
        )
        self.assertIn("no role cards or agent runtime", public_text)
        self.assertNotIn("v0.4.0 provides an agent runtime", public_text.lower())
        self.assertIsNone(re.search(r"(?i)automatic (network|login|download) executor", public_text))


if __name__ == "__main__":
    unittest.main()
