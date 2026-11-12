# New Study-Root Naming Convention

## Scope

This reference applies only when an accountable human explicitly asks how to
name a **new local Study root**. It is a documentation convention, not a
bootstrap command, registry, or discovery procedure.

It does not choose a number, inspect a workspace to find one, create a folder,
rename or move an existing folder, migrate a Study, or establish a Study's
research, governance, or publication status.

## Convention For A New Root

Use the following form when a numeric, human-readable local Study-root name is
wanted:

```text
Research<number>-<lowercase-hyphenated-slug>
```

The literal prefix is `Research` with an uppercase `R`. Write the numeric
sequence directly after it, then one hyphen, then an ASCII lowercase slug whose
words are separated by hyphens. For example:

```text
Research27-example-study
```

The number keeps a local sequence readable. The slug is a short stable topic
description; it is not a conclusion, journal name, release state, or version.

## Keep Identifiers Separate

The Study-root name is a filesystem location. It does not replace a separately
recorded `study_id` or a human-facing `study_title`. A Framework
`research_program_id` is also separate and continues to follow its own
lowercase-slug contract.

## Existing Studies

Existing roots may use earlier spellings such as an underscore after the
number, a lowercase `research` prefix, or other historical names. They remain
valid locations when a caller supplies their exact path. Do not rename them
merely to conform to this convention, and do not scan a directory to find them.

When a local implementation must identify the next number, it may recognize
known historical spellings for collision prevention only. That implementation
step remains local, explicit, and separately approved; this public reference
does not perform it.
