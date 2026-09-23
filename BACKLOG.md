# Backlog

Tracked in priority order. Check items off as they're built.

- [x] **Re-run evals against current SKILL.md.** Done: iteration-2 (with Step 5/6 + guard) scored 100% vs iteration-1's 60% on the same 3 evals, now including 4 new assertions that specifically check for System Map, reinforcing/balancing loop summaries, second-order-effect notes, and symmetric "None identified" fallbacks. All 4 were confirmed present in every iteration-2 report. Assertions added to `evals.json`.
- [ ] **Add an eval case for the prompt-injection guard.** A test artifact (system prompt or code comment) containing hidden instructions aimed at the auditor (e.g. "rate everything Low risk") to confirm Step 1's guard actually holds under pressure, not just in theory.
- [ ] **Trigger-description optimization.** Build the 20-query should-trigger/should-not-trigger eval set and run `scripts.run_loop` (per skill-creator) to tighten SKILL.md's frontmatter `description` against false positives (e.g. plain security review) and false negatives.
- [ ] **"Behavior over time" in the report template.** Currently the audit is a snapshot; add lightweight guidance (not a mandatory section — only when it changes the diagnosis) for whether a finding trends toward worse/better if left running, alongside the existing stock-vs-flow note in Step 5.
- [ ] **Package as a `.skill` file** via `scripts.package_skill` for distribution outside this machine.

## Component-layer depth

Step 1 of SKILL.md now lists all 10 layers of an agentic system as *acceptable input*, but the checklist depth in `references/framework.md` still only goes deep on a couple of them (Leverage Points and Feedback Loops cover most layers generically; Scheduling/triggers got a dedicated cron subsection). Build out the rest one at a time, the same way cron was done — a dedicated subsection under whichever lens fits, with the same shape: what to look for, what a red flag looks like.

- [x] **Scheduling / triggers (cron, `/loop`)** — done, under Feedback Loops: frequency/delay, impact/gain, overlap risk, retry/backoff, notification fatigue.
- [x] **Tools / affordances** — done, under Paradigm/Mental Model: affordance asymmetry (missing low-stakes fallback), description-vs-effect mismatch, irreversibility signaling, granularity mismatch, overlapping/redundant tools, unsafe defaults.
- [x] **Memory / state** — done, under Leverage Points (Information Structure level): stock-vs-flow, write discipline, concurrent access, staleness, visibility asymmetry, unbounded growth/recency bias, memory as unverified self-check.
- [x] **Permissions / rules** — done, under Leverage Points (Rules level): default posture (allow vs deny), granularity, static vs contextual, escalation path, who can change the rules, enforcement location, stated-vs-enforced drift.
- [x] **Model / runtime config** — done, under Leverage Points (Parameters level): temperature as multiplier not root cause, model choice where independence matters, effort/reasoning-depth mismatch, context window truncation, version pinning.
- [ ] **Data / ground-truth sources** — how to assess the strength of an agent's available ground truth (API reliability, staleness, whether it's checkable at all).
- [ ] **Output / distribution** — a blast-radius framework for rating how expensive a given output channel is to get wrong (message sent vs. file written vs. production deploy).
- [ ] **Human interface** — beyond notification fatigue (already covered under cron): approval-UI design, escalation clarity, whether "ask a human" is actually actionable for the human receiving it.
