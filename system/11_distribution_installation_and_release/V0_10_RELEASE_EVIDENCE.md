# v0.10.0 Release Evidence: Local Candidate Preparation

Status: local candidate evidence only. It is not remote CI, C4, a tag, GitHub
Release, or runtime-installation evidence.

| Field | Value |
| --- | --- |
| Intended version | `v0.10.0` |
| Public baseline | immutable `v0.9.0` at `d7b102619c761ffbd468254549177fb27f2aac01` |
| Reviewed implementation commit | `c3095d0bab9da8ddf3ae8c86dc93b9cc28fa2d5c` |
| Exact remote candidate | unresolved until a later evidence-only candidate commit is pushed under C3-remote |
| Capability | `GRW-CAP-100-01` only |
| Framework evidence | existing v0.1.2 exact framework integration evidence must be retained/repeated |
| C4 identity | deliberately unresolved until protected-main merge and separate C4 approval |

Local evidence must include the complete regression suite, dedicated package
tests, static public-boundary review, schema validation, no-write behavior, and
same-host simulation. Any later change invalidates affected evidence under M48.

The reviewed implementation commit passed `203` tests with `3` existing
environment-dependent skips and no failures. It left no bytecode cache and no
diff-check error. This local run does not replace the later exact remote
candidate, Windows/Ubuntu/macOS CI, protected-main review, C4, or local
adoption evidence.
