# Compatibility, migration, and release

## Version axes

processkit versions these axes independently:

- product release SemVer;
- entity API;
- package manifest;
- lifecycle plan and journal;
- machine result;
- event vocabulary;
- skill and ProcessSpecification contracts; and
- extension metaschemas.

The proposed v1 identifiers are:

| Contract | Identifier |
|---|---|
| Entity envelope and standard EntityTypes | `processkit.projectious.work/entity/v1` |
| Package and profile manifests | `processkit.projectious.work/package/v1` |
| Lifecycle plans and journals | `processkit.projectious.work/plan/v1` |
| Machine results | `processkit.projectious.work/result/v1` |
| Event vocabulary | `processkit.projectious.work/event/v1` |
| Application configuration | `processkit.projectious.work/config/v1` |
| Extension metadata | `processkit.projectious.work/extension/v1` |

- **PK-COMPAT-000:** contract identifiers MUST include their semantic surface
  and version. The previous unqualified `processkit.projectious.work/v2`
  Entity API is a migration source, not the identifier for the clean v1
  contract family.

- **PK-COMPAT-001:** `processkit version --format json` MUST report supported
  versions for every public contract axis.
- **PK-COMPAT-002:** each contract MUST define unknown-version, unknown-field,
  supported-window, deprecation, migration, and rollback behavior.
- **PK-COMPAT-003:** persisted data MUST NOT be silently reinterpreted under
  changed semantics.
- **PK-COMPAT-004:** stricter validation, changed defaults, ordering changes,
  new authority requirements, and performance-guarantee changes MUST be
  classified for compatibility even when schema shape is unchanged.

## Compatibility policy

- **PK-COMPAT-005:** before v1.0.0, prereleases MAY make breaking changes with
  migration notes and fixture updates. From v1.0.0 through v1.x:

- additive optional fields and commands may be minor changes;
- bug fixes preserving declared semantics may be patches;
- removal, required-field addition, semantic reinterpretation, incompatible
  validation, or persisted-layout break requires v2 unless an already-declared
  v1 migration boundary permits it;
- deprecated public names remain for at least one minor release and six months,
  unless a security issue requires faster removal.

## Migration

- **PK-MIG-001:** migration is an explicit source-contract to target-contract
  transformation with preconditions, operations, expected hashes, validation,
  evidence, and rollback limits.
- **PK-MIG-002:** analysis and planning MUST be read-only and available in the
  machine result contract.
- **PK-MIG-003:** application MUST operate on a clean Git worktree or create a
  complete contained backup, unless the user explicitly accepts a narrower
  documented recovery boundary.
- **PK-MIG-004:** migrations MUST preserve unknown project-owned extensions or
  stop; they MUST NOT drop fields to make data validate.
- **PK-MIG-005:** append-only events are not rewritten. Identity changes use
  aliases, successor/predecessor relations, and new correction events.
- **PK-MIG-006:** v0 and earlier-v1-alpha importers are compatibility adapters,
  not sources of v1 semantics. Each has representative golden corpora and a
  field-level preservation report.
- **PK-MIG-008:** maintained v0 and released v1-alpha corpora MUST be preserved
  as immutable migration fixtures and compatibility evidence. Fixture
  preservation does not grandfather their schemas, ontology, or behavior.
- **PK-MIG-007:** an unsupported or ambiguous transformation produces a manual
  action and blocks completion; migration MUST NOT guess intent.

## Release topology

The v1 line follows the company version-line standard:

```text
v1.x-dev → v1.x-pre-release → v1.x-release → main
```

Topic branches target `v1.x-dev`. Promotion branches are fast-forward-only
pointers and receive no unique commits. Because earlier experimental v1
history already exists, adoption of this specification requires a separate
reviewed branch-reconciliation decision; this PR does not authorize rewriting
or force-updating a protected branch.

## Artifacts and provenance

- **PK-REL-001:** releases originate from a clean worktree and exact annotated,
  preferably signed tag.
- **PK-REL-002:** publish wheel, source distribution, source archive, resolved
  package manifests, schemas and fixtures, checksums, SBOMs, curated notes,
  installation guidance, and signatures or attestations required by policy.
- **PK-REL-003:** build metadata MUST identify source commit, Python and uv
  versions, dependency lock digest, supported contract versions, and platform
  scope.
- **PK-REL-004:** candidate artifacts MUST be installed and tested without
  repository-relative imports or undeclared network access.
- **PK-REL-005:** published artifacts MUST be downloaded and independently
  verified before publication is considered complete.
- **PK-REL-006:** tags and artifacts are immutable; corrections use a new
  version.

## v1 acceptance sequence

- `alpha`: the complete 89-concept ontology registry and generated contracts,
  repository transactions, install/verify, and MCP workflow proven.
- `beta`: standard profile, harness-adapter and extension conformance,
  migration corpus, complete
  security and platform matrices proven; feature freeze begins.
- `rc`: documentation, compatibility, performance, package set, and exact
  candidate journeys complete with no unexplained skips.
- final: every normative requirement classified, all blockers closed, stable
  tag and artifacts independently verified, and migration/support policy
  published.
