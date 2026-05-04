---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260502_0743-CoolFjord-adopt-provider-neutral-processkit-gateway-daemon
  created: '2026-05-02T07:43:51+00:00'
  updated: '2026-05-02T07:44:38+00:00'
spec:
  title: Adopt provider-neutral processkit gateway daemon architecture
  state: accepted
  decision: Implement a provider-neutral processkit-gateway daemon as an additive
    runtime mode, preserving per-skill stdio servers and aggregate-mcp compatibility
    while keeping aibox as installer/supervisor only.
  context: The user approved the architecture and implementation plan for solving
    MCP memory pressure without making processkit dependent on aibox. Current aggregate-mcp
    reduces many servers to one stdio process per harness, but it is not a shared
    daemon and still eagerly imports source servers.
  rationale: This keeps processkit usable without aibox, supports stdio-only harnesses
    through a proxy, enables OpenCode/Hermes remote or local MCP support, preserves
    Aider fallback limitations, and avoids breaking existing per-skill MCP consumers.
  alternatives:
  - option: Make daemon aibox-owned
    pros:
    - aibox can directly manage devcontainer lifecycle
    cons:
    - Couples processkit runtime semantics to aibox
    - Weakens standalone processkit usability
  - option: Replace per-skill servers with daemon only
    pros:
    - Simpler runtime story
    cons:
    - Breaks existing harnesses
    - Removes fine-grained permission/config mode
  - option: Only keep aggregate-mcp
    pros:
    - Already implemented as a bridge
    cons:
    - Does not solve shared runtime memory pressure across harnesses and subagents
    - Still eagerly imports all source servers
  consequences: 'Positive: shared daemon path, lower process count, provider-neutral
    runtime, non-aibox startup possible, preserved compatibility. Negative: more runtime
    modes to test, explicit session/permission model required, manifest and doctor
    logic must understand gateway mode.'
  deciders:
  - ACTOR-user
  - ACTOR-codex
  decided_at: '2026-05-02T07:43:51+00:00'
  related_workitems:
  - BACK-20260502_0743-CalmHawk-implement-provider-neutral-gateway-daemon
---
