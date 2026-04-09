---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-sunny-dawn-move-processkit-config-out
  created: '2026-04-09T14:52:55+00:00'
  labels:
    component: lib
    area: src
spec:
  title: Move processkit config out of aibox.toml into a provider-neutral location
  state: backlog
  type: task
  priority: low
  description: 'id_format, id_slug, and any future processkit settings are processkit
    concerns but currently live in [context] inside aibox.toml. A project installing
    processkit without aibox has no canonical place for these. Options: (a) a standalone
    processkit.toml at the project root, (b) a [processkit] section in whatever config
    file the installer provides, with config.py discovering it independently of aibox.
    The aibox installer would write this file as part of aibox init. This keeps processkit
    provider-neutral and gives processkit full ownership of its config schema.'
---
