# Migration from v0 and contract compatibility — requirements

This specification defines how processkit converts the governance content of
a processkit v0 repository (decision records, skills, and process
definitions) to v1 content through `processkit migrate --from v0`, what that
conversion must leave untouched (v0 logs, events, work items, and memory
records), the safety rules for analysing, planning, and applying a
conversion, how the conversion is verified, and how processkit versions and
reports its public contracts and treats stored content under newer schemas.
How a reviewed plan is bound, made stale, and confirmed is defined by
`cli@v1`; how files are written is defined by `repository-storage@v1`.

Conventions: requirements use EARS; "shall" is mandatory, "should"
recommended, "may" optional; IDs are stable and never reused. Identifiers,
codes, field names, and the field mapping are in `interfaces.yaml`.

## Converting v0 governance content

- **PK-MIG-001:** processkit shall convert v0 decision records, skills, and
  process definitions to v1 content through an explicit, reviewable command.
- **PK-MIG-002:** processkit shall not convert v0 logs, events, work items,
  or memory records. When processkit migrates a v0 repository, processkit
  shall leave those records untouched as read-only history.
- **PK-MIG-003:** When processkit analyses a v0 repository or plans a
  migration, processkit shall write no file. processkit shall make the
  analysis and the plan available in the versioned JSON result envelope.
  <!-- from governance draft: 11-compatibility-migration-and-release.md
       PK-MIG-002 -->
- **PK-MIG-004:** When processkit applies a migration plan, processkit shall
  first run the committed-target check of `repository-storage@v1`
  (PK-STORE-056) on every plan target, including every v0 source file that
  the plan deletes. If a target fails the check, then processkit shall not
  apply the plan and shall write no file. processkit shall not create a
  backup; Git is the recovery mechanism. No option shall bypass the check
  (`cli@v1` PK-CLI-036).
  <!-- from governance draft: 11-compatibility-migration-and-release.md
       PK-MIG-003 -->
  <!-- changed by owner decision: #213 finding 4 -->
- **PK-MIG-005:** If a v0 item contains a field that is unknown to the
  conversion, then processkit shall either preserve that field in the
  converted item or stop and report the field. processkit shall not drop
  any field to make converted content validate.
  <!-- from governance draft: 11-compatibility-migration-and-release.md
       PK-MIG-004 -->
- **PK-MIG-006:** If a transformation is unsupported or ambiguous, then
  processkit shall report it as a manual action and shall not report the
  migration as complete while that manual action is open. processkit shall
  not guess the author's intent.
  <!-- from governance draft: 11-compatibility-migration-and-release.md
       PK-MIG-007 -->
- **PK-MIG-007:** The v0 conversion shall be a compatibility adapter and
  shall not be a source of v1 semantics. The v0 conversion shall be
  verified against representative golden corpora of v0 content, and a
  field-level preservation report shall state, for every v0 field, how the
  conversion treats it.
  <!-- from governance draft: 11-compatibility-migration-and-release.md
       PK-MIG-006 -->

## Recognizing v0 content

- **PK-MIG-008:** processkit shall read v0 content only from files that Git
  tracks below the directory `context/` of the repository root.
  processkit shall not read files below `context/templates/`. processkit
  shall not read untracked or ignored files as v0 content.
  <!-- agent proposal: OPEN-v0-migration-01 -->
- **PK-MIG-009:** processkit shall support v0 content of the releases
  v0.8.0 to v0.28.8, inclusive. If the file
  `context/.processkit-provenance.toml` exists and its key
  `install.processkit_version` names another release, then processkit shall
  report `migration.unsupported-v0-release` and shall write no file.
  <!-- agent proposal: OPEN-v0-migration-01 -->
- **PK-MIG-010:** processkit shall recognize a v0 source by the fields of
  its front matter, as listed in `interfaces.yaml` (`v0_sources`), and not
  by its `apiVersion` alone. processkit shall treat a file as a v0 item
  only if its front matter has a string `metadata.id`.
  <!-- agent proposal: OPEN-v0-migration-01 -->
