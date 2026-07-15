# Manifest And Profiles

Status: active system manifest; framework-integrated profile is foundation
only.

`../SYSTEM_MANIFEST.yaml` identifies this candidate, its entry point, current
standalone profile, project-ownership behavior, and data boundary.

`FRAMEWORK_INTEGRATION_PLAN.md` states the conditions required before a future
release can advertise the integrated profile.

The system currently supports `standalone` only. A future framework-integrated
profile must declare a compatible framework version, workspace-relative paths,
shared-service dependencies, project-root behavior, and validation evidence.

Do not infer framework support merely because a host contains familiar folder
names or a manifest-looking file.
