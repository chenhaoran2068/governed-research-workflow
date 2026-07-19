# v0.8.0 Public Material And Rights Review

Status: pre-C4 material-review record. It records the implementation and
protected-main review baseline; each later source change requires the affected
exact-tree checks to be repeated.
It does not certify legal, institutional, clinical, ethics, privacy, DUA, or
security compliance, and it does not authorize C4 publication.

## Reviewed Implementation Scope

The reviewed implementation diff from public `v0.7.1` through commit
`49102f9da068b290e311f63437351d1e1ce220e7` contains only generic package
documentation, JSON records and schemas, blank templates, and Python
regression tests for the three proposed v0.8 capabilities.

It introduces no data example, project record, manuscript, account material,
credential, private absolute path, third-party code or prose, image, dataset,
submodule, Git LFS object, binary artifact, dependency manifest change, or CI
workflow change. The candidate commits show the repository maintainer as the
author; that public Git identity was previously accepted by the accountable
human.

## Automated And Manual Boundary Checks

- Candidate-diff scans found no Windows or Unix private path, credential,
  token, key, patient identifier, or common secret-pattern match.
- Changed Python material contains no network client, subprocess invocation,
  or filesystem-write primitive. The v0.8 scope adds no helper script.
- The repository uses Apache-2.0. `requirements.txt` remains the existing
  fixed `jsonschema==4.26.0` dependency.
- GitHub Secret Scanning reported zero open alerts at review time. Dependabot
  alerts are disabled, and code scanning has no configured analysis; neither
  unavailable check is represented as a pass.

## Required Human Confirmation And Exact-Tree Refresh

On 2026-07-19, the accountable human confirmed that the reviewed generic tree
may be publicly released under Apache-2.0 and identified no employment,
institutional, confidentiality, copyright, contributor, or other restriction
blocking that publication. This confirmation does not replace the required
exact-tree refresh after any subsequent source change.

The exact final tracked tree, newly reachable history, generated source
archive, release notes, and planned Release assets must then be scanned again.
Any unknown, restricted, private, or third-party item stops release activity
until removed, licensed, or otherwise resolved through a new candidate.
