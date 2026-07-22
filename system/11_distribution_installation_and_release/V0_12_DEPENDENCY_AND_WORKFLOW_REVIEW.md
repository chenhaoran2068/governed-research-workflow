# v0.12 Dependency And Workflow Review

Status: local pre-C3-remote technical-review record. It records the reviewed
source delta only; it does not certify hosted CI, dependency security, C3,
C4, publication, or runtime installation.

## Dependency And Interface Boundary

| Surface | Result |
| --- | --- |
| Public Python baseline | unchanged: Python 3.11+ |
| Direct runtime dependency | unchanged: `jsonschema==4.26.0` |
| New dependency, lockfile, or package | none |
| New schema, validator, helper, or agent runtime | none |
| Existing helper behavior | unchanged |
| New network, credential, data, or service capability | none |
| Public profiles | unchanged: `standalone` and `framework_integrated` only |
| Framework integration identity | unchanged: Framework `v0.1.2`, commit `97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8` |

The new integration test imports existing explicit validators only inside the
test process. It does not expose a new public validation command or modify an
existing script interface.

## Workflow And Integrity Boundary

The existing workflow remains a read-only Windows, Ubuntu, and macOS matrix
on Python 3.11 and 3.14. Its GitHub Actions remain full reviewed commit SHAs,
and it retains the exact Framework checkout identity above. The v0.12 exact
candidate must receive a separately authorized fresh three-platform matrix
run after it is pushed; local regression cannot substitute for it.

## Required Rechecks Before C4

Compare the exact protected-main candidate with immutable `v0.11.0`; inspect
every dependency, workflow, script, schema, and capability-ledger path;
re-run focused and full local tests; verify hosted CI; recheck protected-main
and immutable-release posture; then obtain an exact human C4 decision. Stop
for any new interface, dependency, workflow, Framework-contract, capability,
or public-boundary drift.
