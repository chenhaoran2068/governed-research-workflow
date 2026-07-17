# v0.4.0 Release Evidence: Historical Pre-C3 Candidate Record

Status: historical pre-C3 preparation evidence only. This document does not identify an
exact candidate commit and therefore cannot support capability admission, C4
authorization, tag creation, GitHub Release creation, or runtime installation.

## Candidate Context

| Field | Current value |
| --- | --- |
| Intended version | `v0.4.0` |
| Current public baseline | `v0.3.1`, commit `0a16e534fb11bc5254bcdd5c2780e09f46cf81d0` |
| Candidate branch at snapshot | `v0.4.0-capability-truth-ledger-candidate` |
| Candidate base commit | `854d6d10910677ebd7988ee61c6ca6a35519e66f` |
| Exact v0.4 candidate commit | not recorded in this pre-C3 snapshot; a later exact-candidate record must identify any exact candidate commit |
| v0.4 public tag / GitHub Release | none |
| Current installed Codex runtime identity | no v0.4 runtime claim; any runtime identity requires a separate controlled installation receipt |

## Current Local Evidence Inputs

- R40-00 through R40-06 completed local implementation review. R40-03 is a
  verified exclusion; all other R40 records remain verified candidates with
  public claims forbidden.
- The release-preparation full local suite passed `76` tests with `0` failed
  and `0` skipped using the exact local Workspace Framework `v0.1.1` tag at
  commit `b0e32d7710b70299e633df1316b6924cd87b647b`. It includes the
  pre-C3 release-document and cross-platform line-ending snapshot checks.
- GitHub's public `releases/latest` route resolved to `v0.3.1` on
  `2026-07-17`; this confirms the current public baseline but is not a v0.4
  hosted-release claim.
- The capability ledger, evidence matrix, candidate-admission record, and
  R40 synthetic-assurance record provide the historical candidate evidence map.

## Evidence Still Required

After candidate source changes, refresh the applicable local suite and complete
the exact worktree material/rights, source-authority, dependency,
workflow, and public-surface review. Before C4, the following remain required:

1. a clean exact candidate commit and a reviewed candidate-to-baseline diff;
2. an explicit capability-admission decision in the canonical ledger;
3. final public-material and rights review for the exact commit and reachable
   new history;
4. successful cross-platform CI for the exact intended release commit;
5. an exact release-control record created from the reviewed commit;
6. explicit C4 approval for the commit, tag, Release notes, and GitHub Release
   action; and
7. independent post-release verification.

No item above may be filled by inference from a local branch, prior release,
passing test, or AI summary.
