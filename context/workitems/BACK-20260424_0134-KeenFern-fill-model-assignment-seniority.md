---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260424_0134-KeenFern-fill-model-assignment-seniority
  created: '2026-04-24T01:34:50+00:00'
spec:
  title: Fill model-assignment seniority ladder gaps — specialist + expert bindings
    for all 10 seeded roles (v0.21.0)
  state: backlog
  type: task
  priority: medium
  assignee: TEAMMEMBER-cora
  description: "**Observed gap (v0.20.0 session):** the roster at `context/team/roster.md`\
    \ declares the seniority ladder as `junior → specialist → expert → senior → principal`\
    \ (5 levels), but the default-bindings pack under `context/skills/processkit/model-recommender/default-bindings/`\
    \ seeds only **3 levels** (junior, senior, principal). `resolve_model(<role>,\
    \ \"specialist\")` and `resolve_model(<role>, \"expert\")` return `{\"error\"\
    : \"no viable model for role=... seniority=...\"}` for **every one of the 10 seeded\
    \ roles**.\n\n**Affected roles (all 10):** ai-research-scientist, assistant, data-scientist,\
    \ product-manager, qa-engineer, research-scientist, security-architect, software-engineer,\
    \ solutions-architect, technical-writer.\n\n**Total missing bindings:** 10 roles\
    \ × 2 seniorities = 20.\n\n**Scope (v0.21.0):**\n\n1. Add 20 `model-assignment`\
    \ bindings via the binding-management MCP. For each (role, seniority) pair pick:\n\
    \   - `specialist` — slot between junior and senior; usually same model as senior\
    \ but with a lower effort band, OR one tier above junior when that's more natural\
    \ for the role.\n   - `expert` — slot between senior and principal; usually same\
    \ model as senior but with a higher effort ceiling, OR same as principal with\
    \ a slightly lower effort floor.\n   Use the existing junior/senior/principal\
    \ rationales as the template; the pattern is consistent (see existing BIND-*.md\
    \ files under `context/bindings/`).\n\n2. Update `context/skills/processkit/model-recommender/default-bindings/MANIFEST.yaml`\
    \ to include the 20 new entries so fresh derived-project installs ship with the\
    \ full 5-level ladder.\n\n3. Add a one-line regression test to `scripts/smoke-test-servers.py`\
    \ (or model-recommender's own test) that loops the 5 seniorities × the 10 seeded\
    \ roles and asserts `resolve_model()` returns at least one candidate for each.\
    \ This catches any future gap.\n\n4. Consider (but do NOT ship in this WI): extending\
    \ `resolve_model` with an ordinal-adjacent-fallback so a missing seniority falls\
    \ back to the nearest covered one. That's a bigger design change — file as a separate\
    \ follow-up if desired.\n\n**Done when:**\n- `resolve_model(role, seniority)`\
    \ returns a viable candidate for all 50 `(role, seniority)` combinations in the\
    \ seeded set.\n- MANIFEST.yaml lists 50 bindings (was 30).\n- pk-doctor 0 ERROR\
    \ / 0 WARN. Drift green.\n- Regression test passes.\n\n**Target:** v0.21.0. **Owner:**\
    \ cora. **Priority:** medium — not release-blocking for v0.21.0 but highly visible\
    \ once anyone tries the specialist/expert tiers."
---
