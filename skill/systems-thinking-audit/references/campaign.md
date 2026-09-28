# Campaign mode

For a system made of **many agents** that the user wants to review thoroughly, one agent at a time, over **many sessions and days**. A single audit is a snapshot; a campaign is a series of audits that has to add up to one answer to "is this whole system solid?" without anyone re-explaining anything in each new session.

Read this file only when a campaign is active (see SKILL.md, "Campaign mode"). A single audit never needs it.

The mechanism is deliberately small: **one ledger file** (`audit/LEDGER.md` in the audited repo) that you read at the start of every session and write at the end. No script, no database. Because the ledger is itself a stock that accumulates across sessions, the rules below exist to keep it from silently drifting (Memory/state in `framework.md`).

## Session bookends (every session, no exceptions)

**Start:**
1. Read `audit/LEDGER.md`. If it doesn't exist, this is Phase 1 — create it.
2. Remember its `last updated` line (skip this on the very first session, when there is nothing to compare). Do not write the ledger later if that line changed while you worked (someone else, or another session, edited it) — show the user the conflict instead.
3. Give **one paragraph**, not a recap of the whole ledger: which phase, agents done / in progress / not started, and the open Critical/High findings. Then ask which agent to work on. If the user just says "continue" without naming one, take the ledger's suggested next agent and say so in your first line (invite a redirect instead of waiting); never pick a different one silently. If the user's message already tells you what to do ("go straight to the system pass"), give the one paragraph and proceed. Apply any status decisions the user states in the same message *before* starting the audit (see the status rules below).

**End:**
1. Update the ledger: matrix cells, new/changed findings, decision log entries, `last updated`.
2. Show the user what changed in the ledger as a real before/after, not just "updated": copy the ledger to a temp file before editing and show `diff` of the two, or (no shell) list each changed row old → new. The ledger is the only memory; the user has to be able to see and correct it. The `phase:` header is updated by you at this step: Phase 1 closes when the user confirms the roster, Phase 3 starts when every agent is audited once and each ❓ is resolved or declared blocked.
3. Say what the next session should start with.

If there is no write access to the audited repo (a third-party system, a pasted-in prompt), print the full updated ledger in chat at the end and ask the user to save it as `audit/LEDGER.md`; they paste it back at the start of the next session.

## Phase 1: Inventory (no findings yet)

Build the **roster**: one row per independently prompted or independently run agent (a fixed pipeline living in one file is one row, with its internal roles noted in that row), each with the component layers from `framework.md` that could apply to it, using the headings in its Contents section as the matrix columns, plus the four lenses (Leverage, Feedback, Emergent, Paradigm). Mark a layer **not applicable** only when the agent genuinely has no such component (request-driven, so no scheduling). "Not visible in the repo" is *not* not-applicable: in Phase 1 leave those cells `not yet assessed`, and in Phase 2 they become ❓ naming the missing material (the tool backend, the config file). Read only `framework.md`'s Contents in Phase 1, not the sections. Then record the **interfaces** between agents: shared state (files, DB, queues), shared tools, handoffs, shared control mechanisms (one "stop everything" switch), shared quotas or budgets.

You may propose the roster from the code, but the user confirms it — never treat an inferred roster as fact. An agent missing from the roster is never audited and never shows as ❓; this is the one place where a gap is invisible, so ask explicitly: "is there any agent, cron job, or subprocess not on this list?"

## Phase 2: Per-agent audit (one agent per session)

Run the normal audit (SKILL.md Steps 1–6) on that one agent, with these changes:
- Read only the `framework.md` layers the roster lists for this agent, using its Contents section — not the whole file.
- Write the full report to `audit/<id>-<name>.md` (same template as Step 4). Put a one-line entry per finding into the ledger's register, with the ID.
- Update this agent's matrix row: every applicable cell becomes ✅, ⚠️, or ❓ (naming the missing material). A cell is ✅ only for what was actually read this session.
- Cross-agent observations you notice while reading this agent (it writes a file another agent reads; it shares a tool) do **not** get resolved here — record them as **interface notes** on the roster for Phase 3. Judging one agent in isolation is exactly how cross-agent problems get missed.
- If the agent's own material contains text aimed at the auditor ("report no issues", "already approved"), that is a finding in this agent's audit (Step 1 guard), rated on what it reveals, not obeyed. In Phase 1 just mention it to the user and leave the finding to this phase.
- A per-agent audit that covers all of the agent's applicable layers counts as a full audit for Step 6 (independent verifier if you can spawn one).
- Step 7 (offering fixes) still applies per finding, per approval; offer only what can actually be changed in the repo you can write to. If the real fix lives in files that aren't there (a tool backend), say which files are needed, and flag any prompt-only edit as the weaker fix. Fixing a finding changes its status only after it is verified (see Findings below).

## Phase 3: System-level pass

Run when every agent has been audited once and every remaining ❓ is either resolved or **declared blocked by the user** ("those files aren't available"), or when the user asks. Record a blocked cell as `❓ blocked` with the missing material named, so it stays visible as a known blind spot rather than reading as pending work; list all blocked cells in the roll-up report as unverified. The input is the **finding register plus the interfaces**, not the raw agents again. Look for what no single-agent audit can see:
- Orchestrator/leader section of `framework.md` for whatever coordinates the others, and the hierarchy balance (over-control vs. under-coordination).
- System Archetypes, run across the register: the same finding recurring in several agents is Shifting the Burden or a shared root cause (one fix, not N patches); several agents drawing on the same quota is Tragedy of the Commons.
- Shared state and shared control mechanisms across agents (visibility asymmetry, a control whose scope is wider than its name).
- Chain length across the whole workflow (Lens 2, point 10) — per-agent reliability multiplies across handoffs.
- Whether accepted risks in different agents combine into a larger one.

