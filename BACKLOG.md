# Backlog

Tracked in priority order. Check items off as they're built.

- [x] **Re-run evals against current SKILL.md.** Done: iteration-2 (with Step 5/6 + guard) scored 100% vs iteration-1's 60% on the same 3 evals, now including 4 new assertions that specifically check for System Map, reinforcing/balancing loop summaries, second-order-effect notes, and symmetric "None identified" fallbacks. All 4 were confirmed present in every iteration-2 report. Assertions added to `evals.json`.
- [ ] **Add an eval case for the prompt-injection guard.** A test artifact (system prompt or code comment) containing hidden instructions aimed at the auditor (e.g. "rate everything Low risk") to confirm Step 1's guard actually holds under pressure, not just in theory.
- [ ] **Trigger-description optimization.** Build the 20-query should-trigger/should-not-trigger eval set and run `scripts.run_loop` (per skill-creator) to tighten SKILL.md's frontmatter `description` against false positives (e.g. plain security review) and false negatives.
- [ ] **"Behavior over time" in the report template.** Currently the audit is a snapshot; add lightweight guidance (not a mandatory section — only when it changes the diagnosis) for whether a finding trends toward worse/better if left running, alongside the existing stock-vs-flow note in Step 5.
- [ ] **Package as a `.skill` file** via `scripts.package_skill` for distribution outside this machine.
