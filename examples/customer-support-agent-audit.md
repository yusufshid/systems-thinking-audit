# Systems Thinking Audit: Aria (CloudStore customer-support agent)

## Scope
Reviewed: the agent's system prompt only ([`evals/input/customer_support_system_prompt.md`](../skill/systems-thinking-audit/evals/input/customer_support_system_prompt.md)). No codebase, scheduling config, memory implementation, or execution trace was available — findings about runtime behavior (Emergent Behavior, parts of Feedback Loops) are plausible scenarios inferred from what the prompt permits, not observed from a real run. See Coverage below for exactly what that limits.

## Coverage
- **Leverage Points** — ✅ Checked, issue found (Rules and Goals levels — see Findings)
- **Feedback Loops** — ✅ Checked, issue found
- **Emergent Behavior** — ✅ Checked, issue found (plausible scenario — no execution trace was available to confirm)
- **Paradigm / Mental Model** — ✅ Checked, issue found
- **Tools / affordances** — ✅ Checked, issue found
- **Human interface** — ✅ Checked, issue found (there is none)
- **Output / distribution** — ✅ Checked, issue found (`send_email` sends on the company's behalf with no review)
- **Permissions / rules (as a config, distinct from the Rules leverage-point finding)** — ❓ Not checked — no separate permission/settings file was given, only the prompt's own description of tool access
- **Memory / state** — ❓ Not checked — no memory implementation or conversation-history handling was described
- **Model / runtime config** — ❓ Not checked — no model/temperature/effort settings given
- **Data / ground-truth sources** — ❓ Not checked — `lookup_order` exists but its data source and reliability weren't described
- **Deployment / rollout, Dependency / supply-chain, Cost / economics, Incident response** — ❓ Not checked — no material covering any of these was provided
- **Scheduling / triggers** — — Not applicable (ticket-driven, not scheduled)
- **Orchestrator / leader agents, Skill portfolio** — — Not applicable (single monolithic-prompt agent, not multi-agent or skill-composed)

## Summary
The single biggest risk is structural, not incidental: the agent is explicitly told to act autonomously with no approval gate on an irreversible financial action (`issue_refund`), while its only two performance signals — resolution speed and CSAT — both reward *acting fast and making the customer happy right now*, with nothing that ever checks whether the action taken (a refund) was actually warranted. These aren't two separate problems; the goal design is the reason the missing approval gate is dangerous rather than merely absent.

## Findings

### Leverage Points
- **Rules (level 4) — Critical.** `issue_refund(order_id, amount)` "no approval needed, executes immediately" is a fully autonomous, irreversible financial action with zero permission gate. *Recommendation: require human approval above a threshold amount, or for any refund not tied to a specific, verifiable order defect.*
- **Goals (level 5) — Critical.** The prompt states performance is measured by "average ticket resolution time" and "CSAT submitted after each ticket closes," and explicitly instructs "issuing refunds if it will make them happy." This is a goal-level problem, not a parameter to tune: the metric rewards the shortcut (refund → happy customer → good CSAT + fast resolution) directly, with no term for whether the refund was warranted. *Recommendation: redefine the goal to include an accuracy/appropriateness signal (e.g., refund-reversal rate, post-hoc audit sampling), not just speed and immediate sentiment.*

### Feedback Loops
**Reinforcing loops found:**
- Speed/CSAT metric → refund used as the fast path to a happy customer → no cost is ever attributed to an unwarranted refund → the behavior that "worked" (refunded, closed fast, good CSAT) gets reinforced every time it recurs, with nothing pushing back.

**Balancing loops found:**
- None identified. This is itself the Critical finding, not just an empty list: there is no approval step, no post-action review, and no mechanism anywhere in the prompt that could catch an inappropriate refund or an unwarranted ticket closure before or after it happens.

Expanded: the reinforcing loop above has no delay — a refund executes and the ticket closes in the same turn, so there's no window for a check even if one existed. Signal source: none (self-check, independent verifier, and human are all absent). Risk: Critical. *Recommendation: introduce a balancing loop with a genuinely independent signal — a threshold-based human approval queue for refunds above a set amount, or a lightweight second check (rule-based or a separate reviewing pass) before `close_ticket` fires on any ticket where a refund was issued.*

### Emergent Behavior Risks
- **Proxy-metric drift (plausible scenario, not observed — no trace available).** Because CSAT and speed are the only measured signals, the agent has a structural incentive to over-issue refunds specifically because it satisfies both proxies at once, even in cases a human reviewer would consider unwarranted. Risk: High. *Recommendation: same as the Goals-level fix above — this is the same root cause manifesting as behavior, not a separate issue to patch independently (see System Map).*
- **Latent capability activation (plausible).** Nothing in the prompt bounds refund amount or frequency per customer; a customer who learns that expressing dissatisfaction reliably produces a refund has no structural reason to stop escalating (see System Archetypes: Escalation, on the customer's side of this loop). Risk: Medium. *Recommendation: a per-customer/per-order refund frequency or amount cap, independent of the approval-gate fix, since a gate alone doesn't prevent a pattern of many small approved-but-still-unwarranted refunds.*

### Paradigm / Mental Model
The prompt's implicit paradigm is "resolve fast and keep the customer happy," with no room for "should this action happen at all" — "Never leave a ticket open if you can resolve it now" and "You do not need to ask a human for approval for any action" together frame *any* fast resolution as success, regardless of whether the resolution was correct. Risk: High. *Recommendation: add an explicit paradigm statement distinguishing "resolve quickly" from "resolve correctly," and name the specific situations (financial action, identity-sensitive request) where speed should yield to a check.*

**Tools / affordances (overlaps OWASP ASI02, Tool Misuse):** `issue_refund` has no low-stakes alternative (no "flag for review" or "offer store credit pending approval" option) and no granularity — one call both decides and executes the refund with no seam for a check in between. `send_email` similarly sends on the company's behalf immediately, with no draft/review step, meaning a wrong or poorly-worded email is just as irreversible as the refund it might accompany. Risk: High. *Recommendation: split `issue_refund` into a propose/approve pair for refunds above a threshold, and consider a draft step for `send_email` when it accompanies a refund or escalation.*

## Recommendations (prioritized)
1. **Redefine the Goals-level metric to include an appropriateness/accuracy signal, not just speed and immediate sentiment** (Critical, highest leverage). This is a goal-level fix, not a parameter tweak — it's more work than adding a gate alone, but it removes the underlying pressure that would otherwise keep pushing against any gate added on top of it. *Second-order effect: without also fixing the goal, an approval gate added in isolation creates pressure to route around it or set the threshold high enough to rarely trigger, because the thing being measured (speed, CSAT) still doesn't reward the gate being used.*
2. **Add an approval gate on `issue_refund` above a threshold amount** (Critical, Rules-level, lower effort than #1 but addresses the same underlying risk from a different angle — do both). *Second-order effect: a threshold that's set too low will generate approval fatigue and get rubber-stamped (see the notification-fatigue pattern in `references/framework.md`'s Human Interface section) — pair this with genuine review capacity, not just a queue.*
3. **Add a per-customer/per-order refund frequency or amount cap**, independent of #2. *Second-order effect: none significant — this is a low-risk, high-leverage addition since it doesn't remove any legitimate capability, only bounds a pattern of repeated approved-but-marginal refunds.*
4. **Give `issue_refund` and `send_email` a lower-stakes counterpart** (propose/flag instead of immediately execute), so the agent has a cheap, reversible option when it's uncertain, rather than only the expensive irreversible one.

## System Map
The goal definition (speed + CSAT, with an explicit instruction to refund for happiness) is the root cause, not a parallel problem to the missing approval gate — it's the reason the missing gate is dangerous rather than just theoretically incomplete: an agent optimized this way will *use* an ungated refund tool aggressively, not accidentally stumble into it. That goal-level pressure is what produces the Emergent Behavior risk (proxy-metric-driven over-refunding) and interacts with the Paradigm gap (no "should I act at all" framing) to make the missing balancing loop the single point where all of this becomes visible and correctable: fixing the goal metric changes what the agent is trying to do, and adding the approval gate changes what it's capable of doing unchecked — both are needed, because either one alone leaves the other's failure mode intact.
