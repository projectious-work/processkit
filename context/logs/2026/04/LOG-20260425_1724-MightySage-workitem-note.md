---
apiVersion: processkit.projectious.work/v1
kind: LogEntry
metadata:
  id: LOG-20260425_1724-MightySage-workitem-note
  created: '2026-04-25T17:24:37+00:00'
spec:
  event_type: workitem.note
  timestamp: '2026-04-25T17:24:37+00:00'
  actor: ACTOR-claude
  summary: WildGrove Phase A landed in processkit; user-visible fix gates on aibox#55
    (Phase B)
  subject: BACK-20260425_1316-WildGrove-processkit-ships-no-preauth
  subject_kind: WorkItem
  details:
    phase: A
    phase_a_artifacts:
    - context/skills/processkit/skill-gate/assets/preauth.json — versioned spec listing
      18 server-wildcard permission patterns and 18 enabledMcpjsonServers entries
    - context/skills/processkit/skill-gate/scripts/README.md — Wiring targets section
      extended with preauth subsection cross-linking aibox#55
    - context/skills/processkit/pk-doctor/scripts/checks/preauth_applied.py — new
      pk-doctor check (registered in REGISTRY) that WARNs when .claude/settings.json
      is missing the spec entries; ERRORs if spec file missing; INFO when in sync;
      also detects spec drift vs the .processkit-mcp-manifest.json
    phase_b_owner: aibox#55
    phase_b_url: https://github.com/projectious-work/aibox/issues/55
    phase_b_summary: aibox sync extends the .claude/settings.json merge pass to additively
      merge preauth.json's permissions.allow[] and enabledMcpjsonServers[] under a
      _processkit_managed block; preserves user-added entries; removes entries no
      longer in spec.
    acceptance_status: Phase A acceptance met (spec ships, doctor diagnoses gap).
      Full WI acceptance (zero permission prompts after rebuild) gates on Phase B
      aibox release picking up the spec.
    verification: uv run pk-doctor --category=preauth_applied — currently reports
      2 WARN as expected (aibox#55 not yet shipped); flips to 1 INFO after Phase B
      sync.
    out_of_scope:
    - Codex CLI parity — no permissions surface in .codex today; revisit if/when Codex
      ships one.
    - Per-skill drift detection — already covered by aibox#54 (closed) via mcp_config_hash.
---
