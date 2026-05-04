# Confidence Determines Speed vs Quality

**Phase:** Decide · **Source:** https://untools.co/confidence-determines-speed-vs-quality

## Entry Predicate
`always_run`

## Inputs
- Computed confidence rubric (from Step 9)
- `frameworks/cynefin.md::domain`
- `intake.reversibility`

## Method
Map confidence to operating mode:
- **HIGH confidence + reversible** → optimize for **speed**: ship the smallest version, learn, iterate.
- **HIGH confidence + one-way-door** → optimize for **quality**: take the time to get it right.
- **LOW confidence + reversible** → ship a **probe** (smallest experiment that produces signal).
- **LOW confidence + one-way-door** → **defer** the decision; gather evidence first via more research or `/investigate`.

## Output Schema (table)
| Confidence | Reversibility | Mode | Action |
|---|---|---|---|
| HIGH | reversible | SPEED | ship MVP, iterate |
| HIGH | one-way | QUALITY | careful build, then ship |
| LOW | reversible | PROBE | smallest experiment |
| LOW | one-way | DEFER | gather more evidence |

Place this run's case on the matrix. Justify in 2-3 sentences.

## Decision Hook
Mode dictates the **shape of the recommendation** in the report:
- SPEED mode → recommendation includes "first step in 24 hours" timeline.
- QUALITY mode → recommendation includes pre-ship checklist.
- PROBE mode → recommendation defines success/failure signals upfront.
- DEFER mode → recommendation is "do not decide yet; here's what to learn first."

## What This Means For The Decision
Confidence is not just a number on the report — it determines **how the decision should be executed**. Treating a low-confidence one-way-door as a high-confidence MVP is the most common decision-making mistake.
