---
name: standard-spec-driven-development
description: Company spec-driven development cycle. Use when implementing a roadmap phase or material change against a specification: baselining the spec, building requirement inventories, planning and reviewing work packages, freezing the contract, writing acceptance tests, verifying, or closing phase evidence.
---

# standard-spec-driven-development

Binding company standard. The rules below are the summary; the linked file is authoritative. Read only the section the task needs.

## Spec-driven development-cycle standard

Baseline the specification, turn the roadmap item into a test-ready contract,
map every normative requirement, plan ownership and evidence, review contract
and plan independently, and freeze the contract. Then write user-facing
acceptance tests in a fresh session from the frozen contract only, implement
in parallel without seeing those tests, and loop until every test passes,
classifying each failure as implementation, test, contract, or
infrastructure defect. Verify independently against the same complete
baseline. No requirement disappears and no specification change is silent.
Small direct changes update baseline and tests in place.

Full standard: `docs/standards/spec-driven-development-cycle.md`. Sections:

- Purpose and scope
- Small-change path
- Principles
- 0. Establish the baseline
- 1. Build requirement, dependency, and risk inventories
- 2. Draft the implementation plan
- 3. Assign agents and models
- 4. Review the plan against the complete baseline
- 5. Approve and baseline the revised plan
- 6. Implement in controlled waves
- 7. Control discoveries and baseline changes
- 8. Verify implementation independently
- 9. Close gaps and repeat verification
- 10. Complete phase evidence
- 11. Retrospect and improve
- Required cycle record
