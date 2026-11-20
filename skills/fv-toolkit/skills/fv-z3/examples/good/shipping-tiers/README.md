# Shipping tiers: a decision table checked for completeness and uniqueness

**Pattern:** rule / eligibility / decision table (catalog A3, F3).
**Teaches:** completeness and uniqueness as two separate formulas, and a rejected design beside the checks that must pass.

## The system

A carrier prices a package by its weight in grams, using three tiers: A for the lightest packages, B for the middle range, and C up to the carrier's limit. Every weight the carrier accepts must fall in exactly one tier.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| Every accepted weight matches some tier | completeness | `check_TiersAreComplete`, `expect: unsat` |
| No weight matches two tiers | uniqueness | `check_TiersAreUnique`, `expect: unsat` |
| The rejected design can still be shown to overlap | witness | `check_RejectedDesignOverlapsAtTheBoundary`, `expect: sat` |

The third check does not describe the shipped tiers. It uses a variant of tier B whose upper bound is inclusive, the same weight tier C's lower bound names, so 2,000 g matches both. It shows the formula can still produce a counterexample when one exists.

## Run

```bash
fv-z3 shipping.py
fv-mutate shipping.mutations
```

Real output, from the pinned z3-solver 5.4.1:

```text
PASS check TiersAreComplete: unsat
PASS check TiersAreUnique: unsat
PASS check RejectedDesignOverlapsAtTheBoundary: sat
  w = 2000
```

## The counterexample, as the user reads it

```text
1. A package weighs 2,000 g.
2. Tier B's rejected bound, w <= 2,000, includes it.
3. Tier C's bound, w >= 2,000, also includes it.
4. The rejected design prices one package two ways.
```

## Bounds and limits

The checks cover every integer weight from 0 g to 30,000 g. `check_TiersAreComplete` and `check_TiersAreUnique` are linear integer arithmetic, so Z3 decides them exactly; this is not a bounded search over a scope.
