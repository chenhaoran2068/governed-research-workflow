#!/usr/bin/env python3
"""Validate one explicit paper repository candidate without modifying it."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from paper_repository_release_common import (
    SCHEMA_ROOT, is_disallowed_relative, is_reparse_or_symlink, load_json,
    relative_posix, safe_relative, scan_text,
)


REQUIRED_ROOT = {"README.md", "CITATION.cff", "DATA_ACCESS.md", "RELEASE_MANIFEST.json"}
MAX_FILE_BYTES = 100 * 1024 * 1024


def issue(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message}


def validate(candidate: Path) -> dict:
    issues: list[dict[str, str]] = []
    if not candidate.is_dir() or is_reparse_or_symlink(candidate):
        return {"status": "invalid", "errors": [issue("candidate", "/", "candidate must be an existing non-link directory")]}

    for name in sorted(REQUIRED_ROOT):
        if not (candidate / name).is_file():
            issues.append(issue("missing_required_file", name, "required root file is missing"))

    manifest_path = candidate / "RELEASE_MANIFEST.json"
    manifest = None
    if manifest_path.is_file():
        try:
            manifest = load_json(manifest_path)
            schema = load_json(SCHEMA_ROOT / "paper_repository_release_manifest.schema.json")
            for error in sorted(Draft202012Validator(schema).iter_errors(manifest), key=lambda item: list(item.absolute_path)):
                issues.append(issue("manifest_schema", "/".join(map(str, error.absolute_path)), error.message))
        except (OSError, ValueError, json.JSONDecodeError) as error:
            issues.append(issue("manifest_input", "RELEASE_MANIFEST.json", str(error)))

    for path in sorted(candidate.rglob("*")):
        rel = relative_posix(path, candidate)
        if is_reparse_or_symlink(path):
            issues.append(issue("link_or_reparse_point", rel, "links and reparse points are not allowed"))
            continue
        if is_disallowed_relative(path.relative_to(candidate)):
            issues.append(issue("disallowed_path", rel, "local environment, cache, dependency tree, or nested Git metadata detected"))
        if path.is_file():
            if path.stat().st_size > MAX_FILE_BYTES:
                issues.append(issue("oversized_file", rel, "file exceeds 100 MiB"))
            for code, message in scan_text(path):
                issues.append(issue(code, rel, message))

    if isinstance(manifest, dict):
        repository = manifest.get("repository", {})
        naming = repository.get("naming")
        if isinstance(naming, dict) and repository.get("name"):
            components = [naming.get("subject_or_domain"), naming.get("core_focus"), naming.get("output_type")]
            expected_name = "-".join(component for component in components if component)
            if repository["name"] != expected_name:
                issues.append(issue("repository_name_mismatch", "repository.name", "name must equal the recorded subject/domain, optional core focus, and output type"))
        for key in ("readme_reference", "citation_reference", "data_access_reference", "expected_output_reference"):
            value = manifest.get("content", {}).get(key)
            if value is None:
                continue
            clean = value.split("#", 1)[0]
            if not safe_relative(clean):
                issues.append(issue("unsafe_reference", f"content.{key}", "reference must be relative and traversal-free"))
            elif not (candidate / Path(clean)).exists():
                issues.append(issue("missing_reference", f"content.{key}", f"referenced path does not exist: {clean}"))
        if manifest.get("release_status") in {"release_candidate", "released"}:
            if not repository.get("name"):
                issues.append(issue("repository_name_missing", "repository.name", "candidate or release requires a stable repository name"))
            if not isinstance(naming, dict):
                issues.append(issue("repository_naming_missing", "repository.naming", "candidate or release requires a naming record"))
            else:
                for key in ("subject_or_domain", "output_type", "rationale"):
                    if not naming.get(key):
                        issues.append(issue("repository_naming_incomplete", f"repository.naming.{key}", "candidate or release requires this naming field"))
                if len(naming.get("selected_dimensions", [])) < 2:
                    issues.append(issue("repository_naming_incomplete", "repository.naming.selected_dimensions", "record at least two research dimensions used to choose the name"))
                if naming.get("human_confirmed") is not True:
                    issues.append(issue("repository_name_unconfirmed", "repository.naming.human_confirmed", "candidate or release requires human confirmation of the repository name"))
            required_gates = ("scope_and_rights", "clean_candidate", "reproducibility", "independent_review")
            for gate in required_gates:
                if manifest.get("validation", {}).get(gate) != "passed":
                    issues.append(issue("release_gate_not_passed", f"validation.{gate}", "candidate or release requires this gate to be passed"))
            for key in ("scope_approved_by", "rights_approved_by", "citation_approved_by"):
                if not manifest.get("human_decisions", {}).get(key):
                    issues.append(issue("human_decision_missing", f"human_decisions.{key}", "candidate requires recorded human confirmation"))
        if manifest.get("release_status") == "released":
            for key in ("commit", "tag", "github_release_url"):
                if not manifest.get("release_identity", {}).get(key):
                    issues.append(issue("release_identity_missing", f"release_identity.{key}", "released status requires exact external identity"))
            if manifest.get("validation", {}).get("release_and_citation") != "passed":
                issues.append(issue("release_gate_not_passed", "validation.release_and_citation", "released status requires this gate to be passed"))

    return {"status": "valid" if not issues else "invalid", "errors": issues}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = validate(args.candidate.resolve())
    except OSError as error:
        result = {"status": "invalid", "errors": [issue("input", "/", str(error))]}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
