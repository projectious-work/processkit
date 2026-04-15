---
apiVersion: processkit.projectious.work/v1
kind: Artifact
metadata:
  id: ART-20260415_1525-LandscapeSummary-ai-provider-comparison-april-2026-structured
  created: '2026-04-15T15:25:00+00:00'
spec:
  name: "AI provider comparison — April 2026 (structured summary)"
  kind: reference-dataset
  location: context/artifacts/ART-20260415_1525-LandscapeSummary-ai-provider-comparison-april-2026-structured.md
  format: markdown
  version: "1.0.0"
  tags: [landscape, landscape-summary, providers, models, cost, benchmarks, team-creator]
  owner: ACTOR-jr-developer
  processed_by: ACTOR-jr-developer
  processed_at: '2026-04-15T15:25:00+00:00'
  source_artifact: ART-20260415_1510-LandscapeSnapshot-ai-provider-comparison-april-2026
  summary: >
    Structured markdown extraction of six major AI providers (Anthropic,
    OpenAI, Google Gemini, Mistral, xAI Grok, DeepSeek) with 8 tables covering
    subscription tiers, €90/mo budget analysis, coding benchmarks, decision
    matrix, automated agent policy, head-to-head comparison, model ladder, and
    API pricing. Extracted from HTML snapshot captured 2026-04-14. All tables,
    prices, and model names preserved verbatim.
  consumes:
    - ART-20260415_1510-LandscapeSnapshot-ai-provider-comparison-april-2026
  consumed_by:
    - FEAT-20260415_1505-TeamWeaver-team-creator-skill
  freshness: |
    Snapshots of the provider landscape go stale within a quarter.
    Re-capture before every `team-rebalance` run. This snapshot is
    valid as of 2026-04-14; treat anything older than 2026-07-14 as
    suspect.
---

# AI provider comparison — April 2026 (Structured Summary)

**Source:** HTML snapshot from 2026-04-14
**Updated:** 2026-04-15 11 April 2026 — includes OpenAI's new $100 Pro
tier (9 Apr) and Google Gemma 4 open-weight family (2 Apr)

---

## Subscription Plans & Pricing

| Provider | Plan | Price / mo | Top Model(s) Included | Context Window | Key Limits / Notes |
|----------|------|-----------|----------------------|-----------------|------------------|
| Anthropic Claude | Pro | $20 | Opus 4.6, Sonnet 4.6, Haiku 4.5 | 200K (1M for Opus) | 5-hr rolling window + weekly cap. Claude Code included. Extended thinking. Peak-hour throttling since March. |
| Anthropic Claude | Max 5× | $100 | Same + priority access | Same | 5× Pro usage. Same 5-hr + weekly structure. Priority routing. |
| Anthropic Claude | Max 20× | $200 | Same + highest priority | Same | 20× Pro usage. Highest priority. Still reports of heavy users hitting limits. |
| OpenAI ChatGPT | Plus | $20 | GPT-5.4, o3, o4-mini, Codex | 128K (GPT-5.4), 256K (reasoning) | ~150 GPT-5.4 msgs / 3-hr window. 100 o3/week. 300 o4-mini/day. Codex included (baseline). "Rebalanced" 9 Apr: more sessions/week, fewer per day. |
| OpenAI ChatGPT | Go | $8 | GPT-5.4 (limited) | ~40 pages equiv. | Ad-supported. Lower limits. No Codex. Launched Jan 2026. |
| OpenAI ChatGPT | Pro 5× | $100 | GPT-5.4, Pro model, GPT-5.3-Codex, all Instant & Thinking models | 400K (reasoning) | 5× Plus Codex usage (10× thru May 31 promo). 5-hr rolling window. GPT-5.4: 20–100 local msgs/5hrs. Codex: 30–150 local + 10–60 cloud tasks/5hrs. Exclusive GPT-5.3-Codex-Spark preview. All Pro features. |
| OpenAI ChatGPT | Pro 20× | $200 | Same as Pro 5× + maximum allowance | 400K (reasoning) | 20× Plus usage. Unlimited Instant/Thinking. Pro reasoning mode. Full Sora 2 / DALL·E. 120 Deep Research/mo. Still listed but de-emphasized on pricing page. |
| Google Gemini | AI Pro | $20 (€19.99) | Gemini 3.1 Pro, 2.5 Pro, Flash | 1M tokens | 1,000 AI credits/mo. Deep Research. Workspace integration. 2 TB storage. Jules coding agent (5× free limits). |
| Google Gemini | AI Ultra | $250 | Gemini 3.1 Pro (highest), Deep Think, Veo 3.1 | 1M tokens | 25,000 AI credits/mo. Highest limits. Project Mariner (10 parallel agent tasks). YouTube Premium. 30 TB storage. |
| Google Gemini | Free | $0 | Gemini 2.5 Flash (+ limited 3 Pro in US) | 32K | ~15–30 queries/day. Thinking mode limited. No Deep Research. |
| Mistral Le Chat | Pro | $15 (€14.99) | Mistral Large 3, Medium 3, Codestral | 128K | ~150 msgs/day soft cap. Flash Answers (1000 wps). No-Telemetry mode. 15 GB doc storage. Codestral in-chat. EU data residency / GDPR. |
| Mistral Le Chat | Free | $0 | Mistral Medium, Small | 32K | ~25 msgs/day. Same inference speed. No Mistral Large access. |
| xAI Grok | SuperGrok Lite | $10 | Grok 3.5 | 128K | Basic access to newer model. Limited DeepSearch. |
| xAI Grok | SuperGrok | $30 | Grok 4, 4.1 | 2M tokens | DeepSearch, Big Brain mode, image/video gen. Real-time X data. Voice mode. |
| xAI Grok | SuperGrok Heavy | $300 | Grok 4 Heavy (multi-agent) | 2M+ (428K memory) | Multi-agent parallel reasoning. Maximum compute priority. Extended thinking. |

