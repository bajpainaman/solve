# Eisenhower Matrix

**Phase:** Decide · **Source:** https://untools.co/eisenhower-matrix

## Entry Predicate
`always_run` if `intake.time_pressure ∈ {now, this-week}`; otherwise `recommended`.

## Inputs
- `frameworks/productive-thinking.md::resource_plan`
- `intake.time_pressure`

## Method
Build a 2×2 matrix on (Urgency × Importance) for the candidate options or sub-decisions.

## Output Schema (table)
| | Urgent | Not Urgent |
|---|---|---|
| **Important** | DO NOW | SCHEDULE |
| **Not Important** | DELEGATE | DROP |

For each cell, list the candidates that fall there with one-line justification.

## Decision Hook
Items in **Drop** are removed from Decision Matrix. Items in **Delegate** are flagged for handoff. Items in **Schedule** become deferred follow-ups in the report's appendix. Items in **Do Now** dominate.

## What This Means For The Decision
Most "decisions" are time-allocation questions in disguise. Eisenhower forces explicit triage so the Decision Matrix only weighs the things that actually need a deliberate choice.
