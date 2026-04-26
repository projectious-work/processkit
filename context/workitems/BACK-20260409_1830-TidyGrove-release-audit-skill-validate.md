---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260409_1830-TidyGrove-release-audit-skill-validate
  created: '2026-04-09T18:30:45+00:00'
  updated: '2026-04-26T15:45:19+00:00'
spec:
  title: Release audit skill — validate entity files, skills, and structure before
    tagging
  state: done
  type: task
  priority: medium
  description: 'Build a release-audit skill (and backing script) that validates processkit
    content before each release tag:

    - Entity files: apiVersion present and correct, kind registered, metadata.id valid
    format

    - Skills: SKILL.md frontmatter compliance (name, description, metadata.processkit.*
    fields), four required sections present

    - MCP servers: all tools have annotations (readOnlyHint, destructiveHint, etc.)

    - Cross-references: uses: entries resolve to existing skills (overlap with validate-skill-dag.py)


    Add to release checklist in AGENTS.md and CONTRIBUTING.md. Replaces the aibox
    lint dependency for content validation.'
  started_at: '2026-04-26T15:29:31+00:00'
  completed_at: '2026-04-26T15:45:19+00:00'
---

## Transition note (2026-04-26T15:29:31+00:00)

v0.23.0-bound (DEC-20260426_1529-TidyLynx). Implementation delegated to a sonnet-tier subagent.


## Transition note (2026-04-26T15:45:16+00:00)

release-audit skill landed at context/skills/processkit/release-audit/ (mirrored). 4 detect-only validation passes: entity_files (frontmatter + apiVersion + kind + id-vs-filename), skill_structure (required frontmatter fields + 4 required body sections), mcp_annotations (every @server.tool has ToolAnnotations with all 4 hint kwargs), cross_references (uses[].skill resolves). Single Markdown report on stdout, exit 0 clean / 1 dirty. Skill ships SKILL.md (199 lines) with the standard 4-section structure, scripts/release_audit.py (727 lines) with #!/usr/bin/env -S uv run --script PEP 723 metadata, scripts/test_release_audit.py (15 tests, all pass), and commands/pk-release-audit.md command file. Live first-run finds 105 ERRORs surfaced in the existing tree across legacy aibox migration prose (no entity frontmatter), team-member sub-files (alt schema), and non-processkit skills missing layer fields — flagged for separate triage, not blocking v0.23.0.


## Transition note (2026-04-26T15:45:19+00:00)

Closed. Will ship in v0.23.0.
