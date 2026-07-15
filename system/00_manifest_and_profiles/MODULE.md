# Manifest And Profiles

Status: active candidate system manifest; framework-integrated validation is
available but stable compatibility remains pending release evidence.

`../../SYSTEM_MANIFEST.yaml` identifies this candidate, its entry point,
candidate profiles, project-ownership behavior, and data boundary.

`FRAMEWORK_INTEGRATION_PLAN.md` records the candidate cross-repository
validation and the remaining requirements before a stable release can
advertise the integrated profile.

The candidate supports `standalone` and a tested `framework_integrated`
profile. The latter must still be retested against an exact released framework
version before it is advertised in a stable release.

Do not infer framework support merely because a host contains familiar folder
names or a manifest-looking file.
