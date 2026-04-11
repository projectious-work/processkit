---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260410_1049-HappyHare-build-artifact-management-skill
  created: '2026-04-10T10:49:56+00:00'
  updated: '2026-04-11T06:23:46+00:00'
spec:
  title: Build artifact-management skill and MCP server
  state: done
  type: story
  priority: high
  description: 'The Artifact primitive (schema: src/context/schemas/artifact.yaml,
    prefix ART, default dir: context/artifacts/) has no management skill or MCP server.
    Confirmed gap from primitive-skills-mapping-2026-03 (NOTE-20260410_1046-BraveSea).
    17 reference notes in context/notes/ are awaiting promotion to Artifact entities
    once this skill exists.


    Deliverables:

    - src/context/skills/artifact-management/SKILL.md

    - src/context/skills/artifact-management/mcp/server.py (MCP server)

    - Tools: create_artifact, get_artifact, query_artifacts, update_artifact

    - Update skill-finder trigger phrases

    - Mirror in context/skills/artifact-management/


    Also still missing: constraint-management, taxonomy-management, state-machine-management
    skills (lower priority).'
  started_at: '2026-04-11T06:23:39+00:00'
  completed_at: '2026-04-11T06:23:46+00:00'
---

## Transition note (2026-04-11T06:23:46+00:00)

SKILL.md, MCP server (create/get/query/update), SERVER.md, mcp-config.json created. Mirrored to context/. Skill-finder updated. Smoke test extended. .mcp.json wired.
