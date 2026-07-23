# V1.0.0 Release Evidence

Status: local C3 evidence for the reviewed candidate tree. This source file is
intentionally commit-neutral: the separately reviewed C3 report must bind the
active exact Git commit and its test results. This file is not a C4 authorization,
Git tag, GitHub Release, or runtime identity.

| Field | Current value |
| --- | --- |
| Intended version | `v1.0.0` |
| Public baseline | immutable `v0.13.0` commit `93645dda399540979b87843432ae601d5fcc114f` |
| Local branch | `v1.0.0-interface-freeze-candidate` |
| Exact local candidate | source record deliberately commit-neutral; exact commit belongs to the separately reviewed C3 report |
| Frozen contract | Support Scope Matrix, Public Interface Manifest, Capability Verification Map, and existing capability ledger |
| Local regression | 260 tests passed with 3 expected framework-integration skips using `PYTHONDONTWRITEBYTECODE=1` |
| Public-material review | pass for the reviewed local tree; no raw private marker, credential, or non-ASCII content found outside historical negative-test literals |
| Dependency/workflow review | pass for the reviewed local tree; Python baseline, pinned dependency, profiles, helper boundary, and workflow architecture remain unchanged |
| Remote CI | not authorized and not run |
| Protected-main/C4/tag/Release/runtime | not authorized and not established |

Every later source change requires a new exact local commit, clean-tree check,
and full-test evidence under M48. A green local suite or a completed evidence
table remains insufficient for remote action or C4 without a separate
authorization.
