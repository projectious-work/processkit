---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260409_1452-SunnyDawn-move-processkit-config-out
  created: '2026-04-09T14:52:55+00:00'
  labels:
    component: lib
    area: src
  updated: '2026-04-11T06:02:04+00:00'
spec:
  title: Move processkit config out of aibox.toml into a provider-neutral location
  state: cancelled
  type: task
  priority: low
  description: 'id_format, id_slug, and any future processkit settings are processkit
    concerns but currently live in [context] inside aibox.toml. A project installing
    processkit without aibox has no canonical place for these. Options: (a) a standalone
    processkit.toml at the project root, (b) a [processkit] section in whatever config
    file the installer provides, with config.py discovering it independently of aibox.
    The aibox installer would write this file as part of aibox init. This keeps processkit
    provider-neutral and gives processkit full ownership of its config schema.'
  completed_at: '2026-04-11T06:02:04+00:00'
---

## Transition note (2026-04-11T06:02:04+00:00)

Decided against a standalone processkit.toml. processkit config lives in the preferences table in AGENTS.md, managed in-place by agents editing context/skills/*/config/settings.toml. aibox writes these at install time. Provider-neutral config story is already solved by the AGENTS.md preferences section.
