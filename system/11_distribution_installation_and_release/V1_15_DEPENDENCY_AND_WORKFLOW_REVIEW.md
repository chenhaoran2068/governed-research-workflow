# v1.15.0 Dependency And Workflow Review

## Dependency Review

| Area | Result |
| --- | --- |
| New dependency, lockfile, or package | None |
| Existing structural validation dependency | `jsonschema==4.26.0` unchanged |
| Framework contract | Exact v0.4.0 unchanged |
| Skill bridge | No new Skill bridge or automatic invocation; the System reads the guidance only for an explicit joint-review-plan task |
| Network or credentialed route | None |

## Workflow Review

The candidate adds generic profile selection/defer metadata, one default
R0-R10 dependency order, a specialist placeholder, Results work-unit assembly
states, and controlled reopen metadata. The validator reads one named plan and
the package-owned schema only. It does not resolve references, enumerate a
workspace, inspect project materials, or write output.

Existing three-platform CI, release-control checks, ethics-bridge checks,
reading-bridge checks, Framework integration checks, and full regression remain
required. Local tests use Python 3.13 with `-B` and
`PYTHONDONTWRITEBYTECODE=1`.
