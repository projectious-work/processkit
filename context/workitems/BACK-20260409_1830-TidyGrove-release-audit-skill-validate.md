---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260409_1830-TidyGrove-release-audit-skill-validate
  created: '2026-04-09T18:30:45+00:00'
spec:
  title: Release audit skill — validate entity files, skills, and structure before
    tagging
  state: backlog
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
---
