<p align="center">
  <img src="assets/logo.svg" width="120" alt="systems-thinking-audit logo" />
</p>

<h1 align="center">systems-thinking-audit</h1>

<p align="center">
  <strong>Audit AI agents with systems thinking — leverage points, feedback loops, emergent behavior, and paradigm/mental model.</strong>
</p>

<p align="center">
  <a href="skill/systems-thinking-audit/SKILL.md">Skill</a> ·
  <a href="skill/systems-thinking-audit/references/framework.md">Framework</a> ·
  <a href="skill/systems-thinking-audit/references/domains.md">Domains</a> ·
  <a href="CONTRIBUTING.md">Contributing</a> ·
  <a href="DESIGN_PRINCIPLES.md">Design Principles</a> ·
  <a href="BACKLOG.md">Backlog</a>
</p>

<p align="center">
  <img src="https://img.shields.io/github/license/yusufshid/systems-thinking-audit" alt="license" />
  <img src="https://img.shields.io/github/last-commit/yusufshid/systems-thinking-audit" alt="last commit" />
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen" alt="PRs welcome" />
</p>

A Claude Code Skill that audits AI agents (single-agent or multi-agent) using a systems-thinking framework — leverage points, feedback loops, emergent behavior, and paradigm/mental model — to find structural risks that ordinary code review or security review miss. Built and tested in public.

## Installation

**In Claude Code:**
- **Personal (all projects):** clone this repo, then copy the skill folder into your personal skills directory:
  ```bash
  cp -r skill/systems-thinking-audit ~/.claude/skills/systems-thinking-audit
  ```
- **Project-scoped (one repo):** same idea, into that project's `.claude/skills/` instead:
  ```bash
  cp -r skill/systems-thinking-audit /path/to/your-project/.claude/skills/systems-thinking-audit
  ```
- **From the packaged file:** grab [`dist/systems-thinking-audit.skill`](dist/systems-thinking-audit.skill) and install it the way your Claude Code client supports (drag into the app, or its "install a skill file" flow).

Either way, Claude Code picks it up automatically — no restart or config needed, and no eval/API dependencies to install. It just triggers based on the description in `SKILL.md`, or you can invoke it directly.

**Outside Claude Code (Codex, Cursor, Windsurf, and similar):** the framework itself (`references/framework.md`, `references/domains.md`, `DESIGN_PRINCIPLES.md`) is plain markdown with no Claude-Code-specific dependency — it's a methodology, not code. What's Claude-Code-specific is just the `SKILL.md` frontmatter that makes it auto-trigger. To use this elsewhere:
- Point your tool's own custom-instructions mechanism (`AGENTS.md` for Codex, a Cursor/Windsurf rules file, etc.) at `SKILL.md`'s body content, or reference `references/framework.md` directly as context when asking for an audit.
- Step 6's "spawn an independent subagent" instruction is already written as conditional — it degrades gracefully to self-verification if your platform has no sub-agent/task-spawning capability, no changes needed.
- References to Claude Code specifics (`/code-review`, `/security-review`, `.claude/skills/`) are pointers to sibling tools in that ecosystem — swap in whatever your platform's equivalent is, or drop the reference if there isn't one.

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
3. **Analyze through four lenses** — Leverage Points, Feedback Loops, Emergent Behavior, Paradigm/Mental Model — using the detailed checklist in [`references/framework.md`](skill/systems-thinking-audit/references/framework.md), which covers 15 component-layer deep-dives (tools, memory, permissions, scheduling, model config, data sources, output channels, human interface, skill portfolios, deployment/rollout, dependency risk, cost/economics, incident response, and more) and named failure patterns (Meadows' system archetypes: Shifting the Burden, Success to the Successful, Escalation, Policy Resistance, Rule Beating, plus hierarchy balance and unstated assumptions).
4. **Rate each finding's risk** — Critical/High/Medium/Low, by structural severity, not by how easy it is to fix.
5. **Connect findings into one causal story** (the "System Map") instead of four disconnected piles — this is usually the most useful part of the report, because it tells you where to intervene once rather than four places to patch separately.
6. **Verify before finalizing** — re-check Critical/High findings against the actual source material, ideally with an independent second pass, instead of trusting a single read.
7. **Offer to contribute back** — if the audit surfaces a genuinely new pattern not already in this project's checklist, the skill offers (briefly, skippably) to help file it as an issue/PR here, so real-world audits keep improving the framework itself.

The report always follows the same structure: Scope, Summary, Findings (per lens), Recommendations (prioritized, with second-order effects noted), and the System Map.

## What the report looks like

A finding names the actual mechanism, not generic vocabulary — "no balancing loop" alone isn't a finding; "the reviewer agent uses the same prompt and model as the writer agent, so it shares the writer's blind spots" is. Every finding gets a risk level and a recommendation. The report ends by tracing one causal chain through the findings rather than leaving them as four separate lists, and flags any adversarial content found in the material being audited (an embedded instruction trying to influence the audit itself is treated as evidence, not obeyed — this is tested in `evals/evals.json`, eval id 3).

## Status

Actively developed — built and updated in the open. See [`BACKLOG.md`](BACKLOG.md) for what's currently being validated or built next.

## Contents

- [`skill/systems-thinking-audit/`](skill/systems-thinking-audit/) — the skill itself:
  - [`SKILL.md`](skill/systems-thinking-audit/SKILL.md) — the workflow (Steps 0–7) and report template
  - [`references/framework.md`](skill/systems-thinking-audit/references/framework.md) — the full checklist: four lenses, fifteen component-layer deep-dives, and Meadows' system archetypes
  - [`references/domains.md`](skill/systems-thinking-audit/references/domains.md) — quick per-domain translation notes
  - [`evals/evals.json`](skill/systems-thinking-audit/evals/evals.json) + [`evals/input/`](skill/systems-thinking-audit/evals/input/) — test cases, including the prompt-injection guard test
- [`dist/systems-thinking-audit.skill`](dist/systems-thinking-audit.skill) — packaged skill file for installing elsewhere
- [`DESIGN_PRINCIPLES.md`](DESIGN_PRINCIPLES.md) — what every contribution is checked against
- [`CONTRIBUTING.md`](CONTRIBUTING.md), [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md), [`CONTRIBUTORS.md`](CONTRIBUTORS.md) — how to contribute, and who has
- [`.github/`](.github/) — issue templates, PR template, and `CODEOWNERS` for the core framework files

## License

[MIT](LICENSE)
