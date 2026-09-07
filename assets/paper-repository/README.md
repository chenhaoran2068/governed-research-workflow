# Public Release Templates

These templates prepare a Study-owned paper repository candidate. They are
scaffolds, not release approval.

Use them under the Study's `07_analysis/public_release/` area. Complete the
release record there before building a separate clean candidate directory.
Never copy this template directory directly to GitHub as if it were a completed
research package.

Files:

- `paper_repository_README.template.md`: reader-facing repository entry page.
- `DATA_ACCESS.template.md`: data availability, access, and restriction facts.
- `CITATION.template.cff`: citation metadata awaiting human confirmation.
- `paper_repository_release_manifest.template.json`: candidate and release
  identity, profile, rights, execution, testing, and human gates.
- `public_export_scope.template.json`: explicit source allowlist and denylist.
- `paper_repository_release_review.template.md`: human review and approval
  record.
- `gitignore.template`: baseline exclusions to adapt to the actual toolchain.

The governing rules are in
`references/paper-repository-standard.md`.

## Bounded tool use

Validate a completed scope record before external action by building into a new
directory:

```powershell
python scripts/build_paper_repository_candidate.py `
  --scope <study-root>\07_analysis\public_release\public_export_scope.json `
  --source-root <study-root> `
  --destination <new-candidate-directory>
```

Every `include` entry names one file. The builder does not recurse through a
directory, overwrite a candidate, initialize Git, or publish anything.

After the candidate contains the completed root records, validate it:

```powershell
python scripts/validate_paper_repository_candidate.py `
  --candidate <new-candidate-directory>
```

An automated `valid` result is only structural and technical evidence. It does
not prove privacy, rights, scientific correctness, author approval, or release
authority.
