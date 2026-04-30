---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260425_1734-TallSage-workitem-note
  created: '2026-04-25T17:34:23+00:00'
spec:
  event_type: workitem.note
  timestamp: '2026-04-25T17:34:23+00:00'
  actor: ACTOR-claude
  summary: 'CleverRiver processkit-side scope landed: pk-doctor migration_integrity
    check; aibox-side fix still pending'
  subject: BACK-20260425_1711-CleverRiver-aibox-sync-emits-defective
  subject_kind: WorkItem
  details:
    phase: processkit-side
    artifact: context/skills/processkit/pk-doctor/scripts/checks/migration_integrity.py
    registered_in: checks/__init__.py REGISTRY
    invariants_checked:
    - 'same-version-with-content: WARN if from_version == to_version AND (affected_groups
      OR affected_files non-empty)'
    - 'affected-files-empty: WARN if affected_groups populated but affected_files
      == []'
    verification: Reproduced rejected MIG-20260425T164303 in a tempdir as pending;
      both invariants fire as expected with WARN findings citing CleverRiver.
    scope_remaining: Upstream fix in aibox sync's diff-generator baseline-snapshot
      resolution. WI stays in backlog as a cross-project tracking entity; processkit-side
      defensive check is now shipping so derived projects can self-diagnose if the
      same malformed migration class recurs.
---
