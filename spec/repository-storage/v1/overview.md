# Repository storage — overview

Non-normative. The requirements are in `requirements.md`.

## Owner goal

The owner wants an organization's governance content to be ordinary,
reviewed files in Git that people and agents edit with their own tools.
processkit must never become a second store of truth, a memory, or a
recovery system (C1). It writes rarely, deterministically, and only over
committed files, so Git review shows every change and Git restores any
mistake (#213 finding 4). Any repository with a `processkit.toml` must work
offline, without a hosted service.

## Purpose

processkit's canonical content is ordinary, reviewed files in Git. This
specification fixes where those files live, how they are encoded and
serialized, how processkit writes the few files it writes, how release-owned
schemas and templates relate to a repository, and what processkit may and
may not do with Git. It also states the product boundary that processkit
stores definitions only, never instances such as events, logs, work items,
transcripts, or memories.

## Boundaries

This slug does not cover:

- the item envelope, `metadata`, relations, and the ontology registry —
  `ontology@v1`;
- the schemas, templates, levels, and fields of each content kind —
  `content-kinds@v1`;
- command syntax, exit codes, `--json` envelopes, and `--dry-run` —
  `cli@v1`;
- `get_context`, briefing, assembly, and caching semantics —
  `mcp-context-serving@v1`;
- upstreams, `processkit.lock` contents, `lock`, and `fetch` —
  `inheritance@v1`;
- authenticators, Roles, and Bindings — `access-control@v1`;
- threat model and size limits — `security@v1`;
- configuration layering and output rules — `cli@v1`;
- conversion of v0 content and treatment of v0 logs and memory —
  `v0-migration@v1`.

## Governing decisions

- **C1** Context, not memory: processkit stores reviewed governance files,
  no events, logs, instances, sessions, or memories.
- **C2** The full ontology is the definition language: definitions are
  stored; instance concepts are vocabulary only.
- **C6** Inheritance through locked upstreams: the lock plus committed files
  are the source from which caches and fetched copies are rebuilt.
- **C8** Two serving modes, read-only: no server writes content; content
  changes are file edits reviewed through Git.

## Provenance

| Baseline (#197) | This slug |
|---|---|
| `spec/doc/v1/03-repository-and-files.md` — Layout | PK-STORE-001 to 004 |
| 03 — File formats | PK-STORE-010 to 013 |
| 03 — Writing | PK-STORE-020 to 022 |
| 03 — Release-owned files | PK-STORE-030, 031 |
| 03 — Git boundary | PK-STORE-040, 041 |
| `01-product-definition.md` — Goals | PK-PROD-001 |
| `01-product-definition.md` — Non-goals | PK-PROD-020 |
| #213 finding 4 (owner decision, 2026-11-08) | PK-STORE-056 |
| Agent proposals resolving the open items | PK-STORE-042 to 055, 057 to 062 |

Supporting context (not carried as requirements): the default
`apiVersion` value from `02-ontology.md`, the writing commands listed in
`06-cli.md` (PK-CLI-004), and the `processkit.toml` configuration layer in
`09-security-configuration-and-output.md`.

Gap items carried from the governance draft: none.

## Resolved open items

| Item | Resolution | Basis |
|---|---|---|
| OPEN-repository-storage-01 | `[content] directory` in `processkit.toml`, default `context` (PK-STORE-042); fixed per-kind locations, Documents through document sources (PK-STORE-045); undeclared path arguments rejected (PK-STORE-047); `init` plans only `processkit.toml` (PK-STORE-060) | agent proposal |
| OPEN-repository-storage-02 | lexical normalization, NFC plus full case folding for collisions, one code per rejection, exit category by source (PK-STORE-055) | agent proposal |
| OPEN-repository-storage-03 | `---` / `---json` opening, `---` closing (PK-STORE-051); YAML 1.2 core subset without anchors, tags, merge keys, explicit keys, directives, several documents (PK-STORE-052); front matter is the only structured region in v1 (PK-STORE-053) | agent proposal |
| OPEN-repository-storage-04 | `schemas/revision.schema.json` in the envelope's `revision`; per-item `status.uncommitted` (PK-STORE-062) | agent proposal |
| OPEN-repository-storage-05 | mechanism and refusal are `cli@v1` PK-CLI-014; entries with action `replace` or `delete` need confirmation | baseline (`cli@v1` PK-CLI-014) |
| OPEN-repository-storage-06 | `schemas/file-change.schema.json` entries in `data.plan` and `data.changed`, sorted by path; unchanged files omitted; partial failure reported (PK-STORE-057) | agent proposal |
| OPEN-repository-storage-08 | missing: `ontology@v1` envelope diagnostic; unsupported: `storage.unsupported-api-version` (PK-STORE-061) | agent proposal |
| OPEN-repository-storage-09 | root must be the working-copy top level (PK-STORE-043); content directory in a nested repository fails; nested repositories in declared locations are skipped silently (PK-STORE-044) | agent proposal |
| OPEN-repository-storage-10 | `storage.invalid-encoding`, `storage.invalid-line-ending` (PK-STORE-048); no schema defines a key order in v1; concrete JSON serialization (PK-STORE-049); `format` behavior (PK-STORE-050) | agent proposal |
| OPEN-repository-storage-11 | `skills/<name>/skill.json` holds every structured field; `SKILL.md` front matter is kept and not interpreted except `name` (PK-STORE-054) | agent proposal |
| OPEN-repository-storage-12 | instance kinds get the `ontology@v1` instance-concept diagnostic (PK-MODEL-003); name and kind must match the location (PK-STORE-046) | agent proposal |
| OPEN-repository-storage-13 | named, exclusive temporary file, removed on failure, permissions kept (PK-STORE-058); no non-atomic fallback, `storage.atomic-replace-failed` (PK-STORE-059) | agent proposal |
| (write precondition) | every existing plan target is tracked and unchanged relative to `HEAD`; untracked and ignored targets fail; non-targets do not count; no bypass, no backup (PK-STORE-056) | owner decision: #213 finding 4 (2026-11-08), C1 |

## Open questions

Mirrors `open` in `interfaces.yaml`.

1. OPEN-repository-storage-07 — vendoring of release-owned schemas and
   templates. Recommendation: no vendoring mechanism and no release-pin key
   in v1; see `interfaces.yaml` for the alternative if the owner wants it.
