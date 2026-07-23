# V1 Dependency And Workflow Review

Status: local review passed for the reviewed local candidate tree. This
record does not certify dependency security, hosted CI, C4, Release, or runtime
installation.

| Surface | Intended v1 boundary |
| --- | --- |
| Python baseline | Python 3.11+ |
| Direct runtime dependency | `jsonschema==4.26.0` |
| New dependency, lockfile, or package | none |
| New helper, validator behavior, or agent runtime | none |
| New data, network, credential, intake, or service capability | none |
| Public profiles | unchanged: `standalone` and `framework_integrated` |
| Framework evidence | exact `v0.1.2`, commit `97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8`; no Framework change |

The existing workflow must remain read-only, use reviewed full action SHAs,
retain explicit minimal permissions, run the Windows/Ubuntu/macOS and
Python 3.11/3.14 matrix, and bind framework-integrated validation to the exact
framework tag and commit. Local regression cannot substitute for later remote
CI.

Before C4, inspect the exact protected-main commit, all dependency/workflow
files, the immutable-release and branch-protection posture, generated archives,
and the final notes. Stop on drift.
