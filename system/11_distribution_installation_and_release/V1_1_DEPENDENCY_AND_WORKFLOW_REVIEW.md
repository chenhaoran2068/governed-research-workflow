# V1.1.0 Dependency And Workflow Review

Status: local review passed for the local candidate tree. This record does not
certify dependency security, hosted CI, repository settings, C4, Release, or
runtime installation.

| Surface | v1.1 candidate finding |
| --- | --- |
| Python baseline | unchanged: Python 3.11+ |
| Direct runtime dependency | unchanged: jsonschema==4.26.0 |
| New dependency, lockfile, or package | none |
| New helper or generic writer | none |
| Existing helper change | the existing empty-workspace bootstrap gains only reviewed empty directories and two draft/no-authority records |
| New validator or agent runtime | none |
| Data, network, credential, intake, or service capability | none |
| Public profiles | unchanged: standalone and framework_integrated |
| Framework change | none; the existing exact Framework v0.1.2 / 97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8 reference remains the framework-integrated test binding |

The existing GitHub Actions workflow remains the later authoritative platform
evidence path: Windows, Ubuntu, macOS, Python 3.11/3.14, reviewed action SHAs,
minimal permissions, and exact Framework binding. Local regression cannot
replace that later remote CI.

Before any C4 decision, inspect the exact protected-main commit, workflow and
dependency files, branch protection, immutable-release posture, final notes,
tag, Release, and generated source archives. Stop on any drift.
