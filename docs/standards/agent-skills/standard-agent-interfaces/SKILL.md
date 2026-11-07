---
name: standard-agent-interfaces
description: Company standard for agent-native product interfaces. Use when a product exposes MCP tools or other agent-facing operations that validate, mutate, deploy, or administer state: MCP/CLI parity, application core, tool schemas, authorization and approval, durable operations, prompt/tool injection, and transport security.
---

# standard-agent-interfaces

Binding company standard. The rules below are the summary; the linked file is authoritative. Read only the section the task needs.

## Agent-native product interfaces

Products that expose consequential operations to agents keep probabilistic reasoning (goals, synthesis, proposals) apart from deterministic mechanisms (validation, authority, mutation, recovery, evidence). MCP and CLI are equivalent adapters over one interface-neutral application core; the CLI stays a complete recovery path. Tools have strict versioned schemas, no arbitrary shell, typed results and safe next actions. Natural language, model confidence, and client confirmation are never identity or approval; self-approval is denied and secrets never appear in tool output. Mutations are idempotent or carry a durable operation id and report partial failure explicitly.

Full standard: `docs/standards/agent-native-product-interfaces.md`. Sections:

- Purpose and scope
- Product posture
- Interface architecture
- Capability design
- Resources, results, and next actions
- Identity and authorization
- Durable operations and recovery
- Security threats
- Transport and deployment
- Verification and release
- Relationship to other standards
