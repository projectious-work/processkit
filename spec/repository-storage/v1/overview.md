# Repository storage — overview

Non-normative. The requirements are in `requirements.md`.

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

Supporting context (not carried as requirements): the default
`apiVersion` value from `02-ontology.md`, the writing commands listed in
`06-cli.md` (PK-CLI-004), and the `processkit.toml` configuration layer in
`09-security-configuration-and-output.md`.

Gap items carried from the governance draft: none.

## Open questions

Mirrors `open` in `interfaces.yaml`.

1. OPEN-repository-storage-01 — `processkit.toml` key for the content
   directory; declaration of per-kind locations and document sources.
2. OPEN-repository-storage-02 — diagnostics for path rejection; which case
   normalization defines a collision.
3. OPEN-repository-storage-03 — exact front-matter delimiters, the safe YAML
   subset, and "declared structured region".
4. OPEN-repository-storage-04 — result fields for revision and the
   uncommitted marker, and their granularity.
5. OPEN-repository-storage-05 — how a user confirms an overwriting plan.
6. OPEN-repository-storage-06 — format of the plan and changed-files report.
7. OPEN-repository-storage-07 — vendoring mechanism, version/digest
   carriage, and the modified-copy diagnostic.
8. OPEN-repository-storage-08 — diagnostic for missing or unsupported
   `apiVersion`.
9. OPEN-repository-storage-09 — behavior when the content directory resolves
   into a nested repository or submodule.
10. OPEN-repository-storage-10 — reporting non-UTF-8 or CRLF input; how a
    schema defines key order.
11. OPEN-repository-storage-11 — location and authority of `skill.json`
    relative to `SKILL.md`.
12. OPEN-repository-storage-12 — diagnostic when a file tries to store an
    instance kind.
13. OPEN-repository-storage-13 — behavior where atomic replace is
    unavailable.
