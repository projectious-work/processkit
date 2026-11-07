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
recommended, "may" optional; IDs are stable and never reused.

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
  operate on a clean Git working copy or shall first create a complete,
  contained backup, unless the user explicitly accepts a narrower,
  documented recovery boundary. If none of these holds, then processkit
  shall not apply the plan and shall write no file.
  <!-- from governance draft: 11-compatibility-migration-and-release.md
       PK-MIG-003 -->
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
