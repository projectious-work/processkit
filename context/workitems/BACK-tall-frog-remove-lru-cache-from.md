---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-tall-frog-remove-lru-cache-from
  created: '2026-04-09T14:51:48+00:00'
  labels:
    component: lib
    area: src
spec:
  title: Remove lru_cache from load_config in config.py
  state: backlog
  type: bug
  priority: medium
  description: 'load_config is @lru_cache(maxsize=4). This freezes the config in each
    MCP server process for its lifetime — editing aibox.toml has no effect until all
    servers restart. Unlike schema/state-machine loaders, config files are actively
    edited by users. Fix: remove the lru_cache decorator. Reading a TOML file is cheap
    enough to not need caching.'
---
