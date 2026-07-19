# Controlled Helper Admission

This reference describes the generic v0.8 helper-admission record. It states
the bounded contract and evidence for a named helper. It is not a per-run approval.
It does not authorize a particular run or grant data access. It is not a public
Release and does not create a local runtime installation. It is not a public Release.

## Initial Scope

The only v0.8 helper-admission record covers the existing
`bootstrap_empty_workspace.py` helper. Its permitted action remains narrowly
limited to a new empty workspace scaffold:

1. the caller supplies an existing physical root outside the skill package;
2. the helper returns a no-write preview;
3. the accountable human approves that exact plan with a nonempty reference;
4. the helper rechecks root identity, links/reparse points, target emptiness,
   and the matching plan ID before writing; and
5. it writes only its allowlisted empty scaffold through owned staging, then
   records a receipt and generated-file hashes.

It is no generic writer: it is not a generic writer and never becomes one. It
cannot read/copy/hash data, access
credentials or the network, call an external service, analyze research,
change a project Gate, create a manuscript, release or submit material,
install a runtime, overwrite a target, resume a prior write, or delete user
content.

## Non-Substitution Rule

Helper admission is generic evidence about a named helper. It is not M53
authorization, a role contract, data/share authority, a project decision, or
the individual preview confirmation required before one filesystem write.

The presence of `framework_integrated` in an admission record means only that
the generic helper's empty-scaffold boundary is tested under that public
profile. It does not install any system into a Framework workspace or prove a
real workspace integration.

## Residual Risk

The record and helper do not enforce operating-system permissions and cannot
stop a same-authority person from bypassing the package outside the helper.
They provide a narrow, tested refusal boundary, not universal safety or
tamper-proof storage.
