---
name: debugging
description: |
  Systematic debugging — reproduce, read the error, isolate, hypothesize, fix, verify, document. Use when tracking down a bug, unexpected behavior, or test failure — including phrases like "this doesn't work", "why is this failing", or "help me debug".
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v1
    id: SKILL-debugging
    version: "1.1.0"
    created: 2026-04-06T00:00:00Z
    category: process
    layer: 3
---

# Debugging

## Intro

Debugging is a fixed loop: reproduce the failure, read the error,
isolate the cause, fix it, verify the fix, and add a regression
test. Skipping steps causes the bug to come back.

## Overview

### The debugging loop

1. **Reproduce** — get the exact steps, inputs, and error
   messages. Confirm you can trigger the issue on demand.
2. **Read the error** — parse the full stack trace or error
   message. The root cause is usually in the first or last frame,
   not the middle.
3. **Isolate** — narrow the scope:
   - Binary search through code (comment out halves)
   - Check recent changes (`git log`, `git diff`)
   - Add targeted logging or print statements
   - Test with the minimal failing input
4. **Hypothesize and test** — form a theory, then test it. Change
   one thing at a time.
5. **Fix** — apply the minimal change that resolves the issue.
6. **Verify** — confirm the original error is gone, run the full
   test suite for regressions, and exercise edge cases near the
   fix.
7. **Document** — add a test that would have caught this bug, and
   a comment if the fix is non-obvious.

### Common diagnosis paths

- **Tests pass locally, fail in CI** — environment differences:
  OS, dependency versions, file paths, timezone, locale, or race
  conditions in parallel tests. Compare CI logs with local output
  to find the divergence point.
- **Function returns wrong results for some inputs** — get the
  specific failing inputs, add assertions at intermediate steps,
  find where actual diverges from expected, trace back.

## Full reference

### Anti-patterns

- **Shotgun debugging** — changing many things at once. You won't
  know which fix worked, and you'll introduce new bugs.
- **Print-statement spelunking with no plan** — adding prints is
  fine, but each one should test a specific hypothesis.
- **Skipping reproduction** — "it sometimes fails" is not a bug
  report. Find the trigger first.
- **Stopping at the first fix** — the first thing that makes the
  symptom go away is often masking the real cause. Verify the
  underlying state is correct, not just the visible output.
- **No regression test** — if you don't add a test, the bug will
  return.

### Tools and techniques

- **`git bisect`** for regressions: a known-good and known-bad
  commit narrows the offending change in log(N) steps.
- **Debuggers over prints** when state is rich (object graphs,
  step-through control flow).
- **Differential debugging** — diff the working case against the
  failing case, not the other way around.
- **Rubber-duck explanation** — articulating the problem out loud
  often surfaces the bug before you write any code.

### When to stop and ask

If you've spent more than ~30 minutes without forming a viable
hypothesis, stop and either gather more information (logs,
reproduction steps, recent commits) or escalate. Continued flailing
is not progress.
