# V0.6 Synthetic Assurance

Status: v0.6 release-source synthetic assurance record. It records source-level
test evidence and is not a public Release, C4 authorization, hosted CI result,
or installed-runtime verification.

## Scope

The admitted `GRW-CAP-060-01` scope combines only public package schemas,
blank templates, one read-only validator, synthetic six-record bundles,
synthetic baseline manifests, and local regression tests. It checks explicit
input path safety, duplicate-key refusal, record shape, declared references,
problem-state visibility, revision/downstream-impact consistency, canonical
JSON identity comparison, and no unlisted-file read or output creation.

It does not open data or pointer targets, contact a URL or service, assess
citation entailment, verify a human identity or actual approval, decide
compliance/Gate/submission/release status, prevent same-authority rewrites, or
prove a real-study workflow.

## Required Release Evidence

- local positive, negative, path-safety, no-output, regression, and review
  evidence tied to an exact source commit;
- a clean Git-tracked source snapshot using the established M51 method;
- framework-integrated validation against Workspace Framework `v0.1.2` at
  `97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8`;
- successful Windows, Ubuntu, and macOS CI for the exact source commit;
- public-material, rights, dependency, capability-admission, C4, and
  post-release evidence kept as separate records.

No listed item is complete merely because this planning document exists.

## Local Source Test Evidence

This block records only a local source run. It is not remote CI, capability
admission, C4 authorization, a GitHub Release, or a runtime-install record.

- command: `python -m unittest discover -s tests -v`, with the exact local
  Workspace Framework `v0.1.2` checkout supplied only through the documented
  integration-test environment variables;
- local result: `121 passed / 0 failed / 0 skipped` on the release-source
  snapshot named below, using Python `3.13.14` on Windows;
- source snapshot SHA-256: `4b2a7b966c21694729eae4ef1f331c3083284ce6c8112d7bef949f5b28421db8`;
- snapshot method: the existing tested tracked-source snapshot helper hashes
  byte-sorted `git ls-files -z` relative paths and source bytes, normalizing
  text line endings while preserving NUL-containing bytes. This assurance file
  is excluded from its own digest;
- source-result boundary: a recorded local test result verifies only the
  named synthetic technical checks. It does not prove any hosted CI outcome,
  source truth, human authorization, compliance, release eligibility, or
  runtime identity.
