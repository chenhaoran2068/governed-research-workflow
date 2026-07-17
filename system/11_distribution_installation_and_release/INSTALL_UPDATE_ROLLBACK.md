# Manual Installation, Update, And Rollback

Status: operating contract for public v0.3.0 and later exact-tag releases. It
is not an automatic installer and does not authorize a research project, data
access, or workflow transition.

## Preconditions

- Use an existing exact Git tag and matching GitHub Release, not a mutable
  branch, for a normal installation.
- Read `CURRENT_RELEASE_STATUS.md` before selecting a tag. A locally retained
  candidate, historical release record, or capability-ledger target is not a
  substitute for the current public installation identity.
- Use Git and Python 3.11 or later. Python is required only for the optional
  empty-workspace bootstrap and test commands; the routing documents do not
  grant any execution authority.
- Keep the package directory separate from real study folders, data,
  manuscripts, credentials, and private records. Do not customize the package
  checkout with project material.
- Preserve a clean Git checkout. A local modification is not a supported
  upgrade target; use a documented fork or a separate private overlay instead.

## Verify The Selected Release

Use the repository's GitHub Release page to obtain the intended tag. Record
the displayed tag and commit identifier in the local operational record used
by the installer. A release is accepted only when the checked-out commit has
that exact tag:

~~~
git describe --exact-match --tags HEAD
git rev-parse HEAD
git status --porcelain
~~~

The first command must print the selected tag, the second identifies the exact
source commit, and the third must be empty. Do not use a mutable branch name
such as main as a release identity.

## Standalone Profile

Standalone means that the package uses only its bundled public resources. It
does not discover a private workspace, source library, account, or shared
service.

Install a selected release under Codex's skill directory. On Windows
PowerShell:

~~~powershell
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
$skillRoot = Join-Path $codexHome "skills\governed-research-workflow"
git clone --branch <selected-reviewed-tag> --depth 1 https://github.com/chenhaoran2068/governed-research-workflow.git $skillRoot
Set-Location $skillRoot
git describe --exact-match --tags HEAD
python --version
python -m unittest discover -s tests -v
~~~

The caller must replace <selected-reviewed-tag> only with an existing, reviewed
release tag.
Close and reopen Codex, then begin a new conversation so the installed skill
metadata can be discovered. The installation does not create a project.

Stop rather than overwrite when the destination already exists, the tag is not
exact, Python is below 3.11 and bootstrap/testing is needed, or validation
fails. The skill may still be used as a read-only routing document when Python
is unavailable; do not invoke its bootstrap helper in that case.

## Framework-Integrated Profile

Framework integration is optional. The v0.3.0 release was validated against
the exact released Governed Research Workspace Framework v0.1.0 tag. The
published v0.3.1 patch retains the v0.1.0 framework-contract version and is
separately validated against the exact v0.1.1 tag. Use only the framework
release explicitly named in the selected Workflow release notes and an existing
empty framework_integrated workspace created under that framework's own
controlled bootstrap procedure.

1. Independently obtain the exact Workspace Framework release named by the
   selected Workflow release and create an empty framework_integrated workspace
   using that framework's documented preview-and-confirm flow.
2. Clone the exact Workflow release into the workspace at
   Systems/governed-research-workflow/:

~~~text
git clone --branch <selected-reviewed-tag> --depth 1 https://github.com/chenhaoran2068/governed-research-workflow.git <workspace>/Systems/governed-research-workflow
~~~

   Do not copy private package files or install it through a hidden global
   path.
3. Confirm that Systems/governed-research-workflow/SYSTEM_MANIFEST.yaml
   exists and that its system_version is the exact selected release version.
4. Add exactly one workspace-relative registration to
   WORKSPACE_MANIFEST.yaml:

~~~yaml
registered_systems:
  - system_id: governed-research-workflow
    path: Systems/governed-research-workflow
    system_version: <selected-release-version>
~~~

5. Confirm that the workspace manifest uses workspace_profile:
   framework_integrated and the framework contract version named by the
   selected Workflow release. Do not create a project binding merely to prove
   installation; a binding belongs to a real project lifecycle and needs its
   own authorization.

The public integration test is a synthetic contract test. To rerun it from a
source checkout, set FRAMEWORK_REPOSITORY_ROOT and FRAMEWORK_RELEASE_TAG to
the exact framework release named by the selected Workflow release notes, then
run:

~~~
python -m unittest discover -s tests -v
~~~

Stop and remain standalone when the framework version differs, the profile is
not framework_integrated, the registration path is absolute or escapes the
workspace, the system is not registered exactly once, or optional shared
services are unavailable. No package behavior may silently repair these
conditions.

## Update

Update only a clean checkout. First record the installed tag and commit:

~~~
git status --porcelain
git describe --exact-match --tags HEAD
git rev-parse HEAD
~~~

If git status --porcelain is not empty, stop. Do not discard local changes or
use a force command. Obtain the next reviewed tag, inspect its release notes
and compatibility statement, then:

~~~
git fetch --tags --prune
git checkout --detach v0.3.1
git describe --exact-match --tags HEAD
python -m unittest discover -s tests -v
~~~

The literal v0.3.1 is a published annotated tag with a matching GitHub
Release. For any later version, use it only after the corresponding tag and
Release exist. For a framework-integrated installation, update the workspace
registered_systems.system_version only after the checkout and validation
succeed. Never change the framework version or project binding as a side effect
of a Workflow package update.

## Rollback

Rollback means returning only the public package to the previously recorded
clean tag or commit. It does not erase a project, data, or workspace state.

~~~
git checkout --detach <previous-reviewed-tag-or-commit>
git status --porcelain
git describe --exact-match --tags HEAD
python -m unittest discover -s tests -v
~~~

For framework integration, restore the matching previous
registered_systems.system_version only after the package rollback validates.
If a compatibility mismatch remains, stop the integrated profile and use no
automatic repair or destructive deletion. Record the reason, prior and new
identifiers, accountable approver, and validation result in the local
operational record.

## Failure Boundary

This package includes no system installer, updater, migration tool, data
importer, or automated rollback helper in v0.3.x. A failure to install,
validate, update, or roll back is an operational stop. It is not permission to
copy from a private system, edit manifests blindly, use an unreviewed branch,
or continue a consequential research task without the required controls.
