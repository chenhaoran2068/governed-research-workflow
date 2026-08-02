# Framework Integration Plan

Status: historical v0.3.0 through v1.5.0 integration evidence remains retained
under M54 and is not reused as v1.5.2 evidence. The v1.5.2 compatibility-
maintenance source declares only the exact released Workspace Framework
`v0.2.0` tag at commit `69c76f84a5b0913b26c17ea48f152dbc50b4bec6`.
Candidate and Release verification for this System remain separate from this
source declaration. A selected public version remains verifiable only through
its exact annotated tag and matching GitHub Release.

## Current Position

`../../SYSTEM_MANIFEST.yaml` uses the public Workspace Framework's generic
system-manifest contract and declares both `standalone` and
`framework_integrated`. For this v1.5.2 source, the latter declares only
Framework contract `0.2.0`; it does not imply a compatibility range. Explicitly invoked
structural validators require only the direct package dependency
`jsonschema==4.26.0`; they do not require the Workspace Framework, an optional
shared service, an absolute workspace path, or a private-runtime assumption.

The cross-repository integration test bootstraps an empty v0.2.0 framework
workspace, proves that it does not create a `Papers/` root, places this concrete
system package at `Systems/governed-research-workflow/`, records a workspace-
relative registration, and adds one synthetic project-system binding. It
validates the workspace, system, and binding records against the framework
schemas and exercises refusal cases for a non-integrated workspace, unsafe
registration path, and unregistered primary system.

The test does not create a real project, copy source data, grant access,
execute research, or establish any formal release compatibility.

## Historical Validation Evidence

Published v0.3.1 validation proves that the historical package could participate in the
declared layout without making an untagged framework a stable dependency. Its
CI uses `v0.1.1` as the compatibility label but checks out and verifies the
recorded framework commit `b0e32d7710b70299e633df1316b6924cd87b647b`; it also
proves that the workspace manifest version and system compatibility declaration
both equal `0.1.0`. A later source revision must repeat this evidence for its
own exact source revision.

The v0.6 release source retains integration evidence against released Workspace Framework `v0.1.2` at commit
`97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8`. That historical evidence remains
retained but is not reused as v1.5.2 evidence.

These historical tests do not establish v1.5.2 compatibility. They do not
approve scientific quality, compliance, source access, project creation, or a
workflow release.

## v1.5.2 Compatibility Evidence Requirements

The v1.5.2 candidate must rerun the cross-repository integration test against
only Framework `v0.2.0` at commit
`69c76f84a5b0913b26c17ea48f152dbc50b4bec6`, with no Framework skip. It must
prove the exact workspace and System contract match, safe workspace-relative
registration, schema validation, and the absence of a generated `Papers/`
root. This remains bounded technical evidence only; it does not establish an
exact System tag, matching GitHub Release, C4 authorization, or runtime
identity.

## Conditions Before Later Release Advertising

Before a later stable release advertises framework integration, maintainers
must:

1. retain historical cross-repository validation as historical evidence only,
   and create separate v1.5.2 evidence against `v0.2.0` at
   `69c76f84a5b0913b26c17ea48f152dbc50b4bec6`;
2. retain exact `0.2.0` in `framework_compatibility`, while identifying the
   exact tested Framework release tag and commit in compatibility evidence and
   release notes;
3. define how this primary project-owning system behaves when optional shared
   services are unavailable;
4. prove standalone-equivalent human controls, no-data-access boundaries, and
   failure behavior in the integrated profile; and
5. retain regression coverage and receive an explicit release decision.

No private workspace, project, account, credential, data source, or absolute
path may be required to meet those conditions.
