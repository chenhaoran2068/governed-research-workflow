# Framework Integration Plan

Status: candidate integration validation passed against the exact released
Workspace Framework `v0.1.0` tag. A stable workflow release remains pending a
separate human decision.

## Current Position

`../../SYSTEM_MANIFEST.yaml` uses the public Workspace Framework's generic
system-manifest contract and declares both `standalone` and
`framework_integrated` for candidate validation. It has no required
dependency, optional shared service, absolute workspace path, or
private-runtime assumption.

The cross-repository integration test bootstraps an empty framework workspace,
places this concrete system package at `Systems/governed-research-workflow/`,
records a workspace-relative registration, and adds one synthetic
project-system binding. It validates the workspace, system, and binding records
against the framework schemas and exercises refusal cases for a non-integrated
workspace, unsafe registration path, and unregistered primary system.

The test does not create a real project, copy source data, grant access,
execute research, or establish any formal release compatibility.

## Validation Evidence

The earlier candidate validation proved that this package can participate in
the declared layout, but did not make an untagged framework a stable
dependency. The released-tag CI resolves `v0.1.0`, verifies that its commit
matches the checked-out framework source, and proves that the workspace
manifest version and system compatibility declaration both equal `0.1.0`.

This test proves a bounded technical integration contract. It does not approve
scientific quality, compliance, source access, project creation, or a workflow
release.

## Conditions Before Stable Release Advertising

Before a stable release advertises framework integration, maintainers must:

1. retain the passed cross-repository validation against the released `v0.1.0`
   tag and rerun it if the compatibility contract changes;
2. retain `0.1.0` in `framework_compatibility` and include the evidence in
   release notes;
3. define how this primary project-owning system behaves when optional shared
   services are unavailable;
4. prove standalone-equivalent human controls, no-data-access boundaries, and
   failure behavior in the integrated profile; and
5. retain regression coverage and receive an explicit release decision.

No private workspace, project, account, credential, data source, or absolute
path may be required to meet those conditions.
