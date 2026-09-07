# Paper Repository Standard v0.1

Status: System-owned reusable standard

This standard governs a public or controlled repository associated with one
research paper or one separately citable research output. It does not authorize
repository creation, external transfer, public release, data access, authorship,
licensing, or publication.

## 1. Purpose

A paper repository should let an independent reader answer five questions:

1. Which paper or research output does this repository support?
2. Which materials are included, and which materials are deliberately absent?
3. How can the included analysis or demonstration be run?
4. How can a reader tell whether the run completed correctly?
5. Which exact version should be cited?

The repository is a reviewed derivative. It is not the authority for the
Study's research question, governance status, real data, result authority,
manuscript authority, or submission history.

## 2. Ownership And Locations

| Layer | Purpose | Normal location | Authority |
| --- | --- | --- | --- |
| Study | Real project facts, approvals, data, code, results, manuscript, QA, and decisions | `Instances/<study-id>/` | Project authority |
| Local release record | Scope, restrictions, approvals, candidate identity, and release evidence | `<study-root>/07_analysis/public_release/` | Project release authority |
| Clean candidate | Newly built allowlisted public or controlled derivative | A collision-refusing candidate directory named in the release record | Candidate only |
| Repository worktree | Reviewed Git worktree for external delivery | `Github/<repository-name>/` | Public delivery surface only |
| Frozen release | Exact tag and release, optionally linked to a persistent archive | GitHub Release and approved archive | Citable delivery version |

Do not initialize Git in a Study root or in a staging directory that also
contains excluded material. Build a new clean candidate from an explicit
allowlist, validate that candidate, and only then place the reviewed derivative
in a repository worktree.

## 3. One Research Output, One Repository

The default unit is one repository for one paper or one independently citable
research output. This keeps its license, citation, release history, issues,
expected outputs, and retirement state understandable.

An exception may combine several papers only when they share one maintained
software product or one inseparable data resource. The release record must name
the reason, ownership, versioning model, and how each paper maps to exact files
and releases.

Repository names use the form
`<subject-or-domain>-<core-focus>-<output-type>`. The core-focus component may
be omitted when the remaining two components identify the output clearly. Use
lowercase ASCII letters, numbers, and hyphens. Select two or three stable,
discriminating elements; do not compress the complete research question into
the name.

Choose the elements according to the research type rather than forcing every
output into PICOS:

| Research type | Candidate naming elements |
| --- | --- |
| Observational | population or condition; exposure or factor; outcome or purpose |
| Causal or interventional | population or condition; intervention or exposure; outcome |
| Diagnostic | condition or use context; index test; diagnostic-accuracy output |
| Prognostic or prediction | target population or condition; predicted outcome; model output |
| Systematic review | topic, intervention, or exposure; main question; review output |
| Qualitative | population or context; phenomenon; qualitative output |
| Methods | method; problem or intended use; method or software output |
| Data or tool | domain or resource; principal function; dataset, software, or workflow output |

The release manifest records the selected components, which research
dimensions they represent, and the human rationale. The README and
`protocol/study-summary.md` retain the fuller identity: research type,
population or subject, context, intervention/exposure/focus, comparator when
applicable, outcome or objective, and time structure. Use `not applicable`
rather than inventing a PICOS element for a design that does not use it.

Do not put a target journal, acceptance or publication claim, confidential
Study identifier, or mutable version number in the repository name. Put
versions in tags and releases. Put additional discovery terms in the GitHub
description, repository topics, README, citation metadata, or an applicable
machine-readable metadata file instead of lengthening the repository name.

## 4. Choose A Release Profile

Every candidate declares exactly one primary profile.

| Profile | Use when | Minimum public evidence |
| --- | --- | --- |
| `code_with_synthetic_demo` | Real data cannot be redistributed, but a fully synthetic demonstration is safe and useful | Executable code, synthetic-data contract and generator, demo configuration, expected outputs, tests |
| `code_with_redistributable_data` | The selected data may lawfully be redistributed | Executable code, precise data provenance and license, checksums or manifest, expected outputs, tests |
| `code_with_access_instructions` | Code may be public but source data must be obtained separately | Executable code, data contract, access instructions, configuration example, tests that do not require restricted data |
| `materials_only` | No custom executable analysis is being released | Approved protocol, forms, supplementary material, or other named materials, with scope and rights stated |

The profile describes the package, not the strength or reproducibility of the
research. A repository must not imply that unavailable data were checked, that
a synthetic run reproduces real numeric results, or that public code grants
access to restricted sources.

## 5. Reader-Facing Structure

Use a small research-compendium structure. Do not copy the complete numbered
Study workspace merely to preserve internal lineage.

