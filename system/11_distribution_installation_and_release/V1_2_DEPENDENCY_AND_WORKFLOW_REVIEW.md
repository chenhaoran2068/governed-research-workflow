# V1.2.0 Dependency And Workflow Review

Status: commit-neutral pre-C4 dependency and workflow review snapshot. This
record does not certify dependency security, current hosted CI, repository
settings, C4, an annotated tag, GitHub Release, or runtime installation.

| Surface | v1.2 versioned-source finding |
| --- | --- |
| Python baseline | unchanged: Python 3.11+ |
| Direct runtime dependency | unchanged: `jsonschema==4.26.0` |
| New dependency, lockfile, or package | none |
| New helper, generic writer, or executor | none |
| New public validators | two explicit caller-named, read-only structural validators; no automatic invocation |
| Data, network, credential, intake, or service capability | none |
| Public profiles | unchanged: `standalone` and `framework_integrated` |
| Framework change | none; the existing exact Framework `v0.1.2` / `97fbd1f4f3cbaabb2cdbb3e106c91a6c9fd8b3a8` remains the framework-integrated validation binding |
| GitHub Actions | unchanged: minimal `contents: read` permission, Windows/Ubuntu/macOS and Python 3.11/3.14 matrix, with reviewed full-SHA action references |

The v1.2 contracts add no data operation, real-source access, mapping action,
promotion, rule integration, external contribution route, generic writer,
agent runtime, or Framework capability. The direct dependency is pinned at the
package level but platform-specific transitive resolution is not hash-locked;
this record must not be read as a full supply-chain lock claim.

The existing GitHub Actions workflow is separately controlled platform evidence.
Before C4, verify the exact protected-main commit, dependency and workflow
files, branch protection, immutable-release posture, final notes, annotated
tag, matching Release, and generated source archives against the exact final
identity. Stop on drift.
