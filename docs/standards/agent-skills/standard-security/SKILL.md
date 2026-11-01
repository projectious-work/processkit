---
name: standard-security
description: Company security and software-supply-chain standard. Use when handling untrusted input, paths, subprocesses, secrets or sensitive data, adding or updating dependencies, signing or attesting releases, or responding to a vulnerability.
---

# standard-security

Binding company standard. The rules below are the summary; the linked file is authoritative. Read only the section the task needs.

## Security and software-supply-chain standard

Identify the trust boundary before coding. Preserve argument and path
boundaries, redact before data leaves the core, review every direct
dependency, and verify the final published artifact rather than trusting the
source build alone.

Full standard: `docs/standards/security-and-software-supply-chain.md`. Sections:

- Purpose and scope
- Security model
- Input, filesystem, and process safety
- Secrets and sensitive data
- Dependency policy
- Release supply chain
- Security regressions and response
