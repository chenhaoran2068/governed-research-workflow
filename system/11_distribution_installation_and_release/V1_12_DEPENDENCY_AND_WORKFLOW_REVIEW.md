# v1.12.0 Dependency And Workflow Review

## Dependency Review

| Area | Result |
| --- | --- |
| New dependency, lockfile, or package | None |
| Existing structural validation dependency | `jsonschema==4.26.0` unchanged |
| External manager integration | None; the System does not operate a manager |
| Network or credentialed route | None |

## Workflow Review

The candidate preserves the three-platform Python 3.11/3.14 CI matrix. It
updates the exact public Framework integration fixture from v0.2.0 to v0.4.0,
whose reviewed commit is `30ba0f4032a90723612b6d213bd54faa7cce5aee`. The
cross-repository test remains synthetic and runs only against an empty
workspace. Local runs use the fixed Python interpreter, `-B`, and
`PYTHONDONTWRITEBYTECODE=1`.

No test opens a paper, PDF, manager database, configured service, real Study,
or real metadata handoff.

