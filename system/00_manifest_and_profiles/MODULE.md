# Manifest And Profiles

Status: v0.8 candidate public system manifest; exact released-framework
integration evidence remains available.

`../../SYSTEM_MANIFEST.yaml` identifies this system, its entry point,
supported profiles, project-ownership behavior, and data boundary.

`FRAMEWORK_INTEGRATION_PLAN.md` records the cross-repository validation for
the advertised integrated profile.

The system supports `standalone` and a `framework_integrated` profile. The
published `v0.3.1` patch retains the `0.1.0` framework-contract version and
validates that profile against the exact released framework `v0.1.1` tag. The
current v0.8 candidate source retains exactly those two public identifiers and
does not add a private profile, service discovery, or a private-path fallback.

Do not infer framework support merely because a host contains familiar folder
names or a manifest-looking file.

The v0.4.0 release source adds
`capability_truth_ledger.json` as the single machine-checkable source for
capability promises, non-promises, evidence, version, and admission state. It
does not alter the package manifest's local `v0.3.2` identity, the released
`v0.3.1` historical public claim boundary, or create a `v0.4.0` Release. The
ledger records the accountable-human admission of the named release scope;
final exact-commit evidence and C4 remain separate. The v0.8 candidate ledger
adds three forbidden candidate records; their presence does not change the
exact-tag-and-matching-Release rule or prove a real Framework installation.
