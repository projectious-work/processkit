---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260426_1740-BraveRabbit-doctor-report
  created: '2026-04-26T17:40:20+00:00'
spec:
  event_type: doctor.report
  timestamp: '2026-04-26T17:40:20+00:00'
  summary: /pk-doctor (verification) — 0 ERROR / 0 WARN / 12 INFO
  actor: claude-opus-4-7
  details:
    doctor_version: 1.0.0
    invocation: /pk-doctor
    duration_ms: 14601
    categories:
      schema_filename:
        ERROR: 0
        WARN: 0
        INFO: 1
      sharding:
        ERROR: 0
        WARN: 0
        INFO: 1
      migrations:
        ERROR: 0
        WARN: 0
        INFO: 1
      migration_integrity:
        ERROR: 0
        WARN: 0
        INFO: 1
      drift:
        ERROR: 0
        WARN: 0
        INFO: 1
      team_consistency:
        ERROR: 0
        WARN: 0
        INFO: 1
      release_integrity:
        ERROR: 0
        WARN: 0
        INFO: 1
      commands_consistency:
        ERROR: 0
        WARN: 0
        INFO: 1
      mcp_config_drift:
        ERROR: 0
        WARN: 0
        INFO: 1
      server_header_drift:
        ERROR: 0
        WARN: 0
        INFO: 1
      preauth_applied:
        ERROR: 0
        WARN: 0
        INFO: 1
      skill_dag:
        ERROR: 0
        WARN: 0
        INFO: 1
    top_findings: []
    fixes_applied:
    - category: migrations
      action: reject_migration
      id: MIG-RUNTIME-20260426T161215
      reason: empty-baseline defect (BACK-20260425_1711-CleverRiver)
    - category: drift
      action: allowlist
      file: scripts/check-src-context-drift.sh
      entry: ALLOWLIST_PROVENANCE
      reason: release-time provenance stamp lives only in dogfood context/
    - category: drift
      action: fix-parser
      file: context/skills/processkit/pk-doctor/scripts/checks/drift.py
      reason: tighten 'differ' substring match to avoid matching 'difference' in script's
        To-fix hint; mirrored to src/context/
---
