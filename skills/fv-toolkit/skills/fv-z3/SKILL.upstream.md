---
name: fv-z3
description: "Encodes a rule table, a policy, or a config invariant as a Z3 SMT formula and asks whether a violation exists. Covers decision-table completeness and uniqueness, policy containment ('does the new policy allow anything the old one denied'), promotion and cap arithmetic, and other constraints over numbers, booleans and small enumerations. Every check pairs a claim with a rejected design that must produce a counterexample, and z3's `unknown` is never read as a pass. Use for rule tables, eligibility and pricing formulas, policy diffs, or when the formal-verification skill routes here. Not for relations and permissions with many objects (use fv-alloy) or for orderings over time (use fv-tlaplus)."
---

# Z3

Z3 is an SMT solver: given a formula over integers, reals, booleans and bounded bit-vectors, it answers `sat` with a satisfying model, `unsat` with a proof that none exists, or `unknown` when the theory in play defeats its decision procedures. Use it when the risk lives in a formula, not in a web of relations: a rule table with a gap, a policy that grew wider than the one it replaced, a cap that a combination of inputs can exceed.

If you came here directly, run steps 1 to 3 of the `formal-verification` skill first. They produce the claims table and the confirmed property ledger.

## Five rules

1. **Check the negation, not the claim.** To show a rule holds for every input, assert its negation and expect `unsat`. Asserting the claim itself and expecting `sat` only shows some input satisfies it, which is true of almost any non-degenerate rule.
2. **`unknown` is never a pass or a fail.** Nonlinear arithmetic and heavy quantifiers can defeat Z3's decision procedures. `fv-z3` always reports `unknown` as `ERROR`, with the reason Z3 gives.
3. **Pair every check that must hold with a witness that must find something.** A check whose constraints are already contradictory is `unsat` no matter what it claims. A rejected design, checked `expect: sat` beside it, shows the formula can still produce a counterexample.
4. **Keep the theory decidable.** Prefer linear arithmetic and bounded integers. A cubic or exponential term, or a quantifier over an unbounded sort, is the usual cause of an `unknown`.
5. **Put the expectation in the check itself.** Write `expect: sat` or `expect: unsat` in the function's own docstring, so a reader sees what counts as a pass without a second file.

## Files to write

| File | Holds |
|---|---|
| `<name>.py` | The check file. Each `check_<Name>` function takes no arguments, returns a `z3.Solver` with its constraints added, and its docstring carries `expect: sat` or `expect: unsat`. The module's top docstring carries `Source read at:` and `Covers:` |
| `<name>.mutations` | The planted bugs, as `${CLAUDE_PLUGIN_ROOT}/references/bite.md` describes |
| `README.md` | The property ledger, the command table, the bounds and limits |

Copy `examples/good/shipping-tiers/` to start.

## Workflow

1. **Write one `check_<Name>` function per claim.** Build the `Solver` from predicates the way the policy or the table states them, not from the code under review.
2. **Add the rejected design beside it**, as a second `check_<Name>` with `expect: sat`, built from a design you know is wrong.
3. **Run it.**

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-z3 <name>.py
   ```

4. **Plant bugs.**

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-mutate <name>.mutations
   ```

5. **Read each counterexample back into the system.** A `sat` result on an unexpected check prints the model below the line; map each variable back to the field or request it represents.

## Reading the output

| Line | Meaning |
|---|---|
| `PASS check X: unsat` | No input satisfies the negation; the claim holds everywhere in the theory Z3 decided |
| `PASS check X: sat` | The check declared `expect: sat`, and Z3 found a satisfying model |
| `FAIL check X: expected unsat, got sat` | A counterexample exists. It is printed below the line |
| `FAIL check X: expected sat, got unsat` | The rejected design no longer produces the state it is meant to witness |
| `ERROR check X: z3 returned unknown (...)` | Z3 could not decide the formula. This is never a pass |
| `ERROR check X: ...` | The function has no `expect:` line, or it raised while building the `Solver` |
| `ERROR <file>: ...` | The file has no `check_*` function, or it failed to import. This is never the violation a check expects |
| `UNAVAILABLE z3: ...` | `uv` or the pinned `z3-solver` is missing |

## Telling a counterexample

Rewrite the model Z3 prints as numbered sentences in the system's own words:

```text
1. A request names region 2 (global) and action 0 (read).
2. The new policy allows it: region is in {0, 2} and action is read.
3. The old policy never named region 2, so it denies the same request.
4. The new policy therefore allows a request the old one denied.
```

## What a pass means

A theory Z3 can fully decide, such as linear integer arithmetic or fixed-width bit-vectors, makes `unsat` a proof over the whole domain of the formula, not a search bounded to a scope. A theory it cannot fully decide, such as general nonlinear arithmetic, can still return `sat` or `unsat` on many instances, but a `pass` from `fv-z3` always states which of the two happened; it never lets `unknown` stand in for either.

## Examples

`examples/INDEX.md` lists every example. `examples/good/shipping-tiers/` checks a decision table for completeness and uniqueness. `examples/good/policy-containment/` checks that a tightened policy allows nothing the old one denied. `examples/bad/existence-not-universality/` and `examples/bad/unknown-read-as-pass/` reproduce the two anti-patterns rule 1 and rule 2 above guard against.

## References

| File | Read when |
|---|---|
| `references/anti-patterns.md` | You review a Z3 check, yours or someone else's |
| `${CLAUDE_PLUGIN_ROOT}/references/bite.md` | You write the mutations file |
