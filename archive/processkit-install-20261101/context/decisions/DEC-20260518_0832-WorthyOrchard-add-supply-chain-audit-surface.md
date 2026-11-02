---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260518_0832-WorthyOrchard-add-supply-chain-audit-surface
  created: '2026-05-18T08:32:43+00:00'
spec:
  title: Add Supply Chain Audit Surface
  state: accepted
  decision: Add a dedicated processkit supply-chain-audit surface consisting of a
    supply-chain-audit skill, pk-supply-chain command, supply-chain-audit MCP server,
    and a lightweight pk-doctor supply_chain category. Keep dependency-management
    as dependency process guidance and dependency-audit as tactical vulnerability/update
    guidance; use supply-chain-audit for dependency inventory, license classification,
    SBOM/reporting, vulnerability/outdated orchestration, and supplier quality signals.
  context: The user approved the proposal after reviewing overlap with dependency-management
    and dependency-audit. Primary objective is license and usage-risk visibility;
    secondary objective is CVE/newer-version review; tertiary objective is supplier
    stability and quality heuristics.
  rationale: 'The existing dependency-* skills cover engineering workflow and scanner
    triage, but they do not provide a governance/reporting surface for included software
    licenses, usage risk, release evidence, or supplier risk. Separating the surfaces
    keeps user UX clear: dependency-* for changing dependencies, pk-supply-chain for
    accounting for them.'
  alternatives:
  - option: Fold into dependency-audit
    reason: Rejected because it would overload a tactical CVE/update skill with legal/governance
      inventory and SBOM concerns.
  - option: Only add pk-doctor check
    reason: Rejected because doctor summaries are too narrow for full inventory, SBOM
      export, scanner orchestration, and policy exceptions.
  - option: Single all-in-one mandatory online scanner
    reason: Rejected because derived projects need deterministic offline-safe behavior
      and predictable UX in restricted environments.
  consequences: 'Implement in phases: offline deterministic license inventory first;
    optional security/outdated probes second; advisory supplier quality third. pk-doctor
    should expose a summary health signal, not become a full SCA engine. Network-dependent
    probes must be opt-in or clearly skipped.'
  related_workitems:
  - BACK-20260518_0832-CleverSpruce-supply-chain-audit-surface
  decided_at: '2026-05-18T08:32:43+00:00'
---
