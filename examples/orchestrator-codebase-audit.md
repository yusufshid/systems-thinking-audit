# Systems Thinking Audit: Research pipeline orchestrator

## Scope
Reviewed: the orchestrator's actual codebase ([`evals/input/orchestrator.py`](../skill/systems-thinking-audit/evals/input/orchestrator.py)) — control flow, both agent prompts, and the retry logic. No execution trace, scheduling config, or deployment info was available, so findings about actual runtime frequency/cost are plausible extrapolations from the code's structure, not observed numbers.

## Coverage
- **Leverage Points** — ✅ Checked, issue found (Goals level — see Findings)
- **Feedback Loops** — ✅ Checked, issue found
- **Emergent Behavior** — ✅ Checked, issue found
- **Paradigm / Mental Model** — ✅ Checked, issue found
- **Memory / state** — ✅ Checked, issue found (`shared_state.json`)
- **Orchestrator / leader agents** — ✅ Checked, issue found (synthesizer's role)
- **Cost / economics** — ✅ Checked, issue found (retry multiplies agent-call volume)
- **Data / ground-truth sources** — ❓ Not checked — researchers "search the web," but the actual search mechanism/tool and how its results are verified aren't in this file
- **Scheduling / triggers** — ❓ Not checked — nothing in this file says how or how often `run_with_retry` gets invoked
- **Permissions / rules** — ❓ Not checked — no permission/settings config was included
- **Deployment / rollout, Dependency / supply-chain, Human interface, Incident response** — ❓ Not checked — no material covering any of these was provided (`agent_runtime` is imported but not shown)
- **Tools / affordances** — — Not applicable — the agents here don't call external tools beyond `call_agent` itself
- **Skill portfolio** — — Not applicable — this is a fixed 4-agent pipeline, not a modular skill-composed agent

## Summary
The pipeline's core design creates the appearance of independent, thorough research while actually providing neither: three researchers that share an identical prompt and model produce correlated rather than independent findings, and the retry loop's success condition (`len(report.split()) > 500`) rewards verbosity, not accuracy — a goal-level proxy-metric problem that the prompt text itself invites ("more findings means a more complete report").

## Findings

### Leverage Points
- **Goals (level 5) — Critical.** `run_with_retry`'s loop condition is `len(report.split()) > 500`, and `RESEARCHER_PROMPT` explicitly tells researchers "include as many findings as possible, since more findings means a more complete report." Word count is a proxy for thoroughness, not a measure of it — the system is structurally rewarded for producing longer output, not more correct output. *Recommendation: replace or supplement the length check with a quality signal that isn't trivially gameable by padding (e.g., a rubric-based check, or at minimum a floor on distinct claims/sources rather than word count).*
- **Information structure (level 3) — Medium.** `shared_state.json` is written after all three researchers finish, described in a comment as "notes," but nothing in this file ever reads it back. It's dead state that implies coordination the code doesn't actually implement. *Recommendation: either remove the write (if it's truly unused) or, if the intent was for researchers to see each other's progress, actually wire that read path in — the comment currently misdescribes the architecture to anyone who reads it without checking.*

### Feedback Loops
**Reinforcing loops found:**
- Retry-on-word-count → a short-but-accurate report gets discarded in favor of retrying → each retry re-runs all 3 researchers and the synthesizer from scratch, and the only thing that changes the outcome is the model happening to produce more words, not better ones.

**Balancing loops found:**
- None identified for output *quality*. There is no check anywhere in this file that verifies the synthesizer's report is factually correct or well-reasoned — only that it's long enough. This is the Critical-adjacent gap: the system has a loop, but it corrects for the wrong variable.

Expanded: the retry loop is reinforcing with no cap on *quality* drift (only a cap on iteration count, `max_retries=10`) — signal source is a proxy metric (word count), not a ground-truth or independent check. Risk: High. *Recommendation: same fix as the Goals-level finding above — these are one problem seen from two lenses, not two separate ones (see System Map).* Separately: after 10 failed attempts, `run_with_retry` "give[s] up, return[s] whatever we have" with no flag anywhere that this happened — a caller receiving the final report has no way to know it's the exhausted-retries fallback rather than a normal success. *Recommendation: return or log a distinct signal when the retry budget is exhausted, so downstream consumers (or a human) can tell the two cases apart.*

### Emergent Behavior Risks
- **Multi-agent interaction / correlated bias.** All 3 researchers run `RESEARCHER_PROMPT` on `model="claude-default"` — identical prompt, identical model. Any systematic blind spot or bias in that combination shows up in all three "independent" findings at once, and the synthesizer has no way to distinguish genuine consensus from three correlated copies of the same mistake. Risk: High. *Recommendation: vary at least one axis — a different prompt framing, a different model, or an explicit adversarial/red-team framing for at least one researcher — so agreement is actually informative.*
- **Cost multiplication from the retry structure.** Each `run_with_retry` call can trigger up to 10 full pipeline runs, each of which is 3 researcher calls + 1 synthesizer call — up to 40 agent calls for a single query, driven entirely by a word-count check rather than by the query's actual difficulty. Risk: Medium (cost/economics, not correctness) — plausible scenario, no trace confirming actual retry frequency in production. *Recommendation: log and monitor actual retry counts in production; if retries are frequent, the word-count threshold is likely miscalibrated rather than the model being unable to write 500 words, which would point back to the Goals-level fix rather than a cost-side patch.*

### Paradigm / Mental Model
`RESEARCHER_PROMPT`'s framing — "be thorough," "include as many findings as possible" — establishes an implicit paradigm of exhaustiveness-as-quality that the retry logic then mechanically enforces. Nothing in either prompt frames the goal as *correctness*; `SYNTHESIZER_PROMPT`'s only guidance for disagreement is "use your best judgment," which asks the synthesizer to adjudicate with no criteria and no independent signal to break ties. Risk: High. *Recommendation: give the synthesizer an explicit standard for resolving disagreement (e.g., prefer claims corroborated by more than one researcher, or flag unresolved disagreements to a human rather than silently picking one) instead of undefined "best judgment."*

**Orchestrator / leader agents:** The synthesizer is built as a collector (merge three inputs into one) but is implicitly expected to act as an adjudicator (resolve disagreements) — "use your best judgment to decide which one is right" hands it that job with no reconciliation mechanism, which is exactly the gap behind contradictory or overconfident multi-reviewer output. Risk: High. *Recommendation: decide explicitly whether this role should be a collector or an adjudicator; if adjudicator, give it the tools that role needs (visibility into *why* each researcher concluded what it did, not just the conclusions, and explicit tie-breaking criteria).*

## Recommendations (prioritized)
1. **Replace the word-count retry condition with a quality signal** (Critical, Goals-level). Higher effort than a parameter tweak, but a parameter tweak (e.g., changing the 500-word threshold) wouldn't fix the underlying issue — any length threshold is still a proxy. *Second-order effect: a genuine quality check adds latency/cost per attempt; that's an acceptable trade only if it actually reduces low-quality retries, so measure before and after.*
2. **Diversify the 3 researchers along at least one axis** (prompt, model, or framing) (High). *Second-order effect: introduces the possibility of genuine, informative disagreement — which only helps if the synthesizer (see #3) is actually equipped to reconcile it rather than just average it away.*
3. **Give the synthesizer explicit disagreement-resolution criteria**, or route unresolved disagreements to a human instead of silent best-judgment (High). *Second-order effect: without #2, this doesn't help much — three correlated researchers rarely disagree in the first place, so there'd be little for better criteria to act on.*
4. **Flag retry-budget exhaustion distinctly from normal success**, and remove or actually wire up `shared_state.json` (Medium/Low, low effort, no significant second-order effect).

## System Map
The retry loop's word-count condition and the researcher prompt's "more findings is better" instruction are the same goal-level problem viewed from two places in the code — one wrote the incentive into the prompt, the other mechanically enforces it in the control flow. That shared root cause is what makes the correlated-researcher risk worse than it would otherwise be: three agents chasing volume under the same prompt and model don't just risk agreeing on the same blind spot, they're actively rewarded for padding rather than for catching each other's gaps, which is exactly what an ideal 3-researcher setup should do. Fixing the goal metric (#1) is the highest-leverage change — it removes the pressure that would otherwise keep undermining a "diversify the researchers" fix (#2) even after that's implemented, since a still-length-obsessed system would just find new ways to pad three differently-framed outputs to the same threshold.
