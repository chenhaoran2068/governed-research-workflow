# Public Material And Rights Review: v0.3.1 Historical Pre-Release Snapshot

Status: historical pre-release review snapshot for the published `v0.3.1`
release. It was completed before the annotated tag and matching GitHub Release
on `2026-07-16`; it is not current material or rights evidence for a later
candidate.

## Scope And Method

This review covers the tracked current tree and all history newly reachable
from the published v0.3.0 release up to the final pre-release v0.3.1 source
commit.
It requires a clean tree and uses:

~~~
git status --porcelain
git log v0.3.0..HEAD --format=%H%x09%an%x09%ae%x09%s
git ls-tree -r -l HEAD
git fsck --no-reflogs --no-dangling
~~~

It also uses a maintained pattern scan for common credentials, private keys,
private local paths, real-project identifiers, unpublished research material,
and restricted clinical-data markers. A pattern scan reduces risk but cannot
prove legal ownership, rights, or the absence of every sensitive fact.

## Reviewed Result

The pre-release v0.3.1 source contained generic documentation, blank templates,
standard-library helper code, tests, GitHub Actions configuration, and the
unmodified Apache-2.0 license text. It contains no Git submodules, Git LFS
objects, tracked file larger than 100 KiB, credential-pattern match, private
key, real research data, patient-derived material, unpublished manuscript,
restricted database extract, source PDF, reviewer correspondence, or private
absolute path.

The only reachable author identity is `Chen, Haoran
<chr17302561945@outlook.com>`. The accountable maintainer previously confirmed
that this generic package material and this public author identity may remain
public. That confirmation must be rechecked at R31-G6 for the exact final
release commit.

Terms such as `patient`, `ethics`, `DUA`, and clinical-database names occur
only in generic public-boundary instructions or tests that refuse prohibited
content. They do not indicate that the corresponding material is bundled.

## Scope Change From v0.3.0

The pre-release v0.3.1 source changed release-status wording, framework
validation evidence from the historical exact Framework v0.1.0 release to
exact Framework v0.1.1 validation, and release-governance records. It adds no
research execution, data-processing, network, credential, clinical,
compliance, migration, or autonomous-release capability.

## Rights And Stop Boundary

This record is technical and documentary evidence, not a legal opinion. Stop
the release if any contributor, license, institution, employer, contract,
privacy, confidentiality, data-use, or copyright question is unresolved. Do
not solve uncertainty by publishing with a disclaimer.

Before R31-G6, the accountable human must confirm that the exact final tree is
original or properly authorized, rights-cleared, free of restricted or private
material, and suitable for public publication under Apache-2.0.
