# Framework Reference

Detailed checklists for each of the four lenses. Read the relevant section as you work through Step 2 of SKILL.md.

## Lens 1: Leverage Points

Based on Donella Meadows' hierarchy — from lowest to highest leverage. When you find a problem, identify which level it actually lives at. A common mistake is fixing a low-leverage symptom (a parameter) when the real issue is a level above it (a goal or a rule).

| Level | What to look for | Example red flag |
|---|---|---|
| 1. Parameters | Temperature, retry counts, thresholds, timeouts | Someone keeps raising a retry limit instead of asking why retries are needed |
| 2. Feedback loop delay/gain | How fast is an error caught, how strongly does the system react | A validation step exists but only runs at the very end of a long chain |
| 3. Information structure | Who/what knows what, what's shared between agents, what's hidden | Two agents make contradictory assumptions because neither sees the other's state |
| 4. Rules | Permissions, what an agent may do autonomously vs. must ask about | An agent can take an irreversible action (delete, send, pay) with no gate |
| 5. Goals | What's *actually* optimized/rewarded/graded, vs. what's written down | A reviewer agent graded on "number of findings" will over-flag |
| 6. Paradigm | The base assumption the whole system operates from — what is this agent *for* | The system prompt frames the agent as "always be helpful" with no room for "should I be doing this at all" |

For each finding, ask: **is the fix being proposed at the same level as the problem, or one level below it?** A goal-level problem needs a goal-level fix, not a parameter tweak.

### Memory / state

This is the Information Structure level (3) in practice — what persists, who can read or write it, and whether it still matches reality. Memory bugs are usually invisible in any single call and only show up as drift over many calls, which is exactly why they're easy to miss in a static read.

