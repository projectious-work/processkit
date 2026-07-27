---
title: v0 Reconciliation
description: Controlled carry-over from the supported v0 line into v1.
---

# v0 Reconciliation

## Baseline

The v1 line forked from `v0.27.1`. Reconciliation therefore compares the
current v1 work against the latest supported v0 release, currently
`v0.28.3`, rather than copying the v0 tree wholesale.

The rule is:

- carry fixes that remain valid under the v1 ontology
- adapt lifecycle and storage behavior to generated v1 contracts
- regenerate catalogs, schemas, and manifests from v1 sources
- defer unrelated v0 features with an explicit disposition
- never overwrite v1 schema sources with flat v0 schemas

## Current Matrix

| v0 surface | v1 disposition | Alpha status |
|---|---|---|
| Refreshable GitHub token-file authentication | Carry unchanged security semantics | Implemented and tested |
| Migration drafting | Adapt to v1 Migration schema and automatic apply mode | Implemented and tested |
| Historical migration filename repair | Carry with append-only audit bridge | Implemented and tested |
| Scope lifecycle | Adapt storage to `Container(kind=scope)` | Implemented and tested |
| TeamMember role assignment | Adapt through the Actor interface | Implemented and tested |
| Immutable release-manifest preflight | Carry `--check`; builds must not mutate tags | Implemented |
| `git-branching` skill | Carry after v1 metadata review | Deferred after alpha |
| `project-reconciliation` skill | Carry after v1 entity-name review | Deferred after alpha |
| `repository-portfolio-review` skill | Carry after v1 entity-name review | Deferred after alpha |
| v0 doctor fixes | Re-evaluate per finding against v1 storage | Ongoing |
| v0 flat schemas and generated catalogs | Never copy; regenerate from v1 sources | Enforced |

## Verification

The server smoke suite exercises the v1-native replacements. The package
smoke suite then extracts only the release tree and repeats the workflow so
repository imports cannot conceal a missing carry-over.

Before each prerelease:

1. compare the selected v0 release with `v1.x-dev`
2. update this matrix
3. run schema, server, package, docs, doctor, and release-audit checks
4. record any intentional deferral with an owner or milestone
