# v1.3.0 Release Notes

Status: pre-C4 prepared notes. These notes do not assert that a tag or GitHub
Release exists.

## Added

- `GRW-CAP-140-01`: generic, metadata-only proportionate historical-
  experience review and retrieval-index contract.
- A blank L1 decision-register template, schema, caller-named read-only
  validator, synthetic fixtures, and negative tests.
- Optional v2 reference-index linkage to a named `mapped` L1 decision with a
  canonical decision-metadata digest.

## Boundaries

- Four L1 outcomes are `mapped`, `not_mapped`, `deferred`, and `blocked`.
- A named batch contains at most twenty decisions; this does not replace one
  accountable-human final decision per source.
- The package does not read sources or pointers, create real mappings, infer
  terms, promote or integrate experience, provide intake/RAG/network action,
  or update a local runtime.
- Legacy v1.2 reference-index and mapping-decision inputs remain supported.