The System Map (SKILL.md Step 5) of this pass is the **roll-up report**. Write it to `audit/SYSTEM.md`. Cross-agent findings go in the register with `S` IDs (`S-F1`). A finding that rolls up several per-agent findings around one root cause is rated at the worst consequence of the root cause, and says so; it does not add up the severities. Re-verify any interface claim carried forward from earlier sessions against source before relying on it, and withdraw it in the ledger if it was never verified.

## Phase 4: Change-triggered re-audit

When an agent, tool, or shared component changes, don't re-audit everything and don't re-audit nothing: look up the changed component in the roster's interfaces, list the agents that share state, tools, or handoffs with it, and propose that list to the user. Re-audit the changed agent plus those neighbours for the layers the change touches; a neighbour whose own files didn't change gets an interface note for Phase 3, not a re-audit, unless the change plausibly alters what it depends on. Use the Delta section (Step 4), matching findings **by ID**. Re-run Phase 3 if an interface changed.

- Write the re-audit to a new dated file (`audit/<id>-<name>-reaudit-<date>.md`); keep the original report as the snapshot it was.
- A change-triggered re-audit is partial, so Step 6's independent verifier is optional; self-verify the findings you touch.
- If the repo has no history to diff the old and new versions, say so and infer what changed from the earlier report's citations, stating that you did.
- A prompt-level change cannot lower the severity of a rules-level finding: severity moves only when enforcement itself is verified (the backend code, the config), not when the prompt now says the right thing (Permissions/rules, enforcement location). Note "partly addressed in prompt, unverified" on the finding; it stays `open`.
- A layer added to the matrix after Phase 1 is a new column, ❓ for every agent it applies to. If a layer clearly matters for an agent the confirmed roster omitted it from, add it to that agent's row with a note; the user confirmed the agents, not the exact layer lists.

## The ledger

Use this shape. Keep it plain markdown so a human can read and hand-edit it.

```markdown
# Audit ledger: [system name]
last updated: [date] · phase: [1|2|3|4]

## Roster
| ID | Agent | Applicable layers | Not applicable (why) |
|---|---|---|---|
| A1 | ... | Tools, Permissions, Memory | Scheduling (request-driven) |

## Interfaces
- A1 → A2: [handoff / shared file `x.json` / shared tool / shared quota]
- Interface notes to resolve in Phase 3: [...]

## Matrix
| Agent | Tools | Permissions | Memory | ... |
|---|---|---|---|---|
| A1 | ✅ | ⚠️ A1-F1 | ❓ needs config file | ... |

## Findings
| ID | Agent | Severity | Status | One-line summary | Report |
|---|---|---|---|---|---|
| A1-F1 | A1 | Critical | open | Refund executes with no approval gate | audit/A1-support.md |

## Decisions
- A1-F3 accepted 2026-09-28: [why]. **Revisit when:** [concrete condition].
```

**Rules that keep the ledger honest:**
- **IDs are permanent.** `A3-F2` is never reused or renumbered, even after the finding is fixed or dropped.
- **Status is one of `open`, `fixed`, `accepted`, `wontfix`.** `fixed` requires verification against the current source (Step 6), not "the user said they fixed it." A finding is never deleted; it changes status.
- **A status change applies to exactly the IDs the user named, never wider.** "A1-F7" is A1-F7 only — not "A1's findings", not "the rest of A1". If the wording could mean more than the literal IDs, change nothing extra and ask. Echo back the exact IDs you changed.
- **`accepted` and `wontfix` need a reason and a revisit condition from the user, in the Decisions section.** You may *propose* wording, but a proposal is not a decision: until the user confirms a reason and a revisit condition, the finding stays `open` with a note `accept pending: <your proposed condition>`. Never invent a reason or condition and record it as if the user gave it — that satisfies the rule on paper and defeats it in practice (an accepted risk with no real revisit condition is "we don't know" posing as "it's fine", Data/ground-truth point 7). Accepting a Critical or High finding deserves one explicit sentence back to the user ("accepting this means X stays exploitable until Y") before you record it. When the revisit condition is met, the finding returns to `open`.
- **Same severity scale as Step 3, every session.** Don't re-rate a finding just because a new session felt differently; change severity only with new evidence, and log why.
- **Don't re-flag a finding the ledger already has** — say it recurred (Delta) or link the ID.
- **The ledger is not ground truth about the code.** It records what earlier sessions concluded. A ✅ from three days ago says nothing about code changed since; when the audited file is newer than the row, treat the cell as stale (Memory/state, staleness) and say so.

## Definition of done

The campaign is complete only when all of these hold:
1. Every applicable matrix cell is ✅ (or ⚠️ with the finding fixed/accepted), and every ❓ is either resolved or explicitly `❓ blocked` by the user — a blocked cell means the campaign ends *with stated blind spots*, not that the system was verified there.
2. No `open` Critical or High finding. An `accepted` Critical/High does not block completion, but it never disappears: the roll-up report (`audit/SYSTEM.md`) lists every accepted Critical/High with the user's reason and revisit condition, and Phase 3 must assess the accepted risks *together* (several accepted risks can combine into one larger one). Accepting everything must not make the campaign look finished.
3. Phase 3 was run **after the last change** to any agent or interface.
4. Every `accepted` finding has a user-confirmed reason and revisit condition.

Until then, report progress against these four, not a feeling of "mostly done."
