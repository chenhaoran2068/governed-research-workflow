# Data And Provenance

The V1 Support Scope Matrix is the machine-readable authority for this
module's support posture; this boundary record does not enlarge that scope.

Status: v0.4.0 released metadata-only register plus a published v0.5.0
metadata-only register set.

This public system does not process patient-derived data, restricted data, or
clinical databases. It may route a user to record data authority, provenance,
access restriction, and analysis boundary, but it does not certify those facts.

Future public content may define generic records or validation procedures only
after privacy, rights, provenance, and test review. It must not bundle raw data,
credentialed access instructions, institution-specific policy, or project data.

The released v0.4.0 scope adds a generic Data And Provenance Register and an
optional restricted or clinical awareness extension. It records metadata,
unknowns, and verification references only. It does not establish access,
ethics, consent, DUA, privacy, institutional, clinical, legal, or regulatory
compliance, and it does not process data content.

The published v0.5.0 baseline adds a bounded register-index contract and an
explicitly invoked read-only structural validator for v0.4-compatible entry records. It
checks only supplied metadata JSON, safe entry paths, identity uniqueness, and
declared reciprocal relationships. It neither reads data content nor proves
that a declared source, derivation, permission, or restriction is true.
