---
title: Alpha.3 Closure Plan
description: Feature-completion gates for the final pre-cutover alpha.
---

`v1.0.0-alpha.3` is the feature-complete pre-cutover target. It does not
authorize a merge to `main`; v0.x remains the stable line until the owner
accepts the final ontology, migration, CLI, and aibox evidence.

The machine-readable gate ledger is
`docs-site/data/v1_alpha3_gates.yaml`. It tracks all 81 original v1 criteria
and all 15 installer criteria from issue #118. A criterion may be `met`,
`partial`, `missing`, `owner-review`, or `deferred-post-cutover`.

Alpha.3 closes the pre-cutover implementation work:

1. complete the 89-concept ontology and 70 executable schema contracts;
2. provide operational MCP, index, transition, and event parity;
3. migrate representative manual-v0 and aibox-managed corpora;
4. execute the retained agent-scenario and first-ART suites;
5. finish installer planning, structured reconciliation, security, and
   Codex/Claude parity;
6. validate the exact release artifact in a bare aibox container; and
7. publish reproducible, signed, exact-pinnable release assets.

The G6 owner decision and every R7 criterion remain outside alpha.3 because
they require an actual cutover and post-cutover observation.
