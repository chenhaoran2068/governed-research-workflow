# v0.10.0 Release Evidence: Historical Candidate Preparation

Status: historical C3-remote candidate evidence is recorded below for one exact
commit. It is not C4 authorization, a tag, GitHub Release, protected-main
evidence, or runtime-installation evidence. Any later commit requires affected
evidence to be repeated under M48.

| Field | Value |
| --- | --- |
| Intended version | `v0.10.0` |
| Public baseline | immutable `v0.9.0` at `d7b102619c761ffbd468254549177fb27f2aac01` |
| Reviewed implementation commit | `c3095d0bab9da8ddf3ae8c86dc93b9cc28fa2d5c` |
| Exact C3-remote candidate | `3edf684a94ab8becc958ea451e3b1f1e5a565990` on `v0.10.0-voluntary-experience-package-candidate` |
| Remote CI | [run 29738250097](https://github.com/chenhaoran2068/governed-research-workflow/actions/runs/29738250097): success on Windows, Ubuntu, and macOS with Python 3.11 and 3.14 |
| Evidence refresh | This historical document records the preceding remote result. Any later commit requires fresh affected-test and remote-CI evidence before C4 review. |
| Capability | `GRW-CAP-100-01` only |
| Framework evidence | existing v0.1.2 exact framework integration evidence must be retained/repeated |
| C4 identity | deliberately absent from this historical pre-C4 snapshot |

Local evidence must include the complete regression suite, dedicated package
tests, static public-boundary review, schema validation, no-write behavior, and
same-host simulation. Any later change invalidates affected evidence under M48.

The reviewed implementation commit passed `203` tests with `3` existing
environment-dependent skips and no failures. The later exact C3-remote
candidate passed `204` local tests with the same `3` existing skips, and its
remote CI passed on all six platform/Python jobs. Neither result replaces
protected-main review, C4, a hosted Release, or local-adoption evidence.
