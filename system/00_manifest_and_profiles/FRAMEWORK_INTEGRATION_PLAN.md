# Framework Integration Plan

Status: design target only. This candidate does not currently advertise or
implement framework-integrated operation.

## Current Position

`../SYSTEM_MANIFEST.yaml` uses the public Workspace Framework's generic system
manifest contract, but declares only the `standalone` profile. It has no
required dependency, optional shared service, absolute workspace path, or
private-runtime assumption.

Using a compatible schema does not establish a runtime integration claim. The
system remains usable only with its bundled public resources and explicitly
provided user inputs.

## Conditions Before Advertising Integration

Before adding `framework_integrated` to `supported_profiles`, a future release
must:

1. validate against a released Workspace Framework version and record that
   compatible version in `framework_compatibility`;
2. provide a synthetic workspace manifest, a system registration, and a
   project-system binding using workspace-relative paths only;
3. define how this primary project-owning system behaves when optional shared
   services are unavailable;
4. prove standalone-equivalent human controls, no-data-access boundaries, and
   failure behavior in the integrated profile; and
5. add regression coverage and receive an explicit release decision.

No private workspace, project, account, credential, data source, or absolute
path may be required to meet those conditions.
