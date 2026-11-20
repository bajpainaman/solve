# Anti-pattern: a SYMMETRY set used with a liveness property

**Symptom:** TLC reports a violation of the liveness property, and the counterexample it prints is not a behaviour the fair spec actually allows.

Three processes pass a token to any other process. `WF_holder(Pass)` is declared, and `Pass` is always enabled (there are always two other processes to hand the token to), so no behaviour of `FairSpec` may stutter forever. Checked without `SYMMETRY`, TLC 1.7.4 finds the real violation: two processes pass the token back and forth and starve the third.

```text
PASS NoSymmetry.cfg: liveness (properties: EveryoneEventuallyHolds) (3 distinct states)
  1. Initial: holder = p2
  2. Pass: holder: p2 -> p3
  The behaviour then returns to state 1 and repeats.
```

Checked with `SYMMETRY Symm`, where `Symm == Permutations(Procs)`, TLC 1.7.4 also reports a violation, with a different, smaller counterexample:

```text
PASS WithSymmetry.cfg: liveness (properties: EveryoneEventuallyHolds) (1 distinct states)
  1. Initial: holder = p1
  2. Stuttering: no variable changed
```

This trace is not a behaviour of `FairSpec`. `Pass` is enabled in every state reachable from `Init`, so `WF_holder(Pass)` forbids a behaviour that stutters forever at `holder = p1`. TLC found a counterexample that the fair spec does not actually have. Both runs end the same way, as a violation that `fv-tlc` reports as `PASS` against an `expect: liveness` header, because both commands got the outcome the header declares. The header on `WithSymmetry.cfg` is declaring a known-wrong result, not a correct one, which is the point of shipping it.

TLC does not warn or error when `SYMMETRY` and a temporal `PROPERTY` are both present in the same config. It runs, finishes, and prints a result exactly as if the combination were sound.

## Why it is wrong

The symmetry reduction collapses states that are equivalent under a permutation of `Procs` into one representative. The liveness check, which TLC implements by searching for a cycle (a "lasso") in the state graph that violates the property, runs over the reduced graph. A lasso in the reduced graph does not always correspond to a real lasso in the full graph, because the permutation that identifies two states can differ from the permutation that identifies their successors. TLC's own documentation states that a `SYMMETRY` set makes liveness checking unsound for exactly this reason. This run shows the concrete shape of that unsoundness: a counterexample that violates the spec's own fairness condition.

## The fix

Use `SYMMETRY` only on a config whose `PROPERTY` line is absent, that is, on a safety-only check with only an `INVARIANT`. Check liveness properties, such as `EveryoneEventuallyHolds`, in a config with no `SYMMETRY` line, as `NoSymmetry.cfg` does here.

## The check that catches it

No mechanical check in this repository catches a `SYMMETRY` set combined with a `PROPERTY` line, because the config both parses and produces a result that satisfies its own declared `expect` header. The two configs here have to be compared by a reader: a liveness counterexample that violates the very fairness condition the config declares is the sign that symmetry, not the design, produced it.
