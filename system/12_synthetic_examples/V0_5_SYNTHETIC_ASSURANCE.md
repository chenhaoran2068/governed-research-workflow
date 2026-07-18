# V0.5 Synthetic Assurance

Status: pre-C3 candidate synthetic assurance evidence. It is not an exact
candidate-commit identity, public Release record, C4 authorization,
installed-runtime verification, or claim that a hosted release is ready.

## Scope

This route combines only public package documentation, blank templates,
synthetic metadata fixtures, and local regression tests. It checks the
candidate boundaries for `GRW-CAP-050-01`: metadata-only input, explicit
read-only validator invocation, safe paths, structural schema checks, no
unlisted-file read, dependency-version refusal, and current-versus-historical
release separation.

It does not access real data, a source locator, URL, credential, institution,
external service, installed runtime, or hosted GitHub state. Passing this route
does not prove data existence, access, permission, provenance truth, ethics,
DUA, privacy, legal, scientific, security, installation, or release
correctness.

## Candidate-Source Snapshot Identity

- working-tree source snapshot SHA-256: `56a445caf5d85d7aff69e86dbbd8fe38e4335e88f19585f266ed7e43d53ea2ce`
- snapshot method: SHA-256 over each `git ls-files -z` Git-tracked repository
  source file's UTF-8 relative path, a NUL separator, normalized source bytes,
  and a final NUL separator, in byte-sorted path order. Text files normalize
  CRLF and lone-CR line endings to LF; binary files containing a NUL byte remain
  byte-for-byte. This evidence file is excluded so it does not hash itself.
  Untracked or ignored directories and files, including CI framework checkouts
  and interpreter caches, are deliberately excluded.
- framework tag: `v0.1.1`
- framework resolved commit: `b0e32d7710b70299e633df1316b6924cd87b647b`

This is a transparent candidate-source snapshot. A later exact C3 candidate
commit and C4 decision must rerun the required checks and record their own
exact identities.

## Synthetic Evidence Boundaries

- register fixtures contain only synthetic metadata identifiers and
  `example.invalid` pointers;
- the validator returns `valid`, `invalid`, or `not_assessed` for bounded
  structural checks only;
- a valid structural result is not data access, sharing permission, scientific
  suitability, ethics/DUA/privacy/legal compliance, or provenance truth;
- no C4 authorization, tag, GitHub Release, merge, or runtime installation
  occurs in this test route.