- **PK-MIG-011:** If processkit cannot read the front matter of a file
  below a v0 directory of a converted type (`interfaces.yaml`,
  `v0_sources`), then processkit shall report
  `migration.unreadable-source` as a manual action. If a v0 source
  declares an `apiVersion` other than `processkit.projectious.work/v1` or
  `processkit.projectious.work/v2`, then processkit shall report
  `migration.unsupported-source` as a manual action. If processkit cannot
  read the front matter of a file in any other directory, then processkit
  shall report `migration.unreadable-file` as a warning and shall leave
  the file untouched.
  <!-- agent proposal: OPEN-v0-migration-01 -->

## Mapping and writing converted items

- **PK-MIG-012:** `processkit migrate --from v0` shall require a selected
  repository root with `processkit.toml` (`cli@v1` PK-CLI-008). processkit
  shall write each converted item to the location of its kind in the
  content directory (`repository-storage@v1` PK-STORE-045), in the
  serialization that processkit writes (`repository-storage@v1`
  PK-STORE-049).
  <!-- agent proposal: OPEN-v0-migration-03 -->
- **PK-MIG-013:** The plan shall delete every v0 source file of a converted
  item. If a source file has the same path and the same content as a file
  of the converted item, then the plan shall not list it. When processkit
  applies the plan, it shall write every created or replaced file before
  it deletes any file. processkit shall then remove every directory below
  `context/` that the deletes left empty.
  <!-- agent proposal: OPEN-v0-migration-03 -->
- **PK-MIG-014:** processkit shall set each field of a converted item only
  by the rules of `interfaces.yaml` (`field_mapping`). A value shall come
  from the v0 source, from the v1 supplement of PK-MIG-015, or from a fixed
  value that `field_mapping` states. If a rule does not apply to the type
  or shape of a v0 value, then processkit shall leave the v1 field unset.
  <!-- agent proposal: OPEN-v0-migration-02 -->
- **PK-MIG-015:** processkit shall read a v1 supplement from the v0 source
  when it is present, at the member that `interfaces.yaml` (`supplement`)
  names. The supplement shall have the shape of
  `schemas/v0-supplement.schema.json`. A supplement value shall replace
  the value that `field_mapping` derives for the same v1 field. If the
  supplement does not have that shape, then processkit shall report
  `migration.invalid-supplement` as a manual action.
  <!-- agent proposal: OPEN-v0-migration-02 -->
- **PK-MIG-016:** processkit shall preserve every v0 field whose value is
  not carried into a v1 field as an annotation of the converted item, with
  the key and value rules of `interfaces.yaml` (`preservation`). This
  includes every field that is unknown to the conversion. For a Skill,
  the unchanged `SKILL.md` preserves its front matter, and processkit
  shall add no annotation.
  <!-- agent proposal: OPEN-v0-migration-12 -->
- **PK-MIG-017:** If a v0 field cannot be preserved as an annotation
  within the limits of `ontology@v1` (PK-MODEL-012), or two fields would
  get the same annotation key, then processkit shall report
  `migration.field-not-preservable` as a manual action that names the file
  and the field.
  <!-- agent proposal: OPEN-v0-migration-12 -->
- **PK-MIG-018:** Before processkit plans to write a converted item, it
  shall validate the item as `processkit validate` would validate it after
  the plan is applied. For each diagnostic with severity `error`,
  processkit shall report `migration.converted-item-invalid` as a manual
  action.
  <!-- agent proposal: OPEN-v0-migration-02 -->
- **PK-MIG-019:** If two v0 sources map to the same target path, or a
  target path exists and the plan does not delete or keep it as a source
  file, then processkit shall report `migration.target-conflict` as a
  manual action for each such source.
  <!-- agent proposal: OPEN-v0-migration-03 -->
