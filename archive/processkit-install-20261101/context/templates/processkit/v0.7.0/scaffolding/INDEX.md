# src/scaffolding/

Project-init templates that processkit ships for installation at a
consumer project's repository root or `context/` directory. Unlike the
catalog content under `src/{primitives,skills,processes,packages,lib}/`,
files here are **copied verbatim** (with placeholder substitution) into
the target project's filesystem at install time.

## Layout

```
src/scaffolding/
  INDEX.md             ← this file (not installed)
  AGENTS.md            ← installed at <target>/AGENTS.md
```

## Install rules

- The path inside `src/scaffolding/` is the relative path inside the
  target project. `src/scaffolding/AGENTS.md` → `<target>/AGENTS.md`.
  `src/scaffolding/context/foo.md` → `<target>/context/foo.md`.
- Placeholders use the form `{{PLACEHOLDER_NAME}}` and are substituted
  by the installer (or filled in manually for unmanaged installs).
- Files here must be **provider-neutral** (no Claude/Codex/Cursor
  references) and **aibox-neutral** (processkit must be consumable
  without aibox; see the standalone principle).

## Manual install

A consumer who installs processkit without aibox simply copies the
contents of `src/scaffolding/` from a tagged release into their project
root, then fills in the placeholders. No tooling required.

## What does NOT belong here

- Catalog content (primitives, skills, processes, packages, lib) — those
  live at `src/{primitives,skills,...}/` and are loaded by tooling, not
  installed at project root.
- Anything specific to a particular agent harness (Claude Code, Codex,
  Cursor, etc.) — provider-specific files are per-project pointers,
  created by the consumer as needed.
