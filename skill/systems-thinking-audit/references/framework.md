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
3. **Tool design and affordances** — do the available tools imply a worldview? (E.g., an agent whose only destructive tool is `delete` will lean toward deleting when uncertain, simply because that's what's on offer.)
4. **Base model training** — for anything that can't be changed by prompting, note it as a known constraint rather than a fixable finding — the audit should distinguish "you can fix this by editing a file" from "this is baked into the model and needs a different mitigation (e.g., a guardrail, not a better prompt)."
5. **Consistency across multi-agent systems** — if there's more than one agent, do they share a paradigm, or does each subagent implicitly believe something different about the system's purpose? Divergent paradigms between agents is a common, underrated source of the kind of emergent behavior in Lens 3.
