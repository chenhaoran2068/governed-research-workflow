# v1.16.0 Dependency And Workflow Review

## Dependency Review

| Area | Result |
| --- | --- |
| New dependency, lockfile, or package | None |
| Existing structural validation dependency | `jsonschema==4.26.0` unchanged |
| Framework contract | Exact v0.4.0 unchanged |
| Style-source access | No external retrieval, account, subscription, manual download, or source copy route |
| Network or credentialed route | None |

## Workflow Review

The candidate adds a generic record for a selected manuscript style profile,
reporting-guidance status, target-journal requirement status, precedence,
conflicts, and source-boundary limits. The validator reads one named JSON
record and the package-owned schema only. It does not resolve references,
enumerate a workspace, inspect project material, download a manual, verify a
journal instruction, or write output.

The public System does not select `ama_11_default` or any other profile. A
private configuration may do so only after separately recording the Study,
profile source boundary, reporting-guidance status, target-journal state, and
accountable-human decision. Existing three-platform CI, release-control checks,
ethics-bridge checks, reading-bridge checks, Framework integration checks, and
full regression remain required. Local tests use Python 3.13 with `-B` and
`PYTHONDONTWRITEBYTECODE=1`.
