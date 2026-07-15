# Framework Integration Plan

Status: candidate integration validation is implemented. It is not yet a
stable-release compatibility claim.

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

Candidate validation uses the Workspace Framework's public candidate branch.
It proves the package can participate in the declared layout, but does not
make an untagged framework a stable dependency.

## Conditions Before Stable Release Advertising

Before a stable release advertises framework integration, maintainers must:

1. release and tag the reviewed Workspace Framework version, then rerun this
   cross-repository validation against that exact release;
2. record the released compatible version in `framework_compatibility` and
   release notes;
3. define how this primary project-owning system behaves when optional shared
   services are unavailable;
4. prove standalone-equivalent human controls, no-data-access boundaries, and
   failure behavior in the integrated profile; and
5. retain regression coverage and receive an explicit release decision.

No private workspace, project, account, credential, data source, or absolute
path may be required to meet those conditions.
