# Public Material And Rights Review: v0.4.0 Historical Pre-C3 Candidate

Status: historical pre-C3 preparation record. It reviewed an uncommitted candidate
working tree at that time. It is not final evidence for an exact commit, a public
release, or C4 authorization. The review must be repeated after the candidate
commit is created and before any public release decision.

## Purpose And Boundary

The intended public package is a generic research-governance skill and system
foundation. It may include generic documents, blank templates, schemas,
standard-library Python, tests, CI configuration, and Apache-2.0 license text.
It must not include real research workspaces, patient or restricted data,
unpublished manuscripts, reviewer material, private audit trails, private
prompts, credentials, personal memory, local absolute paths, or third-party
content without a verified redistribution right.

## Required Pre-C3 Review Method

The preparation review must inspect the candidate worktree for:

1. tracked and untracked file inventory, proposed public scope, file size, and
   generated or binary artifacts;
2. credentials, private keys, connection strings, private local paths, and
   unexpected personal identifiers;
3. real-project, patient, restricted-data, unpublished-material, and
   third-party redistribution risks;
4. Git LFS, submodules, Actions/workflow references, dependencies, and planned
   Release assets; and
5. license, author/contributor, institution/employer, confidentiality, and
   publication-authority questions requiring accountable-human confirmation.

Pattern scans reduce risk but cannot prove legal ownership, rights clearance,
or absence of every sensitive fact. Terms such as `patient`, `ethics`, `DUA`,
or database names are acceptable only when used in generic boundary guidance or
synthetic refusal tests, never as bundled project content.

## Historical Pre-C3 Finding

On `2026-07-17`, the pre-C3 candidate worktree preparation scan found:

- `88` non-`.git` files; largest file `22,641` bytes; no PDF, Office, image,
  archive, or manually attached Release-asset file;
- no match for the maintained private-key, GitHub-token, cloud-key, OpenAI-key,
  connection-string, Windows drive-qualified, or user-home private-workspace
  path patterns;
- one email identity only: `chr17302561945@outlook.com`, the existing public
  Git author identity previously accepted by the accountable maintainer;
- no `.gitattributes`/Git-LFS configuration and no Git submodules;
- a passing `git fsck --no-reflogs --no-dangling` check and no whitespace error
  from `git diff --check` (Git reported local LF/CRLF conversion warnings only,
  not content errors); and
- two newly reachable committed history entries since `v0.3.1`, both authored
  by the same accepted public identity. The current v0.4 work remains
  uncommitted at the time and therefore was not part of that committed-history result.

The package contains no runtime Python dependency or lockfile. Its read-only
CI workflow has `contents: read` permission and uses full-SHA-pinned
`actions/checkout` and `actions/setup-python` references. The workflow installs
only the exact Workspace Framework `v0.1.1` validation dependencies for
synthetic integration testing; this is not a runtime dependency or a
hash-locked supply-chain claim.

This is a preliminary public-boundary pass for the local worktree, not a final
rights opinion or an exact-commit clearance. Before C4, repeat the scan and
review for the exact candidate commit, newly reachable history, generated
source archives, and any intended Release assets. The accountable human must
reconfirm publication authority, author identity, institutional/employer and
contributor rights, and Apache-2.0 suitability for that exact final tree.

## Stop Rule

Stop candidate progression if any rights, ownership, private-material,
institutional, employer, contributor, license, credential, or confidentiality
question remains unresolved. Do not cure uncertainty with a disclaimer,
redaction assumption, or an AI inference. Keep the item outside the candidate
until the accountable human has a documented basis for a decision.
