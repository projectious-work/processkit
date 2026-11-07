---
apiVersion: processkit.projectious.work/v2
kind: Discussion
metadata:
  id: DISC-20260416_0800-CommandScope-v017-command-strategy-session
  created: '2026-04-16T08:00:00+00:00'
spec:
  title: v0.17.0 command strategy — /pk- namespace, cross-harness uniformity, AGENTS.md-driven
    build/test
  question: What is the v0.17.0 slash-command scope for processkit — which commands
    to ship, what namespace, how to handle cross-harness uniformity and AGENTS.md-driven
    build/test/lint?
  state: concluded
  participants:
  - ACTOR-pm-claude
  - ACTOR-20260421_0144-ThriftyOtter-owner
  summary: |
    Multi-turn working conversation on 2026-04-15 → 2026-04-16 that produced the v0.17.0 slash-command scope and refined the strategic principle in DEC-CommandNexus. Captured here because the owner explicitly requested the discussion context be preserved against accidental /clear or session loss.
  key_exchanges:
  - topic: /pk- namespace adoption
    owner_position: |
      Wants clear distinction between processkit-shipped and harness-built-in commands. Proposed pk- prefix.
    outcome: Adopted. All processkit commands ship as /pk-<verb>.
  - topic: Session lifecycle decomposition
    owner_position: |
      /onboard was wrong framing. Three distinct moments: session start (agent reads context, gives status + recommendation), mid-session status check, session end (wrap up, handover log).
    outcome: |
      /pk-resume (start), /pk-status + alias /pk-standup (mid), /pk-wrapup (end). Owner accepted /pk-resume + /pk-wrapup naming; vetoed /pk-wrap in favor of /pk-wrapup.
  - topic: /pk-decide dropped
    owner_position: |
      Decisions are conversational — 70% yes/no but 30% questions or redirects. A slash command doesn't fit the moment. Rely on Rail 5 shadow-mode + long-form /decision-record-write.
    outcome: Dropped from v0.17.0. Revisit after LLM-classifier.
  - topic: Capture split into /pk-note + /pk-discuss
    owner_position: |
      Two distinct patterns: (1) fleeting capture of unordered ideas/features → later promoted; (2) structured discussion where the owner has a thought and wants agent input/research.
    outcome: |
      /pk-note on note-management (with Zettelkasten qualified-link emphasis), /pk-discuss on discussion-management.
  - topic: Zettelkasten qualified links at capture + transition time
    owner_position: |
      Essential. When recording a note, search for and propose useful qualified links. At transitions/promotions, check against the note corpus. Goal: build a knowledge web.
    outcome: |
      v0.17.0: doc-driven link suggestion via search_entities at /pk-note capture time. v0.18.0+: programmatic link-suggest MCP tool on cross-reference-management.
  - topic: Provider independence re-evaluation
    owner_position: |
      Earlier answers were too Claude-Code-focused. Need cross- harness analysis of which commands are actually uniform.
    outcome: |
      Cross-harness matrix built. Finding: outside session housekeeping, harness built-in command sets are almost completely non-overlapping. Planning, release, research, meta = zero built-in coverage anywhere. This confirmed the hypothesis that processkit should fill the gaps.
  - topic: Build/test/lint as processkit commands
    owner_position: |
      If /test is built into Aider but not Claude Code/Cursor/ OpenCode, a user switching harnesses loses /test. processkit should make this uniform.
    outcome: |
      Reversed the DEC-CommandNexus exclusion. processkit DOES ship /pk-test, /pk-build, /pk-lint as AGENTS.md-driven commands (read project's declared command from a structured YAML block in AGENTS.md, execute it). Provider-neutral AND project- neutral. DEC-CommandNexus amended.
  - topic: Alias vs own implementation
    owner_position: Asked for analysis.
    outcome: |
      Always own implementation, never alias a harness built-in. /pk-test reads AGENTS.md, not the harness's /test. pk- prefix avoids collision; both coexist.
  - topic: AGENTS.md-driven command surface
    owner_position: |
      Structured YAML block preferred over heading-name lookup.
    outcome: |
      Add a pk-commands YAML block to AGENTS.md declaring project- specific build/test/lint/fmt commands. /pk-test reads this block and executes the declared command.
  conclusion: |
    v0.17.0 ships 12 /pk- commands (9 skill-driven + 3 AGENTS.md- driven) + 1 bug fix. DEC-CommandNexus amended to remove the build/test/lint exclusion. Discussion recorded per owner request.
  outcomes:
  - DEC-20260415_2030-CommandNexus-pk-prefix-namespace-and-command-strategy
---

# Discussion log

This discussion spanned the 2026-04-15 evening session and continued
into 2026-04-16 morning. The full conversational context is in the
Claude Code session transcript; this entity captures the strategic
content so it survives /clear or session loss.

See `spec.key_exchanges` above for the structured record of each
topic, the owner's position, and the outcome.

## Cross-references

The original `spec.related` list held IDs that the Discussion schema's
`related` field cannot carry (it accepts only `DISC-…` entries). They
are preserved here instead:

- DecisionRecord produced by this discussion (now in `spec.outcomes`):
  `DEC-20260415_2030-CommandNexus-pk-prefix-namespace-and-command-strategy`
- Artifacts referenced during the discussion:
  - `ART-20260415_1830-CommandCompass-processkit-slash-command-inventory-and-proposal`
  - `ART-20260415_2000-ShadowCount-rail5-marker-calibration`
