"""Synthetic validation and refusal checks for bounded-autonomy records."""

from __future__ import annotations

import copy
import json
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPOSITORY_ROOT / "system" / "09_schemas_records_and_templates" / "bounded_autonomy_authorization.schema.json"
TEMPLATE_PATH = REPOSITORY_ROOT / "assets" / "bounded-autonomy-authorization.template.json"
GUIDANCE_PATH = REPOSITORY_ROOT / "references" / "bounded-autonomy-authorization.md"
DEPENDENCY_RECORD_PATH = REPOSITORY_ROOT / "tests" / "TEST_DEPENDENCY_PROVENANCE.md"


def active_record() -> dict:
    return {
        "schema_version": "1.0.0",
        "record_type": "bounded_autonomy_authorization",
        "authorization_id": "SYNTHETIC-BAA-0001",
        "record_revision": 1,
        "created_at": "2026-07-16T00:00:00Z",
        "status": "active",
        "state_transition_history": [
            {
                "at": "2026-07-16T00:00:00Z",
                "from_status": None,
                "to_status": "pending_human_approval",
                "reason": "synthetic request created",
                "actor_label": "synthetic-requester",
            },
            {
                "at": "2026-07-16T00:05:00Z",
                "from_status": "pending_human_approval",
                "to_status": "active",
                "reason": "synthetic accountable-human approval",
                "actor_label": "synthetic-approver",
            },
        ],
        "task_binding": {
            "request_reference": "SYNTHETIC-REQUEST-0001",
            "task_summary": "Review a synthetic route document for required headings.",
            "project_or_workspace_reference": "SYNTHETIC-WORKSPACE",
        },
        "purpose": "Exercise a synthetic, bounded review record.",
        "expected_output": "A review note in the declared synthetic review location.",
        "success_criteria": ["The note lists every required heading and no unsupported claim."],
        "risk_assessment": {"level": "low", "rationale": "Synthetic documentation review only."},
        "requester": "synthetic-requester",
        "accountable_approver": "synthetic-approver",
        "approval": {
            "status": "approved",
            "reference": "SYNTHETIC-APPROVAL-0001",
            "approved_at": "2026-07-16T00:05:00Z",
        },
        "scope": {
            "exact_scope": "Review only the named synthetic route document.",
            "allowed_inputs": [{"input_id": "synthetic-route", "input_class": "synthetic-document", "known_restriction_state": "not_applicable"}],
            "allowed_tool_classes": ["reasoning_only"],
            "allowed_action_classes": ["audit"],
            "allowed_outputs_and_locations": ["synthetic/review-note.md"],
            "excluded_actions": ["network access", "data access", "submission", "release"],
        },
        "evidence_and_audit": {
            "evidence_requirements": ["Synthetic route headings checked."],
            "audit_record_location": "synthetic/audit-record.md",
        },
        "feedback_and_correction_route": "Return a specific diagnosis to the accountable approver.",
        "next_mandatory_human_decision": "Approve, revise, pause, or retire the next bounded task.",
        "budget": {"applicable": True, "iteration_limit": 2},
        "expires_at": "2099-01-01T00:00:00Z",
        "stop_and_escalation_conditions": ["Stop when scope changes or a prohibited action is requested."],
        "conditional_context": {
            "file_write": {"requested": False},
            "network_or_external_service": {"requested": False},
            "data_bearing": {"contains_data_content": False},
            "delegation_or_multiple_roles": {"requested": False},
            "environment_dependent": {"requested": False},
        },
    }


def operational_refusal_reasons(record: dict | None, requested_action: str, now: datetime) -> list[str]:
    """A test-only routing model; it is not a package executor or policy engine."""
    if record is None:
        return ["authorization record is required"]

    reasons: list[str] = []
    if record["status"] != "active":
        reasons.append("authorization is not active")
    if record["approval"]["status"] != "approved":
        reasons.append("human approval is absent")
    if record["risk_assessment"]["level"] == "unknown":
        reasons.append("risk level is unknown")
    if datetime.fromisoformat(record["expires_at"].replace("Z", "+00:00")) <= now:
        reasons.append("authorization is expired")
    if requested_action not in record["scope"]["allowed_action_classes"]:
        reasons.append("requested action is out of scope")
    if requested_action in record["scope"]["excluded_actions"]:
        reasons.append("requested action is explicitly excluded")

    data_context = record["conditional_context"]["data_bearing"]
    if data_context["contains_data_content"] and data_context.get("access_restriction_share_status") == "unknown":
        reasons.append("data access or sharing status is unknown")
    if record["conditional_context"]["delegation_or_multiple_roles"]["requested"]:
        reasons.append("delegation or multiple roles are excluded in v0.4")
    return reasons


class BoundedAutonomyAuthorizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.template = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())

    def assert_valid(self, record: dict) -> None:
        errors = sorted(self.validator.iter_errors(record), key=lambda error: list(error.absolute_path))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))

    def assert_invalid(self, record: dict) -> None:
        self.assertTrue(list(self.validator.iter_errors(record)), "record unexpectedly validated")

    def test_schema_template_and_dependency_record_are_present(self) -> None:
        self.assertTrue(SCHEMA_PATH.is_file())
        self.assertTrue(TEMPLATE_PATH.is_file())
        self.assertTrue(DEPENDENCY_RECORD_PATH.is_file())
        self.assertTrue(GUIDANCE_PATH.is_file())
        self.assert_valid(self.template)
        dependency_record = DEPENDENCY_RECORD_PATH.read_text(encoding="utf-8")
        self.assertIn("`jsonschema`", dependency_record)
        self.assertIn("`4.26.0`", dependency_record)
        self.assertEqual(version("jsonschema"), "4.26.0")

    def test_complete_approved_synthetic_record_validates(self) -> None:
        self.assert_valid(active_record())

    def test_active_record_requires_human_approval_and_known_risk(self) -> None:
        unapproved = active_record()
        unapproved["approval"] = {"status": "not_granted", "reference": "not-yet-approved", "approved_at": None}
        self.assert_invalid(unapproved)

        unknown_risk = active_record()
        unknown_risk["risk_assessment"] = {"level": "unknown", "rationale": "not assessed"}
        self.assert_invalid(unknown_risk)

    def test_required_task_and_success_fields_are_refused_when_missing(self) -> None:
        missing_task = active_record()
        del missing_task["task_binding"]
        self.assert_invalid(missing_task)

        missing_success = active_record()
        missing_success["success_criteria"] = []
        self.assert_invalid(missing_success)

    def test_file_write_requires_location_overwrite_and_recovery_controls(self) -> None:
        record = active_record()
        record["conditional_context"]["file_write"] = {"requested": True}
        self.assert_invalid(record)

        controlled = copy.deepcopy(record)
        controlled["conditional_context"]["file_write"].update(
            {
                "allowed_directories": ["synthetic/output"],
                "overwrite_policy": "forbidden",
                "rollback_or_recovery_route": "Stop and retain the prior file; request human direction.",
            }
        )
        self.assert_valid(controlled)

    def test_unknown_data_status_allows_only_non_content_planning(self) -> None:
        record = active_record()
        record["conditional_context"]["data_bearing"] = {
            "contains_data_content": True,
            "provenance_record_reference": "SYNTHETIC-PROVENANCE-0001",
            "access_restriction_share_status": "unknown",
            "data_content_action_boundary": "content_access_requested_requires_separate_data_authority",
        }
        self.assert_invalid(record)

        record["conditional_context"]["data_bearing"]["data_content_action_boundary"] = "planning_only_no_content_access"
        self.assert_valid(record)
        reasons = operational_refusal_reasons(record, "audit", datetime(2026, 7, 16, tzinfo=UTC))
        self.assertIn("data access or sharing status is unknown", reasons)

    def test_delegation_and_expiry_are_refused(self) -> None:
        delegated = active_record()
        delegated["conditional_context"]["delegation_or_multiple_roles"] = {
            "requested": True,
            "delegation_policy": "No delegation is admitted in v0.4.",
            "named_role_boundary": "synthetic future role only",
            "accountable_human": "synthetic-approver",
            "decision": "prohibited_v0_4",
        }
        self.assert_invalid(delegated)

        expired = active_record()
        expired["expires_at"] = "2026-07-15T00:00:00Z"
        reasons = operational_refusal_reasons(expired, "audit", datetime(2026, 7, 16, tzinfo=UTC))
        self.assertIn("authorization is expired", reasons)

    def test_ordinary_task_classification_cannot_infer_authorization(self) -> None:
        reasons = operational_refusal_reasons(None, "audit", datetime(2026, 7, 16, tzinfo=UTC))
        self.assertEqual(reasons, ["authorization record is required"])

    def test_guidance_preserves_default_and_non_executor_boundaries(self) -> None:
        guidance = GUIDANCE_PATH.read_text(encoding="utf-8")
        skill = (REPOSITORY_ROOT / "SKILL.md").read_text(encoding="utf-8")
        worksheet = (REPOSITORY_ROOT / "assets" / "collaboration-mode-authorization.template.md").read_text(encoding="utf-8")
        self.assertIn("Human-governed interactive work is the default", guidance)
        self.assertIn("record definitions and tests only", guidance)
        self.assertIn("autonomous executor", guidance)
        self.assertIn("cannot substitute", guidance)
        self.assertIn("human_governed_interactive", worksheet)
        self.assertIn("does not authorize data access", skill)


if __name__ == "__main__":
    unittest.main()
