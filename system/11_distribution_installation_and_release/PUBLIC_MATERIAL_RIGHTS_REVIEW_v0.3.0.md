# Public Material And Rights Review: v0.3.0 Candidate

Status: candidate review completed for the public tracked tree. Final release
authorization remains a maintainer action under R30-G6.

## Scope And Method

This review covers every tracked file in the v0.3.0-system-foundation
candidate branch, including history introduced relative to main. It uses:

~~~
git ls-files
git diff --name-status main...HEAD
git diff --check main...HEAD
git fsck --no-reflogs --full
git log --all --format=%H%x09%an%x09%ae%x09%s
~~~

It also uses a text scan for private local paths, common credential markers,
real-project identifiers, known local account markers, and sensitive clinical
database names. A scan is evidence of absence for the selected patterns, not
a legal guarantee or a substitute for maintainer knowledge.

## Reviewed Material Classes

| Material class | Included paths | Provenance and rights finding | Public decision |
| --- | --- | --- | --- |
| Package governance | root Markdown files, .gitignore, LICENSE, SECURITY.md, CONTRIBUTING.md | Generic package documentation authored for this repository. LICENSE is the unmodified Apache-2.0 license text. | Admit. |
| Thin skill and Codex metadata | SKILL.md, agents/openai.yaml | Generic operational instructions and interface metadata. No private runtime configuration or account credential. | Admit. |
| Route guidance | references/ | Generic rewritten workflow guidance. It links to no bundled paper, journal page, or proprietary source payload. | Admit. |
| Blank assets | assets/ | Empty templates and generic markers only. No real study, author, institution, patient, manuscript, or audit content. | Admit. |
| Controlled helper | scripts/bootstrap_empty_workspace.py | Repository-authored Python standard-library helper. No network, package, credential, or data-access implementation. | Admit. |
| Tests and CI | tests/, .github/workflows/ | Synthetic test fixtures only. GitHub Actions use pinned official Action commit SHAs. The test checks out the public Framework v0.1.0 tag but does not copy its source into this package. | Admit subject to the integrity policy. |
| System-foundation records | SYSTEM_MANIFEST.yaml, system/ | Generic module boundaries, installation contract, release controls, and synthetic integration description. Foundation-only modules do not contain an implementation or a private knowledge corpus. | Admit. |

## Explicitly Reviewed Exceptions

- LICENSE intentionally redistributes Apache License 2.0 text.
- Release-control documents link to official GitHub documentation and Semantic
  Versioning. They summarize the controls in original wording; they do not
  bundle third-party documentation.
- Tests contain private-path and project-name sentinel strings solely to assert
  that those markers are absent from the public system tree. They are not real
  local paths or project content.
- Terms describing sensitive data, credentials, and private-project sentinels
  occur only as prohibited-content descriptions or test sentinels. No
  associated material is included.
- The CI test installs validation-only dependencies from the exact public
  Workspace Framework v0.1.0 checkout. This package has no runtime Python
  dependency and no vendored third-party package.

## Prohibited-Material Result

The review found no tracked real project folder, raw or processed data,
patient-derived material, credential, secret, account token, private absolute
path, unpublished manuscript, reviewer correspondence, author list,
institution-specific record, source PDF, or database extract.

No Git LFS objects or Git submodules are present. The candidate contains only
text source, templates, tests, and the standard Apache-2.0 license. The
repository .gitignore excludes common research material, generated files,
credentials, and local configuration, but maintainers must still review staged
content before every release.

Candidate execution record: at candidate commit 503e270ef1ad852512b524bb4a9345c02d5f27ad,
the selected current-tree private-path and credential scan returned zero
matches. A reachable-history scan covered 16 commits and returned zero matches
for common GitHub-token, AWS-key, private-key, assignment-style secret, and
known local-path patterns. These are pattern-based checks with the limitations
described above.

## Rights And Provenance Limits

This review establishes a technical and documentation-level public boundary.
It cannot prove a contributor's legal ownership or authority outside the
repository. Before R30-G6 approval, the accountable maintainer must confirm
that each admitted contribution is original, properly authorized, or used
under a compatible license, and that no institutional, DUA, employment,
copyright, privacy, or confidentiality obligation prevents publication.

Any uncertain file is a release stop, not a reason to publish it with a
disclaimer. A future public contribution needs the same independent rewrite,
rights, provenance, privacy, and scope review before admission.
