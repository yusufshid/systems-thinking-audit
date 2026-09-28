# Systems Thinking Audit: agents/ folder, system-level roll-up (Phase 3)

## Scope
Phase 3 of the campaign, run 2026-09-28 on the user's instruction ("files that don't exist are simply unavailable, go straight to the system pass"). Input: the finding register (A1-F1..F9, A2-F1..F6, A3-F1..F7), the interface notes in `audit/LEDGER.md`, and the three per-agent reports. To verify cross-agent claims (Step 6) the three source files were re-read in full: `agents/support/customer_support_system_prompt.md` (16 lines), `agents/helpdesk/injection_guard_system_prompt.md` (16 lines), `agents/research/orchestrator.py` (47 lines). Not in the repo, so unreadable and left as ❓: `agent_runtime.call_agent`, every tool backend (refund, email, ticket, password, access), model/effort config, permissions/config, cron, the human escalation queue, logs or traces, rollout process, the consumer of A3's report. All findings are **plausible from static material**; none is trace-grounded. No independent verifier (no subagents in this session): Critical/High findings were self-re-verified against the cited lines, and that check caught one wrong claim (see S-F3).

## Coverage
Lenses (system level):
- Leverage points: ⚠️ Checked, issue found (S-F1)
- Feedback loops: ⚠️ Checked, issue found (S-F2)
- Emergent behavior: ⚠️ Checked, issue found (S-F1 trajectory; S-F3). No emergent risk that needs two agents to interact was found, because no hand-off between agents exists in the repo.
- Paradigm / mental model: ⚠️ Checked, issue found (S-F1: one paradigm replicated three times)

Phase 3 checklist (`campaign.md`):
- Orchestrator/leader layer and hierarchy balance: ⚠️ There is no system-level orchestrator (A3's `orchestrator.py` coordinates only A3's own researchers, covered in A3-F2). Direction: **under-coordination**, evidence in S-F2. Over-control: not found; the opposite is written into prompts (A2 line 11 "don't wait for a human", A1 line 16 "never leave a ticket open").
- System archetypes across the register: ⚠️ Rule Beating fits (S-F1). Shifting the Burden fits, observed once in the change history (S-F1). Policy Resistance fits inside A1 (S-F1). Tragedy of the Commons: ❓ candidate only, unverifiable (S-F3). Escalation, Success to the Successful: none identified.
- Shared state and shared control mechanisms: ❓ (S-F3): `close_ticket` name is shared by A1 and A2; whether it is one backend is not readable. A3's `shared_state.json` is private to A3 (A3-F4).
- Chain length across the whole workflow: ✅ Checked. No agent hands work to another agent, so per-agent reliability is not multiplied across agents. The only chain is A3's internal one (up to 40 sequential calls, A3-F3).
- Accepted risks combining: ✅ Checked, none to combine. No Critical/High finding is accepted (see "Accepted Critical/High" below).
- Cost across agents: ❓ needs billing/quota config (S-F3).
- Output/distribution and Deployment/rollout at system level: ❓ needs the consumers of the outputs and a rollout/eval process (not in repo).

## Summary
The single biggest structural risk is not in any one agent: all three are steered by a number that the agent (or its own pipeline) produces, and none has an independent check on whether the result is right. Aria and Milo are scored on speed and a satisfaction rating collected around their own ticket closure, and each holds an immediate irreversible tool; the research pipeline is gated on word count. One goal-level decision fixes the shared cause, while per-agent patches (the $50 rule in A1) have already been absorbed by the standing goal. Beyond that, nothing connects the three agents: no run records, no owner of "did we get this right", and the only human path is a queue we cannot see.

## Findings

### Leverage Points

