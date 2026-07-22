# v0.10.2 Dependency And Workflow Review

Status: local pre-C3-remote technical-review record for a zero-new-capability maintenance source. It does not certify hosted CI, dependency security, C3 authorization, C4 authorization, or publication.

## Dependency Boundary

| Item | Decision |
| --- | --- |
| Python | Existing public baseline: Python 3.11+ |
| Runtime dependency | Existing pinned `jsonschema==4.26.0` only |
| New dependency or lockfile | none |
| Validator or helper behavior | unchanged |
| New network, write, credential, or service capability | none |

`v0.10.2` changes no runtime executable code, schema, fixture, workflow, GitHub Action reference, Framework identity, or dependency declaration. Its maintenance changes are documentation and regression-test controls only.

## Workflow And Integrity Boundary

Any later exact remote candidate must retain the existing SHA-pinned Actions and exact Framework integration identity. The exact candidate must run the existing Windows, Ubuntu, and macOS CI matrix after separate authorization. A green local run, a private pilot result, or a mutable branch cannot substitute for that evidence.

## Required Rechecks Before C4

Compare the exact protected-main candidate with immutable `v0.10.1`; inspect every dependency and workflow path; rerun focused and full local tests; verify the required hosted CI results; and stop for any dependency, workflow, Framework-contract, or capability-scope drift. This review does not authorize changes to repository settings or external services.
