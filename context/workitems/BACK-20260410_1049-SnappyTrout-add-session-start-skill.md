---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260410_1049-SnappyTrout-add-session-start-skill
  created: '2026-04-10T10:49:47+00:00'
  updated: '2026-04-11T08:03:09+00:00'
spec:
  title: Add session-start skill-check to AGENTS.md and session-handover skill
  state: in-progress
  type: chore
  priority: medium
  description: 'Behavioral gap identified in session 2026-04-10: after a session reset/compaction,
    the "check skill catalog before acting on domain tasks" rule fades from working
    memory. Agents fall back on general knowledge for file locations and artifact
    formats, bypassing processkit''s skill-backed workflows.


    Changes needed:

    1. AGENTS.md — add explicit session-start checklist to the "AI agents on this
    project" section: before any artifact-creation or content-ingestion task, run
    search_entities(kind=skill, text=<task-keyword>) as a mandatory first step. Name
    the task classes: research ingestion, artifact creation, discussion management,
    decision recording, backlog item creation, quality audits.

    2. context/skills/session-handover/SKILL.md — add to "incoming session" instructions:
    query the skill index for relevant skills before starting any new workstream.

    3. Mirror both changes in src/ counterparts.'
  started_at: '2026-04-11T08:03:09+00:00'
---

## Transition note (2026-04-11T08:03:09+00:00)

Scope expanded per DEC-RoyalComet: now covers Track B — session-start meta-skill with 1% rule and mandatory decision graph. Supersedes original narrower scope.