**S-F1 (Goal / paradigm, level 5-6) - Critical. Shared root cause of A1-F2, A2-F2, A3-F1 (and through them A1-F1/F5/F6/F8/F9, A2-F1/F4/F5).**
Verified against source: A1 lines 3, 12-14 and 16 (fast, "as few messages as possible", CSAT collected after the ticket closes, never leave open); A2 lines 10-12 and 16 (closure speed, requester rating, trust stated identity, don't wait for a human, minimize friction); A3 lines 7-9 and 41-45 (more findings is better, gate on >500 words). Same structure three times: the score is measured on something the agent itself produces or ends (it closes the ticket, then the rating arrives; it writes the synthesis, then the length is counted), so the cheapest way to score well is to act fast and look thorough, not to be right. That is Rule Beating. It is one defect with three symptoms, not three problems: patching each agent's tool gate separately leaves the goal that pushes against every gate.

Observed once in the history, not only inferred: the 2026-09-28 A1 change added a $50 threshold and `escalate_to_human` (lines 8 and 15) but left lines 3, 12-14 and 16 alone. The re-audit found A1-F2 recurring unchanged and added A1-F9 (the escalation path is penalized by the speed/CSAT metric). This is Shifting the Burden (a threshold rule used in place of the goal fix) and Policy Resistance (the patch is pulled against by lines 12-16 in the same prompt). Treat it as one observed instance for A1; for A2 and A3 it is still plausible only. Trajectory: for A1 and A2 it worsens over repeated runs, because customers and requesters can learn what works (A1-F6, A2-F5 reinforcing loop) and nothing caps it; for A3 it plateaus (bounded at 10 attempts per query, A3-F3), but the padding bias is present on every run.

Recommendation (needs a human decision, not a mechanism): choose, per agent, one outcome measured by something the agent does not control: A1 refunds later reversed or disputed plus repeat contacts on the same order; A2 access grants later confirmed by the account owner or a manager; A3 claims backed by a checked source. Collect the satisfaction score independently of the agent's own close, and let it stay as a secondary signal only. Second-order effect: if the new measure is again something the agent can produce or influence (a same-model judge, a self-reported "verified"), the proxy just moves; keep at least one signal from outside the pipeline. Also note the limit of this repo: the rating collection and refund/access enforcement live in files that are not here, so the goal fix can be started in the prompts but not completed or verified from this repo.

### Feedback Loops
**Reinforcing loops found:**
- Learned-bypass loop, A1 and A2: anger or "urgent" works, so customers/requesters use it more; the metric rewards giving in, and no one sees the trend (A1-F6, A2-F5).
- Padding loop, A3: length gate plus resample (A3-F1).
- Cross-system: the same goal pattern in three places means the same failure appears three times and is patched three times (the shifting-the-burden loop in S-F1).

**Balancing loops found (system level):**
- A1: `escalate_to_human` for refunds over $50 (line 15), into an unread queue, model-enforced only, and penalized by the metric (A1-F8, A1-F9).
- A3: word-count gate, on the wrong variable (A3-F1).
- A2: none. Nothing spans the three agents.

**S-F2 (Feedback / incident loop, Lens 2 points 3 and 9, Incident response 3 and 6, Orchestrator point 7) - High.** Nobody owns "did we get this right", and nothing connects the agents' failures to each other. Verified: the only correction available to A2 is none (A2 has no escalation tool and line 11 forbids waiting for a human); A1 has one narrow human path (line 15); A3 has none, and adjudication is a same-model synthesizer (line 13). No agent is required to check ground truth before acting (A1 has `lookup_order` at line 4 but no line requires it; A2 has no identity lookup; A3 asks for no sources). No run logging is visible for any agent (A1-F7, A2-F6, A3-F7, all consistent with the sources; whether the runtime logs is ❓). So if the same category of failure happens in all three, each occurrence is handled alone and no record lets anyone compare them. That is the system-level accountability gap and under-coordination: three autonomous agents, nothing above them reconciling or even observing them. Plausible from static material.
Recommendation: one owner and one small per-agent record (calls, tool arguments, outcome, later reversal), reviewed on a schedule with a defined action at a threshold (for example refund reversal rate, admin grants per week, share of A3 claims without a source). Second-order effect: a dashboard nobody has to act on becomes a dormant loop; attach the review to a named person and a trigger, or it adds the look of oversight without the substance.

### Emergent Behavior Risks
No risk that requires two agents to interact: there are no hand-offs, so no cross-agent chains. The combined risk is the same shape repeated: A1 and A2 each let one message trigger an irreversible action that the agent then closes itself (A1-F1, A2-F1, A2-F5), which leaves a clean record. See S-F1 (trajectory) and S-F3 (unverified shared resources).

**S-F3 (Interfaces / cost, Lens 3 point 6, Cost points 3 and 4) - Medium. Unresolved cross-agent interfaces; two earlier claims corrected.** Verified against source:
- `close_ticket` appears in A1 (line 7, "support ticket") and A2 (line 7, "a ticket"). The prompts name two different organizations (CloudStore and NimbusWorks), which makes a shared ticket backend less likely than the earlier notes implied, but the backend is unread, so it stays unknown.
- **Correction to the ledger and to the A3 report:** they say A3's `claude-default` is "the same alias as A1/A2". Only A3 shows a model (orchestrator.py lines 24 and 35). A1 and A2 have no model in their files, so a shared model alias or shared quota is not established. The Tragedy-of-the-Commons reading (A3's worst case of 40 calls per query drawing on a quota shared with A1/A2) stays a candidate only, not a finding about A1/A2.
- A1's human queue versus A2: unknown whether the same people; A2 has no path into it anyway (A2-F4).
- What consumes A3's report: unknown.
What would resolve it: one line from the user (same org or separate deployments? one shared quota or not?). Recommendation: if any of these is shared, record it as an interface and re-run this pass; if separate, mark the interface notes closed. Second-order effect: none.

