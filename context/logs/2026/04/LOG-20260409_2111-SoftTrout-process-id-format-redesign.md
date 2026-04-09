---
apiVersion: processkit.projectious.work/v1
kind: LogEntry
metadata:
  id: LOG-20260409_2111-SoftTrout-process-id-format-redesign
  created: '2026-04-09T21:11:33+00:00'
spec:
  event_type: process.id-format-redesign
  timestamp: '2026-04-09T21:11:33+00:00'
  summary: ID format redesign — CamelCase word pairs, datetime prefix, date-based
    sharding, all entities migrated
  actor: ACTOR-claude
  details:
    phases:
      camel_word_pairs: ids.py word_style param; config.py id_word_style; settings.toml
        word_style=camel; server.py updated
      datetime_prefix: ids.py datetime_prefix param; config.py id_datetime_prefix;
        settings.toml datetime_prefix=true; entities migrated with YYYYMMDD_HHMM from
        metadata.created
      date_sharding: paths.entity_path() added; event-log server updated; LogEntry
        sharding enabled; logs/ moved to 2026/04/
      decision_recorded: DEC-20260409_2102-GrandGlade-no-state-based-directory — no
        state-based sharding accepted
      migration: 149 entities scanned; workitems, logs, artifact migrated; SKILL.md
        filenames preserved; schemas updated for underscore in ID patterns
    workitems_closed:
    - BACK-20260409_2006-CoolOak-camelcase-word-pairs-in
    - BACK-20260409_2006-SpryFjord-date-time-prefix-in
    - BACK-20260409_2006-MightySpruce-date-based-directory-sharding
    note: MCP servers must restart for new format to take effect in current session
      — new entities created via MCP this session will be in old format and caught
      by next migration run
---
