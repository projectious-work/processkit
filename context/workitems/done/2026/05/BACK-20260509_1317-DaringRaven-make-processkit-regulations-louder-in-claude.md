---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260509_1317-DaringRaven-make-processkit-regulations-louder-in-claude
  created: '2026-05-09T13:17:50+00:00'
  labels:
    github_issue: 19
    area: harness-claude-code
    cluster: agent-dispatch
  updated: '2026-05-10T03:46:06+00:00'
spec:
  title: Make processkit regulations 'louder' in Claude Code harness (gh#19)
  state: done
  type: task
  priority: medium
  description: 'Triaged from GH #19. Claude Code-specific companion to gh#18. Seven
    recommendations:\n1. Migrate pk-compliance v2 from per-turn UserPromptSubmit hook
    to a `compliance-refresh` skill loaded once per session (~60 lines/turn savings)\n2.
    Auto-configure `skillOverrides: name-only` for rarely-invoked verbose skills (team-creator,
    brand-package, etc.)\n3. Recommend `ENABLE_TOOL_SEARCH=auto` in harness env\n4.
    If keeping the hook, slim to 3 absolute non-negotiables + 1 positive ref\n5. Promote
    3 critical positive actions into the contract (Claude Code-aware)\n6. Bake TeamMember
    identity + RuntimeBinding into `export_claude_subagent` output\n7. Document harness
    contract: `docs/harness-claude-code.md` + `~/.claude/settings.example.json`\n\nIndependent
    of gh#18 — both needed.'
  started_at: '2026-05-09T14:12:26+00:00'
  completed_at: '2026-05-10T03:46:06+00:00'
---

## Transition note (2026-05-09T14:12:26+00:00)

Wave 3c dispatch — TEAMMEMBER-finn (SE/senior) on Sonnet 4.5. Scope: rec 4 (slim hook), rec 5 (positive actions in hook payload), rec 2 (skillOverrides=name-only), rec 3 (ENABLE_TOOL_SEARCH=auto), rec 6 (TeamMember identity in export_claude_subagent), rec 7 (docs/harness-claude-code.md + settings.example.json). Rec 1 (hook → session skill) REJECTED per DEC-20260509_1403-LivelyClover.


## Transition note (2026-05-09T14:20:24+00:00)

Wave 3c shipped 6 of 7 recs (rec 1 rejected by DEC-LivelyClover). Rec 4: Option B markers (`&lt;!-- BEGIN/END HOOK --&gt;`) in compliance-contract.md; emit_compliance_contract.py extracts slim block for UserPromptSubmit, full block for SessionStart. Rec 5: 14-line slim payload with 3 positive + 3 negative + 1 reference (now active — visible in this turn's hook reminder). Rec 2: skillOverrides=name-only for 4 large infrequent skills (skill-builder/reviewer 514+496 lines, team-creator 445, agent-management 437). Rec 3: ENABLE_TOOL_SEARCH=auto documented (sandbox blocked live settings.json write). Rec 6: export_claude_subagent now writes self-describing HTML-comment header with TeamMember ID/slug/role/seniority + resolved binding info. Rec 7: docs/harness-claude-code.md (~120 lines, 6 sections) + settings.example.json (landed at docs/ instead of .claude/ — sandbox-blocked). 4 new tests, all passing (hooks 87/87, team-manager 56/56). Trees in sync. Open: live .claude/settings.json untouched (managed file, installer-rewritten); skillOverrides shape not schema-validated against Claude Code.


## Transition note (2026-05-10T03:46:06+00:00)

Shipped to main on 2026-05-09 via PR #24; closing per v0.26.0 release prep.
