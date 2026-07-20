# v0.10.0 Candidate Evidence Map

Status: candidate evidence map. It records a bounded local snapshot and one
exact C3-remote CI result. It does not prove a protected-main commit, C4
authorization, hosted Release, or installed runtime.

| Claim | Evidence | Limit |
| --- | --- | --- |
| Finite metadata-only manifest | `tests/test_voluntary_experience_package.py` valid/schema tests | Does not inspect real content. |
| Boundary refusal | Unsafe-path/link/no-discovery tests | Does not prove an unnamed file is safe. |
| Manual-review and withdrawal semantics | State-combination/non-substitution tests | Does not prove a decision, consent, or recall. |
| No validator write | Byte-for-byte fixture comparison | Does not prove another process did not write. |
| Same-host receive simulation | Explicit-copy test of named synthetic records | Not Computer B, cross-device, upload, or external-user evidence. |
| Public capability boundary | Ledger, admission record, reference, README, ROADMAP tests | Does not create a Release or local installation. |

Before C4, repeat affected local and cross-platform CI evidence for any commit
that follows the recorded remote candidate, then complete public-material,
rights/privacy, dependency, release-control, and exact-final-identity reviews.

## Local Verification Snapshot

| Field | Value |
| --- | --- |
| Reviewed implementation commit | `c3095d0bab9da8ddf3ae8c86dc93b9cc28fa2d5c` |
| Command | `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -p test_*.py` |
| Result | `203` passed; `3` existing environment-dependent skips; no failures |
| Hygiene | No `__pycache__`, `.pyc`, or `.pyo` artifact after the run; `git diff --check HEAD^ HEAD` passed. |
| Static boundary review | New public surface contained no local identity/credential marker; new validator contained no network, recursive discovery, or write executor. |
| Limitation | This is local evidence for `c3095d0...`, not remote CI, protected-main, C4, hosted Release, installed runtime, Computer B, or real contribution evidence. |

## C3-Remote Verification Snapshot

| Field | Value |
| --- | --- |
| Exact candidate | `3edf684a94ab8becc958ea451e3b1f1e5a565990` |
| Branch | `v0.10.0-voluntary-experience-package-candidate` |
| Local result | `204` passed; `3` existing environment-dependent skips; no failures |
| Remote result | [GitHub Actions run 29738250097](https://github.com/chenhaoran2068/governed-research-workflow/actions/runs/29738250097) succeeded on Windows, Ubuntu, and macOS with Python 3.11 and 3.14. |
| Limitation | This does not validate this later evidence-map revision, protected `main`, C4, a tag/Release, Computer B, real transfer, or a local runtime installation. |
