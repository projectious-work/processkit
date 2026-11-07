# Migration from v0 and contract compatibility — overview

Non-normative. The requirements are in `requirements.md`.

## Purpose

processkit v0 was agent context and memory infrastructure; v1 is a
context framework that stores governance definitions only (decision C1).
This slug lets a v0 repository move its governance content - decision
records, skills, and process definitions - to v1 content with one explicit,
reviewable command, `processkit migrate --from v0` (roadmap phase PK1-P7),
while v0 logs, events, work items, and memory records stay where they are
as read-only history. It adds the safety rules a conversion needs: analysis
and planning never write, applying needs a clean working copy or a backup,
unknown fields are kept or the run stops, and anything unsupported or
ambiguous becomes a blocking manual action instead of a guess. The v0
converter is a compatibility adapter checked against golden corpora with a
field-level preservation report.

The slug also holds the release-wide compatibility rules: the five
independently versioned contracts reported by `processkit version`, the
pre- and post-v1.0.0 break policy, and the rule that stored content is never
silently reinterpreted under a newer schema.

## Boundaries

This slug does not cover:

- the `migrate` and `version` command syntax, `--dry-run`, `--json`,
  `--yes`, exit codes, the result envelope, and how a reviewed plan is
  bound, made stale, and confirmed (PK-CLI-012 to PK-CLI-014) -
  `cli@v1`;
- atomic file writes, multi-file plans and change reports, the overwrite
  rule, `apiVersion`-based validation, and the Git boundary
  (PK-STORE-020 to PK-STORE-022, PK-STORE-031, PK-STORE-040) -
  `repository-storage@v1`;
- the v1 target kinds DecisionRecord, Skill, and ProcessSpecification and
  what validates them - `content-kinds@v1`;
- the item envelope and extension maps for preserved fields
  (PK-MODEL-015) - `ontology@v1`;
- the lock format itself - `inheritance@v1`; the MCP tool contract -
  `mcp-context-serving@v1` (this slug only requires that their versions are
  independent and reported);
- the rule that processkit stores no events, logs, work items, or memories
  (PK-PROD-020) - `repository-storage@v1`;
- verification (PK-TEST), performance (PK-PERF), and release (PK-REL)
  requirements of the baseline's chapter 11, which are not part of this
  slug.

## Governing decisions

- **C1** Context, not memory: v0 logs, events, work items, and memory
  records are not converted and stay untouched; Git is the recovery
  mechanism, which shapes PK-MIG-004.
- **C2** The full ontology is the definition language: converted process
  definitions become ProcessSpecifications in ontology terms.
- **C3** Decision records stay: v0 decision records are carried into v1
  as DecisionRecords.

## Provenance

| Baseline (#197) | This slug |
|---|---|
| `spec/doc/v1/11-verification-and-release.md` - Migration from v0 | PK-MIG-001, PK-MIG-002 |
| 11 - Compatibility | PK-COMPAT-001 to PK-COMPAT-003 |
| `06-cli.md` - Commands (`migrate`, `version`) | referenced via `cli@v1` |
| `roadmap.yaml` - PK1-P7 | scope |

Supporting context (not carried as requirements): PK-OUT-005 and
PK-CLI-004, PK-CLI-006, PK-CLI-012 to PK-CLI-014 of `cli@v1`;
PK-STORE-003, PK-STORE-021, PK-STORE-022, PK-STORE-031 of
`repository-storage@v1`; PK-ARCH-002 (v0 code is evidence only); PK-DEC-003
(an accepted decision is never rewritten in meaning), which the no-guessing
rule protects during conversion.

Chapter 11 has no migration journey; journeys 1 to 8 are new.

Gap items carried from the governance draft (tag
`archive/processkit-v1-governance-standards`, file
`spec/doc/v1/11-compatibility-migration-and-release.md`, section
"Migration"). The draft's IDs collide with the baseline's, so they were
renumbered after PK-MIG-002:

| New ID | Draft ID | Adaptation |
|---|---|---|
| PK-MIG-003 | PK-MIG-002 | "machine result contract" read as the versioned JSON result envelope of `cli@v1` |
| PK-MIG-004 | PK-MIG-003 | "worktree" read as Git working copy; backup location and acceptance mechanism left open (OPEN-v0-migration-05) |
| PK-MIG-005 | PK-MIG-004 | "unknown project-owned extensions" generalized to fields unknown to the conversion |
| PK-MIG-006 | PK-MIG-007 | unchanged in meaning |
| PK-MIG-007 | PK-MIG-006 | limited to the v0 importer; "earlier-v1-alpha importers" not carried (the v1 alpha is evidence only in #197) |

Not carried: draft PK-MIG-001 (generic transformation with journals,
expected hashes, and rollback limits), PK-MIG-005 (append-only events,
aliases, correction events), and PK-MIG-008 (immutable v1-alpha fixtures):
they presuppose events, journals, or alpha content that decision C1 and
the baseline removed. Nothing about converting v0 logs, events, work items,
or memory was carried; PK-MIG-002 keeps them untouched.

## Open questions

Mirrors `open` in `interfaces.yaml`.

1. OPEN-v0-migration-01 - supported v0 releases, their layout, and how v0
   record types are recognized.
2. OPEN-v0-migration-02 - field mapping to DecisionRecord, Skill, and
   ProcessSpecification; v1 required fields without a v0 counterpart.
3. OPEN-v0-migration-03 - where converted items go; fate of converted v0
   source files; whether `processkit.toml` must exist first.
4. OPEN-v0-migration-04 - definition of a clean working copy.
5. OPEN-v0-migration-05 - backup location, format, and content; how a
   narrower recovery boundary is accepted; tension with PK-STORE-003 and C1.
6. OPEN-v0-migration-06 - representation, exit code, and write behavior of
   open manual actions.
7. OPEN-v0-migration-07 - envelope fields of the analysis and plan; whether
   untouched records are listed.
8. OPEN-v0-migration-08 - format, location, and treatments of the
   preservation report.
9. OPEN-v0-migration-09 - composition and location of the golden corpora.
10. OPEN-v0-migration-10 - field names, identifier formats, and current
    values of the five contract versions in `processkit version`.
11. OPEN-v0-migration-11 - `migrate` without `--from`: source versions,
    behavior when current, other `--from` values.
12. OPEN-v0-migration-12 - where unknown fields are preserved; whether
    stopping is the only outcome without an extension map.
13. OPEN-v0-migration-13 - what "documented migration" means; how breaking
    changes are classified.
