---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260420_1720-GentleHill-doctor-report
  created: '2026-04-20T17:20:26+00:00'
spec:
  event_type: doctor.report
  timestamp: '2026-04-20T17:20:26+00:00'
  summary: /pk-doctor — 153 ERROR / 17 WARN / 4 INFO
  actor: ACTOR-agent-claude
  details:
    doctor_version: 1.0.0
    invocation: /pk-doctor
    categories:
      schema_filename:
        ERROR: 153
        WARN: 5
        INFO: 1
      sharding:
        ERROR: 0
        WARN: 12
        INFO: 1
      migrations:
        ERROR: 0
        WARN: 0
        INFO: 1
      drift:
        ERROR: 0
        WARN: 0
        INFO: 1
    top_findings_count: 20
    duration_ms: 454
    fixes_applied: []
    run_context: Phase 1 landing validation run; full stdout report saved at /tmp/doctor-real.txt
    top_findings_sample:
    - severity: ERROR
      category: schema_filename
      id: schema.parse-error
      entity_ref: context/workitems/FEAT-20260414_1432-InkStamp-mcp-tool-description-1pct-rule.md
      message_excerpt: 'YAML parse error: backtick char cannot start token'
    - severity: ERROR
      category: schema_filename
      id: schema.invalid
      entity_ref: context/workitems/RES-...
      message_excerpt: 'type: ''research'' is not one of [task, story, bug, epic,
        spike, chore]'
    - severity: WARN
      category: sharding
      id: sharding.log-wrong-bucket
      entity_ref: context/logs/LOG-loyal-vale.md
      message_excerpt: LogEntry not under YYYY/MM/
    - severity: WARN
      category: sharding
      id: sharding.migration-no-bucket
      entity_ref: context/migrations/20260419_1003_0.18.6-to-0.18.7.md
      message_excerpt: Migration not under pending/in-progress/applied/
---
