# Inheritance across repositories — overview

Non-normative. The requirements are in `requirements.md`.

## Owner goal

The owner wants organizations to govern in levels: a company sets rules, a
team refines them, and a project applies them, each level in its own
repository (PK-PROD-009, C6). Every inherited rule must come from an exact,
reviewed upstream commit, every override must be explicit and justified,
and every served item must say where it came from, so that agents and
reviewers can trust what they receive. Network access and lock changes
happen only by explicit command and are reviewed as ordinary file changes
(PK-PROD-026, C8; owner decision #213 finding 3: fetch, then lock).

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

This specification fixes how upstreams are declared, fetched by explicit
command, and then pinned in `processkit.lock` from the fetched data; how
the repository and
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
- command syntax, `-o json` envelopes, `--dry-run`, exit codes, and the
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

Baseline tensions, resolved: PK-INH-030 speaks of the "downstream
configuration" importing access rules while chapter 09 lists "imported
access rules" in operator configuration; the import is an operator key
(PK-INH-059). PK-INH-012 lets an override replace an item, add rules, or
change a rule's level "as declared by the item's schema"; the Standard
schema gains `spec.overrides.effect`, `ruleLevels`, and `addRules` (owned
by `content-kinds@v1`), whose semantics are PK-INH-051.

Owner decision #213 finding 3 (2026-11-08), "fetch, then lock", changed
PK-INH-002 and PK-INH-004: `processkit lock` resolves only from the local
cache (`cli@v1` PK-CLI-044), and `processkit fetch` also fetches declared
upstreams that are not locked yet (PK-INH-036).

Owner decision 2026-11-11 (#212), CLI style B, changed PK-INH-020 and
PK-INH-043: `processkit lock --update [UPSTREAM...]` replaces
`lock --update [NAME]` and accepts several upstreams. Item provenance is
shown by `processkit describe TYPE NAME`, which replaces `explain KIND NAME`
(ADR `docs/adr/0001-cli-command-style.md`).

## Resolved open items

| Item | Resolution | Basis |
|---|---|---|
| OPEN-inheritance-01 | `processkit.lock` is JSON (`schemas/lock.schema.json`, PK-STORE-049 serialization), `apiVersion` `lock.processkit.projectious.work/v1`, entries `{name, source, ref, commit, digest}` sorted by name; transitive entries named `<introducer>/<name>` (PK-INH-040); `[[upstream]]` keys and source forms (PK-INH-032); ref resolution order (PK-INH-035) | agent proposal |
| OPEN-inheritance-02 | SHA-256 over a sorted manifest of every file and symbolic link of the commit tree (PK-INH-038); verified when fetch stores a commit, mismatch `inheritance.digest-mismatch` (PK-INH-037) | agent proposal |
| OPEN-inheritance-03 | `[[winner]]` tables with `item` (typed name) and `upstream`, one item each; `inheritance.winner-invalid`, `inheritance.winner-unused` (PK-INH-049) | agent proposal |
| OPEN-inheritance-04 | overrides and `final` only for kinds whose schema defines them, as `content-kinds@v1` declares (PK-INH-050); `spec.overrides.effect` `replace` (serve the overriding item) or `amend` (upstream item with `ruleLevels` applied and `addRules` appended), rules matched by `id` (PK-INH-051); final rule change defined per effect (PK-INH-052); field shapes owned by `content-kinds@v1` | agent proposal |
| OPEN-inheritance-05 | plain `lock` keeps unchanged declarations and resolves new or changed ones from the latest fetch (PK-INH-042); `--update` without UPSTREAM re-resolves all, each UPSTREAM only that upstream (PK-INH-043); confirmation only by `cli@v1` rules (PK-INH-044); fetch result data (PK-INH-039) | owner decision: #213 finding 3; agent proposal |
| OPEN-inheritance-06 | `status.provenance` per `schemas/provenance.schema.json` (`origin`, `overrides`, `restricted`, `restrictedBy`); repository identity is lock entry name plus source; `status.references[].origin` is the target's `provenance.origin` (PK-INH-055); PROV mapping, no PROV output (PK-INH-056) | agent proposal |
| OPEN-inheritance-07 | `inheritance.*` codes with category and scope in `interfaces.yaml` `errors` (PK-INH-054); stale override is a validation failure (PK-INH-053); lock checks (PK-INH-045); upstream errors (PK-INH-048) | agent proposal |
| OPEN-inheritance-08 | `[downstream] restricted` in the providing repository's `processkit.toml` (PK-INH-061); stdio and CLI serve restricted items to the local principal (PK-INH-062) | agent proposal |
| OPEN-inheritance-09 | operator key `inheritance.import-access-rules`, lock entry names; project configuration cannot import (PK-INH-059); imported rules add grants, "downstream rules" are the downstream's own (PK-INH-060) | agent proposal |
| OPEN-inheritance-10 | transitive entries copied from each upstream's own lock, never re-resolved (PK-INH-041); recursive effective sets (PK-INH-046); identical diamond candidates merge, different ones need a winner (PK-INH-047) | agent proposal |
| OPEN-inheritance-11 | stale means `spec.overrides.version` differs from the upstream item's `spec.version` (PK-INH-053) | agent proposal |
| OPEN-inheritance-12 | added, removed, changed, newly conflicting defined over inherited items after winners; `schemas/lock-result.schema.json` (PK-INH-057, PK-INH-058) | agent proposal |
| OPEN-inheritance-13 | no credentials in sources (`cli.config-forbidden-key`, PK-INH-033); fetch uses only the Git credential mechanisms of the operating-system user (PK-INH-034) | agent proposal |
