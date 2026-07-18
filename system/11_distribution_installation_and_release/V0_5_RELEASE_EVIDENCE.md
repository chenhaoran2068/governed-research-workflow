# v0.5.0 Release Evidence: Pre-C3 Candidate Record

Status: pre-C3 preparation evidence only. This document does not identify an
exact candidate commit and therefore cannot support capability admission, C4
authorization, tag creation, GitHub Release creation, or runtime installation.

## Candidate Context

| Field | Current value |
| --- | --- |
| Intended version | `v0.5.0` |
| Published public baseline | `v0.4.0`, commit `0fa4a75ffbd43b98c2e2d634eb0b2b9d8ff32370` |
| Candidate branch at snapshot | `v0.5.0-provenance-register-candidate` |
| Candidate base commit | `0fa4a75ffbd43b98c2e2d634eb0b2b9d8ff32370` |
| Exact v0.5 candidate commit | not recorded in this pre-C3 snapshot |
| v0.5 public tag / GitHub Release | none |
| Installed Codex runtime identity | no v0.5 runtime claim; a separate controlled-installation receipt is required |

## Current Local Evidence Inputs

- The proposed capability is `GRW-CAP-050-01`, a metadata-only register index
  and explicit read-only structural validator. It remains verified candidate
  content with public claim forbidden until a later exact-release admission.
- The current local suite passed `97` tests with `0` failures using local
  Python `3.11.9`, `jsonschema==4.26.0`, and Workspace Framework `v0.1.1` at
  exact commit `b0e32d7710b70299e633df1316b6924cd87b647b`.
- The local test result is preparation evidence only. It does not substitute
  for GitHub CI of an exact candidate commit, a public material/rights review,
  capability admission, C4 authorization, or post-release verification.

## Evidence Still Required

Before C4, the following remain required for the exact release candidate:

1. clean exact candidate commit, source snapshot, object checks, and reviewed
   diff from `v0.4.0`;
2. final public-material, rights, private-material, dependency, workflow, and
   public-surface review for that exact commit and newly reachable history;
3. successful GitHub CI on Windows, Ubuntu, and macOS for Python 3.11 and
   3.14 for the exact intended release commit;
4. accountable-human admission or exclusion decision for `GRW-CAP-050-01`;
5. release-control record and final Release notes tied to the exact commit;
6. explicit C4 approval for the exact commit, tag, notes, and GitHub Release;
   and
7. independent post-release verification.

No item above may be inferred from a local worktree, candidate branch,
historical v0.4 record, passing test, or AI statement.
