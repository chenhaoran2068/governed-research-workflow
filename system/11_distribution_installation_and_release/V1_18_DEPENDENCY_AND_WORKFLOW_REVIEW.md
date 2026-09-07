# v1.18.0 Dependency And Workflow Review

## Dependency Review

| Area | Result |
| --- | --- |
| Python dependency | Existing `jsonschema==4.26.0`; no new dependency |
| Framework contract | Exact v0.4.0 unchanged |
| Network or credential route | None |
| Git/GitHub library | None |
| Real Study or data dependency | None |

## Workflow Review

The status validator reads one caller-named JSON snapshot, its package-owned
schema, and stage catalogue. It does not discover or write a Study.

The paper candidate builder reads one caller-named JSON export scope and only
the explicitly listed regular files. It writes to one new caller-named
destination, removes that incomplete destination on a failed build, and writes
a checksum inventory. It never initializes Git or performs network activity.

The paper candidate validator reads one caller-named candidate and its
package-owned schema. It reports structural and selected risk markers but does
not decide privacy, rights, science, or release approval. Real release work
still requires independent review and an accountable-human decision.

Existing three-platform CI and full regression remain required.
