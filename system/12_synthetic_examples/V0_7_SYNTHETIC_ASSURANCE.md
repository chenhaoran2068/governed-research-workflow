# V0.7 Candidate Synthetic Assurance

Status: candidate synthetic-assurance evidence. It records local source-level
test evidence only. It is not a public Release, capability admission, C4
authorization, hosted-CI outcome, or installed-runtime verification.

## Scope

The v0.7 candidate combines only generic schemas, blank templates, one
read-only validator, synthetic bundles, public documentation, and regression
tests. It checks explicit input-path safety, duplicate-key refusal,
automatic-promotion refusal, cross-record candidate/decision/integration
consistency, visible supersession, no unlisted-file read, no output creation,
and no supersession cycle.

It does not read project material or data, follow pointers, contact services,
verify a human identity or actual authority, modify a target, make a scientific
or compliance decision, or prove public availability or runtime identity.

## Local Source Test Evidence

This block was completed from the staged candidate tree before its exact-commit
review. The source snapshot excludes this file only, because the file records
its own digest; every other intended candidate file was staged before
calculation.

- source snapshot SHA-256: `f09719290290502d2de1d77c7e1af8331cc1d126403c3b05e52bf304db0e07e6`;
- snapshot method: the established tracked-source helper hashes byte-sorted
  `git ls-files -z` relative paths and source bytes, normalizing text line
  endings while preserving NUL-containing bytes; and
- result boundary: a local test result validates only the named synthetic
  technical checks. It does not prove hosted CI, human approval, capability
  admission, C4 authorization, public Release, or local runtime adoption.
