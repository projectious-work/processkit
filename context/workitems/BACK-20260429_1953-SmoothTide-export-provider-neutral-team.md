---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260429_1953-SmoothTide-export-provider-neutral-team
  created: '2026-04-29T19:53:06+00:00'
  labels:
    area: harness
    release: next
    source: user-request
    provider-adapter: claude-code
spec:
  title: Export provider-neutral team members to Claude Code subagents
  state: backlog
  type: story
  priority: medium
  description: Add optional Claude Code subagent export for projects that use Claude
    Code while keeping processkit provider-neutral. Processkit should generate project-level
    .claude/agents/*.md files from TeamMember/Role definitions as a harness adapter,
    not as the canonical team model. The adapter should preserve role identity, tool
    restrictions, and delegation descriptions and remain disabled or irrelevant for
    non-Claude harnesses.
---
