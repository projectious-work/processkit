---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260423_2049-VastLake-truequail-split-processkit-ships
  created: '2026-04-23T20:49:37+00:00'
spec:
  title: TrueQuail split — processkit ships manifest + pk-doctor check; aibox repo
    owns installer reconcile
  state: accepted
  decision: 'Split TrueQuail (BACK-20260423_0829-TrueQuail) across repos: processkit
    v0.19.2 ships (a) an aggregate sha256 manifest over all per-skill `mcp-config.json`
    files, regenerated at release time; (b) a pk-doctor check that compares the manifest
    hash against the derived project''s current `.mcp.json`-derived hash and flags
    drift locally; (c) a short `AGENTS.md` section documenting the manifest contract.
    The aibox repo ships the `aibox sync` change that always re-merges when the manifest
    hash differs, independent of version delta. Keep BACK-20260423_0829-TrueQuail
    open in the processkit backlog until both sides land; file a GitHub issue at projectious-work/aibox
    for the aibox-side work.'
  context: TrueQuail was filed in processkit's backlog but its named remedy ("installer
    re-merges on drift, not just on version delta") is aibox-CLI behavior. Aibox source
    is not in this repo — it lives at github.com/projectious-work/aibox. Attempting
    the full fix here would be misscoped. Confirmed by the user in-session.
  rationale: Processkit can deliver the version-independent drift signal (the manifest
    hash) without touching aibox, which immediately unblocks the pk-doctor safety
    net in every derived project. Aibox can then trivially consume the signal with
    a one-line comparison. Splitting the work avoids cross-repo coupling at release
    time and gives each repo a scope that fits its code.
  alternatives:
  - option: Implement the aibox fix from a processkit session via a cross-repo checkout
    reason_rejected: Violates repo boundaries; aibox source not available locally;
      risks divergent release cadences
  - option: Wait for the aibox fix and ship a processkit-side workaround later
    reason_rejected: Leaves derived projects without a drift warning for an indefinite
      period; the hand-merge violation keeps recurring
  - option: Close TrueQuail and re-file in the aibox repo only
    reason_rejected: Loses the processkit-side contributions (manifest + pk-doctor
      check) that are the actual safety net
  consequences: 'Derived projects on v0.19.2 will detect drift via `/pk-doctor` even
    before aibox ships its fix — they''ll still need a manual `aibox sync --force`
    (or equivalent) until the aibox change lands, but they will at least know. Sets
    a precedent for future cross-repo WIs: file in the repo whose code actually changes,
    or split into two WIs, rather than leaving a single misscoped item.'
  deciders:
  - TEAMMEMBER-thrifty-otter
  - TEAMMEMBER-cora
  related_workitems:
  - BACK-20260423_0829-TrueQuail-aibox-installer-reconcile-mcp
  decided_at: '2026-04-23T20:49:37+00:00'
---
