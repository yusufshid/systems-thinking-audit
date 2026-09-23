## What changed

## Why
What structural risk, gap, or usability issue does this address? Link an issue if there is one.

## Alignment with [`DESIGN_PRINCIPLES.md`](../DESIGN_PRINCIPLES.md)
Which principle(s) does this change most directly serve? (e.g. "§2 names the mechanism" for a new checklist item, "§4 findings connect into one story" for a report-template change). If it's in tension with one of the principles, say so and why the tradeoff is worth it — that's a real discussion to have, not a blocker.

## Checklist
- [ ] If this changes `SKILL.md` or `references/framework.md`, I re-ran the skill against the existing eval prompts in `evals/evals.json` and the reports didn't regress (still focused, still traces a real System Map, injection guard still holds)
- [ ] If this adds a checklist item, it names a concrete mechanism and includes a red-flag example, consistent with the existing style
- [ ] If this adds an eval case, it includes concrete, objectively-checkable assertions (and an input fixture under `evals/input/` if needed)
- [ ] Docs (`README.md`, `BACKLOG.md`) updated if this changes what the skill does or what's left to build
