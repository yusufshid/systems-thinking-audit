# systems-thinking-audit

A Claude Code Skill that audits AI agents (single-agent or multi-agent) using a systems-thinking framework — leverage points, feedback loops, emergent behavior, and paradigm/mental model — to find structural risks that ordinary code review or security review miss. Built and tested in public.

## What it's for

Most AI agent failures that are hard to debug — drift over long sessions, an agent that technically satisfies its metric while missing the point, two agents that quietly contradict each other — aren't bugs in any single line of code. They come from how the pieces interact over time: what the agent is optimized for, whether anything catches its own mistakes, what its tools quietly imply, how much autonomy it has and over what.

This skill exists to find those risks **before** they show up as a real incident, by asking structural questions instead of "is this line correct?" It is **not** a substitute for `/code-review` (correctness bugs) or `/security-review` (vulnerabilities) — use those for that. This skill's job is the layer above both: is the system built so that being wrong gets caught, or built so that being wrong compounds silently.

## When to use it

Reach for this skill when:
- You're asked to **audit** an agent's design, permissions, cron schedule, or a specific aspect of it (a full sweep or a narrow one — see Scope below)
- You're trying to understand **why an agent behaves strangely** — drifts over long sessions, hallucinates despite "double-checking," gives technically-correct-but-wrong answers, or two agents/reviewers keep contradicting each other
- You're designing a new agent (single or multi-agent) and want a structural sanity check before shipping it — especially one with autonomous, hard-to-reverse actions (refunds, admin access, trades, published content)
- You want to know if a specific concern applies: "is there a missing balancing loop here," "what's the leverage point mismatch," "is this goal metric gameable," "is this a Shifting-the-Burden pattern"

It works from whatever you have — a system prompt, `SKILL.md`/`CLAUDE.md`, a narrated description of the architecture, or the actual codebase. You don't need all of them; see the skill's own Step 1 for what each is good for.

It applies across domains, not just "software agents" — customer service, sales, trading, financial advisory, business/ops management, marketing, admin/scheduling agents, content generation, coding agents, and orchestrator/leader agents coordinating a team of subagents. See [`references/domains.md`](skill/systems-thinking-audit/references/domains.md) for a quick per-domain translation of the checklist categories.

## How it works (the flow)

1. **Gather material** — whatever's available: prompt, architecture description, codebase, scheduling config, etc.
2. **Decide scope** — a full audit (all four lenses) or a targeted one (just cron, just the goal definition, just permissions) if that's what was actually asked.
3. **Analyze through four lenses** — Leverage Points, Feedback Loops, Emergent Behavior, Paradigm/Mental Model — using the detailed checklist in [`references/framework.md`](skill/systems-thinking-audit/references/framework.md), which also covers 10 component layers (tools, memory, permissions, scheduling, model config, data sources, output channels, human interface) and named failure patterns (Meadows' system archetypes: Shifting the Burden, Success to the Successful, Escalation, Policy Resistance, Rule Beating, plus hierarchy balance and unstated assumptions).
4. **Rate each finding's risk** — Critical/High/Medium/Low, by structural severity, not by how easy it is to fix.
5. **Connect findings into one causal story** (the "System Map") instead of four disconnected piles — this is usually the most useful part of the report, because it tells you where to intervene once rather than four places to patch separately.
6. **Verify before finalizing** — re-check Critical/High findings against the actual source material, ideally with an independent second pass, instead of trusting a single read.

The report always follows the same structure: Scope, Summary, Findings (per lens), Recommendations (prioritized, with second-order effects noted), and the System Map.

## What the report looks like

A finding names the actual mechanism, not generic vocabulary — "no balancing loop" alone isn't a finding; "the reviewer agent uses the same prompt and model as the writer agent, so it shares the writer's blind spots" is. Every finding gets a risk level and a recommendation. The report ends by tracing one causal chain through the findings rather than leaving them as four separate lists, and flags any adversarial content found in the material being audited (an embedded instruction trying to influence the audit itself is treated as evidence, not obeyed — this is tested in `evals/evals.json`, eval id 3).

## Status

Actively developed — built and updated in the open. See [`BACKLOG.md`](BACKLOG.md) for what's currently being validated or built next.

## Contents

- [`skill/systems-thinking-audit/`](skill/systems-thinking-audit/) — the skill itself:
  - [`SKILL.md`](skill/systems-thinking-audit/SKILL.md) — the workflow (Steps 0–6) and report template
  - [`references/framework.md`](skill/systems-thinking-audit/references/framework.md) — the full checklist: four lenses, ten component-layer deep-dives, and Meadows' system archetypes
  - [`references/domains.md`](skill/systems-thinking-audit/references/domains.md) — quick per-domain translation notes
  - [`evals/evals.json`](skill/systems-thinking-audit/evals/evals.json) + [`evals/input/`](skill/systems-thinking-audit/evals/input/) — test cases, including the prompt-injection guard test

## License

[MIT](LICENSE)
