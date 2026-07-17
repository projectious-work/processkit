---
title: Test Strategy
description: Automated testing strategy for processkit v1.0.
---

# Test Strategy

The current exploratory strategy is to install processkit into a new
aibox project and try workflows manually. That remains useful as a human
dogfood check, but it is not enough for v1.0. It is not automated, it
makes aibox a hard dependency, and it cannot prove release-gate criteria
repeatably.

## Test Goals

The v1.0 test strategy must prove:

- schema generation is deterministic
- generated schemas validate real and adversarial fixtures correctly
- MCP tools match their Python signatures and JSON Schemas
- writes enforce state machines, guards, validation modes, and event logs
- index reads match canonical files after creates, transitions, and
  migrations
- `query_by_interface` returns complete mixed-kind results
- migration tools preserve data within the RFC gate limits
- pk-doctor catches deliberately invalid entities and every actionable
  finding has an executable or formally recognized disposition
- docs and examples remain buildable
- aibox integration works as an adapter, not as the only system test

## Automated Layers

| Layer | Purpose |
|---|---|
| Schema unit tests | Render Jinja + YAML fragments, compare `_generated` output to golden files, and verify merge strategies. |
| Schema contract tests | Validate generated draft-2020-12 schemas against valid and invalid entity fixtures. |
| MCP contract tests | Check every tool signature against its JSON Schema and run typed request/response fixtures. |
| State-machine tests | Exercise valid and invalid transitions, guard failures, terminal states, and emitted events. |
| Index tests | Create and mutate fixture entities, then assert search, relation traversal, backlinks, and interface grouping. |
| Migration tests | Plan and execute v0.x fixture migrations; assert field-loss, orphan, source-hash, alias-resolution, and append-only gates. |
| pk-doctor adversarial tests | Require every expected finding, validate remediation tools against the gateway catalog, execute remediations, and require a clean recheck. |
| Package smoke tests | Install processkit from the local tree or release tarball into a temporary fixture project without aibox. |
| Docs tests | Build Docusaurus and verify links to generated reference pages. |
| Adapter tests | Run a small aibox install/apply workflow to prove integration, but keep it outside the core correctness suite. |

## Fixture Projects

Use local fixture projects under the test tree:

- `empty-project`: no context, used for first install and schema
  generation
- `alpha-project`: small valid corpus covering the alpha ontology slice
- `migration-v0-project`: representative v0.x corpus for migration
  adapters
- `adversarial-project`: invalid frontmatter, bad transitions, broken
  links, malformed bindings, and inconsistent index state
- `remediation-project`: actionable doctor findings with safe fixes,
  archives, migrations, policy exceptions, and external blockers
- `art-project`: a compact first-ART scenario that exercises planning,
  execution, demo, inspect-and-adapt, decisions, risks, and evidence

These fixtures should run with plain repository commands in CI. aibox can
consume the same fixtures in an adapter suite, but the fixtures must not
require aibox to exist.

## Alpha Proof

Alpha automation should pass before any alpha tag:

- full schema rebuild from `schemas/src/`
- committed `_generated` tree matches the renderer output
- create/read/transition MCP paths work for the alpha slice
- `query_by_interface` works for at least `Record`
- strict and tolerant validation modes are observable
- the alpha fixture migrates from v0.x or maps explicitly
- actionable alpha findings close through the shipped gateway or resolve to
  a recognized non-executable disposition
- docs build locally

Manual dogfood remains useful after this automated baseline, not instead
of it.

## Final Release Proof

The final gate should include:

- all strict 81-gate criteria green
- first-ART validation completed with recorded evidence
- all MCP tools schema-checked
- pk-doctor adversarial and remediation fixtures green after executing their
  declared closure paths
- package smoke tests green from release artifact
- aibox adapter test green for a pinned `v1.0.0-rc.*`
- no known index/schema/migration blocker

This keeps the RFC's first-ART proof while removing the current hard
dependency on manual aibox experimentation.
