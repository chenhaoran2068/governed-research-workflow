# v1.2.1 Release Gate

Status: commit-neutral pre-C4 maintenance-gate snapshot.

## Intended Scope

v1.2.1 changes release narration only. `GRW-CAP-120-01` remains the single
v1.2 capability, last fully capability-verified in published v1.2.0. No other
capability, interface, schema, validator, dependency, Framework behavior, data
action, source action, mapping, promotion, runtime behavior, or public intake
is added or changed.

## Gate Conditions

1. Changes stay within the approved maintenance path list.
2. The v1.2.1 control record validates and the new regression test proves the
   release notes have no future/later-Release, candidate, pending, or runtime
   installation wording.
3. README, ROADMAP, release-status guidance, and the ledger distinguish
   v1.2.0 historical capability verification from v1.2.1 selected-version
   tag-and-Release verification.
4. v1.2.0 immutable historical records remain unchanged.
5. Focused and complete local tests pass; separately authorized remote CI passes
   on Windows, Ubuntu, and macOS at Python 3.11 and 3.14.
6. A protected-main merge yields a new exact commit. A separately evidenced C4
   action must create the annotated v1.2.1 tag and matching GitHub Release with
   no additional assets.

This source snapshot is not an exact candidate, CI result, protected-main
identity, C4 authorization, annotated tag, GitHub Release, or installation
statement.
