---
apiVersion: processkit.projectious.work/v1
kind: Artifact
metadata:
  id: ART-20260414_1500-ClearSignal-codex-agents-md-reinjection-probe
  created: 2026-04-14T15:00:00Z
spec:
  name: "Codex CLI AGENTS.md re-injection probe — session-start-only, not per-turn"
  kind: document
  location: context/artifacts/ART-20260414_1500-ClearSignal-codex-agents-md-reinjection-probe.md
  format: markdown
  version: "1.0.0"
  tags: [research, codex, enforcement, processkit, agents-md, hooks]
  produced_by: BACK-20260414_1435-QuietProbe-codex-reinjection-probe
  owner: ACTOR-jr-researcher
  links:
    workitem: BACK-20260414_1435-QuietProbe-codex-reinjection-probe
    related_artifacts:
      - ART-20260414_1230-ReachReady-processkit-enforcement-research
      - ART-20260414_1430-SteadyBeacon-enforcement-implementation-plan
---

# Codex CLI AGENTS.md re-injection probe

**Author:** Jr Researcher (Sonnet) · **Date:** 2026-04-14
**WorkItem:** `BACK-20260414_1435-QuietProbe-codex-reinjection-probe`
**Method used:** Docs + source (Method 2) — the `codex` CLI binary is not available in this environment; the empirical probe (Method 1) could not be run. The documentary evidence is sufficiently clear that a confident answer is possible without it.

---

## Finding

**AGENTS.md content is loaded once per session (at session start) and is NOT re-injected on every turn.**

Confidence: **Likely** (strong multi-source documentary evidence; empirical probe not run due to CLI unavailability)

---

## Evidence chain

### E1 — Official docs: "limited amount in the first turn" [Confirmed]

The official OpenAI Codex AGENTS.md guide states:

> "Codex reads AGENTS.md (and related files) and includes a limited amount of project guidance **in the first turn of a session**."

Source: https://developers.openai.com/codex/guides/agents-md (fetched via search, April 2026)

This is the direct primary-source quote that the earlier research (ART-20260414_1230-ReachReady §6) flagged as uninstrumented. The phrase "first turn of a session" explicitly scopes injection to session start.

### E2 — "Builds an instruction chain once per run" [Confirmed]

The Bolin / OpenAI post "Unrolling the Codex agent loop" (https://openai.com/index/unrolling-the-codex-agent-loop/) states:

> "Codex builds an instruction chain when it starts (**once per run**; in the TUI this usually means once per launched session)."

This is a second authoritative source confirming that the instruction chain — which contains AGENTS.md user-role messages — is constructed once, not rebuilt per turn.

Source: https://openai.com/index/unrolling-the-codex-agent-loop/

### E3 — GitHub issue #3198 closed "not planned" [Confirmed]

The GitHub issue "AGENTS.md should be reloaded on Each Turn" (openai/codex#3198, opened 2025-09-05) explicitly requested per-turn re-injection. OpenAI closed it as **"not planned"**. This is an explicit product decision to keep the session-start-only behaviour.

Source: https://github.com/openai/codex/issues/3198

### E4 — GitHub issue #8547 corroborates: edits don't take effect mid-session [Confirmed]

Issue #8547 "Automatically reread AGENTS.md within a session when it is modified" reports:

> "When you initialize Codex on a repository with an AGENTS.md file … then modify or remove the instruction content, and run another task **in the same Codex session**, Codex still follows the old or removed instructions."

This behaviour — where mid-session edits are ignored — is only explicable if AGENTS.md is not re-read on each turn.

Source: https://github.com/openai/codex/issues/8547

### E5 — Compaction re-prepends fixed items, but AGENTS.md is not among them [Likely]

The Codex agent loop re-prepends two items after a compaction event: a `role=developer` message containing `<permissions instructions>`, and a `role=user` message containing `<environment_context>`. AGENTS.md content is carried as separate `role=user` messages injected before the first user prompt — these are folded into the compacted `encrypted_content` blob (the model's latent understanding), not re-prepended as live text. They therefore survive compaction only as implicit model state, not as fresh verbatim text in the context window.

Sources: https://openai.com/index/unrolling-the-codex-agent-loop/ ; https://developers.openai.com/api/docs/guides/compaction

### E6 — Silent 32 KiB truncation: "limited amount" is real [Confirmed]

Issue #13386 (and #7138) confirms AGENTS.md content is capped at 32 KiB (`project_doc_max_bytes`) at read time. Even the once-per-session injection is partial for large files. This reinforces that the injection window is narrow and there is no compensating mechanism per turn.

Sources: https://github.com/openai/codex/issues/13386 ; https://github.com/openai/codex/issues/7138

---

## What the WorkItem probe method would have added

The empirical probe (insert sentinel → run 20 turns → query sentinel) would have moved confidence from **Likely** to **Confirmed** and would additionally reveal:

- Whether the compaction `encrypted_content` blob is sufficient for the model to recall a sentinel it saw at turn 1 after 20 turns of unrelated work.
- Whether mid-session AGENTS.md edits (the WorkItem's second probe) are ever picked up by any mechanism other than session restart.

Given the current evidence, those questions have practical answers: recall at turn 20 is plausible via latent state but not reliable as prose; mid-session edits are not picked up (E4).

---

## Recommendation

**Codex hooks remain primary enforcement transport on Codex.**

AGENTS.md injection at session start is subject to:
1. 32 KiB hard cap (silently truncated);
2. No re-injection on subsequent turns — rules evaporate from live context as conversation grows;
3. No re-injection after compaction as verbatim text — only as latent model state;
4. Mid-session edits are entirely invisible until session restart.

The compliance-contract hook scripts (`emit_compliance_contract.py` wired to `SessionStart` + `UserPromptSubmit` in `.codex/hooks.json`) are therefore the primary mechanism to keep enforcement rules in live context on Codex, exactly as concluded in SteadyBeacon §1.4. AGENTS.md (re-layered per `FEAT-RightPath`) remains valuable as the session-start anchor and for harnesses without hook support, but it is not a substitute for hooks on Codex.

The WorkItem `BACK-20260414_1433-SteadyHand-provider-neutral-hook-scripts` should be prioritised accordingly — there is no evidence that AGENTS.md alone is sufficient for multi-turn Codex sessions.

---

## Summary table

| Evidence item | Finding | Confidence |
|---|---|---|
| Official AGENTS.md docs: "first turn of a session" | Injection is session-start only | Confirmed |
| Bolin post: "instruction chain built once per run" | No per-turn rebuild | Confirmed |
| GH issue #3198 closed "not planned" | OpenAI explicitly rejects per-turn re-injection | Confirmed |
| GH issue #8547: mid-session edits ignored | Session-start-only behaviour observed in the wild | Confirmed |
| Compaction re-prepend analysis: AGENTS.md not in fixed items | Post-compaction content is latent state only, not live text | Likely |
| 32 KiB truncation cap | Even session-start injection is partial for large files | Confirmed |

**Overall finding confidence: Likely** (all documentary sources agree; empirical probe not run)

---

## Sources

- https://developers.openai.com/codex/guides/agents-md
- https://openai.com/index/unrolling-the-codex-agent-loop/
- https://github.com/openai/codex/issues/3198
- https://github.com/openai/codex/issues/8547
- https://github.com/openai/codex/issues/7138
- https://github.com/openai/codex/issues/13386
- https://developers.openai.com/api/docs/guides/compaction
