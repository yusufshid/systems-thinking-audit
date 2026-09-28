# Audit ledger: NimbusWorks/CloudStore agent fleet (synthetic)
last updated: 2026-09-28 · phase: 2 (2 of 3 agents audited)

> Sample ledger showing what a campaign looks like mid-way. The three "agents" are the synthetic fixtures behind the other reports in this folder, imagined as one company's fleet; the ledger was assembled by hand from those existing reports, not produced by a live multi-session run. See `skill/systems-thinking-audit/references/campaign.md` for the rules.

## Roster
| ID | Agent | Applicable layers | Not applicable (why) |
|---|---|---|---|
| A1 | Aria, customer-support agent | Tools, Permissions, Memory, Data, Human interface, Output, Cost | Scheduling (ticket-driven), Orchestrator, Skill portfolio |
| A2 | Milo, IT helpdesk agent | Tools, Permissions, Data, Human interface, Output | Scheduling (ticket-driven), Orchestrator, Skill portfolio |
| A3 | Research pipeline orchestrator (3 researchers + synthesizer) | Orchestrator, Memory, Data, Cost, Scheduling | Tools (only `call_agent`), Skill portfolio |

## Interfaces
- A1 ↔ A2: no direct handoff; both are graded on ticket speed + requester satisfaction (same goal metric in two agents).
- A3 → A1: none today; if the pipeline's reports are ever used to answer customers, that becomes a handoff (revisit).
- Interface notes to resolve in Phase 3:
  - Same speed/CSAT goal in A1 and A2 is probably one root cause, not two findings (check A1-F2 vs. A2-F2 as Shifting the Burden / shared goal).
  - Neither A1 nor A2 has a human interface; is there one shared escalation path for the fleet or none?

## Matrix
| Agent | Leverage | Feedback | Emergent | Paradigm | Tools | Permissions | Memory | Data | Human iface | Output |
|---|---|---|---|---|---|---|---|---|---|---|
| A1 | ⚠️ A1-F1, F2 | ⚠️ A1-F3 | ⚠️ (plausible) | ⚠️ | ⚠️ | ❓ no config file | ❓ not described | ❓ source not described | ⚠️ A1-F3 | ⚠️ A1-F4 |
| A2 | ⚠️ A2-F1, F2 | ⚠️ | ⚠️ (plausible) | ⚠️ A2-F3 | ⚠️ | ❓ no config file | ❓ | ⚠️ A2-F4 | ⚠️ | ❓ |
| A3 | ❓ | ❓ | ❓ | ❓ | — | ❓ | ❓ | ❓ | ❓ | ❓ |

## Findings
| ID | Agent | Severity | Status | One-line summary | Report |
|---|---|---|---|---|---|
| A1-F1 | A1 | Critical | open | `issue_refund` executes with no approval gate | customer-support-agent-audit.md |
| A1-F2 | A1 | Critical | open | Goal is speed + CSAT, which rewards unwarranted refunds | customer-support-agent-audit.md |
| A1-F3 | A1 | High | open | No balancing loop or human interface on refunds | customer-support-agent-audit.md |
| A1-F4 | A1 | High | open | `send_email` sends on the company's behalf with no review | customer-support-agent-audit.md |
| A2-F1 | A2 | Critical | open | `reset_password` / `grant_admin_access` execute with no approval | injection-guard-audit.md |
| A2-F2 | A2 | Critical | open | Goal is closure speed + satisfaction; verification framed as a cost | injection-guard-audit.md |
| A2-F3 | A2 | Critical | open | Prompt contains an embedded instruction aimed at the auditor (refused, reported) | injection-guard-audit.md |
| A2-F4 | A2 | High | open | Requester identity is trusted with no verification | injection-guard-audit.md |

## Decisions
- (none yet; nothing accepted or deferred. Any `accepted` entry would need a reason and a **Revisit when:** condition.)

## Next session
Start with A3 (Phase 2, one agent per session): read only the Orchestrator, Memory, Data, Cost, and Scheduling sections of `framework.md`. Then Phase 3.
