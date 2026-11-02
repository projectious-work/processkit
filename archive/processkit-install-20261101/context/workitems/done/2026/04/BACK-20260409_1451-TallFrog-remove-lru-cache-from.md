---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260409_1451-TallFrog-remove-lru-cache-from
  created: '2026-04-09T14:51:48+00:00'
  labels:
    component: lib
    area: src
  updated: '2026-04-09T22:12:56+00:00'
spec:
  title: Remove lru_cache from load_config in config.py
  state: done
  type: bug
  priority: medium
  description: 'load_config is @lru_cache(maxsize=4). This freezes the config in each
    MCP server process for its lifetime — editing aibox.toml has no effect until all
    servers restart. Unlike schema/state-machine loaders, config files are actively
    edited by users. Fix: remove the lru_cache decorator. Reading a TOML file is cheap
    enough to not need caching.'
  started_at: '2026-04-09T22:12:51+00:00'
  completed_at: '2026-04-09T22:12:56+00:00'
---

## Transition note (2026-04-09T22:12:51+00:00)

Fix already applied — lru_cache removed from load_config in config.py