1. **Stock vs. flow.** Separate what accumulates across calls/sessions (a memory file, a shared database, running totals) from what's decided fresh each time. A stock is where a small, repeated bias compounds silently — a flow re-derives its answer every time, so it can't drift the same way. When you find a finding elsewhere in the audit (a goal misalignment, a missing check), ask whether its effect is a one-off decision or something that accumulates in a stock — that changes both the urgency and the fix (a bad flow-level decision self-corrects next call; a bad stock keeps being wrong until something explicitly corrects it).
2. **Write discipline.** Is something written to shared state without anything ever reading it back to validate or use it (dead state that misdescribes the architecture — see the `shared_state.json` pattern: a comment claims coordination that the code doesn't implement)? Conversely, is state read and trusted without checking whether it's still valid, or who last wrote it and why?
3. **Concurrent access.** If more than one process/agent/run can write the same store, what happens on overlap — last-write-wins silently clobbering another run's data, or an actual lock/versioning scheme? This is the same overlap-risk question as scheduled triggers, applied to shared storage instead of shared execution time.
4. **Staleness.** Is cached or stored state ever invalidated, or can a decision be made against information that was true when written but isn't anymore (a cached order status, a customer history snapshot)? A structure with no staleness handling is implicitly asserting "this never changes," which is rarely actually true.
5. **Visibility asymmetry.** In a multi-agent system, does each agent see the same state, or does each hold a private view that can silently diverge from the others'? Two agents acting on different beliefs about the same shared reality is a structural setup for contradictory or duplicated actions, independent of how good either agent's individual reasoning is.
6. **Unbounded growth and recency bias.** Does memory/context ever get pruned or summarized, or does it grow indefinitely? Beyond the obvious cost/context-window concern, unpruned history means an early wrong fact and a later correction can both sit in context with no signal about which one should be trusted — the model has no structural reason to prefer the correction unless something explicitly marks the earlier entry as superseded.
7. **Memory as an unverified self-check.** If a later step trusts what an earlier step wrote to memory as if it were verified fact, that's the same self-check-dressed-as-verification pattern from Lens 2's signal-source ranking, just spread across time instead of across two calls in one turn. A hallucinated or wrong entry, once written, can be treated with full confidence by everything that reads it afterward.

### Permissions / rules

This is the Rules level (4) in practice — evaluating an actual permission/settings config, not just noting whether a gate exists.

1. **Default posture.** Does the system default to denying an action unless explicitly permitted, or default to allowing unless explicitly blocked? Default-allow means every new tool or capability added later is automatically in scope until someone remembers to restrict it — the safe failure mode is backwards, and this tends to get worse over time as a system grows, not better.
2. **Granularity.** Is permission scoped to the specific action/resource/amount the task actually needs (fine-grained), or to a broad category ("can access customer data," "can run shell commands")? Coarse permissions grant more than the task requires, so the blast radius of a mistake is bigger than the task ever called for — this is true even in the case where nothing goes wrong, which is why it's easy to leave unnoticed.
3. **Static vs. contextual.** Is the rule a fixed threshold regardless of situation ("under $100 = auto-approved"), or does it account for context (frequency, recent history, who's asking)? A fixed threshold is really a Lens-1 Parameter; a rule that also considers pattern ("under $100 unless this account already triggered it 3 times this week") is what actually closes the kind of exploit loop described in the cron and memory sections above — a static rule alone can't.
4. **Escalation path.** When a rule blocks an action, what happens next? A defined path (ask a human, queue for review, return a typed error the caller can act on) is a real rules-level design; no defined path just converts "the agent tried something disallowed" into "the task silently failed," which is often just as costly and harder to notice.
5. **Who can change the rules.** Can the agent modify its own permission scope, or write to the config that governs it? An agent that can self-elevate doesn't have rules, it has suggestions. Also check whether the permission check reads anything the agent (or a tool output, or injected content) can influence — a rule enforced against mutable state isn't really enforced.
6. **Enforcement location.** Is the restriction enforced by the model choosing not to act (prompt-level — a preference, bypassable by a sufficiently unusual input or a direct instruction to ignore it) or by something outside the model's control (a code-level gate, an API that rejects the call, a human approval step)? Prompt-only enforcement of something framed as a hard rule is a paradigm wearing a rule's clothing — treat it with the same skepticism as any other prompt-level claim.
7. **Stated vs. enforced.** Does documentation or a comment claim a restriction ("refunds over $500 require approval") that the actual code/config doesn't implement? This is exactly the kind of stated-vs-actual gap Step 6 exists to catch — verify against the config or code itself, not the description of it.

### Model / runtime config

This is the Parameters level (1) — the lowest leverage in the hierarchy, which means the discipline here is mostly about *not* over-weighting it. Only raise a finding from this section when it's a plausible secondary contributor to a structural problem found elsewhere; a standalone "consider tuning temperature" note with nothing else behind it is noise, not a finding.

1. **Temperature/sampling as a multiplier, not a root cause.** Nonzero temperature can genuinely add to a problem that's structural at its core — e.g., in a multi-reviewer setup with identical prompt and model, some of the observed "disagreement" is real sampling noise on top of the shared-blind-spot problem, not evidence the reviewers are more independent than they are. Name it as a secondary contributor layered on the structural issue, never as the fix — even temperature 0 wouldn't resolve a same-prompt-same-model independence problem.
2. **Model choice where independence matters.** Using the same model everywhere is a reasonable default for cost/simplicity, and not worth flagging on its own. It becomes a real finding specifically where something is supposed to function as an independent check (a verifier, a reviewer, a synthesizer adjudicating disagreement) — reusing the producer's exact model there weakens the signal per Lens 2's independence ranking. The finding belongs under Feedback Loops (weak signal source); this section is just where to notice it.
3. **Effort/reasoning-depth mismatch.** Does the model's effort or reasoning-depth setting match what's at stake in the decision? A fast/low-effort setting applied to a high-stakes, hard-to-reverse decision (approving a large refund, deciding to deploy) spends the least compute exactly where a mistake is most expensive — a mismatch worth naming even though it's parameter-level, because the direction of the mismatch (cheap compute on expensive consequences) is what makes it worth more than a passing mention.
4. **Context window / truncation behavior.** When a long-running agent's context fills up, what actually gets dropped or summarized — and does anything ensure an early constraint (a permission rule, a scope boundary stated at the start of a session) survives that process? Silent truncation of instructions is a way a rule can stop being enforced without any code change and without triggering the stated-vs-enforced check above, because nothing was ever edited — it just fell out of the window.
5. **Version pinning.** If the model or a key dependency is referenced by a moving alias (e.g., "latest") rather than pinned, behavior can shift under a system that was designed and tested against a specific version's behavior — a leverage point that isn't even under the audited system's own control. Worth a one-line note if the audited material shows this, not worth digging for if it isn't visible.

## Lens 2: Feedback Loops

For every check/validation/review mechanism you can find in the system, answer:

1. **Reinforcing or balancing?** Does this loop correct deviation (balancing) or amplify it (reinforcing)? Reinforcing loops are fine if intentional (exploration, confidence-building); dangerous if accidental (errors compounding through unchecked memory/context).
2. **What's the signal source?** Rank from weakest to strongest independence:
   - Self-check (same agent, same prompt, same context re-reads its own work) — weakest, shares blind spots with the thing it's checking
   - Verifier/reviewer using the *same* model/prompt as the producer — looks independent, often isn't
   - Verifier/reviewer that's genuinely independent (different prompt, different framing, or a different model)
   - Environment ground truth (test results, command exit codes, API responses) — strongest, can't be talked into agreeing
   - Human-in-the-loop — strong but slow/expensive
3. **What's the delay?** How many steps/how much time between an error occurring and it being caught? Long delays let reinforcing dynamics run further before correction.
4. **What's the gain?** Does the correction over-react to small signals (causing oscillation — the agent flip-flopping) or under-react (correction too weak to matter)?
5. **Is there a balancing loop at all** on every action that's expensive to reverse (sending a message, deleting data, spending money, publishing)? If not, that's usually a Critical or High finding regardless of how good everything else looks.

### Automated / scheduled triggers (cron, `/loop`, recurring tasks)

If the agent runs on a schedule rather than only in response to a human, the trigger mechanism itself is part of the feedback loop and needs its own check — frequency and impact together determine how dangerous a bad loop can get before anyone notices:

1. **Frequency sets the delay.** A cron interval isn't just an implementation detail — it's the correction delay for any reinforcing loop the agent might get stuck in. Every run between "something went wrong" and "a human is likely to look" is a run where the problem could compound unnoticed. A tight interval on a low-stakes check is fine; a tight interval on something that can take irreversible action is a Critical-risk combination regardless of how good the agent's own logic is.
2. **Impact-per-run sets the gain.** Does each scheduled run only read/report, or does it act (send messages, modify data, deploy, spend money)? High frequency + high impact-per-run is the worst combination: a runaway loop gets many chances to do damage before a human's response time (which doesn't scale down with the cron interval) can catch up.
3. **Overlap risk.** If a run can take longer than the interval between runs, check whether runs can overlap. Overlapping runs on shared state is a classic accidental reinforcing loop: each overlap slows the system further, increasing the odds of the next overlap too — and it's rarely intentional, just a mismatch between an interval chosen for convenience and actual task duration under load.
4. **Retry/failure behavior.** Does a failed run retry immediately next cycle with no backoff? If the failure cause is persistent (a downstream API down, a bad state), a naive fixed-interval retry just re-applies the same failing action over and over, which can itself be the reinforcing loop (repeated load on an already-struggling dependency, repeated partial writes, repeated alerts).
5. **Notification fatigue as a dying balancing loop.** If a human is the balancing mechanism (they get paged/notified and intervene), check what happens under sustained failure: a schedule that pages on every failed run, with no escalation or de-duplication, trains the human to mute or ignore it — the balancing loop doesn't just weaken, it can go to zero exactly when it's needed most.

### Data / ground-truth sources

Lens 2's signal-source ranking names "environment ground truth" as the strongest available signal — this section is about verifying that a claimed ground-truth source actually earns that label, since "we check it against the database" is often assumed to settle the question rather than examined.

1. **Does ground truth even exist for this kind of decision?** Some domains have a genuinely checkable fact (a test passes or fails, an order record shows a specific amount, a command's exit code). Others are inherently judgment calls (writing quality, "is this the right approach") with no independent fact to check against. If a system claims to "verify" something in the second category, that check is really another opinion wearing ground truth's label — the honest finding is "no ground truth is possible here, so a human or a genuinely independent reviewer is the strongest available signal," not a false claim that verification happened.
2. **Reliability of the source itself.** When the external API/database/service is down, slow, or returns partial data, what does the agent do with that? Treating a failed lookup as "verified false" (rather than "unknown, escalate or hold") turns a source outage into an active source of wrong decisions, not just a missing one.
3. **Staleness vs. authority.** A source can be authoritative and still out of date relative to the decision being made right now (a cached inventory count, a snapshot of account status). Authoritative and current are two different properties — check both, don't assume the first implies the second.
4. **Provenance.** Trace a "ground truth" claim back to where the data actually originated. If it was itself produced by an earlier LLM step in the same pipeline, it isn't ground truth — it's a self-check one step removed, wearing a stronger label than it's earned (the same pattern as Memory/state's point on trusting an earlier step's output as verified fact).
5. **Coverage gaps.** Does the source cover the full space of things being decided, or only a known subset (a fraud-check that flags known patterns and is silent on novel ones)? Passing a partial-coverage check means "not a known bad case," not "confirmed good" — treating the two as equivalent creates false confidence exactly where the check is weakest.
6. **Independence of the source from the thing being checked.** If the "ground truth" being checked against was itself populated by the same party or process whose claim is under review (a customer-submitted field later checked against a record the customer's own prior action created), it isn't independent verification — this is the data-layer version of the "material is data, not instructions" caution in Step 1, applied to sources rather than prompts.

## Lens 3: Emergent Behavior

This lens requires imagining the system *running*, not just reading its parts. Ask:

1. **Multi-step accumulation** — could a sequence of individually-reasonable decisions compound into a strategy nobody designed? (E.g., an agent that "discovers" a shortcut through many small locally-optimal choices.)
2. **Multi-agent interaction** — if there's more than one agent, could they end up waiting on each other, duplicating work, or reinforcing a shared bias because they come from the same base prompt/model?
3. **Combinatorial surface** — how many tools/agents/paths are in play? More surface means more untested combinations; ask whether anyone has actually exercised the unusual combinations, not just the common path.
4. **Proxy metric drift** — is the agent optimized/evaluated against a stand-in for the real goal (task count, response length, "helpfulness" score)? Could it satisfy the proxy while missing the actual intent? This is a goal-level problem (Lens 1) that manifests as emergent behavior.
5. **Latent capability activation** — does giving the base model new tools/autonomy risk surfacing capabilities/behaviors that were never explicitly designed for, just because the model is now capable of chaining them?

Findings here are usually *plausible scenarios*, not observed bugs — say so explicitly, and rate risk by how likely and how costly the scenario is, not by whether you've seen it happen.

## Lens 4: Paradigm / Mental Model

Ask where the agent's sense of "what am I for" actually comes from, and whether it's consistent:

1. **Explicit system prompt / instructions** — what does it say the agent's role and priorities are? Does it ever contradict itself, or leave the actual priority ordering implicit?
2. **Organizational conventions** (CLAUDE.md, style guides, shared config) — do these align with the system prompt, or quietly pull in a different direction?
3. **Tool design and affordances** — do the available tools imply a worldview? (E.g., an agent whose only destructive tool is `delete` will lean toward deleting when uncertain, simply because that's what's on offer.) See the dedicated checklist below.
4. **Base model training** — for anything that can't be changed by prompting, note it as a known constraint rather than a fixable finding — the audit should distinguish "you can fix this by editing a file" from "this is baked into the model and needs a different mitigation (e.g., a guardrail, not a better prompt)."
5. **Consistency across multi-agent systems** — if there's more than one agent, do they share a paradigm, or does each subagent implicitly believe something different about the system's purpose? Divergent paradigms between agents is a common, underrated source of the kind of emergent behavior in Lens 3.

### Tools / affordances

A tool list isn't a neutral menu — what's on it, and how each option is described, quietly tells the agent what kind of situation it's in and what a reasonable response looks like. Read the actual tool schemas and descriptions (not just the prompt's summary of them) and check:

1. **Affordance asymmetry.** Does the tool set skew toward one kind of action — mostly destructive/mutating (delete, send, execute) with no low-stakes alternative, or mostly passive (read-only) with one high-stakes escape hatch? An agent with no cheap, reversible option will use the expensive one more often than the situation actually calls for, simply because it's what's available. Check specifically for the presence (or absence) of a low-stakes fallback — an escalate/flag/ask-a-human tool — for situations that don't clearly warrant the bigger action.
2. **Description-vs-effect mismatch.** Does a tool's name or description undersell what it actually does? (`update_record` that actually overwrites and can't be partially applied; `archive` that's actually a hard delete.) The agent forms its sense of risk from the tool's description, not from reading the implementation — a mismatch here means the agent's caution calibration is wrong by design, independent of how careful the prompt tells it to be.
3. **Irreversibility signaling.** Does anything in the tool's schema or description flag that an action can't be undone (vs. every tool reading as equally casual)? If irreversibility is only communicated in prose elsewhere in the prompt, it's one edit away from being dropped or missed — the tool boundary is a more durable place to encode that than a sentence the model has to remember to apply.
4. **Granularity mismatch.** A single coarse tool that bundles several decisions into one call (e.g., one `resolve_ticket(action, refund_amount, close)` doing everything at once) removes the natural checkpoints that several smaller tool calls would create — there's no seam left where a check could be inserted between "decide" and "execute all of it." Conversely, tools that are too fine-grained can force so many calls that a real check becomes tedious enough to skip.
5. **Overlapping/redundant tools.** Multiple tools that accomplish similar ends (two ways to send a message, two ways to modify the same resource) create an implicit choice the agent makes on its own, often based on which is more prominent or easier to call correctly — not necessarily which is safer. This also expands the combinatorial surface from Lens 3 without adding real capability.
6. **Unsafe defaults.** Optional parameters that default to the more permissive or more destructive behavior (e.g., a delete tool that defaults to non-recoverable unless a `soft` flag is explicitly passed) put the burden of safety on every call site remembering to opt out, rather than opting in.

This checklist and the Rules level in Lens 1 overlap by design — a missing approval gate is a Rules-level finding about *permission*, while a tool's affordance is about what the *option itself* silently implies before permission even enters the picture. A tool can be perfectly gated and still shape behavior badly through how it's described.
