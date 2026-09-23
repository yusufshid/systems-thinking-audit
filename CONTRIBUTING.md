# Contributing

This repo is a single Claude Code Skill (`skill/systems-thinking-audit/`) plus its checklist reference and eval suite. Contributions are welcome — a few things to know before opening an issue or PR:

**Read [`DESIGN_PRINCIPLES.md`](DESIGN_PRINCIPLES.md) first.** It's the reference point every PR gets checked against — not a bureaucratic hurdle, but the fastest way to get a PR merged without back-and-forth, since a change that clearly serves one of those principles is easy to say yes to. The PR template asks you to name which principle(s) your change serves.

## What's here
- [`SKILL.md`](skill/systems-thinking-audit/SKILL.md) — the workflow the skill follows (Steps 0–7)
- [`references/framework.md`](skill/systems-thinking-audit/references/framework.md) — the detailed checklist behind each lens and component layer
- [`references/domains.md`](skill/systems-thinking-audit/references/domains.md) — per-domain translation notes
- [`evals/`](skill/systems-thinking-audit/evals/) — test prompts, input fixtures, and assertions used to validate changes

See [`BACKLOG.md`](BACKLOG.md) for what's currently being worked on.

## Proposing a change to the framework
If you're adding or changing a checklist item (a new component layer, a new archetype, a new red flag):
1. Explain the *why* — what failure mode does this catch that the existing checklist misses? A concrete example (a real or realistic agent config that would trigger the finding) is more useful than an abstract description.
2. Keep it consistent with the existing style: name the mechanism, give a red-flag example, and note which lens/level it belongs to.
3. Don't force new sections into the report template unless the finding type is common enough to need a fixed home — most additions belong as checklist items under an existing lens.

## Proposing a change to `SKILL.md` itself
Changes to the core workflow (the Steps) should be validated against the eval suite before merging — run the skill against the existing eval prompts in `evals/evals.json` and check the report quality didn't regress, especially:
- The report still stays focused rather than padding out every checklist item regardless of relevance
- The System Map still connects findings into one causal story
- The prompt-injection guard (eval id 3) still holds

## Adding an eval case
Add a new entry to `evals/evals.json` with a `prompt`, `expected_output`, and concrete `assertions` (objectively checkable, not subjective). If it needs an input file, add it under `evals/input/` and reference it by relative path.

## Issues
Bug reports, unclear checklist items, or domains that don't map well to the framework are all welcome as issues — include what you were auditing (or a sanitized version of it) and what the skill got wrong or missed.

## Recognition
A merged PR that clearly follows [`DESIGN_PRINCIPLES.md`](DESIGN_PRINCIPLES.md) gets its author added to [`CONTRIBUTORS.md`](CONTRIBUTORS.md) — this is deliberate, not automatic: the project wants contributions that reinforce its direction to be visibly rewarded, the same way [Success to the Successful](skill/systems-thinking-audit/references/framework.md) works when it's used on purpose instead of by accident. If you're looking for a model of what a well-aligned change looks like, the commit history on `skill/systems-thinking-audit/references/framework.md` is a running example — each addition names a mechanism, gives a red-flag case, and states which lens it belongs to.
