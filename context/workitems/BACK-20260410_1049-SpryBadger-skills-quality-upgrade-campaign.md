---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260410_1049-SpryBadger-skills-quality-upgrade-campaign
  created: '2026-04-10T10:49:28+00:00'
spec:
  title: Skills quality upgrade campaign — bring thin-tier skills to deep-tier standard
  state: backlog
  type: chore
  priority: medium
  description: 'The March 2026 quality audit (NOTE-20260410_1046-RapidPeak) found
    ~55% of skills are "thin-tier": no code examples (54% of skills), no allowed-tools
    declaration (55%). The audit covered 85 skills; processkit now ships 128+, warranting
    a fresh audit.


    Process:

    1. Run skill-reviewer against all src/context/skills/ entries

    2. Identify thin-tier skills (no code blocks, no allowed-tools)

    3. Upgrade 5 skills per sprint using skill-builder patterns

    4. Priority: process skills (highest agent usage) first


    Start with a fresh audit using skill-reviewer before upgrading.'
---
