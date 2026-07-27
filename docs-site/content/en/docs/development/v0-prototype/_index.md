---
title: v0 Prototype
description: Status and origin of the current processkit prototype line.
---

# v0 Prototype

The current project is the v0 prototype line of processkit. It is usable
and dogfooded, but it is not the final v1.0 architecture. It proves the
product shape: git-backed process memory, skills, state machines, MCP
tools, package tiers, release machinery, and a Docusaurus docs site for
human readers.

## Current Status

As of the v1.0 branch start, `main` is at the v0.27.x line with
additional development documentation. The prototype has:

- a shipped `src/` deliverable boundary for consumers
- file-backed process entities with YAML frontmatter
- processkit API v2 entity schemas and state machines
- package tiers for selected skill and context bundles
- per-domain MCP management tools plus a processkit gateway mode
- `pk-doctor` health checks and release-audit style validation
- release tarball, provenance, and docs publishing scripts
- a manual GitHub Pages publish flow for `docs-site`
- aibox-assisted installation and synchronization in derived projects

The v0 line remains the maintenance and migration-source line while
v1.0 is built on a parallel branch.

## How We Got Here

The context index shows the prototype grew through dogfooding rather
than from a single upfront platform rewrite:

- The product target was captured in
  `ART-20260409_1854-KindCrane-processkit-product-requirements-document`
  as provider-neutral process memory, skills, and MCP tools for agentic
  software projects.
- Early releases established the file-backed entity model, package
  tiers, skill catalog, and consumer-facing `src/` mirror.
- Release automation was hardened after the v0.19.0/v0.19.1 learning
  that `git push --tags` is not the same thing as publishing a GitHub
  Release.
- The aibox integration became an installer/supervisor path, not the
  processkit source of truth. The v0.25 handover records the package and
  MCP-gateway handoff shape for downstream projects.
- The provider-neutral gateway decision
  `DEC-20260502_0743-CoolFjord-adopt-provider-neutral-processkit-gateway-daemon`
  kept processkit standalone while adding a lower-process-count runtime
  path for MCP-capable harnesses.
- Later v0 work added stricter doctor checks, release integrity checks,
  MCP config drift detection, TeamMember routing, and docs-site coverage.

## Why v1.0 Is Needed

The v0 prototype proved the workflow but exposed model pressure:

- the current primitive set cannot cleanly express the full v1.0
  ontology without overloading tags, kinds, and fields
- agents still need better query surfaces than concrete-kind guessing
- schema composition, generated runtime schemas, and validation modes
  need to become first-class
- migration and test evidence need to be automated rather than relying
  on manual aibox dogfood
- pk-doctor and MCP tooling need adversarial fixtures and stronger
  contract tests

v0 should therefore be treated as working evidence and migration source.
v1.0 is the revised implementation line.

