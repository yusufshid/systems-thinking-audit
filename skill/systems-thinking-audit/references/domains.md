# Domain Quick-Reference

The four lenses and ten component-layer checklists in `framework.md` are domain-agnostic by design — they assess structure (goals, feedback loops, tools, memory, permissions, output channels), not subject-matter correctness. The same questions apply whether the agent writes marketing copy or executes trades; only the concrete answers differ.

This file exists because the worked examples throughout `framework.md` all come from software/customer-support contexts. Read the entry below for the domain being audited to translate the checklist categories into that domain's own terms faster — these are starting points, not a replacement for actually reading the material being audited.

## Customer service
Already the primary worked example throughout `framework.md` (the Aria/CloudStore case). Watch especially: goal metrics (CSAT/speed) that reward appeasement over correctness, autonomous irreversible actions (refunds, cancellations) with no approval gate, and customers adaptively learning what triggers a favorable outcome.

## Sales
- **Goals**: measured on deals closed or leads contacted (volume) rather than win-rate or long-term fit — a proxy-metric-drift pattern.
- **Permissions/rules**: can the agent offer discounts or custom terms autonomously? Same structure as an unauthorized refund.
- **Output/distribution**: outbound messages carry the company's authority to external prospects; a promised price or timeline becomes a hard-to-retract commitment the moment it's sent.
- **Data/ground-truth**: stale CRM data (lead/deal status) causes duplicate or contradictory outreach.
- **Emergent behavior**: if aggressive tactics correlate with higher response rates and nothing checks for brand-safety/ethics, the system can drift toward pushier behavior with no one having designed that outcome.
- **Human interface**: hand-off to a human rep for a large deal — does the rep get real context, or just a "hot lead" ping (actionability)?

## Trading / investment
One of the highest-stakes fits for this framework — irreversibility and frequency (the cron lens) both tend to be extreme here.
- **Output/distribution**: an executed trade is the canonical irreversible action — rate it accordingly in Step 3 regardless of how confident the logic behind it looked.
- **Data/ground-truth**: market data staleness is not a theoretical risk here — a "ground truth" price feed that's seconds old can already be wrong.
- **Permissions/rules**: position limits, kill switches, and whether they're enforced in code (rules level) or only as a prompt-level preference (paradigm level, easily bypassed).
- **Scheduling/triggers**: high-frequency automated trading combines high frequency with high impact-per-run — the framework's worst-case combination.
- **Feedback Loops — portfolio-level circuit breaker, distinct from per-trade limits.** A per-trade stop-loss/position-size cap controls one decision at a time; it says nothing about a string of individually-reasonable trades adding up to unacceptable aggregate drawdown. A mature setup has a second, portfolio-level balancing loop — e.g., pause all new deployment if rolling realized loss over a window exceeds a capital threshold — as a distinct mechanism from any single trade's own risk controls. Its absence is a real gap even when every individual trade is well-gated.
- **Feedback Loops — a reactive detector on an external leading indicator can itself become the reinforcing loop it's meant to prevent.** If a system correlates its performance against a leading indicator (market sentiment, a volatility index) and someone proposes automating a response to it (auto-pause on high fear, auto-reduce on a regime-shift signal), consider recommending report-only/human-correlated first rather than automatic action — an automated reactive layer on top of an already-reactive strategy is a new coupling that can oscillate or overreact exactly when conditions are already unstable. This is a second-order-effect judgment call (Step 5, point 2) worth surfacing explicitly rather than defaulting to "more automation is more safety."

## Financial management / advisory
- **Goals**: growth in assets-under-management or fee revenue vs. the client's actual best interest is a classic goal-misalignment pair worth checking explicitly.
- **Permissions/rules**: approval thresholds for large transactions or allocation changes.
- **Human interface**: does the client (or advisor reviewing the agent's recommendation) get enough context to actually evaluate it, or just a recommendation with no visible reasoning?

## Business / operations management
- **Leverage Points**: KPI-driven goals are especially prone to Goodhart's-law style drift here — the KPI is usually an explicit, written-down proxy for a fuzzier real objective (business health, team wellbeing).
- Often implemented as an orchestrator/leader agent coordinating department-specific subagents — see that dedicated section in `framework.md` (Lens 3).

## Marketing
- **Goals**: engagement/click metrics vs. brand trust or long-term customer relationship — proxy-metric drift is close to the default failure mode in this domain.
- **Output/distribution**: public-facing content posted under a brand account carries maximum "borrowed authority" and audience-visibility risk (Leverage Points/Rules) — once public, a bad post can't be fully un-shown even if deleted.

## Administration / operations (email, calendar, data entry, workflow)
- **Scheduling/triggers**: these agents often run literally on cron — apply that checklist directly, not just by analogy.
- **Permissions/rules**: autonomy over a calendar or inbox is a real permission boundary (compare to this environment's own "explicit permission required" categories for sending messages or changing settings) — check whether the agent's actual scope matches what was intended.

## Content / copywriting
- **Goals**: engagement/virality as a proxy for quality, same pattern as marketing.
- **Feedback loops**: is there any check for factual accuracy or brand-safety before publishing, or does content go straight from generation to output?
- **Emergent behavior**: at scale, a content agent can produce many pieces with the same shared blind spot (from one prompt/model) that look independently produced but aren't — the multi-reviewer independence problem, applied to content instead of review.

## Coding / development
- **Data/ground-truth**: usually the strongest case for real ground truth available (tests, compiler, CI, exit codes) — check whether the system actually uses it as the primary signal or falls back to self-check/same-model review instead.
- **Emergent behavior**: multi-agent code review sharing the same model is the exact pattern tested in this skill's own eval cases — same-prompt reviewers looking independent but sharing blind spots.
- Overlaps with `/code-review` and `/security-review` for correctness/vulnerability findings — this skill's job here is the structural layer (is there a test gate at all, not whether a specific bug exists).

## Orchestrator / leader agents
Not really a separate domain — any of the above can be implemented this way. See the dedicated "Orchestrator / leader agents" section under Lens 3 in `framework.md` for the full checklist (delegate-vs-verify role clarity, visibility into subagent reasoning, paradigm consistency across the team, task starvation, bottlenecking, stale model of team capability, accountability gap, self-referential oversight).
