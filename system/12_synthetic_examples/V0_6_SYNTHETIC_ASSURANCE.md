# V0.6 Synthetic Assurance Candidate

Status: local pre-C4 candidate assurance plan. This record will identify an
exact candidate commit only after implementation, review, and a clean source
snapshot are complete. It is not a public Release, C4 authorization, hosted
CI result, or installed-runtime verification.

## Candidate Scope

The proposed `GRW-CAP-060-01` scope combines only public package schemas,
blank templates, one read-only validator, synthetic six-record bundles,
synthetic baseline manifests, and local regression tests. It checks explicit
input path safety, duplicate-key refusal, record shape, declared references,
problem-state visibility, revision/downstream-impact consistency, canonical
JSON identity comparison, and no unlisted-file read or output creation.

It does not open data or pointer targets, contact a URL or service, assess
citation entailment, verify a human identity or actual approval, decide
compliance/Gate/submission/release status, prevent same-authority rewrites, or
prove a real-study workflow.

## Required Candidate Evidence

- local positive, negative, path-safety, no-output, regression, and review
  evidence tied to an exact local candidate commit;
- a clean Git-tracked source snapshot using the established M51 method;
- framework-integrated validation against Workspace Framework `v0.1.2` at
  `97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8`;
- successful Windows, Ubuntu, and macOS CI for the exact candidate commit;
- public-material, rights, dependency, capability-admission, C4, and
  post-release evidence kept as separate records.

No listed item is complete merely because this planning document exists.

## Local Candidate Test Evidence

This block records only a local source-candidate run. It is not remote CI, a
capability admission, C4 authorization, a GitHub Release, or a runtime-install
record.

- command: `python -m unittest discover -s tests -v`, with the exact local
  Workspace Framework `v0.1.2` checkout supplied only through the documented
  integration-test environment variables;
- local result: `120 passed / 0 failed / 0 skipped` on the candidate source
  snapshot named below, using Python `3.13.14` on Windows;
- candidate source snapshot SHA-256: `effb110fda008abc9068e2f5e9cb22eb6af01cb935210c67350d06fc4a6bc047`;
- snapshot method: the existing tested tracked-source snapshot helper hashes
  byte-sorted `git ls-files -z` relative paths and source bytes, normalizing
  text line endings while preserving NUL-containing bytes. This assurance file
  is excluded from its own digest;
- candidate-result boundary: a recorded local test result verifies only the
  named synthetic technical checks. It does not prove any hosted CI outcome,
  source truth, human authorization, compliance, release eligibility, or
  runtime identity.