**Note:** Alongside the new $100 tier, OpenAI "rebalanced" Plus Codex limits
— spreading usage across more sessions/week but reducing per-day allowance.
Effectively a Plus nerf timed with the upsell launch. Promo limits (10× for
Pro 5×) end May 31.

---

## Value at ~€90/mo Budget (≈ Claude Max 5×)

| Provider | What €90/mo buys | Coding Agent | Practical daily usage | Limit transparency |
|----------|------------------|--------------|----------------------|-------------------|
| Claude | Max 5× ($100) — 5× Pro limits | Claude Code (included, shared quota) | Post-promo: heavy users report 1–4 hrs before hitting 5-hr window. Peak-hour throttling. | Opaque — no published token quotas, only relative multipliers |
| ChatGPT | New Pro 5× ($100) — 5× Plus Codex usage (10× thru May 31 promo) | Codex (5× Plus limits). Full via Pro 20× ($200). | All Pro features, Pro model access, exclusive Codex-Spark. GPT-5.4: 20–100 local msgs/5hrs. Matches Claude Max 5× pricing exactly. | Moderate — published message ranges per model, but "rebalanced" Plus limits raise trust questions |
| Gemini | AI Pro ($20) + ~$70 API credits OR save | Jules (included, 5× free limits on Pro) | 1M context is generous. Credits system can be confusing. Workspace integration strong. | Moderate — credit-based system, limits shown in UI |
| Mistral | Pro (€14.99) + ~€75 for API / second sub | Codestral in Le Chat. API separate. | 150 msg/day soft cap with fastest inference (~1000 wps). Cheapest premium tier. | Clear — straightforward daily cap, no telemetry mode |
| Grok | SuperGrok ($30) + ~$60 for API or other | No dedicated coding agent | 2M context unique. Real-time data strong. Coding via chat only. | Opaque — "soft caps" not documented |

---

## Coding Capability — Benchmarks & Models (March 2026)

