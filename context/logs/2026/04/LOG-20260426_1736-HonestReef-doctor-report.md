---
apiVersion: processkit.projectious.work/v1
kind: LogEntry
metadata:
  id: LOG-20260426_1736-HonestReef-doctor-report
  created: '2026-04-26T17:36:11+00:00'
spec:
  event_type: doctor.report
  timestamp: '2026-04-26T17:36:11+00:00'
  summary: /pk-doctor — 0 ERROR / 5 WARN / 9 INFO
  actor: claude-opus-4-7
  details:
    doctor_version: 1.0.0
    invocation: /pk-doctor
    duration_ms: 14660
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
        WARN: 1
        INFO: 0
      migration_integrity:
        ERROR: 0
        WARN: 2
        INFO: 0
      drift:
        ERROR: 0
        WARN: 2
        INFO: 0
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
    top_findings:
    - severity: WARN
      id: migration.pending-count
      message: 1 pending migration(s) — review and apply via migration-management
        MCP (or `/pk-doctor --fix=migrations`)
    - severity: WARN
      id: migration_integrity.same-version-with-content
      entity_ref: MIG-RUNTIME-20260426T161215
      message: from_version == to_version (0.21.1) but affected_groups=2, affected_files=0;
        same-version migrations should be no-op (likely empty-baseline defect — see
        BACK-20260425_1711-CleverRiver)
    - severity: WARN
      id: migration_integrity.affected-files-empty
      entity_ref: MIG-RUNTIME-20260426T161215
      message: affected_groups has 2 entries but affected_files is empty — body rows
        and file list are inconsistent (likely post-processor defect — see BACK-20260425_1711-CleverRiver)
    - severity: WARN
      id: drift.detected
      message: 'Only in /workspace/context: .processkit-provenance.toml'
    - severity: WARN
      id: drift.detected
      message: 4. If the difference is intentional, add a justified entry to the
    fixes_applied: []
---
