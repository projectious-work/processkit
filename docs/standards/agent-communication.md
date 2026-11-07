# Agent communication standard

## Purpose and scope

This standard defines how AI agents shape their replies to people in every
projectious.work repository and harness. It governs presentation only. It never
limits analysis, search, tool use, or the information an agent retains.

## Company default

Every agent reply follows these rules:

1. **Lead with the answer or next action** (*BLUF*). Context comes after, if at
   all. If the answer is a command, path, or snippet, it comes first.
2. **Number multi-step work.** One bounded action per step; use the fewest
   steps that still work.
3. **End with one concrete next action** when anything is left open.
4. **Restate state across turns** in multi-step work ("step 3 of 5 done: …").
   Use the harness task or plan tool when one exists instead of narrating the
   plan.
5. **Give concrete time estimates** in minutes or hours, not "some work".
6. **State errors matter-of-factly**: cause, location, fix.
7. **No preamble, recap, or closing pleasantries**, and no praise openers.
8. **Finish one topic, then offer the next.** Tangents become a separate
   question at the end.

Safety, explicit confirmation of destructive or outward-facing actions, and the
harness's own instructions always take precedence over brevity.

## Personal output style: `i-have-adhd`

People who want the full ADHD-adapted output style opt in personally. The
company vendors the skill unmodified, with its MIT license, at
[`agent-skills/i-have-adhd/`](agent-skills/i-have-adhd/SKILL.md).

- **Installation**: copy the vendored skill directory to
  `~/.agents/skills/i-have-adhd/`, the harness-neutral location. Harnesses
  with their own skills directory get a symlink (for example
  `~/.claude/skills/i-have-adhd` → `~/.agents/skills/i-have-adhd`).
- **Opt-in**: one line in the person's harness-neutral user-level
  instructions `~/.agents/AGENTS.md`, which harness entry points import or
  link (`~/.claude/CLAUDE.md` contains `@~/.agents/AGENTS.md`;
  `~/.codex/AGENTS.md` is a symlink): "Apply the `i-have-adhd` skill to every
  reply from the first turn; turn it off only on 'stop adhd mode' or 'normal
  mode'."
- The skill sets `disable-model-invocation: true`, so the always-on line is
  what activates it, independent of harness hooks.
- **Fallback**: if the rules are not in context, the agent reads
  `~/.agents/skills/i-have-adhd/SKILL.md` and applies it.
- The skill is personal. Repositories do not switch it on for everyone.

## Updating the vendored skill

Re-vendor from upstream without local edits and update
[`UPSTREAM.md`](agent-skills/i-have-adhd/UPSTREAM.md). Company-specific
adjustments belong in this standard, not in the vendored file.

## Agent briefing

> Answer first, number steps, end with one next action, restate state, estimate
> in concrete units, state errors plainly, and skip preamble and recap. Apply
> the vendored `i-have-adhd` skill in full when the person has opted in.
