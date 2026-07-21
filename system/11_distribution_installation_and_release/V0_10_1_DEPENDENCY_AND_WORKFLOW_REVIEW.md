# v0.10.1 Dependency And Workflow Review

Status: candidate review. Exact remote-CI evidence must be refreshed for the
later C3-remote candidate commit.

## Dependency Boundary

| Item | Decision |
| --- | --- |
| Python | Existing public baseline: Python 3.11+ |
| Runtime dependency | Existing pinned `jsonschema==4.26.0` only |
| New dependency | none |
| New network capability | none |
| New write capability | none |
| New credential or service requirement | none |

The new validator imports the existing v0.10 package validator from the same
package. It uses only declared local JSON files and standard-library hashing.
It must return `not_assessed` rather than misclassifying unavailable
`jsonschema` as invalid input.

## CI Requirement

The existing pinned GitHub Actions workflow must run the exact C3-remote
candidate on Windows, Ubuntu, and macOS. A green local run, private-pilot run,
or mutable branch cannot substitute for this exact candidate evidence.

## Compatibility Statement

The v0.10 experience-package schema stays at `1.0.0`; no existing package is
migrated or rewritten. v0.10.1 adds only an explicit optional receipt validator
that requires both a named package manifest and a named receipt. The receipt
hash normalizes physical CRLF/CR line endings only for already validated UTF-8
JSON metadata, so cross-platform checkouts do not create false drift.