| Model | Provider | SWE-bench Verified | SWE-bench Pro | LiveCodeBench | Community Coding Rating | Strengths |
|-------|----------|-------------------|---------------|----------------|------------------------|-----------|
| Claude Opus 4.6 | Anthropic | 80.8% | ~46% | Strong | ★ 9.5/10 | Complex refactoring, multi-file changes, intent understanding on vague prompts, architecture. Powers Cursor & Windsurf. |
| Claude Sonnet 4.6 | Anthropic | ~75% | — | Good | ★ 8.5/10 | Best daily-driver balance of speed/cost/quality. Clean, idiomatic code. Strong types. |
| GPT-5.4 | OpenAI | ~80% | 57.7% | Strong | ★ 9.0/10 | Best all-rounder. Agent loops. Native computer use. 1M context in Codex. Structured output king. |
| GPT-5.3 Codex | OpenAI | ~78% | Strong | Strong | ★ 8.8/10 | Tuned for agentic coding. Faster, more concise. Explicit instruction following. |
| GPT-5.4 Mini | OpenAI | — | 54.4% | Good | ★ 7.8/10 | 94% of GPT-5.4 coding at ~6× lower cost ($0.40/$1.60). 2× faster. 72% OSWorld. Free tier access. Collapses at 64K+ context and terminal ops. Best as subagent / daily driver. |
| Gemini 3.1 Pro | Google | 80.6% | 54.2% | Leader | ★ 8.5/10 | 1M context for entire codebases. Cheapest frontier API ($2/$12). Needs precise prompts. Great for bulk. |
| Gemini 2.5 Flash | Google | ~65% | — | Good | ★ 7.2/10 | Ultra-cheap ($0.30/$2.50). Great for high-volume tasks. Sweet spot for cost/quality. |
| Grok 4 | xAI | ~75% | — | Competitive | ★ 8.0/10 | Real-time data integration. Strong reasoning. 2M context. Less mature coding ecosystem. |
| Mistral Large 3 | Mistral | ~68% | — | Good | ★ 7.2/10 | Cheapest premium API ($0.50/$1.50). 262K context. Strong multilingual. EU data residency. Codestral for code. |
| DeepSeek V4 | DeepSeek | ~78% | — | Strong | ★ 8.2/10 | Open-weight 1T params. 27× cheaper than closed peers. Best multilingual. V4 Lite self-hostable. Privacy concerns (China). |
| MiniMax M2.5 | Open-weight | 80.2% | — | Good | ★ 8.0/10 | Open-weight near frontier. $0.30/$1.20 API. Lightning variant at 100 tok/s. Self-hostable. |
| Gemma 4 31B Dense | Google | — | — | 80.0% | ★ 8.4/10 | Open-weight (Apache 2.0). 89.2% AIME, 86.4% τ2-bench agentic, 84.3% GPQA. Fits on 1×H100 or 2×A6000 at BF16 (~62GB). 256K ctx. Multimodal. #3 open model on Arena. Best for fine-tuning (dense arch). |
| Gemma 4 26B MoE | Google | — | — | 77.1% | ★ 8.2/10 | Only 3.8B active params → 80–150+ tok/s on 2×A6000. 88.3% AIME. Fits BF16 in ~50GB. 256K ctx. Multimodal. #6 open model on Arena. Apache 2.0. Best speed/quality for local self-hosting. |

---

## Decision Matrix — Which Provider for What

| If you need… | Best choice | Runner-up | Why |
|--------------|-------------|-----------|-----|
| Best code quality / refactoring | Claude Opus 4.6 | GPT-5.4 | Opus understands implicit constraints. Powers top IDE integrations. |
| Agentic coding / automation | GPT-5.4 + Codex | Claude Code | Native computer use, 1M context in Codex, fastest agent loops. |
| Largest codebase analysis | Gemini 3.1 Pro | Grok 4 | 1M context that actually works well. Cheapest at scale. |
| EU data residency / GDPR | Mistral | Self-hosted open-weight | French company, EU infra, no-telemetry mode, GDPR by design. |
| Maximum bang for €90/mo | Gemini Pro + Claude Pro | Mistral Pro + ChatGPT Plus | Two subs for ~€40, remaining budget for API. Use Gemini for bulk, Claude for hard problems. |
| Self-hosted / full control | Gemma 4 26B MoE / 31B | MiniMax M2.5 / DeepSeek V4 | Gemma 4 fits BF16 on 2×A6000 — no quant needed. Apache 2.0. US jurisdiction. Multimodal. MiniMax/DeepSeek are stronger on SWE-bench but require heavy quant and have China concerns. |
| Fastest local inference | Gemma 4 26B MoE | Gemma 4 31B Dense | 3.8B active params → 80–150+ tok/s. Faster than cloud Sonnet (40-60 tok/s). 31B Dense is slower (~40-60 tok/s) but higher quality. |
| Transparent, predictable limits | ChatGPT Plus | Mistral Pro | Published message counts. Mistral's ~150/day cap is simple and clear. |