```text
README.md
CITATION.cff
LICENSE
LICENSE-DATA.md                 # when data or synthetic data are distributed
DATA_ACCESS.md
RELEASE_MANIFEST.json

protocol/
  study-summary.md
  analysis-specification.md

code/
  run-analysis.<ext>
  ...

config/
  example-config.*

demo/                           # when the selected profile uses a demo
  generate-synthetic-data.<ext>
  input/

expected/
  expected-output-contract.md
  small-reference-outputs/

tests/
  ...

.github/workflows/              # when GitHub Actions is approved
```

Only include directories that the selected profile needs. A simpler package is
preferable to empty ceremonial directories.

## 6. Required Content

### 6.1 README

The README must state:

- the paper or output supported by the repository;
- repository status: candidate, released, superseded, or retired;
- the selected release profile;
- included and excluded materials;
- system and software prerequisites;
- installation, configuration, and execution order;
- one shortest supported run command;
- expected run time and resource needs when known;
- where outputs are written and how they are validated;
- data-access and restriction boundaries;
- the exact version to cite after release;
- support, maintenance, and archival expectations.

### 6.2 Citation

Provide `CITATION.cff` at the repository root. Authors, order, identifiers,
title, repository version, release date, and preferred paper citation require
human confirmation. A release candidate must not present itself as an already
published final release.

### 6.3 Licenses And Rights

Record rights separately for code, data, synthetic data, text, figures, and
third-party material. One code license does not automatically license every
other file. Absence of a license is not permission to reuse.

### 6.4 Data Access

`DATA_ACCESS.md` must distinguish:

- data distributed in the repository;
- data generated synthetically;
- public data obtained from another provider;
- controlled or restricted data that users must obtain independently;
- data that cannot be shared.

It must name versions, source or provider, access route, restrictions, and the
relationship between demonstration outputs and real Study results without
exposing restricted details.

### 6.5 Execution And Environment

Provide one documented entry command for the shortest complete supported run.
Pin or record language and package versions. State required system libraries,
external tools, environment variables, and platform limitations. Do not commit
local package libraries, virtual environments, downloaded dependencies, caches,
credentials, or machine-specific configuration.

All code and configuration must use repository-relative paths or explicit
caller-provided paths. Hard-coded private paths are prohibited.

### 6.6 Expected Outputs And Tests

Describe the required output files, schemas, important invariants, and allowed
numeric tolerance. Separate:

- byte-identical outputs that may be checked by checksum;
- semantically equivalent outputs that require schema or tolerance checks;
- platform-dependent binary or rendered outputs that must not use unstable
  checksums as the only acceptance rule.

Include a small reference output when it is safe, licensed, useful, and not
misleading. A successful process exit alone is not evidence that the scientific
outputs are correct.

## 7. Prohibited Or Restricted Content

Do not release any of the following unless a separately documented authority
and review explicitly permit it:

- patient-level, person-level, restricted, controlled, or confidential data;
- real results that are not approved for release;
- credentials, tokens, passwords, private keys, cookies, or secret-bearing
  configuration;
- ethics attachments, data-use agreements, institutional correspondence,
  training records, or signatures;
- private local paths, usernames, device identities, internal addresses, or
  unredacted logs;
- copyrighted papers, questionnaires, images, or third-party code without
  redistribution permission;
- local package libraries, environments, caches, temporary files, model
  objects, bulky generated outputs, or unrelated history;
- author, affiliation, identifier, acknowledgement, or funding claims that the
  accountable humans have not confirmed.

Synthetic data must be newly generated. If its distributions, counts, rare
combinations, dates, or effect sizes were calibrated from restricted records,
that derivation requires explicit disclosure-risk and rights review. Renaming,
perturbing, sampling, or partially masking real records does not by itself make
them synthetic.

## 8. Candidate Construction

The release record, using the System-owned JSON template and schema, must
identify:

- exact private source pointers;
- an allowlist of files or generated derivatives to include;
- an explicit denylist and the reason for each category;
- the candidate destination;
- the selected release profile;
- transformations, redactions, and synthetic-generation steps;
- the candidate's file manifest and checksums;
- the reviewer and human approval gates.

The export operation must:

1. refuse to overwrite an existing candidate;
2. read only named sources;
3. write only below a new named destination;
4. copy only allowlisted files or create explicitly declared derivatives;
5. fail on missing required files, unexpected files, unsafe paths, or links;
6. produce a deterministic inventory for review;
7. never publish, commit, push, tag, or create a release automatically.

### 8.1 Promote The Reviewed Candidate To A Repository Worktree

Keep the release record, allowlist, denylist, review evidence, candidate
inventory, checksums, and human decisions under the Study's
`07_analysis/public_release/` area. These records remain the project authority.

Only after the exact clean candidate passes the declared pre-release checks
and a human confirms its name and public scope may it be promoted to a Git
worktree. In a Framework-integrated workspace, the normal worktree is
`Github/<repository-name>/`; a standalone installation must declare its
equivalent location. Copy only the files represented by the accepted candidate
inventory and verify their hashes after promotion. Do not copy the complete
Study, initialize Git in the Study root, or maintain an automatic bidirectional
sync between the Study and the repository worktree.

