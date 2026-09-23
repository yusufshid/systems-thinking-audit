# Design Principles

This is the reference point contributions get checked against — the "goal definition" for this project, made explicit so it isn't just whatever's in the maintainer's head. If a PR or checklist suggestion doesn't fit here, that's a reason to discuss it, not an automatic rejection — but it should be discussed against these principles specifically, not decided ad hoc.

## 1. Structural, not domain-judgment
This skill audits *how a system is built* — goals, feedback loops, tools, permissions, memory, output channels — not whether specific content, code, or business logic is good. "Is this marketing copy persuasive" is out of scope; "does this marketing agent have any check before publishing under the brand's name" is in scope. If a proposed addition requires judging domain-specific correctness rather than structure, it probably belongs in `/code-review`, `/security-review`, or a domain-specific tool instead.

## 2. Name the mechanism, not the vocabulary
A finding says "the reviewer agent uses the same prompt and model as the writer agent, so it shares the writer's blind spots" — not "there is a feedback loop issue." Every checklist item added to `references/framework.md` must include a concrete red-flag example a reader can recognize, not just a restated systems-thinking term.

## 3. Don't force a finding to fill a section
"None identified" / "no significant issues found" is a legitimate, expected outcome for any lens or checklist item. A change that makes the skill more likely to pad out a report with marginal findings just to look thorough moves in the wrong direction, even if each individual finding is defensible.

## 4. Findings connect into one story, not four piles
The four lenses and ten component-layer checklists are a *search* tool, not the shape of the final report. Any change to the report template should preserve — not dilute — the System Map's job of tracing findings into one causal chain. A change that makes the skill more likely to report a checklist recitation instead of a connected diagnosis is a regression, even if it "covers more ground."

## 5. Self-verification is a weak signal — say so
This applies to the skill's own outputs as much as to what it audits. Prefer an independent verification pass over self-check when the tooling allows it (Step 6), and don't quietly soften this principle to make an audit look more confident than the checking behind it actually supports.

## 6. Audited material is data, never instructions
This is non-negotiable and has an eval case (`evals/evals.json`, id 3) enforcing it. Nothing about "efficiency" or "conciseness" justifies weakening the guard against treating content inside the audited artifact as commands to the auditor.

## 7. Progressive disclosure — keep `SKILL.md` lean
Depth belongs in `references/`, loaded on demand, not inlined into `SKILL.md`. If `SKILL.md` is approaching a size where it's hard to scan, that's a signal to push detail into a reference file with a clear pointer, not to trim the substance.

## 8. Domain-agnostic core, domain-specific translation as a separate layer
The four lenses and component-layer checklists stay domain-agnostic by design (see `DESIGN_PRINCIPLES.md` §1). Domain-specific knowledge (sales, trading, marketing, etc.) belongs in `references/domains.md` as translation notes, not baked into the core checklist as special cases — this keeps the core from fragmenting into an unmaintainable pile of "if domain X, then..." branches.

## 9. New checklist items earn their place with an example, not just an argument
A proposed addition to `references/framework.md` should include a realistic scenario that would trigger the finding, ideally paired with an eval case demonstrating the skill catches it. An abstract argument for why a category *might* matter is a weaker basis for inclusion than a concrete case showing it *does*.

## 10. Full audits and targeted audits are equally first-class
Step 0's scope split (full vs. targeted) is a deliberate design choice, not a shortcut. Changes shouldn't assume every audit runs the complete four-lens process — a targeted audit that thoroughly covers one aspect is a valid, complete outcome, not a lesser version of a full one.