### Paradigm / Mental Model
One paradigm, three copies: "the measure is the goal, and the agent may decide alone." Each prompt was written by someone optimizing a different visible number (rating, satisfaction, length) with no statement of what a wrong outcome costs. That is consistent across agents, which is why a single goal decision (S-F1) is available rather than three. One extra note: A2's file carries a governance claim it cannot back up (an auditor-directed note asserting a security team approval, logged and not obeyed as A2-F3). If real people read that comment as "approved", it suppresses review at the organization level, which is the same effect as S-F2; whether such an approval exists is ❓ and only the user can say.

## Accepted Critical/High
None. No Critical or High finding is `accepted` or `wontfix`. The only accept-pending item is A1-F7 (Medium), which stays `open` until the user gives a revisit condition.

## Definition of done: progress
1. Every applicable cell ✅ or ⚠️ with the finding fixed/accepted, no ❓: **not met.** The remaining ❓ cells all need files the user says are not available, so they cannot be resolved; the user has to decide whether to treat them as permanent gaps (a decision, not one this audit can record for them).
2. No `open` Critical or High: **not met.** Open Critical: 5 per-agent (A1-F1, A1-F2, A2-F1, A2-F2, A3-F1) plus S-F1. Open High: 11 per-agent plus S-F2. Nothing is fixed or accepted.
3. Phase 3 run after the last change to any agent or interface: **met** (this session, after the A1 change of 2026-09-28). It has to be re-run if an agent or interface changes.
4. Every `accepted` finding has a confirmed reason and revisit condition: **vacuously met** (nothing accepted; A1-F7 is pending, not accepted).

## Recommendations (prioritized)
1. **One goal decision applied to all three agents (S-F1).** Highest leverage; resolves the root of about eight findings at once. Needs a human choice of what "a good outcome" means for each agent. Second-order effect: the new measure must not be something the agent produces itself, or the proxy just moves.
2. **An outside signal before each irreversible action (A1-F1/F3, A2-F1/F4, A3-F2/F5).** Enforce in the backend (refund and access tools), not only in the prompt; the backends are not in this repo, so a prompt-only edit is the weaker fix and cannot lower a finding's severity. Second-order effect: a gate with the old goal still in place gets bypassed or loosened later (that is the A1 history).
3. **Owner plus per-agent run record and threshold review (S-F2).** Lower leverage than 1 and 2; it is what makes the fixes visible and what would catch the failure the next time. Second-order effect: dormant dashboard unless tied to an owner and a trigger.
4. **Close the interface unknowns (S-F3)** with one answer from the user; cheapest item, and it removes a possible wrong claim from the ledger.
5. Housekeeping from the per-agent reports (A3-F3 cap and status, A3-F4, A3-F6, A3-F7) stays as listed there; those are code changes A3's own file can take.

## System Map
One goal pattern (a score the agent itself produces: speed and a rating around its own ticket close, or word count of its own synthesis) is written into all three agents -> because of it, the only checks that exist are self-checks or a human queue nobody can see (A1's $50 path, A3's length gate, nothing for A2) -> so each agent can take an immediate, irreversible or unverified action and leave a clean record, and the people or queries on the other side can learn what works -> and because no agent hands off to another and nothing sits above them or logs runs, the same failure appears three times with no one comparing them, so each incident is fixed locally (the $50 rule) while the goal that produced it stays. That is Rule Beating at the root, with Shifting the Burden observed once in A1's own change history and Policy Resistance where the patch meets lines 12-16. Whether A1, A2 and A3 also share a ticket system, a human queue, or a model quota is unknown and, contrary to earlier notes, not indicated by anything in the files that can be read.
