# Backlog

Genuinely open items first. Below that is a done-log from an extended real-world validation phase (auditing `lp-meridian-mod-cupz`, a production Solana LP bot, purely to find gaps in this skill's own checklist) — kept for provenance of why each checklist item exists, not because it's still "backlog" in the pending sense.

## Open

- [ ] **`examples/` folder with 2-3 real (anonymized) sample audit reports**, drawn from the existing eval cases. Pure packaging/adoption — lets someone evaluating the skill see a full report before running it themselves, no logic change needed.
- [~] **`PORTABILITY.md`** — first draft written (general knowledge, not hands-on testing per platform; each platform section is explicitly confidence-labeled). Still needs verification/expansion from someone who's actually run this on Codex, Cursor, Windsurf, Copilot, Cline, Aider, or Antigravity — good first contribution, see CONTRIBUTORS.md's recognition loop.
- [~] **Trigger-description optimization — blocked by a bug in the skill-creator tool, not our skill.** Built the 20-query should-trigger/should-not-trigger eval set (saved at `systems-thinking-audit-workspace/trigger-eval-set.json` outside this repo) and ran `scripts.run_loop`. Result: 0% recall across all 5 iterations regardless of how the description was rewritten — traced this to `run_eval.py` registering the test skill as a `.claude/commands/` slash command (which only triggers on literal `/name` invocation) while checking for a `Skill`-tool trigger event that a command file can never produce. Not worth re-running until the upstream harness is fixed; the current description stands on manual review.

## Done — skill hardening

- [x] Re-run evals after Step 5/6 + injection guard were added: iteration-2 scored 100% vs iteration-1's 60% on the same 3 evals, with 4 new assertions checking for System Map, loop summaries, second-order-effect notes, and symmetric "None identified" fallbacks.
- [x] Eval case for the prompt-injection guard: an IT-helpdesk prompt with dangerous tools plus an embedded instruction telling the auditor to suppress findings. The guard held completely and the injection attempt itself became a structural finding.
- [x] "Behavior over time" in the report template — Step 5 point 4, optional trajectory guidance for loop findings.
- [x] Packaged as `dist/systems-thinking-audit.skill` — required trimming the frontmatter description from 1172 to 934 characters (limit 1024).

## Done — external feedback (2026-09-24)

Solid critique from an outside reviewer, acted on rather than filed away:

- [x] **Pair the qualitative audit with a quantitative eval harness explicitly.** Deployment/rollout point 3 now names concrete signals (trace-level success rate per tool-call, error taxonomy, token/step budget) and states this audit and a harness answer different questions.
- [x] **Cross-reference OWASP GenAI Security Project's "Top 10 for Agentic Applications" (ASI01–ASI10, published 2025-12-09) — now 10/10.** Verified against the official source, not memory. 6 of 10 had strong pre-existing coverage (tagged inline). 4 genuine gaps found and added: ASI05 Unexpected Code Execution (Tools/affordances), ASI07 Insecure Inter-Agent Communication (Orchestrator/leader agents), ASI10 Rogue Agents (Emergent Behavior), ASI08 Cascading Failures (Feedback Loops — sharpened further below with a real Meridian example).
- [x] **Practical-vs-theoretical leverage note in the Leverage Points table.** Paradigm ranks highest in Meadows' abstract hierarchy, but for a pretrained-model agent it's inaccessible — Rules (tool boundary, permission scope) is usually the highest *actionable* leverage point.
- [x] **Deepen ASI03 (Permissions/rules) with a real redundant-enforcement example** — K0's entries-paused flag checked independently at 3 separate call sites, plus fail-closed default when the marker file itself is unreadable. Added: redundant enforcement at multiple points as a defense against one new code path skipping a central gate, and fail-open/fail-closed as a deliberate choice when a state-read itself fails.
- [x] **Sharpen ASI08 Cascading Failures with a real Meridian example**: a field silently dropped at one destructuring choke point fanning into multiple unrelated downstream failures (a log, an alert, a gate all going silent from one missing value) — recurring because each past fix restored only the specific field, not the choke point's forwarding behavior. Code-level Shifting the Burden.
- [x] **System Archetypes gains a 6th pattern: Tragedy of the Commons** — multiple independent monitoring/cron processes drawing on the same rate-limited API quota, none individually greedy, nobody tracking aggregate consumption.
- [x] **Shifting the Burden gains a second example**: a recurring credential-pasted-into-chat incident "fixed" each time by manual rotation rather than a structural prevention.

## Done — delta/re-audit mode

- [x] **Each audit was a one-off snapshot with no way to compare against a prior audit of the same system.** Added "previous audit report (optional)" as a Step 1 material, and a **Delta** section to the report template (right after Summary, only when a previous report was given): Resolved / Recurring / New findings. A Recurring finding is now treated as near-automatic Shifting the Burden evidence (cross-referenced from both Step 2's archetype-check and `framework.md`'s Shifting the Burden entry — a repeat across audits is an *observed fact about history*, stronger than the single-snapshot inference the archetype check otherwise relies on) and as direct evidence for Step 5's loop-trajectory note (still-present after a prior audit named it means "not fixed," not "not worse yet," at the same risk level). README and report-structure description updated to match.

## Done — offer to implement fixes (vibecoder self-review)

- [x] **Self-review from a "vibecoder" (fast-shipping, AI-assisted solo builder) perspective: the skill diagnosed well but stopped at prose recommendations, even when running inside a coding session with the audited codebase right there.** Added Step 7, "Offer to implement fixes for what you found" (renumbering the old Step 7 "contribute back a new pattern" to Step 8): after the report, split Critical/High findings into concretely-implementable (a missing gate, a null/staleness check, a retry cap) versus needs-a-human-judgment-call (a goal redefinition, a paradigm shift), offer to implement only the former and only after asking, follow the target codebase's own conventions and verification, and never deploy/merge without a separate go-ahead — mirrors exactly how the real lp-meridian-mod-cupz fixes were handled manually earlier in this project's own validation phase (worktree, `node --check`, committed but not merged). README's flow list updated to match (now 8 steps).

## Done — Coverage section in the report template

- [x] **The report showed findings but never showed what was actually checked.** A reader could tell what went wrong, but not tell "this lens was inspected and came back clean" apart from "this lens was silently never looked at" — the two look identical when a section just has no findings under it, which is easy to miss especially on a full audit walking through 15 component-layer subsections. Added a **Coverage** section to Step 4's report template, right after Scope: a per-lens (and per-subsection, for a full audit with codebase access) accounting of ✅ Checked-no-issue / ⚠️ Checked-issue-found / ❓ Not-checked (naming what material is missing) / — Not-applicable. Replaces the old ad hoc "Out of scope for this audit" notes scattered under individual Findings headers (Step 0) with one consolidated, explicit table. Step 6 self-verification now also spot-checks the Coverage table itself, since a ✅ nobody can point to source material for is really a ❓.

## Done — external feedback: execution traces as material, trace-grounded vs. plausible findings

- [x] **Valid critique: the skill only listed static material (prompt/code/config) as input, but Feedback Loop and Emergent Behavior findings are claims about interaction *over time* — those can only be observed, not proven, from a static read.** Added "Execution traces / logs" as an 11th material category in SKILL.md Step 1, with a note on what a trace confirms that code alone can only suggest (an actual tool-call sequence, retries that actually fired, state actually carried across turns). Added explicit trace-grounded vs. plausible-from-static-material tagging guidance to Step 4's report instructions, and cross-referenced it from Lens 3's existing "these are plausible scenarios, not observed bugs" line in `framework.md`. README's material list and "what it's for" section updated to match. This doesn't change what the audit can run on without a trace (still proceeds, per Step 1's existing "don't stall over one missing lens") — it changes whether the report is honest about which findings are evidence-backed vs. inferred.

## Done — MITRE ATLAS cross-reference

- [x] **Cross-referenced [MITRE ATLAS](https://atlas.mitre.org/) (v2026.09, 16 tactics / 208 techniques) against `framework.md`.** Verified directly from MITRE's official `atlas-data` repo, not from memory. ATLAS is technique-level (adversary TTPs), one step more granular than OWASP's risk-category taxonomy, and mostly maps onto sections already covered here — but cross-referencing surfaced 3 genuinely new structural angles, each tagged inline with its AML technique ID: Memory/state point 10 (trust segregation within context — the root cause behind prompt injection, RAG poisoning, and context poisoning all being the same missing distinction between "instruction" and "data"), Tools/affordances point 10 (a tool's definition/schema is a mutable trust surface that can change after initial review, not a one-time-verified fact — "tool poisoning"/rug-pull), Cost/economics point 6 (cost exhaustion as a deliberate external attack, not just an internal-bug risk). README's "what it's for" section updated to name both taxonomies.

## Done — real-world stress test against lp-meridian-mod-cupz

Audited a real, mature production system (a live Solana LP trading bot with its own independently-built Meadows-style feedback-loop audit practice) as a series of targeted passes, purely to find gaps in this skill's own checklist by comparison. Each entry names the mechanism found and what it closed:

- [x] **Dormant loop check** — a balancing loop can be fully implemented yet never fire (empty recipient ID, a flag defaulting off). Lens 2 point 6: verify activation, not presence.
- [x] **Self-reinforcing scoring/weighting** — a mechanism that boosts influence on recent success is a reinforcing loop built on purpose, needing an explicit floor/ceiling/decay. Lens 2 point 7.
- [x] **Evidentiary discipline for deferred findings** — "not enough data yet" and "the data says it's fine" are different claims; a deferred finding needs its revisit condition actually checked. Data/ground-truth point 7.
- [x] **Trading domain notes**: portfolio-level circuit breakers distinct from per-trade limits, and "report-only, not auto-act" for external leading indicators. Added to `domains.md`.
- [x] **Tools/affordances gets real-world insight**: sensitive-input channel (stdin vs. CLI arg vs. file) as a security-relevant design choice; a function that looks like a pure read can have hidden side effects making it unsafe to reuse for probing; a tool assuming an interactive terminal can silently accept empty input in a non-interactive context.
- [x] **Third-party/vendored skills as a supply-chain dependency** — an installed diagram-generation skill with careful update-consent language ("silence is never consent"). Distinguish self-authored from vendored skills; check whether a self-update mechanism requires explicit consent.
- [x] **Recurring review reason signals a classifier fix, not more triage** — if the same reason keeps flagging items for human review, fix the upstream classifier; continuing to triage each instance is Shifting the Burden wearing a human-review costume.
- [x] **Automation-readiness as an explicit gate, and dormant-loop verification technique** — not everything manual is a gap; check for an explicit criterion for when automation is warranted. Verify dormant-loop activation against live config (real crontab), not a document that claims it.
- [x] **Flagged-not-blocked as a third outcome state, and dual-trigger (cron + on-demand)** — a rule that doesn't act should record the near-miss, not discard it; a cron-only check forces delay when a human has already noticed something urgent.
- [x] **Structural HARKing refusal, metric-labeling honesty, passive-vs-active risk class** — the strongest HARKing defense is refusing the backwards order at intake, not detecting it after; an honestly-labeled heuristic beats a metric borrowing more rigor than it earns; passive analysis and active intervention are different risk classes even sharing code.
- [x] **Explicit status fields vs. parsed status, and cross-boundary duplication** — a finalized decision's status should be a structured field, not inferred from prose; duplicated authoritative data across a deployment boundary is usually synced by a manual ritual with no automated check.
- [x] **Applied the context-budget-cost finding to ourselves** — `framework.md` had grown to 238 lines with no navigation aid while SKILL.md told every audit to read it in full. Added a Contents section and pointed targeted audits at the relevant section only.
- [x] **Context budget cost of the instruction surface, and navigational staleness** — from a real skill auditing a repo's own doc/skill efficiency: total doc+skill size read per session is itself an operating cost; a navigation aid can itself go stale.
- [x] **Toothless validators, break-glass procedures, explicit skill-boundary disambiguation** — a check that runs but can't fail is worse than no check; a break-glass procedure needs to not depend on the malfunctioning system's own tools; skill role clarity is stronger when descriptions explicitly disambiguate from siblings.
- [x] **Inherited upstream capabilities, verification-standard mismatch, stock isolation for untrusted data** — a default-on upstream feature can carry undocumented behavior; a new input channel bypassing the system's established verification standard is a risk in its own right; less-trusted data should be walled off from persistent stocks.
- [x] **Coverage symmetry, observer-effect monitoring, per-dependency failure modes** — a circuit breaker for one loss category doesn't imply one for a mechanically similar category; a monitor can itself worsen the exhaustion it's meant to catch; similar-looking dependencies can fail completely differently on exhaustion.
- [x] **Failover automaticity, quota-as-predictable-stock, silent-recovery visibility** — automatic vs. manually-noticed failover is a fast vs. slow loop; quota exhaustion is foreseeable, not a random outage; an automatic recovery should still surface to a human.
- [x] **Four new layers added**: Deployment/rollout, Dependency/supply-chain risk, Cost/economics as a feedback signal, Incident response/postmortem loop.
- [x] **HARKing, outlier robustness, sample clustering** — from a real overfitting-prevention skill: was a threshold set before or after seeing the triggering data point; sample clustering can inflate apparent confidence; replication needed before acting on one passing result among many hypotheses tested at once.
- [x] **Step 7: offer to contribute back a genuinely new pattern** — closes the loop this whole phase ran manually (Meridian → insight → back into the skill) into something the skill offers on its own going forward.
- [x] **Time-boxed elevation fail-open/fail-closed, and gate-vs-process bypass** — does a temporary permission elevation auto-expire or need explicit revert; a gate can be code-enforced and still let bypassing it skip a deeper process.
- [x] **Stock outflow and memory-length matching** — a decision-driving stock needs an outflow, not just an inflow; a stock's memory length needs to match the timescale of the risk it's meant to catch.
- [x] **Skill portfolio checklist added** — coverage, role clarity/overlap, staleness, review/upgrade cadence, orphaned skills.
- [x] **Documentation/instruction completeness check added** — distinct from stated-vs-enforced and unstated assumptions: does written guidance exist for failure modes people already half-know matter.

## Component-layer buildout

The original 10 component layers, each built out one at a time the same way (a dedicated subsection, red-flag examples):

- [x] Scheduling/triggers, Tools/affordances, Memory/state, Permissions/rules, Model/runtime config, Data/ground-truth sources, Output/distribution, Human interface — all done, see `references/framework.md` for the full checklist under each.

## Validation log

- **Iteration 3** (after all 10 original component-layer checklists + Orchestrator/Leader section + domains.md were added): re-ran the same 3 evals. All 3 reports stayed focused — each explicitly noted which checklists didn't apply rather than padding them in, and 2 of 3 runs used Step 6's independent-subagent verification successfully. Confirmed the much larger `references/framework.md` didn't cause bloat or dilute report quality.