---

## Automated Agent Policy — Subscription vs API (April 2026)

| Use Case | Anthropic Claude | OpenAI ChatGPT |
|----------|------------------|-----------------|
| Human-driven IDE tools (Cursor, Windsurf, Copilot) | ✅ Allowed via subscription | ✅ Allowed via subscription |
| Official coding agent (Claude Code / Codex) | ✅ Included in subscription (shared quota) | ✅ Included in subscription (separate Codex limits) |
| Third-party agent harness (OpenClaw, custom agents) | ❌ Technically blocked since April 4 — subscription tokens no longer work with 3rd-party harnesses | ⚠ Tolerated, not guaranteed — ToS says "Reselling access or using ChatGPT to power third-party services" is prohibited; enforcement is lax today but could change |
| Fully automated overnight agents (no human in loop) | ❌ Subscription: blocked. API: allowed (pay-per-token) | ⚠ ToS prohibits "automatically or programmatically extracting data." Currently not enforced for Codex. API: allowed. |
| API pay-per-token (no subscription) | ✅ Fully allowed for all use cases incl. automated agents | ✅ Fully allowed for all use cases incl. automated agents |

---

## Head-to-Head: Sonnet 4.6 vs GPT-5.4 Thinking — Code Quality

| Dimension | Sonnet 4.6 | GPT-5.4 Thinking | Winner |
|-----------|------------|------------------|--------|
| SWE-bench **Pro** (harder, uncontaminated) | ~44% | 57.7% | GPT-5.4 — significant gap |
| SWE-bench Verified (easier, contaminated) | 79.6% | ~80% | Tie (treat with caution) |
| Terminal-Bench 2.0 | — | 75.1% | GPT-5.4 — wide margin |
| Computer use (OSWorld) | 94% (insurance) | 75% (general) | GPT-5.4 — surpasses human baseline (72.4%) |
| Output speed (subscription) | 40–60 tok/s | 80–85 tok/s | GPT-5.4 |
| Context window | 1M tokens (standard pricing) | 128K–400K (1M in Codex mode) | Sonnet for large contexts |
| Intent understanding / vague prompts | Best-in-class — infers what you *meant* | Good but more literal | Sonnet |
| Code readability / style | Thoughtful senior-dev quality | Functional, "checklist-like" | Sonnet |
| Structured output / JSON | Good | Best-in-class | GPT-5.4 |
| Agent / tool orchestration | Good (Claude Code ecosystem) | Excellent (Toolathlon leader) | GPT-5.4 |
| API pricing (per M tok) | $3 / $15 | $2.50 / $15 | GPT-5.4 slightly |

**Summary:** GPT-5.4 wins on raw benchmarks, speed, terminal ops, and
agentic work. Sonnet 4.6 wins on code quality/style, intent understanding,
and large-context work. They complement each other well — which is why the
dual $100+$100 subscription makes sense for power users.

---

## Model Ladder — Quality, Quota Burn & Best Use (Opus = 100% Baseline)

All quality and quota figures are relative to **Claude Opus 4.6** as the
reference (100%). "In $100 sub" indicates whether the model is included in
the respective provider's $100/month subscription tier. Use this table to
decide which model to route each task to — saving your premium quota for
work that genuinely needs it.

### Anthropic Claude

