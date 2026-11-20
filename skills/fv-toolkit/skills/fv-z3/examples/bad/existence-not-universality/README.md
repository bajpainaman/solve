# Anti-pattern: checking that the claim can be true, not that it always is

**Symptom:** `check_SomeWeightMatchesATier` passes even though the table has a real gap.

`tiers_with_a_gap.py` is the same shipping tiers as `examples/good/shipping-tiers/`, with tier B narrowed to stop at 1,900 g while tier C still starts at 2,000 g. No tier covers a package between 1,900 g and 2,000 g.

The wrong check asserts the claim itself, `Or(tier_a(w), tier_b(w), tier_c(w))`, and declares `expect: sat`. Z3 finds a weight that matches some tier, because almost every weight does, and the check passes. It never asked whether every weight matches one.

```text
PASS check SomeWeightMatchesATier: sat
  w = 24712
FAIL check EveryWeightMatchesATier: expected unsat, got sat
  w = 1900
```

The second check in the same file, `check_EveryWeightMatchesATier`, asserts the negation, `Not(Or(...))`, and declares `expect: unsat`. It finds the gap at 1,900 g on the same real run.

## The fix

For a claim meant to hold over the whole domain, assert its negation and expect `unsat`. Asserting the claim and expecting `sat` only shows the claim can be true somewhere, which is true of nearly every rule that was not written to always be false.

## The check that catches it

None, mechanically. `fv-z3` reports exactly what the check file asks it to report; a check that asks the wrong question gets a correct answer to that wrong question. Review every `expect: sat` on a claim and ask whether the claim was meant to hold for some input or for all of them.
