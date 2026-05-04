# Framework Depth Template

Every framework in `frameworks/<name>.md` follows this spine. The full reference exemplar is `cynefin.md` — read that first for shape, then copy the section ordering here. Target length is ~2000 lines per framework, matching gstack-skill depth.

This file is documentation, not a runnable framework. It does not appear in `frameworks/` listings consumed by `/solve` (the leading underscore exempts it). Keep this file and `cynefin.md` in sync when the spine changes.

---

## Required sections (in this exact order)

### 1. Header
- Title: `# <Framework Name>`
- One-line subtitle: `**Phase:** Define|Systems|Decide · **Source:** <untools URL>`

### 2. Entry Predicate (formal logic)
A single block stating when this framework runs. Use formal-logic notation that the orchestrator (definer / systems-thinker / decider) can evaluate against `intake.json` + prior framework outputs.

Examples:
- `always_run` — runs every time the phase fires
- `intake.stakeholders ≠ "single-decider"` — only when ≥ 2 parties
- `∃ cycle ∈ connection-circles.cycles : type = balancing`
- `cynefin.domain ∈ {complex, chaotic} ∨ intake.time_pressure = "now"`

After the predicate, list **inputs** (what this framework reads from `$RUN_DIR/`) and **outputs** (where it writes).

### 3. Operating Principles
3-5 non-negotiables that shape every output of this framework. Each principle gets:
- One bold one-liner (the rule)
- A 2-3 sentence justification (the why)
- An anti-pattern (what violating this looks like)

Borrow style from gstack/office-hours Phase 2A "Operating Principles" — short, sharp, evidence-grounded.

### 4. Response Posture
How the agent should behave while running this framework:
- Tone (direct? empathetic? adversarial?)
- Pacing (one question at a time? batched?)
- Push depth (when to accept an answer vs push for specifics)
- Where to escalate (when to surface to lead via SendMessage)

### 5. Anti-Sycophancy Rules
Never-say / always-do patterns. Lift the format from office-hours:
- **Never say** "that's interesting" / "could work" / "you might want to consider..."
- **Always do** take a position, name the specific evidence that would change the call, name common failure patterns explicitly.

### 6. Pushback Patterns
3-5 paired patterns showing soft (BAD) vs forcing (GOOD) responses to common user inputs. Format:

> **Pattern N: <name> → <outcome>**
> - User: "<typical vague input>"
> - BAD: "<encouraging-but-empty response>"
> - GOOD: "<specific, evidence-demanding response>"

These are the most-reread sections in any deep skill. Make them concrete and domain-tuned to this framework.

### 7. Method (step-by-step)
The actual workflow. Numbered steps. Each step:
- States the action
- Lists prerequisites (what must be true before running)
- Shows expected output type (text / table / mermaid / file write)
- Names the failure mode (what happens if the step is skipped)

If the framework has parallel fan-out (Zwicky axes, Six Hats roleplays), spell out the fan-out shape: how many agents, what each gets briefed with, how outputs reconcile.

### 8. Question Patterns
Specific prompts the agent uses to extract evidence. Each pattern has:
- The exact wording
- What "good" looks like (specific, evidence-bound)
- Red flags (what to push back on)
- Smart-skip conditions (when this question is unnecessary)

For frameworks that don't ask user questions directly (most systems frameworks), this section becomes "Probe Patterns" — the questions the agent asks itself while analyzing prior outputs.

### 9. Forcing Exemplars
For each major prompt or recommendation this framework produces, give a paired example:
- **SOFTENED (avoid):** the polite, hedged version
- **FORCING (aim for):** the version that surfaces the truth

Use the office-hours pattern: the difference between "what's your target user" and "name the actual human, not 'product managers' but the specific role and the specific consequence they're avoiding."

### 10. Output Schema
The exact structure the framework writes to `$RUN_DIR/frameworks/<name>.md`:
- mermaid blocks (graph TD / graph LR / quadrantChart) with example node shapes
- markdown tables with sample rows showing types and units
- prose sections with required headings and bullet shape
- end always with a "What This Means For The Decision" block

For tables, list every column with: name, type, unit, allowed values, derivation rule.

