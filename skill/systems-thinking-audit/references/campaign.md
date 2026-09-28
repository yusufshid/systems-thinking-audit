# Campaign mode

For a system made of **many agents** that the user wants to review thoroughly, one agent at a time, over **many sessions and days**. A single audit is a snapshot; a campaign is a series of audits that has to add up to one answer to "is this whole system solid?" without anyone re-explaining anything in each new session.

Read this file only when a campaign is active (see SKILL.md, "Campaign mode"). A single audit never needs it.

The mechanism is deliberately small: **one ledger file** (`audit/LEDGER.md` in the audited repo) that you read at the start of every session and write at the end. No script, no database. Because the ledger is itself a stock that accumulates across sessions, the rules below exist to keep it from silently drifting (Memory/state in `framework.md`).

## Session bookends (every session, no exceptions)

**Start:**
1. Read `audit/LEDGER.md`. If it doesn't exist, this is Phase 1 — create it.
2. Remember its `last updated` line. Do not write the ledger later if that line changed while you worked (someone else, or another session, edited it) — show the user the conflict instead.
3. Give **one paragraph**, not a recap of the whole ledger: which phase, agents done / in progress / not started, and the open Critical/High findings. Then ask which agent to work on (suggest the next one, don't decide silently).

**End:**
1. Update the ledger: matrix cells, new/changed findings, decision log entries, `last updated`.
2. Show the user the diff of what you changed in the ledger, not just "updated." The ledger is the only memory; the user has to be able to see and correct it.
3. Say what the next session should start with.

If there is no write access to the audited repo (a third-party system, a pasted-in prompt), print the full updated ledger in chat at the end and ask the user to save it as `audit/LEDGER.md`; they paste it back at the start of the next session.

## Phase 1: Inventory (no findings yet)

Build the **roster**: one row per agent, with the component layers from `framework.md` that actually apply to it (Memory/state, Tools/affordances, Permissions/rules, …) and which do not (mark those — so they never show up as an unexamined gap later). Then record the **interfaces** between agents: shared state (files, DB, queues), shared tools, handoffs, shared control mechanisms (one "stop everything" switch), shared quotas or budgets.

You may propose the roster from the code, but the user confirms it — never treat an inferred roster as fact. An agent missing from the roster is never audited and never shows as ❓; this is the one place where a gap is invisible, so ask explicitly: "is there any agent, cron job, or subprocess not on this list?"

## Phase 2: Per-agent audit (one agent per session)

Run the normal audit (SKILL.md Steps 1–6) on that one agent, with these changes:
- Read only the `framework.md` layers the roster lists for this agent, using its Contents section — not the whole file.
- Write the full report to `audit/<id>-<name>.md` (same template as Step 4). Put a one-line entry per finding into the ledger's register, with the ID.
- Update this agent's matrix row: every applicable cell becomes ✅, ⚠️, or ❓ (naming the missing material). A cell is ✅ only for what was actually read this session.
- Cross-agent observations you notice while reading this agent (it writes a file another agent reads; it shares a tool) do **not** get resolved here — record them as **interface notes** on the roster for Phase 3. Judging one agent in isolation is exactly how cross-agent problems get missed.
- Step 7 (offering fixes) still applies per finding, per approval. Fixing a finding changes its status only after it is verified (see Findings below).

## Phase 3: System-level pass

Run when every agent's row has no ❓ that can be resolved, or when the user asks. The input is the **finding register plus the interfaces**, not the raw agents again. Look for what no single-agent audit can see:
- Orchestrator/leader section of `framework.md` for whatever coordinates the others, and the hierarchy balance (over-control vs. under-coordination).
- System Archetypes, run across the register: the same finding recurring in several agents is Shifting the Burden or a shared root cause (one fix, not N patches); several agents drawing on the same quota is Tragedy of the Commons.
- Shared state and shared control mechanisms across agents (visibility asymmetry, a control whose scope is wider than its name).
- Chain length across the whole workflow (Lens 2, point 10) — per-agent reliability multiplies across handoffs.
- Whether accepted risks in different agents combine into a larger one.

The System Map (SKILL.md Step 5) of this pass is the **roll-up report**. Write it to `audit/SYSTEM.md`. Cross-agent findings go in the register with `S` IDs (`S-F1`).

## Phase 4: Change-triggered re-audit

When an agent, tool, or shared component changes, don't re-audit everything and don't re-audit nothing: look up the changed component in the roster's interfaces, list the agents that share state, tools, or handoffs with it, and propose that list to the user. Re-audit the changed agent plus those neighbours for the layers the change touches. Use the Delta section (Step 4), matching findings **by ID**. Re-run Phase 3 if an interface changed.

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
- **`accepted` and `wontfix` need a reason and a revisit condition** in the Decisions section. Without one, an accepted risk is "we don't know" posing as "it's fine" (Data/ground-truth, point 7). When the revisit condition is met, the finding returns to `open`.
- **Same severity scale as Step 3, every session.** Don't re-rate a finding just because a new session felt differently; change severity only with new evidence, and log why.
- **Don't re-flag a finding the ledger already has** — say it recurred (Delta) or link the ID.
- **The ledger is not ground truth about the code.** It records what earlier sessions concluded. A ✅ from three days ago says nothing about code changed since; when the audited file is newer than the row, treat the cell as stale (Memory/state, staleness) and say so.

## Definition of done

The campaign is complete only when all of these hold:
1. Every applicable matrix cell is ✅ (or ⚠️ with the finding fixed/accepted) — no ❓ remains.
2. No `open` Critical or High finding.
3. Phase 3 was run **after the last change** to any agent or interface.
4. Every `accepted` finding has a revisit condition.

Until then, report progress against these four, not a feeling of "mostly done."
