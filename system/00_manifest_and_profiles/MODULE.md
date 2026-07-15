# Manifest And Profiles

Status: active public system manifest; exact released-framework integration
evidence is available.

`../../SYSTEM_MANIFEST.yaml` identifies this system, its entry point,
supported profiles, project-ownership behavior, and data boundary.

`FRAMEWORK_INTEGRATION_PLAN.md` records the cross-repository validation for
the advertised integrated profile.

The system supports `standalone` and a `framework_integrated` profile. The
unreleased `v0.3.1` maintenance candidate is retesting that profile against
the exact released framework `v0.1.1` tag.

Do not infer framework support merely because a host contains familiar folder
names or a manifest-looking file.