### 11. Decision Hook
How this framework's output feeds downstream:
- Which other framework(s) consume it
- What synthesis logic combines this with peers
- Confidence-rubric impact (does it +1, +2, or 0 the rubric?)
- When this framework's output overrides another (e.g. Hard Choice overrides Decision Matrix when triggered)

### 12. Cross-Framework Triggers
Conditions in this framework's output that force other frameworks to run, or that fire mid-run handoffs to other skills:
- iceberg.structures = bug-shape → invoke `/investigate`
- decision-matrix.top_two_within_5pct → trigger Hard Choice
- six-hats.black_score ≥ 8 → escalate adversary, mark dissent

### 13. Failure Modes
3-5 ways this framework fails silently or misleads:
- The specific trap
- How it manifests in output
- The check that catches it
- The recovery action

Example for Issue Tree: "MECE violation — branches overlap. Manifests as the same evidence appearing under two leaves. Check: dedupe leaf IDs. Recovery: redraw the tree with peer review."

### 14. Jargon Glossary
List of domain terms used in this framework that need glossing on first use. Format: `term — one-line plain-English meaning`.

Borrow office-hours' jargon-list pattern: idempotent, race condition, deadlock, etc. Tune to this framework's vocabulary (e.g. Cynefin: emergence, equifinality, retrospective coherence; Decision Matrix: orthogonality, dominance, weighted sum scaling).

### 15. Completeness Scoring
Self-rate the framework output 0-10 on coverage:
- 10 = every dimension explored, every alternative considered, every assumption tested
- 7 = happy path covered, 1-2 edges
- 3 = shortcut, demo path only

Define the rubric for THIS framework. What does 10 look like for this specific framework? What does 7 look like? Be concrete.

The completeness score appears in the framework output and feeds the overall Confidence rubric in Step 9 of SKILL.md.

### 16. Worked Example
A 200-400 line walkthrough of this framework on a real problem. Use a recurring example across frameworks for continuity:

**Canonical example problem:** "Should we migrate our LayerZero OFTv1 deployment to OFTv2?"

Show:
- The intake state going in
- Each step of the framework method applied
- The actual output the agent would produce (full mermaid blocks, full tables, prose)
- The decision hook firing (what the next framework receives)

This is the most concrete part of the file. New users skip everything else and read this.

### 17. What This Means For The Decision
Final 1-2 paragraph synthesis: when this framework is decisive vs supportive, the specific decision pattern this framework produces, and the cost of skipping it.

---

## Voice (apply to every section)

**Builder-to-builder.** Direct, concrete, evidence-grounded. No filler.

- Lead with the point. Say what the framework does, why it matters, what changes for the decision.
- Be concrete. Name specific examples, specific evidence shapes, specific outputs.
- Tie technical/analytical choices to decision outcomes: what the user can now act on.
- Be direct about quality. Bad framing matters. Wrong predicate matters. Fix the whole framework, not the demo path.
- Sound like a builder talking to a builder.
- Never corporate, academic, PR, or hype.
- **No em dashes.** No AI vocabulary: delve, crucial, robust, comprehensive, nuanced, multifaceted, furthermore, moreover, additionally, pivotal, landscape, tapestry, underscore, foster, showcase, intricate, vibrant, fundamental, significant.
- The user has context the framework does not. Cross-framework agreement is a recommendation, not a decision. The user decides.

**Good:** "Cynefin = complex means the cause-effect is only knowable in retrospect. Probe with 3-5 small experiments before committing the architecture. Don't let Decision Matrix bully you into a choice the data can't support yet."

**Bad:** "It is important to note that complex problems require careful consideration of multiple factors and a nuanced approach to decision-making."

---

## Length target

~2000 lines per framework. If your framework is shorter, the worked example is too thin or the failure modes are missing. Add concrete examples, more pushback patterns, more failure modes.

If your framework is much longer than 2500 lines, you're padding. Cut filler.

---

## Cross-references

Every framework lists which others it depends on (in Inputs) and which it feeds (in Cross-Framework Triggers). The 25 framework files form a directed graph. Make the edges explicit.

When in doubt, read `cynefin.md` for the canonical shape.