- **PK-MIG-027:** If a file that the plan leaves in place is at a declared
  location of a v1 kind in the content directory, then processkit shall
  report `migration.leftover-in-content-location` as a warning that names
  the file. processkit shall not move or delete that file.
  <!-- agent proposal: OPEN-v0-migration-03 -->

## Manual actions and results

- **PK-MIG-020:** processkit shall report a manual action as a diagnostic
  with severity `error`, category `validation`, a code from
  `interfaces.yaml` (`errors`), the v0 source path in `file`, and a fix.
  <!-- agent proposal: OPEN-v0-migration-06 -->
- **PK-MIG-021:** If any manual action is open, then processkit shall not
  ask for confirmation, shall write no file, and shall exit with code 1.
  With `--dry-run`, processkit shall still print the plan of the items
  without a manual action.
  <!-- agent proposal: OPEN-v0-migration-06 -->
- **PK-MIG-022:** When `processkit migrate -o json` runs, the envelope's
  `data` shall have the shape of `schemas/migrate-result.schema.json`. It
  shall list every converted source with the treatment of each of its
  fields, and the number of untouched v0 items per v0 kind.
  <!-- agent proposal: OPEN-v0-migration-07; changed by owner decision:
       2026-11-11 (#212), CLI style B -->
- **PK-MIG-023:** If the analysis finds nothing to convert or rewrite, then
  processkit shall report `migration.nothing-to-migrate` with severity
  `info`, shall not ask for confirmation, shall write no file, and shall
  exit with code 0.
  <!-- agent proposal: OPEN-v0-migration-11 -->
- **PK-MIG-024:** When `processkit migrate` runs without `--from`,
  processkit shall rewrite only items whose `apiVersion` is a supported
  content API version older than the current one. The option `--from`
  shall accept only the value `v0`.
  <!-- agent proposal: OPEN-v0-migration-11 -->

## Verifying the conversion

- **PK-MIG-025:** The golden corpora shall be kept in the repository at the
  location that `interfaces.yaml` (`verification.golden_corpora`) names.
  They shall contain at least the corpora listed there, each with its v0
  input, its golden v1 output, and its golden manual actions.
  <!-- agent proposal: OPEN-v0-migration-09 -->
- **PK-MIG-026:** The field-level preservation report shall consist of
  `interfaces.yaml` (`field_mapping`) of this specification, which covers
  every field of the v0 schemas of the supported releases, and of the
  `fields` list that every `processkit migrate` run reports per item.
  <!-- agent proposal: OPEN-v0-migration-08 -->

## Contract versions and compatibility

- **PK-COMPAT-001:** processkit shall version content `apiVersion`, the
  ontology version, the MCP tool contract, the CLI result contract, and the
  lock format independently of each other. When `processkit version` is
  run, the processkit CLI shall report the version of each of these
  contracts.
- **PK-COMPAT-002:** Before v1.0.0, processkit prereleases may break
  contracts, provided the migration is documented. After v1.0.0, a breaking
  change to a contract shall require a new major version of the affected
  contract.
- **PK-COMPAT-003:** processkit shall not silently reinterpret stored
  content under a newer schema. When `processkit migrate` rewrites content,
  it shall rewrite the content explicitly and shall report every change.
- **PK-COMPAT-004:** When a release breaks a contract, its release notes
  shall contain a section `Breaking changes`. That section shall state, for
  each broken contract, the old and the new version, the migration steps,
  and whether a rollback to the previous release is possible. If the
  change affects stored content, then `processkit migrate` shall perform
  the rewrite.
  <!-- agent proposal: OPEN-v0-migration-13 -->
- **PK-COMPAT-005:** processkit shall classify each change to a contract
  as compatible, conditionally compatible, or breaking, by the rules of
  `interfaces.yaml` (`compatibility.change_classification`).
  <!-- agent proposal: OPEN-v0-migration-13 -->
