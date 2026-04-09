---
apiVersion: processkit.projectious.work/v1
kind: LogEntry
metadata:
  id: LOG-20260409_2225-SnowyEmber-session-handover
  created: '2026-04-09T22:25:55+00:00'
spec:
  event_type: session.handover
  timestamp: '2026-04-09T22:25:55+00:00'
  actor: ACTOR-claude
  summary: >-
    Session handover — v0.8.0 released; note IDs, GrandLily, SolidSky
    complete
  details:
    session_date: '2026-04-10'
    current_state: |
      v0.8.0 has been tagged, pushed, and released with a tarball asset on
      GitHub. The codebase is in a clean, releasable state on main. Three
      major workstreams completed across this and the prior session:
      GrandLily (src/ restructured to mirror a consumer project root),
      SolidSky (auto-log side effects added to all 8 entity-mutating MCP
      servers), and note-management ID format fix (Note added to
      KIND_PREFIXES; sequential NOTE-001 scheme replaced by generate_id
      timestamp format). The smoke test passes green.
    open_threads:
      - >-
        BACK-20260409_1830-TidyGrove — Release audit skill (validate entity
        files, skills, and structure before tagging) — backlog, medium
      - >-
        BACK-20260409_1738-NobleBrook — Skill DAG validator, cycle detection
        and layer constraint checks — backlog, medium
      - >-
        BACK-20260409_1652-WildButter — Create, polish and deploy Docusaurus
        docs-site — backlog, high priority epic
      - >-
        BACK-20260409_1452-SunnyDawn — Move processkit config out of
        aibox.toml into a provider-neutral location — backlog, low
      - >-
        BACK-20260409_1449-BoldVale — FTS5 full-text search in the SQLite
        index — backlog, medium
      - >-
        .mcp.json now has "cwd": "/workspace" on all servers (fixes the
        wrong-project-root bug); MCP servers need a restart for it to take
        effect
    next_recommended_action: |
      Start WildButter — the docs-site epic is the highest-priority
      backlog item. Begin with a Docusaurus skeleton, wire up the existing
      skills catalog as the first section, and deploy to GitHub Pages.
    branch: main
    commit: 8a4aed4
    behavioral_retrospective:
      - >-
        MCP servers ran from /home/aibox (not /workspace) because .mcp.json
        had no cwd. This caused find_project_root() to return /home/aibox,
        where no config lives, so ID generation fell back to defaults
        (kebab, no datetime prefix). Fixed by adding "cwd": "/workspace"
        to all entries in .mcp.json. Rule: always set cwd in .mcp.json
        when server paths are relative.
      - >-
        session-handover SKILL.md did not specify generate_id or sharded
        path — it gave a flat context/logs/ instruction. Fixed in SKILL.md.
        Rule: skill writing instructions must reference generate_id and
        the correct shard path.
      - >-
        Wrote a memory file to /workspace/home/aibox/... instead of
        /home/aibox/... (wrong path). home/ directory deleted from repo
        root. Rule: memory paths start with /home/aibox, never
        /workspace/home/aibox.
      - >-
        Added semver version prefixes to commit messages (v0.8.0 —) without
        being asked. Saved as feedback memory. Rule: describe the change,
        not the version.
---
