---
title: "v0 Compatibility"
description: "Read-only evidence and migration boundary for v0 projects."
weight: 50
---

> **v1.x development status:** Exact-release inspection and a guarded
> fresh-target transition are implemented. Native in-place migration and
> automatic legacy-entity transformation are not supported.

The v1 installer identifies legacy processkit evidence without consulting
aibox, harness, devcontainer, or MCP configuration files.

```sh
processkit inspect-compatibility \
  --root /path/to/legacy-tree \
  --distribution /path/to/processkit-v1-release \
  --json
```

An `exact-release` result requires every immutable anchor in a shipped
compatibility manifest to match. The beta manifests cover v0.27.1 and
v0.28.4 release trees. A partial installed project may be classified only as
`legacy-project-candidate`; its exact version is never guessed.

Compatibility inspection is read-only. Detection does not mutate the
inspected tree and does not authorize an in-place install.

## Transition an exact release

Create an empty directory outside the legacy tree, review the compatibility
result, and first generate a non-mutating plan:

```sh
mkdir /path/to/fresh-v1-project
processkit migrate-v0 \
  --source /path/to/exact-v0-release \
  --root /path/to/fresh-v1-project \
  --distribution /path/to/processkit-v1-release \
  --profile managed \
  --harness codex \
  --plan-only \
  --json
```

Resolve every blocking finding, review the dispositions and hashes, then omit
`--plan-only` and acknowledge installation:

```sh
processkit migrate-v0 \
  --source /path/to/exact-v0-release \
  --root /path/to/fresh-v1-project \
  --distribution /path/to/processkit-v1-release \
  --profile managed \
  --harness codex \
  --yes \
  --json
```

The command accepts only an exact v0.27.1 or v0.28.4 release match. The target
must be empty, separate from the source, and outside the source tree. It
installs v1 transactionally in the target and reports the matched manifest,
source release, target release, and corpus disposition. The source stays
read-only.

The result includes a deterministic corpus plan for project-owned actors,
decisions, discussions, gates, logs, migrations, notes, scopes, and work
items. Each entry binds its source SHA-256 and reports one of:

- `copy-compatible` for a structurally compatible mutable entity;
- `preserve-immutable` for a LogEntry or applied Migration; or
- a blocking finding for invalid frontmatter, an unsupported API version,
  unsafe links, missing identity, or a kind/directory mismatch.

Every entry includes an explicit `fieldLoss` array. It is empty for the
currently accepted v2 envelopes. The planner rejects the migration before
installation when any finding is blocked.

`artifacts`, `bindings`, `roles`, and `team-members` are explicitly excluded
because these v0 release trees also shipped producer-owned files in those
roots. They remain blocked until per-release baselines can distinguish product
content from user additions without guessing.

The plan remains evidence-only: the command transitions the runtime and
managed installation surface but does not yet copy entity files. To retain
legacy project data:

1. copy the project
2. run the v0-to-v1 corpus migration planner
3. review source hashes, field-loss reports, unsupported kinds, and immutable
   LogEntry evidence
4. validate the migrated copy
5. use `migrate-v0` to install v1 into a fresh or disposable target

Automatic entity copying and in-place migration remain unsupported until
historical installed-project fixtures prove mapping, immutable preservation,
rollback, and user-modification behavior. This boundary prevents a structural
lookalike or a downstream manager's lock file from being mistaken for
processkit provenance.
