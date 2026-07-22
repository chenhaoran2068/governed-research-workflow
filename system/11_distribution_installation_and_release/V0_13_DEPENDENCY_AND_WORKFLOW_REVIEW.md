# v0.13 Dependency And Workflow Review

Status: local pre-C3-remote technical-review record. It records the reviewed
source delta only; it does not certify hosted CI, dependency security, C3,
C4, publication, or runtime installation.

## Dependency And Interface Boundary

| Surface | Result |
| --- | --- |
| Public Python baseline | unchanged: Python 3.11+ |
| Direct runtime dependency | unchanged: `jsonschema==4.26.0` |
| New dependency, lockfile, or package | none |
| New operational schema, validator, helper, or agent runtime | none |
| New public data, network, credential, intake, or service capability | none |
| Existing helper and validator behavior | unchanged |
| Public profiles | unchanged: `standalone` and `framework_integrated` only |
| Framework integration identity | unchanged: Framework `v0.1.2`, commit `97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8` |

The new JSON Schema describes a static public support matrix. It has no
runtime invocation, CLI, helper, dependency, or network path. Existing
validators and bootstrap behavior remain the only pre-existing executable
interfaces and retain their existing boundaries.

## Workflow And Integrity Boundary

The existing workflow remains a read-only Windows, Ubuntu, and macOS matrix on
Python 3.11 and 3.14. Its GitHub Actions remain full reviewed commit SHAs, and
it retains the exact Framework checkout identity above. The v0.13 exact
candidate must receive a separately authorized fresh three-platform matrix
run after it is pushed; local regression cannot substitute for it.

GitHub documentation states that Releases are based on Git tags and that an
immutable Release locks the associated tag and Release assets after
publication. Therefore the exact protected-main commit, draft material, tag,
and Release content must be reviewed before C4 rather than repaired in place
after publication. See:

- <https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases>
- <https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases>

## Required Rechecks Before C4

Compare the exact protected-main candidate with immutable `v0.12.0`; inspect
every dependency, workflow, script, schema, capability-ledger path, and
matrix-related public claim; re-run focused and full local tests; verify
hosted CI; recheck protected-main and immutable-release posture; then obtain
an exact human C4 decision. Stop for any new operational interface,
dependency, workflow, Framework-contract, capability, or public-boundary
drift.
