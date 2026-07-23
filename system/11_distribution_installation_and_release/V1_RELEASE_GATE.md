# V1.0.0 Release Gate

Status: local C3 interface-freeze preparation. This gate is not an exact commit,
remote candidate, GitHub Actions result, protected-main merge, C4 authorization,
Git tag, GitHub Release, or installation statement.

## Intended Scope

v1.0.0 freezes existing bounded public interfaces. The authoritative interface
inventory is `v1_public_interface_manifest.json`; module posture remains in
`v1_support_scope_matrix.json`; individual promises remain in
`capability_truth_ledger.json`; v1 regression traceability is in
`v1_capability_verification_map.json`.

No new research operation, data-content action, external service, intake,
agent/runtime, generic writer, dependency, profile, or runtime update is
admitted.

## Gate Conditions

1. Every change remains within the C2 file scope and local-only C3 boundary.
2. The interface manifest, support matrix, verification map, ledger, and their
   schemas validate and cross-reference existing files.
3. Full local regression passes for the exact candidate with bytecode writing
   disabled; all map entries then receive a separately reviewed local-evidence
   update.
4. Public-material, private-path, credential, dependency, license, and workflow
   reviews pass for the exact candidate.
5. A later separately authorized remote candidate receives Windows, Ubuntu, and
   macOS CI against the exact framework tag and commit.
6. Protected-main merge creates a new exact commit that receives a separate C4
   decision with final notes, tag, Release, and integrity settings review.

C2 permits implementation. Local C3 permits only this local candidate branch.
Neither permits remote push, PR, merge, tag, Release, private source/runtime
adoption, or a real-material action.

## Local C3 Progress

Conditions 1 through 4 have been reviewed for the local candidate tree:
the changes remain in scope; the new records validate and cross-reference;
full local regression passed 260 tests with 3 expected unconfigured-framework
skips; and scoped material, secret, dependency, and workflow review passed.
The active local candidate must be bound to its exact Git commit in the
separately reviewed C3 report; every later source change requires an M48
retest. Remote CI and all later conditions remain unapproved.
