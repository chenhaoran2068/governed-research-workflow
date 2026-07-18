# Framework Integration Plan

Status: published `v0.3.1` integration validation targets the exact released
Workspace Framework `v0.1.1` tag. Historical `v0.3.0` evidence remains bound
to framework `v0.1.0` and is not reused as evidence for a later version. The
v0.6 release source retains integration evidence against released
Workspace Framework `v0.1.2` at commit
`97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8`.

## Current Position

`../../SYSTEM_MANIFEST.yaml` uses the public Workspace Framework's generic
system-manifest contract and declares both `standalone` and
`framework_integrated` for released-profile validation. It has no required
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

Published v0.3.1 validation proves that this package can participate in the
declared layout without making an untagged framework a stable dependency. Its
CI uses `v0.1.1` as the compatibility label but checks out and verifies the
recorded framework commit `b0e32d7710b70299e633df1316b6924cd87b647b`; it also
proves that the workspace manifest version and system compatibility declaration
both equal `0.1.0`. A later source revision must repeat this evidence for its
own exact source revision.

This test proves a bounded technical integration contract. It does not approve
scientific quality, compliance, source access, project creation, or a workflow
release. The v0.6 source rerun is technical evidence only; it does not itself
establish an exact tag, matching GitHub Release, C4 authorization, or runtime
identity.

## Conditions Before Later Release Advertising

Before a later stable release advertises framework integration, maintainers
must:

1. retain the historical passed cross-repository validation against the
   released `v0.1.1` tag, and retain/review the v0.6 source integration against
   `v0.1.2` at
   `97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8`;
2. retain `0.1.0` in `framework_compatibility`, while identifying the exact
   tested Framework release tag and commit in the compatibility evidence and
   release notes;
3. define how this primary project-owning system behaves when optional shared
   services are unavailable;
4. prove standalone-equivalent human controls, no-data-access boundaries, and
   failure behavior in the integrated profile; and
5. retain regression coverage and receive an explicit release decision.

No private workspace, project, account, credential, data source, or absolute
path may be required to meet those conditions.