After commit, tag, and Release, write the exact commit, tag, release URL, and
any persistent identifier back to the Study-owned release manifest. The Git
worktree is the external delivery surface; it does not replace the Study's
authority records.

## 9. Validation Gates

### Gate A: Scope And Rights

- owners, coauthors, institution, provider, consent, privacy, DUA, embargo,
  copyright, and license conditions permit the proposed scope;
- author and citation metadata are confirmed;
- the selected release profile is truthful.

### Gate B: Clean Candidate

- the candidate was built from the recorded allowlist into a new directory;
- the inventory contains no unexpected file, symlink, reparse point, nested Git
  repository, local environment, cache, or oversized unexplained artifact;
- all text-like exported files were checked for secrets, direct identifiers,
  private paths, internal hosts, credentials, and restricted terms;
- automated scanning is treated as supporting evidence, not proof of safety.

### Gate C: Reproducibility

- a clean environment can follow the README from start to finish;
- dependency restoration and the shortest supported command work;
- required outputs pass contract checks;
- failure cases are understandable and do not silently fall back to private
  paths or unavailable data;
- supported operating systems are tested, while untested platforms are stated
  rather than implied.

### Gate D: Independent Review

- a reviewer who did not assemble the candidate checks scope, readability,
  rights, execution, output mapping, and manuscript consistency;
- unresolved high-severity findings block release;
- the accountable human accepts residual risks and the exact candidate.

### Gate E: Release And Citation

- the reviewed commit is identified exactly;
- the release tag and release notes identify the same content;
- `CITATION.cff`, README, manuscript availability statement, and archive record
  agree on the repository and version;
- a persistent archive identifier is recorded when used;
- the public URL is added to a manuscript only after it resolves to the approved
  release.

## 10. Lifecycle

Use the existing project release states:

| State | Meaning |
| --- | --- |
| `not_planned` | No repository release is currently planned. |
| `not_applicable` | A repository is not applicable to this output. |
| `blocked_by_restriction` | A known rights, privacy, ownership, or technical restriction blocks the proposed release. |
| `private_preparation` | Materials are being prepared locally; no external availability is implied. |
| `release_candidate` | One exact clean candidate has passed declared checks but still requires release approval. |
| `released` | The approved external release exists and its exact identity is recorded. |
| `retired` | The release is no longer maintained or recommended; retained versions remain traceable. |

Corrections after release use a new commit, tag, and release. Do not silently
rewrite a cited release. Before archiving or retiring a repository, update its
README and repository description, resolve or close active work where
appropriate, and record the successor or reason.

## 11. Relationship To The Paper

The manuscript and repository must agree about:

- what code, data, and materials are available;
- the exact repository and release identity;
- whether outputs are demonstrations or real Study results;
- data access and redistribution restrictions;
- software versions and execution scope;
- known limitations and unsupported platforms.

The repository must provide a mapping from key paper tables and figures to the
responsible code and expected output. This mapping supports review; it does not
replace the Study's result manifest or joint review.

## 12. External Reference Basis

This standard was informed by:

- GitHub documentation for [citation files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files),
  [licenses](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository),
  [releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases),
  [large files](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github),
  [repository archiving](https://docs.github.com/en/repositories/archiving-a-github-repository/archiving-repositories),
  and [secret scanning](https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning);
- published biomedical studies of
  [research-code sharing](https://pmc.ncbi.nlm.nih.gov/articles/PMC10441317/),
  [Jupyter notebook reproducibility](https://pmc.ncbi.nlm.nih.gov/articles/PMC10783158/),
  and [large-scale research-code execution](https://pmc.ncbi.nlm.nih.gov/articles/PMC8861064/),
  which document inaccessible repositories, missing dependencies, absent
  files, hard-coded paths, and non-reproducing analyses;
- the published [Reproduction Package](https://pmc.ncbi.nlm.nih.gov/articles/PMC8059663/)
  pattern and the Zenodo
  [research-compendium curation policy](https://zenodo.org/communities/research-compendium/curation-policy),
  which emphasize code, data, execution instructions, environment capture,
  expected results, licenses, and self-contained reproduction material.

External guidance is evidence, not project authority. Current links and their
applicability should be rechecked when a real Study prepares a release.

## 13. Human Decisions Required For Each Repository

Before any external action, the accountable human must approve:

- whether a repository will exist;
- repository owner, name, visibility, and audience;
- selected release profile and exact file scope;
- data, code, text, and figure licenses;
- author and citation metadata;
- supported platforms and reproducibility claims;
- exact candidate, commit, tag, release, and archive route;
- timing relative to submission, review, acceptance, embargo, and publication;
- maintenance owner, correction route, and retirement conditions.
