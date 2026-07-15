# Manifest And Profiles

Status: active candidate system manifest; exact released-framework integration
evidence is available, while workflow release remains a separate decision.

`../../SYSTEM_MANIFEST.yaml` identifies this candidate, its entry point,
candidate profiles, project-ownership behavior, and data boundary.

`FRAMEWORK_INTEGRATION_PLAN.md` records the candidate cross-repository
validation and the remaining requirements before a stable release can
advertise the integrated profile.

The candidate supports `standalone` and a tested `framework_integrated`
profile. It passed against the exact released framework `v0.1.0` tag; a stable
workflow release still requires a separate maintainer decision.

Do not infer framework support merely because a host contains familiar folder
names or a manifest-looking file.
