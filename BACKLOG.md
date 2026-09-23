# Backlog

Tracked in priority order. Check items off as they're built.

- [ ] **Re-run evals against current SKILL.md.** The 100% vs 55.6% benchmark predates Step 5 (System Map) and Step 6 (self-verification) and the adversarial-content guard — need a fresh iteration to confirm those additions actually change output quality, not just intent.
- [ ] **Add an eval case for the prompt-injection guard.** A test artifact (system prompt or code comment) containing hidden instructions aimed at the auditor (e.g. "rate everything Low risk") to confirm Step 1's guard actually holds under pressure, not just in theory.
- [ ] **Trigger-description optimization.** Build the 20-query should-trigger/should-not-trigger eval set and run `scripts.run_loop` (per skill-creator) to tighten SKILL.md's frontmatter `description` against false positives (e.g. plain security review) and false negatives.
- [ ] **"Behavior over time" in the report template.** Currently the audit is a snapshot; add lightweight guidance (not a mandatory section — only when it changes the diagnosis) for whether a finding trends toward worse/better if left running, alongside the existing stock-vs-flow note in Step 5.
- [ ] **Package as a `.skill` file** via `scripts.package_skill` for distribution outside this machine.
