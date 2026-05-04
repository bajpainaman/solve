# Inversion (Define-Phase)

**Phase:** Define · **Source:** https://untools.co/inversion

## Entry Predicate
`always_run`

## Note
This is the **define-phase** inversion: surfaces failure modes early. The continuous adversary (spawned in Step 4) handles ongoing critique. The final inversion-as-dissent runs after Step 8.

## Inputs
- `intake.problem_refined`

## Method
1. Ask: **"What would guarantee failure?"** List 5-10 failure paths.
2. For each: what conditions must be true for that failure to manifest?
3. Convert each failure condition to a **constraint** the solution must avoid.
4. The constraint set becomes a **solution-space filter** for Phase 3.

## Output Schema
```
FAILURE PATHS
  F1: <path> — conditions: [c1, c2, c3]
  F2: ...

CONSTRAINTS DERIVED
  - solution must NOT [...]
  - solution must NOT [...]
  - if [...], abort
```

## Decision Hook
Constraints feed Decision Matrix as **disqualifiers** (any option failing a constraint scores 0).

## What This Means For The Decision
Inversion is cheap. Spending 10 minutes on "how could this fail" prevents the 80% of bad decisions made by only thinking about success.
