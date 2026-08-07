# Manifest And Profiles

The V1 Support Scope Matrix is the machine-readable authority for this
module's support posture; this boundary record does not enlarge that scope.

Status: v1.0.0 frozen public-interface source manifest. Historical synthetic
integration assurance and exact framework-integration evidence remain retained
as bounded evidence, not current release or runtime claims.

`../../SYSTEM_MANIFEST.yaml` identifies this system, its entry point,
supported profiles, project-ownership behavior, and data boundary.
`v1_public_interface_manifest.json` is the sole machine-readable inventory
of frozen public interfaces, while
`../../system/10_assurance_evaluation_and_audit/v1_capability_verification_map.json`
names their required v1 candidate-regression evidence.

`FRAMEWORK_INTEGRATION_PLAN.md` records the cross-repository validation for
the advertised integrated profile.

The system supports `standalone` and a `framework_integrated` profile. The
published `v0.3.1` patch retains the `0.1.0` framework-contract version and
validates that profile against the exact released framework `v0.1.1` tag. The
frozen v1 source retains exactly those two public identifiers and does not add
a private profile, service discovery, or a private-path fallback.

Do not infer framework support merely because a host contains familiar folder
names or a manifest-looking file.

The v0.4.0 release source adds
`capability_truth_ledger.json` as the single machine-checkable source for
capability promises, non-promises, evidence, version, and admission state. It
does not alter the package manifest's local `v0.3.2` identity, the released
`v0.3.1` historical public claim boundary, or create a `v0.4.0` Release. The
ledger records the accountable-human admission of the named release scope;
final exact-commit evidence and C4 remain separate. The historical v0.8.0
ledger records three verified, release-scope-admitted records; that admission
does not change the exact-tag-and-matching-Release rule or prove a real
Framework installation.

The v0.11 source extended the ledger's controlled capability identifier pattern
for `GRW-CAP-110-01` through `GRW-CAP-110-06`. v0.12 adds no identifier-pattern
change, profile, framework contract, dependency, helper, runtime, or
service-discovery behavior.

The v1.7 source extends the current ledger identifier pattern only for
`GRW-CAP-170-01`, Public Collaboration Guidance Derivatives. It does not alter
the frozen v1 public-interface inventory, profile, Framework contract,
dependency, helper, runtime, or service-discovery behavior.
