# Migration from v0 and contract compatibility — overview

Non-normative. The requirements are in `requirements.md`.

## Owner goal

The owner wants existing v0 users to reach v1 without retyping their
governance content and without losing anything. v1 keeps decision records,
skills, and process definitions (C2, C3) but drops events, logs, work
items, and memory (C1), so the conversion must carry the governance
content across and leave the history alone. Because Git is the only
recovery mechanism in v1, the conversion must be a reviewed plan applied to
committed files, and it must stop and ask the author whenever a value
cannot be derived, instead of guessing. The release also needs stable,
separately versioned contracts so that users can see which of them a
release changes.

## Purpose

processkit v0 was agent context and memory infrastructure; v1 is a
context framework that stores governance definitions only (decision C1).
This slug lets a v0 repository move its governance content - decision
records, skills, and process definitions - to v1 content with one explicit,
reviewable command, `processkit migrate --from v0` (roadmap phase PK1-P7),
while v0 logs, events, work items, and memory records stay where they are
as read-only history. It adds the safety rules a conversion needs: analysis
and planning never write, applying needs every plan target committed in
Git (no backup), unknown fields are kept as annotations or the run stops,
and anything unsupported or ambiguous becomes a blocking manual action
instead of a guess. The author resolves a manual action by adding a v1
supplement to the v0 source. The v0
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
| PK-MIG-004 | PK-MIG-003 | "clean worktree or backup" replaced by the committed-target check of `repository-storage@v1` PK-STORE-056; no backup, no narrower recovery boundary (owner decision #213 finding 4) |
| PK-MIG-005 | PK-MIG-004 | "unknown project-owned extensions" generalized to fields unknown to the conversion |
| PK-MIG-006 | PK-MIG-007 | unchanged in meaning |
| PK-MIG-007 | PK-MIG-006 | limited to the v0 importer; "earlier-v1-alpha importers" not carried (the v1 alpha is evidence only in #197) |

Not carried: draft PK-MIG-001 (generic transformation with journals,
expected hashes, and rollback limits), PK-MIG-005 (append-only events,
aliases, correction events), and PK-MIG-008 (immutable v1-alpha fixtures):
they presuppose events, journals, or alpha content that decision C1 and
the baseline removed. Nothing about converting v0 logs, events, work items,
or memory was carried; PK-MIG-002 keeps them untouched.

## v0 prior art

The v0 facts in `interfaces.yaml` (`v0_sources`, `field_mapping`) come from
the release tags v0.8.0 to v0.28.8 and the branch `lts/v0`: the v0 schemas
`src/context/schemas/decisionrecord.yaml`, `process.yaml`, and
`artifact.yaml`, the skill format `src/context/skills/FORMAT.md`, and the
retired dogfood install `archive/processkit-install-20261101/`. Three v0
formats exist: v0.8.0 (item `apiVersion` `processkit.projectious.work/v1`,
flat skills, kind `Process`), v0.10.0 to v0.24.0 (the same with skills
nested by category), and v0.25.0 to v0.28.8 (`apiVersion`
`processkit.projectious.work/v2`, process definitions as Artifacts of
subtype `process-definition`). v0 used the same `apiVersion` group as v1,
so a v0 item is recognized by its `metadata.id`, not by `apiVersion`.

## Resolved open items

| Item | Resolution | Basis |
|---|---|---|
| OPEN-v0-migration-01 | v0 content is read only from Git-tracked files below `context/`, without `context/templates/`. Supported releases are v0.8.0 to v0.28.8; the optional aibox marker `context/.processkit-provenance.toml` is checked. Sources are recognized by front matter (`kind`, `metadata.id`, `spec.kind`, `metadata.processkit.id`) (PK-MIG-008 to PK-MIG-011, `v0_sources`). | agent proposal |
| OPEN-v0-migration-02 | Field mapping per source type in `field_mapping`. v1 required fields without a v0 counterpart (for example `triggers`, `sideEffects`, `workItemType`, `stateMachine`) come only from an author-written v1 supplement in the v0 source; without it the converted item fails validation and the run reports `migration.converted-item-invalid` as a manual action. Fixed values exist only for Skill applicability, empty Skill lists, and `parts` (PK-MIG-014, PK-MIG-015, PK-MIG-018). | agent proposal |
| OPEN-v0-migration-03 | Converted items go to the kind locations of the content directory of `processkit.toml`, which must exist (run `processkit init` first). The plan deletes the v0 source files, writes before it deletes, removes empty directories, and warns about leftovers in v1 locations (PK-MIG-012, PK-MIG-013, PK-MIG-019, PK-MIG-027). | agent proposal |
| OPEN-v0-migration-04 | Not a whole clean working copy: every plan target must pass the committed-target check of `repository-storage@v1` PK-STORE-056; untracked and ignored files that are not targets do not count (PK-MIG-004). | owner decision: #213 finding 4 |
| OPEN-v0-migration-05 | No backup and no narrower recovery boundary; recovery is through Git; no option bypasses the check (`cli@v1` PK-CLI-036) (PK-MIG-004). | owner decision: #213 finding 4 |
| OPEN-v0-migration-06 | A manual action is a diagnostic with a `migration.*` code, severity `error`, category `validation`. While one is open, nothing is written, no confirmation is asked, and the exit code is 1 (PK-MIG-020, PK-MIG-021). | agent proposal |
| OPEN-v0-migration-07 | `data` follows `schemas/migrate-result.schema.json`; the plan is the `cli@v1` plan. Untouched records are counted per v0 kind, not listed (PK-MIG-022). | agent proposal |
| OPEN-v0-migration-08 | The preservation report is `field_mapping` (static, per release) plus `data.items[].fields` of every run; treatments `mapped`, `annotated`, `kept`, `supplement` (PK-MIG-026). | agent proposal |
| OPEN-v0-migration-09 | Six corpora at `tests/golden/v0-migration/<corpus>/`, one per v0 format and one per failure class, each with `input/`, `expected/`, and `expected-diagnostics.json` (PK-MIG-025). | agent proposal |
| OPEN-v0-migration-10 | Field names and value owners are those of `cli@v1` PK-OUT-010 and `schemas/version.schema.json`, which are canonical for both PK-OUT-005 and PK-COMPAT-001 and resolve their conflict as one union report. | baseline |
| OPEN-v0-migration-11 | `migrate` without `--from` rewrites only items with an older supported content API version; v1 has none, so it reports `migration.nothing-to-migrate` and exits 0. `--from` accepts only `v0` (PK-MIG-023, PK-MIG-024). | agent proposal |
| OPEN-v0-migration-12 | The target kinds declare no extension map, so unmapped and unknown fields become annotations `v0.processkit.projectious.work/<pointer>` with RFC 8785 JSON values; if a limit is exceeded, the run stops with `migration.field-not-preservable` (PK-MIG-016, PK-MIG-017). | agent proposal |
| OPEN-v0-migration-13 | Release notes section `Breaking changes` with old and new version, migration steps, and a rollback statement; stored-content changes are rewritten by `processkit migrate`; changes are classified as compatible, conditionally compatible, or breaking (PK-COMPAT-004, PK-COMPAT-005). | standard: compatibility-and-machine-interfaces.md#change-classification |
