# Manifest And Profiles

Status: active public system manifest; exact released-framework integration
evidence is available.

`../../SYSTEM_MANIFEST.yaml` identifies this system, its entry point,
supported profiles, project-ownership behavior, and data boundary.

`FRAMEWORK_INTEGRATION_PLAN.md` records the cross-repository validation for
the advertised integrated profile.

The system supports `standalone` and a `framework_integrated` profile. The
published `v0.3.1` patch retains the `0.1.0` framework-contract version and
validates that profile against the exact released framework `v0.1.1` tag. The
local `v0.3.2` candidate preserves the same bounded contract.

Do not infer framework support merely because a host contains familiar folder
names or a manifest-looking file.

This unreleased candidate branch adds
`capability_truth_ledger.json` as the single machine-checkable source for
capability promises, non-promises, evidence, version, and admission state. It
does not alter the package manifest's local `v0.3.2` identity, the released
`v0.3.1` public claim boundary, or admit a `v0.4.0` capability.
