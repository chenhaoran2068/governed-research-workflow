# v0.10.1 Release Notes

Status: versioned release notes for the v0.10.1 source scope. The normal
public-installation rule always requires an exact annotated tag and matching
GitHub Release for the selected version; this source file does not make a
hosted-release or installed-runtime claim.

## Added

- `GRW-CAP-101-01`: a self-controlled synthetic experience-exchange pilot
  receipt contract and an explicit read-only structural validator.
- Synthetic checks for named-path containment, link/reparse refusal,
  identity/revision/hash consistency, correction/future-use relationships,
  no-write behavior, unlisted-file exclusion, and CRLF/LF checkout stability.
- A bounded private-pilot protocol that distinguishes a clean-clone simulation
  from physical Computer B or external-contributor evidence.

## Compatibility

The v0.10 metadata-only experience-package schema remains `1.0.0`. Existing
v0.10 records are neither migrated nor rewritten. v0.10.1 adds an opt-in
receipt validator only when both explicit paths are supplied.

## Not Added

This version does not add public intake, external contributor support, real
experience handling, network upload/download helpers, identity or rights
verification, actual multi-machine proof, automatic review/promotion, or
correction/withdrawal/deletion/recall execution.
