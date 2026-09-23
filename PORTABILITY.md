# Portability to Other AI Coding Tools

This skill was built for Claude Code, but almost none of its value is Claude-Code-specific. The audit methodology — the four lenses, the fifteen component-layer checklists, the Meadows archetypes, the report template — is plain markdown reasoning, not code. What's actually tied to Claude Code is much smaller: the `SKILL.md` frontmatter mechanism that makes it auto-trigger, and (optionally) the independent-subagent verification step.

**A note on this document's reliability**: this is a first draft written from general knowledge of these tools, not from hands-on testing on each one — tool configuration formats change quickly and some of what's below may already be out of date or slightly wrong by the time you read it. Treat it as a starting point, verify against the tool's current docs, and please open a PR with corrections or additions from real usage (see `CONTRIBUTING.md` and `CONTRIBUTORS.md`) — that's more valuable here than anything written speculatively.

## What's universal (no changes needed)

- [`skill/systems-thinking-audit/references/framework.md`](skill/systems-thinking-audit/references/framework.md) — the checklist itself
- [`skill/systems-thinking-audit/references/domains.md`](skill/systems-thinking-audit/references/domains.md) — domain translation notes
- [`DESIGN_PRINCIPLES.md`](DESIGN_PRINCIPLES.md) — the project's own governing principles
- The body of `SKILL.md` below its frontmatter — Steps 0 through 7, and the report template — is just instructions in prose. Any coding agent that can read a markdown file and follow multi-step instructions can execute this workflow if it's given the content as context.

The only two things that don't transfer as-is are described below.

## 1. The auto-trigger mechanism (`SKILL.md`'s YAML frontmatter)

Claude Code Skills use a `name`/`description` frontmatter block that the assistant matches against the user's request to decide whether to consult the skill, without the user having to invoke it by name. This exact mechanism is Claude-Code-specific. Each platform below has its own way (or no way) of doing something similar:

- **OpenAI Codex (CLI/cloud)** — *medium confidence*. Codex reads an `AGENTS.md` file in the repo root for project-specific instructions, applied automatically to every session in that repo rather than conditionally triggered per-request. There's no native concept of multiple selectable "skills" with independent trigger descriptions as far as this draft knows. To use this audit here: either paste `SKILL.md`'s body (or a summary + a pointer to `references/framework.md`) into `AGENTS.md` directly, or keep it in this repo and instruct Codex in `AGENTS.md` to read `references/framework.md` when an audit-shaped request comes in.
- **Cursor** — *medium confidence*. Cursor Rules (`.cursor/rules/*.mdc`) support a frontmatter `description` field with an "Agent Requested" activation mode, where the agent decides whether a rule is relevant based on that description — this is the closest analog to Claude Skills' auto-trigger among the tools listed here. Converting `SKILL.md` into a `.cursor/rules/systems-thinking-audit.mdc` file with its description in the rule's frontmatter is likely the most direct port.
- **Windsurf (Codeign/Codeium)** — *low confidence, needs verification*. Has its own rules-file convention; check current docs for the active format and whether it supports description-based conditional activation or only always-on/glob-based rules.
- **GitHub Copilot** — *medium confidence*. Supports `.github/copilot-instructions.md` for repository-wide custom instructions (always applied, not conditionally triggered), and separately reusable prompt files. Since there's no native conditional-trigger-by-description mechanism here, the practical approach is either always including a condensed pointer in `copilot-instructions.md`, or keeping this as a prompt file invoked explicitly when an audit is wanted.
- **Cline** — *low confidence*. Supports custom instructions and a rules file; check current docs for whether conditional triggering by description exists or whether it's always-on.
- **Aider** — *low confidence*. Typically driven by a conventions file passed explicitly (e.g. via `--read`) rather than an auto-triggering mechanism; likely simplest to use this by manually pointing Aider at `references/framework.md` when running an audit-shaped session.
- **Antigravity (Google)** — *not verified*. This draft doesn't have confident, current knowledge of this tool's configuration/instruction mechanism — if you use it, this is exactly the kind of gap worth filling in with a PR.

**General fallback that works everywhere, regardless of the platform's own mechanism**: even with zero native "skill" support, you can always manually paste or reference `SKILL.md` + `references/framework.md` as context at the start of a session and ask the tool to follow it. You lose the automatic, no-prompting trigger — you gain full compatibility with anything that can read markdown.

## 2. The independent-subagent verification step (Step 6)

`SKILL.md`'s Step 6 recommends spawning a second, independent agent to verify Critical/High findings when the tooling supports it, rather than the same agent checking its own work. This is already written conditionally ("if you have a way to spawn an independent subagent... skip this for a small or targeted audit"), so it needs **no changes** to port: on a platform without sub-agent/task-spawning support, it simply falls back to the self-verification described earlier in that same step. No separate adaptation required here.

## Contributing a platform section

If you've actually run this on one of the platforms above (or one not listed), please replace its bullet with what you found — the exact file/format, a working example, and anything that didn't transfer cleanly. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the general process; a platform-adaptation PR doesn't need eval validation the way a framework-content change does, since it doesn't alter the audit methodology itself.