| Model | Quality vs Opus | Speed | Quota burn vs Opus | API Price (in/out) | In $100 sub? | Best used for | When NOT to use |
|-------|-----------------|-------|-------------------|-------------------|--------------|---------------|------------------|
| Opus 4.6 | 100% (ref) | 20–30 tok/s | 1.0× (ref) | $5 / $25 | ✅ Max 5× | Complex multi-file refactoring, architecture decisions, Agent Teams, deep debugging where first-attempt accuracy matters | Simple questions, high-volume batch, anything time-sensitive (slow) |
| Sonnet 4.6 | ~95% | 40–60 tok/s | ~0.5× | $3 / $15 | ✅ Max 5× | Daily driver for 80%+ of tasks — coding, content, analysis. Best quality-to-cost ratio in the Claude family | Deepest reasoning tasks (Opus), maximum throughput needs (Haiku) |
| Haiku 4.5 | ~75% | 80–100+ tok/s | ~0.15× | $1 / $5 | ✅ Max 5× | Classification, triage, routing, linting, simple edits, high-volume batch. The "cheap filter" before escalating. | Nuanced reasoning, multi-step logic, long outputs (8K max) |

### OpenAI Model Ladder

| Model | Quality vs Opus | Speed | Quota burn vs Opus | API Price (in/out) | In $100 sub? | Best used for | When NOT to use |
|-------|-----------------|-------|-------------------|-------------------|--------------|---------------|------------------|
| GPT-5.4 Pro | ~103% | ~20–30 tok/s | N/A (dedicated GPU) | $30 / $180 | ✅ Pro 5× & 20× | Highest-stakes tasks — legal, medical, financial. Maximum accuracy. Dedicated compute = no shared-queue latency spikes. | Anything routine — the 12× premium over GPT-5.4 is almost never justified |
| GPT-5.4 Thinking | ~98% | 80–85 tok/s | ~0.5× | $2.50 / $15 | ✅ Pro 5× | Well-defined coding, structured output, agent loops, terminal ops, computer use. The "fast executor." | Ambiguous prompts where you need the model to "read your mind" (Sonnet is better) |
| GPT-5.4 Mini | ~83% | 150+ tok/s | ~0.15× | $0.75 / $4.50 | ✅ Pro 5× (+ Free) | Subagent work, autocomplete, simple code review, bulk CI checks. 94% of GPT-5.4 coding at ~6× less cost. Uses 30% of GPT-5.4 quota in Codex. | Long-context work (collapses at 64K+), terminal ops, complex agentic chains |
| GPT-5.3-Codex-Spark | ~80% | Near-instant | Separate limit | N/A (sub only) | ✅ Pro only (research preview) | Real-time pair programming. Near-zero latency for interactive "typing alongside you" coding. Pro-exclusive. | Heavy agentic work, batch processing, complex reasoning |
| GPT-5.4 Nano | ~70% | 200+ tok/s | N/A | $0.20 / $1.25 | ❌ API only | Classification, data extraction, ranking, routing, coding subagents for simple tasks. Cheapest GPT-5.4-class model. | Anything requiring quality reasoning, computer use (39% OSWorld), or long context |

**Quota-saving playbook:** On Claude Max 5×, route ~70% to Haiku, ~25% to
Sonnet, ~5% to Opus → stretches your session window ~3× vs all-Sonnet. On
OpenAI Pro 5×, route routine tasks to Mini (30% of GPT-5.4 quota) and use
Spark for interactive pairing → you get 3–5× more messages per window. Both
providers reward model routing with dramatically more usable daily capacity.

---

## API Pricing — All Models (for Agentic Fan-Out)

For automated agents you **need** API billing (subscriptions don't guarantee
automated use). This table helps evaluate cost-per-task when fanning out
across models. Sorted by output price. Prices as of April 2026.

