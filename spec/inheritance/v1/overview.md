# Inheritance across repositories — overview

Non-normative. The requirements are in `requirements.md`.

## Purpose

Organizations govern in levels: a company sets rules, a business unit or
team refines them, and a project applies them and adds its own. In
processkit each level is a repository, and a repository inherits from the
levels above:

```text
company-standards        (governing)
  └── platform-team      (governing; inherits company-standards)
        └── payments-api (project; inherits platform-team)
```

This specification fixes how upstreams are declared, pinned in
`processkit.lock`, and fetched by explicit command; how the repository and
its locked upstreams resolve into one deterministic effective set of items;
how overrides, `final` items and rules, and declared winners between
upstreams work; that every served item carries provenance; how upstream
changes are reviewed; and that upstream access rules grant nothing
downstream unless imported. Reproducibility comes from exact commits and
digests; reviewability comes from the lock being an ordinary committed file.

## Boundaries

This slug does not cover:

- the item envelope, typed references (including resolving references to
  inherited items through the lock, PK-MODEL-022), and upstream ontology
  extensions — `ontology@v1`;
- the fields and schemas of each kind, including the Standard schema that
  defines `final` and `overrides` — `content-kinds@v1`;
- the location of `processkit.lock`, the `.processkit/` cache, atomic writes,
  and the Git read boundary — `repository-storage@v1`;
- command syntax, `--json` envelopes, `--dry-run`, exit codes, and the
  offline-read rule for an unfetched upstream — `cli@v1`;
- assembly inputs (the lock is one), caching by lock digest, and generation
  switching when the lock or cache changes — `mcp-context-serving@v1`;
- authenticators, Roles, Bindings, and the shared server —
  `access-control@v1`;
- threat model, untrusted upstream content, configuration layering —
  `security@v1`;
- the versioning of the lock format (PK-COMPAT-001) and resolution test
  coverage (PK-TEST-003) — release and verification requirements outside
  these feature slugs.

## Governing decisions

- **C5** Deterministic, cacheable assembly: the lock is an assembly input,
  so resolution must be deterministic for a revision and lock.
- **C6** Inheritance through locked upstream repositories: pinned upstreams,
  a lockfile, explicit overrides, final items, provenance, explicit fetch.
- **C7** Kubernetes-pattern access control: upstream Roles and Bindings are
  not effective downstream unless imported; access is deny-by-default.
- **C8** Two serving modes, read-only: serving never fetches or updates the
  lock; lock changes are reviewed file changes.

## Provenance

| Baseline (#197) | This slug |
|---|---|
| `spec/doc/v1/05-inheritance.md` — Declaring upstreams | PK-INH-001 to 004 |
| 05 — Resolution | PK-INH-010 to 016 |
| 05 — Upstream changes | PK-INH-020, 021 |
| 05 — Inherited access | PK-INH-030, 031 |
| `01-product-definition.md` — Goals | PK-PROD-009, PK-PROD-026 |
| `11-verification-and-release.md` — Acceptance journey 4 | journey 1 |

Supporting context (not carried as requirements): the `[[upstream]]`
example from chapter 05; `processkit lock`, `lock --update`, `fetch`,
`validate`, and `explain` from `06-cli.md`; `processkit.lock` and
`.processkit/` from `03-repository-and-files.md`; "upstreams, override
winners" in project configuration and "imported access rules" in operator
configuration from `09-security-configuration-and-output.md`; and the
`final`, `rules[].final`, and `overrides` fields of the published Standard
schema (`spec/schemas/v1/standard.schema.json`, owned by
`content-kinds@v1`).

Gap items carried from the governance draft: none.

Baseline tensions noted, not resolved here: PK-INH-030 speaks of the
"downstream configuration" importing access rules while chapter 09 lists
"imported access rules" in operator configuration (OPEN-inheritance-09);
PK-INH-012 lets an override replace an item, add rules, or change a rule's
level "as declared by the item's schema", but the Standard schema's
`overrides` object has no way to select that effect (OPEN-inheritance-04).

## Open questions

Mirrors `open` in `interfaces.yaml`.

1. OPEN-inheritance-01 — serialization, keys, and format version of
   `processkit.lock`; keying of transitive entries.
2. OPEN-inheritance-02 — algorithm and scope of the content digest; how a
   mismatch is detected at fetch.
3. OPEN-inheritance-03 — the `processkit.toml` key and granularity for
   declaring the winning upstream.
4. OPEN-inheritance-04 — `final` and `overrides` for kinds other than
   Standard; how a schema declares allowed override effects; how one
   overridden rule is identified.
5. OPEN-inheritance-05 — `lock --update` without NAME; whether plain `lock`
   re-resolves; confirmation after the change summary.
6. OPEN-inheritance-06 — provenance field names and repository identity;
   W3C PROV mapping.
7. OPEN-inheritance-07 — diagnostic codes and exit categories; whether a
   stale override fails validation or warns.
8. OPEN-inheritance-08 — the restricted marker field; restricted items under
   stdio.
9. OPEN-inheritance-09 — where and how access rules are imported (project or
   operator configuration).
10. OPEN-inheritance-10 — diamond transitive upstreams; whether an
    upstream's own lock is honoured.
11. OPEN-inheritance-11 — exact definition of a stale override (version
    mismatch or content digest change).
12. OPEN-inheritance-12 — computing "newly conflicting" and the JSON shape
    of the change summary.
13. OPEN-inheritance-13 — credentials for private Git sources.
