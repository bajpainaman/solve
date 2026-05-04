# Zwicky Box (Morphological Analysis)

**Phase:** Define · **Source:** https://untools.co/zwicky-box

## Entry Predicate
`∃ ≥ 2 design dimensions in problem` — run when the problem has multiple independent axes.

## Inputs
- `intake.problem_refined`
- `frameworks/first-principles.md::atomic_truths`
- `frameworks/issue-tree.md::dimensions`

## Method
1. Identify 3-5 **dimensions** (axes) of the solution space.
2. For each dimension, list 3-7 **options**.
3. Build the matrix (axes × options).
4. **Combinatorial generation**: total solutions = product of option counts.
5. Filter: prune combos that violate constraints from inversion-define.
6. Cluster surviving combos into 5-10 **archetypes** (named solution families).

## Parallel Fan-Out
Spawn 1 Agent subagent per axis to generate options + research that axis. Saves to `$RUN_DIR/evidence/zwicky-axis-<n>.md`.

## Output Schema
Table:

| Dimension | Option A | Option B | Option C | Option D |
|---|---|---|---|---|
| Architecture | monolith | microservices | modular monolith | serverless |
| Storage | postgres | mongo | sqlite | dynamodb |
| Auth | session | JWT | oauth | passkeys |

Then:

```
ARCHETYPE 1 (named): <combo>
ARCHETYPE 2 (named): <combo>
...
```

## Decision Hook
Archetypes become **options** in the Decision Matrix.

## What This Means For The Decision
Zwicky exposes solutions you wouldn't have brainstormed. The matrix forces the team to consider combos, not just the obvious 2-3 candidates.
