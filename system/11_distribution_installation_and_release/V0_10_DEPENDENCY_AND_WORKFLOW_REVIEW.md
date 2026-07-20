# v0.10.0 Dependency And Workflow Review

Status: source/dependency review plus a recorded C3-remote CI result for
`3edf684a94ab8becc958ea451e3b1f1e5a565990`. This document is not C4
authorization, a protected-main identity, a tag, GitHub Release, or runtime
installation evidence. Any later commit requires affected evidence to be
repeated under M48.

- Runtime dependency remains exactly `jsonschema==4.26.0`; no dependency file
  change is introduced.
- The new validator uses standard-library path/JSON facilities plus the existing
  pinned JSON Schema dependency. It imports no network client, Git wrapper,
  subprocess executor, database client, or write helper.
- Existing CI remains the Windows/Ubuntu/macOS Python matrix. The recorded
  C3-remote candidate passed [run 29738250097](https://github.com/chenhaoran2068/governed-research-workflow/actions/runs/29738250097)
  on all six Windows/Ubuntu/macOS and Python 3.11/3.14 jobs. Any later commit
  must repeat affected local and cross-platform verification.
- Existing standalone and framework-integrated profile tests remain required;
  no framework dependency or profile expansion is added.
- Protected-main, immutable-release, and required Action-SHA-pinning posture
  were independently rechecked during release preparation. They must be
  rechecked again against the later protected-main candidate before C4; this
  source review cannot create or substitute for those controls.
