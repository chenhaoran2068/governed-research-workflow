# v0.9.0 Release Evidence: Pre-C3-Remote Preparation Record

Status: pre-C3-remote preparation evidence. It preserves local candidate
evidence and identifies what must be repeated for an exact remote candidate.
It is not C3-remote authorization, C4 authorization, a tag, GitHub Release,
installation target, or runtime statement.

## Preparation Context

| Field | Recorded value |
| --- | --- |
| Intended version | `v0.9.0` |
| Public baseline | immutable `v0.8.1`, commit `9439983971e0d5f8299a337b683055aa469e0a5f` |
| Initial local implementation commit | `9a3a6c9b3183863f0153477bdb804d16c53ec5d1` |
| Exact remote candidate | unresolved; a later local commit must include final release-preparation material |
| Intended framework identity | `v0.1.2`, commit `97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8` |
| Intended capability set | `GRW-CAP-090-01`, `GRW-CAP-090-02`, and `GRW-CAP-090-03` only |
| Exact C4 release identity | deliberately unresolved until protected-main merge and a separate C4 decision |

## Local Candidate Evidence

- The local candidate suite passed `187` tests with `3` expected skips where
  Framework integration environment variables were intentionally absent.
- Dedicated integrity-audit tests covered valid input, no-write behavior,
  path/indirection refusal, duplicate JSON keys and cross-type identities,
  declared-input mismatch, reliable harness conditions, correction linkage,
  refusal-safe operational preflight, and machine-readable CLI output.
- Static review found no private absolute path, credential marker, runtime
  identity, premature v0.9 release/C4 claim, networking client, Git invocation,
  or write-capable call in the new validator surface.
- The implementation diff contains generic Markdown, JSON, JSON Schema, and
  Python only. It contains no dependency manifest or workflow change, submodule,
  Git LFS object, symlink, or binary artifact.

## Required Refresh Before C4

The following cannot be inherited once release-preparation content changes:

1. an exact local candidate commit and reviewed tracked-source snapshot;
2. complete local test result for that exact commit;
3. six-context GitHub CI result for that exact commit and the protected-main
   release commit;
4. refreshed public-material, rights, privacy, secret, dependency, workflow,
   protected-main, and release-integrity review;
5. verification that capability admission still matches the exact final scope;
   and
6. C4 approval naming the post-merge commit, tag, notes, and Release action.
