# Framework Integration Plan

Status: pre-release candidate validation is implemented. Exact released-tag
validation against Workspace Framework `v0.1.0` is pending CI.

## Current Position

`../../SYSTEM_MANIFEST.yaml` uses the public Workspace Framework's generic
system-manifest contract and declares both `standalone` and
`framework_integrated` for candidate validation. It has no required
dependency, optional shared service, absolute workspace path, or
private-runtime assumption.

The candidate integration test bootstraps an empty framework workspace, places
this concrete system package at `Systems/governed-research-workflow/`, records
a workspace-relative registration, and adds one synthetic project-system
binding. It validates the workspace, system, and binding records against the
framework schemas and exercises refusal cases for a non-integrated workspace,
unsafe registration path, and unregistered primary system.

The test does not create a real project, copy source data, grant access,
execute research, or establish any formal release compatibility.

## Candidate Validation Boundary

The earlier candidate validation proved that this package can participate in
the declared layout, but did not make an untagged framework a stable
dependency. The current CI must resolve the exact `v0.1.0` tag and prove the
checkout, workspace manifest, and system compatibility declaration agree.

## Conditions Before Stable Release Advertising

Before a stable release advertises framework integration, maintainers must:

1. rerun this cross-repository validation against the released `v0.1.0` tag;
2. record the released compatible version in `framework_compatibility` and
   release notes;
3. define how this primary project-owning system behaves when optional shared
   services are unavailable;
4. prove standalone-equivalent human controls, no-data-access boundaries, and
   failure behavior in the integrated profile; and
5. retain regression coverage and receive an explicit release decision.

No private workspace, project, account, credential, data source, or absolute
path may be required to meet those conditions.
