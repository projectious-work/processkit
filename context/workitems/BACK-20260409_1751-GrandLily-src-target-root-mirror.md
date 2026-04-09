---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260409_1751-GrandLily-src-target-root-mirror
  created: '2026-04-09T17:51:04+00:00'
spec:
  title: src/ → target-root mirror restructure
  state: backlog
  type: epic
  priority: high
  description: 'Restructure src/ so it is a literal mirror of a fresh consumer project
    root:

    - src/AGENTS.md → shipped as /AGENTS.md

    - src/context/... → shipped as /context/...

    - Catalog content moves to src/.processkit/{primitives,skills,processes,packages,lib}/

    - src/scaffolding/ is eliminated as a separate subtree


    Blast radius: airborne is the only current consumer. Breaking change accepted
    — owner coordinates aibox-side update. apiVersion stays at v1. Every cross-reference
    in PROVENANCE.toml, _find_lib(), smoke-test-servers.py, all MCP servers, docs-site,
    FORMAT.md, INDEX.md files, and CONTRIBUTING.md must be updated.'
---
