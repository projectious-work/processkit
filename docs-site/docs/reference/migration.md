---
sidebar_position: 3
title: "Version Migration"
---

# Version Migration

processkit is distributed as versioned releases. Upgrading pinned
versions is deliberate: processkit does not silently rewrite a consuming
project's context. A version bump should produce a `Migration` document
under `context/migrations/pending/` that the user and agent work through
together.

## The model

processkit ships a generic diff script (`scripts/processkit-diff.sh`) that
compares two tagged versions of any processkit-compatible source — upstream
processkit, a company fork like `processkit-acme`, or any other downstream.
The script reads `src/PROVENANCE.toml` at each tag (a single file mapping
every shipped file to the tag in which it last changed) and emits a
structured diff: added, removed, changed, unchanged.

Managed installers can consume this diff model. For example, when
`aibox sync` notices a new pinned version, it:

1. Fetches the new tag into `~/.cache/aibox/processkit/<version>/`
2. Calls the diff script (or reimplements its logic) to compare the
   currently-installed version against the new one
3. For each affected file, computes three SHAs on the fly:
   - **template SHA** — from the verbatim reference at
     `context/templates/processkit/<current-version>/<file>`
   - **cache SHA** — what the new upstream version says
   - **live SHA** — what's actually in the project right now

   and uses them to classify the file:
   - **changed-upstream-only** — safe to take with one approval
   - **changed-locally-only** — no-op for this migration
   - **conflict** — both sides changed, must be resolved by hand
   - **new-upstream** — added by upstream, decide whether to take it
   - **removed-upstream** — removed by upstream, decide whether to drop locally
4. Writes a `Migration` document to `context/migrations/pending/MIG-<id>.md`
   containing the briefing
5. Updates `context/migrations/INDEX.md` with the new pending entry
6. Reports the result and stops — **never auto-applies**

The user reads the briefing, approves a project-specific plan, and the
migration moves through `pending/` → `in-progress/` → `applied/`. See the
[`migration-management` skill](https://github.com/projectious-work/processkit/blob/main/src/context/skills/processkit/migration-management/SKILL.md)
for the workflow details.

## What's git-tracked vs cache

| Where | Git status | Purpose |
|---|---|---|
| `aibox.lock` (project root) | tracked | Pinned source URL + version + resolved commit (Cargo-style) |
| `context/templates/processkit/<v>/...` | tracked | Verbatim reference copy of every shipped file (the "as-installed" reference for diffs) |
| `context/migrations/pending/MIG-*.md` | tracked | Pending migration briefings |
| `context/migrations/in-progress/MIG-*.md` | tracked | Migrations being worked through |
| `context/migrations/applied/MIG-*.md` | tracked | Historical record |
| `context/migrations/INDEX.md` | tracked | Always-loaded summary |
| `context/.cache/processkit/...` | NOT tracked | Per-project runtime cache (e.g. SQLite index) |
| `~/.cache/aibox/processkit/<v>/...` | NOT tracked | aibox's fetched upstream cache, reproducible from the lock |

A new developer cloning the project gets `aibox.lock` + the reference
templates + migration documents from git. `aibox sync` fetches the
upstream cache as needed. Everything is reconstructible from the git
checkout.

## Upgrading

```toml
# aibox.toml
[processkit]
source           = "https://github.com/projectious-work/processkit.git"
version          = "v0.4.0"   # was: "v0.3.0"
src_path         = "src"      # default — matches upstream layout
```

Then:

```bash
aibox sync         # fetches new tag, generates the migration document
aibox migrate      # walks through the pending migration with you
<validator>        # structural validation after migration is applied
```

## v1 to v2 context migration

The v2 deliverable direction is intentionally breaking: processkit does
not provide compatibility shims that let v1 and v2 contracts coexist
inside the same shipped `src/` tree. A live v1 project context is valid
only as a migration source until the generated migration is worked
through.

The explicit path is:

1. Keep the live project on its pinned v1 processkit version until
   `aibox sync` creates the v2 `Migration`.
2. Review the generated briefing, including `source_api_version`,
   `target_api_version`, `source_processkit_version`, and
   `target_processkit_version`.
3. Run the v2 migration through `migration-management` with dry-run
   diagnostics first.
4. Apply the approved plan, then run structural validation and the
   processkit smoke checks.

This path is the only supported bridge for v1 contexts. v2 schemas and
index semantics are authoritative once the migration is applied.

See the v0.25.0 changelog for the public breaking-change summary.

## Configurable source URL

The `[processkit] source` field accepts any git URL. The default
upstream is `https://github.com/projectious-work/processkit.git`, but
companies can fork processkit into their own repository, customize it,
and have their projects consume the fork:

```toml
[processkit]
source  = "https://gitlab.acme.com/platform/processkit-acme.git"
version = "v0.4.0-acme.1"
```

The fork is responsible for regenerating its own `PROVENANCE.toml` against
its git history and tagging releases. The diff script and migration model
work identically for forks — they just see the fork's tags instead of
upstream's.

For forks pulling from upstream periodically, use the diff script
directly:

```bash
# Inside the processkit-acme checkout
scripts/processkit-diff.sh --from upstream/v0.4.0 --to upstream/v0.5.0 --format toml > upstream-changes.toml
```

The maintainer applies the changes to the fork manually, then re-tags as
e.g. `v0.5.0-acme.1`. ACME's projects then bump their `version` and run
`aibox sync` to pick up the changes.

## Pre-v0.4.0 behavior (deprecated)

Versions before v0.4.0 used a simpler model: every project copied the
processkit content into its own files, and `aibox migrate` produced
text-only migration documents at `context/migrations/<from>-to-<to>.md`.
This worked but had no concept of provenance, no manifest, and no way to
classify "user-modified vs unchanged" without manual diffing. The v0.4.0
model is a strict superset and is backward-compatible: pre-v0.4.0
migration documents are not touched and remain readable.

## What `aibox sync` will not do

- Auto-overwrite any file the user has touched (per the user-confirmed
  Strawman D rule)
- Apply changes from a pending migration without explicit user approval
- Re-generate a migration document for a version pair that already has
  one in `pending/` or `in-progress/` (it tells the user "pending
  migration exists, run `aibox migrate` to work on it")

## Downgrading

Downgrading is supported but discouraged. To downgrade:

```toml
[processkit]
version = "v0.3.0"   # was: "v0.4.0"
```

then `aibox sync`. If the downgrade skips past a schema `apiVersion` bump,
existing entities may become incompatible with the older schemas.
validation should flag the failures. You may need to manually edit or
delete incompatible entities.
