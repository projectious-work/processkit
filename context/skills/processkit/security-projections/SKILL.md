---
name: security-projections
description: |
  Project processkit security policy Artifacts into runtime policy
  files for Agent-IDS and Tetragon-style enforcement. Use when an
  agent-ids-rule or image-provenance-policy Artifact must become an
  executable security configuration.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-security-projections
    version: "2.0.0-alpha.1"
    created: 2026-04-30T00:00:00Z
    category: processkit
    layer: 3
    provides:
      primitives: [Artifact, Binding, LogEntry]
      mcp_tools:
        - project_agent_ids_rule
        - project_tetragon_tracing_policy
---

# Security Projections

## Intro

Security projections keep the source of truth in processkit Artifacts
while emitting runtime policy files for enforcement systems. Agent-IDS
rules project to canonical JSON. Tetragon tracing policies project to
YAML shaped like Cilium Tetragon `TracingPolicy` resources.

