# v1.14.0 Dependency And Workflow Review

## Dependency Review

| Area | Result |
| --- | --- |
| New dependency, lockfile, or package | None |
| Existing structural validation dependency | `jsonschema==4.26.0` unchanged |
| Framework contract | Exact v0.4.0 unchanged |
| Skill bridge | Unchanged; the existing System entry only reads the added guidance for an explicit manuscript-work-sequence request |
| Network or credentialed route | None |

## Workflow Review

The candidate extends existing generic manuscript guidance with a Results-first
work sequence, a nested Results review sequence, assembly modes, and documented
exceptions. It adds source-free regression assertions for order, review,
exception, and refusal boundaries. Existing three-platform CI, release-control
checks, ethics-bridge checks, reading-bridge checks, and exact Framework
integration checks remain required. Local tests use Python 3.13 with `-B` and
`PYTHONDONTWRITEBYTECODE=1`.

No test opens a real Study, data, protocol, ethics/access/registration record,
paper, PDF, manuscript, figure, table, manager, configured service, or metadata
handoff.
