# V0.7 Release-Source Synthetic Assurance

Status: historical v0.7.0 release-source synthetic-assurance snapshot. It
records the local source-level test evidence used before the v0.7.0 exact-commit
review. It is retained as historical evidence only; it is not a public Release,
capability admission, C4 authorization, hosted-CI outcome, current-source
identity, or installed-runtime verification.

## Scope

The v0.7 release source combines only generic schemas, blank templates, one
read-only validator, synthetic bundles, public documentation, and regression
tests. It checks explicit input-path safety, duplicate-key refusal,
automatic-promotion refusal, cross-record candidate/decision/integration
consistency, visible supersession, no unlisted-file read, no output creation,
and no supersession cycle.

It does not read project material or data, follow pointers, contact services,
verify a human identity or actual authority, modify a target, make a scientific
or compliance decision, or prove public availability or runtime identity.

## Local Source Test Evidence

This block was completed from the staged release-source tree before its
exact-commit review. The source snapshot excludes this file only, because the
file records its own digest; every other intended release-source file was
staged before calculation.

- source snapshot SHA-256: `40ee245ab08c26b6f3abe5c0bfa75ef27f12d82f3d82ed7ae9649102fbe409a3`;
- snapshot method: the established tracked-source helper hashes byte-sorted
  `git ls-files -z` relative paths and source bytes, normalizing text line
  endings while preserving NUL-containing bytes; and
- result boundary: a local test result validates only the named synthetic
  technical checks. It does not prove hosted CI, human approval, capability
  admission, C4 authorization, public Release, or local runtime adoption.