| Model | Provider | Input / M tok | Output / M tok | Cache Hit | Batch Discount | Context | Best For (Agentic) |
|-------|----------|---------------|-----------------|-----------|----------------|---------|-------------------|
| DeepSeek V3.2 | DeepSeek | $0.28 | $0.42 | $0.028 (90% off) | — | 128K | Cheapest capable model. Bulk tasks, classification, simple coding. China jurisdiction. |
| GPT-5.4 Nano | OpenAI | $0.20 | $1.25 | — | 50% off (batch) | 400K | Cheapest GPT-5.4-class. 52% SWE-Pro. Classification, extraction, routing, simple coding subagents. API only — not in subscriptions. |
| MiniMax M2.5 | MiniMax | $0.15 | $1.20 | — | — | 200K | Near-Opus SWE-bench at 1/20th cost. Multi-file coding. Open-weight. China jurisdiction. |
| Gemma 4 26B MoE | Google (open) | $0.13 | $0.40 | — | — | 256K | Via OpenRouter. Or **self-host free** on 2×A6000 at BF16 (~50GB). 3.8B active → 80–150+ tok/s. 77% LiveCodeBench. Apache 2.0. Multimodal. |
| Gemma 4 31B Dense | Google (open) | ~$0.20 | ~$0.60 | — | — | 256K | Via OpenRouter (est.). Or **self-host free** on 2×A6000 at BF16 (~62GB). 80% LiveCodeBench, 89% AIME. Best open model for fine-tuning. |
| GPT-5.4 Mini | OpenAI | $0.75 | $4.50 | — | — | 400K | 94% of GPT-5.4 coding at ~3× less. Best subagent. Included in Free tier. Collapses at 64K+ context. |
| Haiku 4.5 | Anthropic | $1.00 | $5.00 | $0.10 (90% off) | 50% off | 200K | Classification, triage, simple edits. 5× cheaper than Sonnet. Batch+cache: $0.25/$1.25. |
| Gemini 3.1 Pro | Google | $2.00 | $12.00 | 75% off (explicit) | 50% off | 1M | Frontier quality at mid-tier price. 119 tok/s. 1M context that works. 2× pricing >200K. |
| GPT-5.4 | OpenAI | $2.50 | $15.00 | — | — | 1M (Codex) | Best all-rounder. 57.7% SWE-Pro. 75% OSWorld. Native computer use. 2× pricing >272K. |
| Sonnet 4.6 | Anthropic | $3.00 | $15.00 | $0.30 (90% off) | 50% off | 1M | Best code quality/style. 79.6% SWE-Verified. Intent understanding. Batch: $1.50/$7.50. |
| Opus 4.6 | Anthropic | $5.00 | $25.00 | $0.50 (90% off) | 50% off | 1M | Deepest reasoning. 80.8% SWE-Verified. Agent Teams. Reserve for hardest problems. Batch: $2.50/$12.50. |
| GPT-5.4 Pro | OpenAI | $30.00 | $180.00 | — | — | 400K | Maximum accuracy. Dedicated GPU. Only for highest-stakes tasks. |
| Opus 4.6 Fast | Anthropic | $30.00 | $150.00 | $3.00 | No | 1M | Same Opus quality at 2.5× speed. 6× standard pricing. Speed-critical agent tasks only. |

**Agentic cost strategy:** Route 70% of tasks to cheap models
(Gemma 4 self-hosted/Mini/Haiku/DeepSeek), 25% to mid-tier
(Sonnet/GPT-5.4/Gemini), 5% to premium (Opus). Gemma 4 26B MoE self-hosted
is effectively **$0/token** — only Vast.ai GPU rental cost (~$0.60/hr). With
Anthropic's prompt caching (90% off) + batch API (50% off), Sonnet drops to
$0.30/$7.50 for cached batch work. For high-volume local agentic loops,
Gemma 4 is now the cost champion.

---

## Sources & Methodology

Pricing from official provider pages (April 2026). OpenAI $100 Pro tier from
TechCrunch, VentureBeat, CNBC reporting 9 April 2026. Gemma 4 benchmarks
from Google DeepMind official model card and blog (2 April 2026), Arena AI
leaderboard, and community testing. SWE-bench Pro data from Scale AI SEAL
leaderboard. SWE-bench Verified from swebench.com (note: OpenAI considers
Verified contaminated and recommends Pro instead). Other benchmarks from LM
Council and published model reports. Community ratings synthesized from
r/ClaudeAI, r/ChatGPT, r/LocalLLaMA, Hacker News, and developer forums
(March–April 2026). All prices in USD unless noted. This comparison reflects
the state as of 11 April 2026 and will change rapidly.
