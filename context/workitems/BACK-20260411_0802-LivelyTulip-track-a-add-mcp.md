---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260411_0802-LivelyTulip-track-a-add-mcp
  created: '2026-04-11T08:02:17+00:00'
  updated: '2026-04-11T08:03:09+00:00'
spec:
  title: Track A — Add MCP server to skill-finder (find_skill, list_skills)
  state: in-progress
  type: epic
  priority: high
  description: 'Build a processkit MCP server for skill-finder so it becomes a callable
    tool in every agent turn rather than prose loaded once at session start.


    Tools to implement:

    - find_skill(task_description) → matching skill name + SKILL.md path + one-line
    description

    - list_skills(category?) → catalog listing, optionally filtered by category


    Supersedes BACK-AmberCliff (catalog query mode) — that scope is now covered by
    list_skills.


    Related decision: DEC-RoyalComet (reliable skill invocation five-track plan)'
  started_at: '2026-04-11T08:03:09+00:00'
---
