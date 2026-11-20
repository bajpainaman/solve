# Anti-pattern: reading `unknown` as a pass

**Symptom:** a hand-rolled check prints `PASS`, on a run where Z3 never decided the formula.

The rule under review is "no three discount multipliers cube-sum to the chargeback threshold of 114." Someone encoded the rule with cubic terms, `x**3 + y**3 + z**3 == 114`, which puts it in nonlinear integer arithmetic, a theory Z3 cannot always decide.

`naive_check.py` runs this formula directly with `python`, outside `fv-z3`, and reads the result with `if str(result) != "sat"`. Z3's real answer is `unknown`, with `timeout` as the reason, and the naive check treats that the same as `unsat`.

```text
PASS NoChargebackCombination: the combination is unreachable
```

`fixed_check.py` asks the same question through `fv-z3`, which never lets `unknown` stand in for a verdict:

```text
ERROR check NoChargebackCombination: z3 returned unknown (timeout)
```

## The fix

Route every check through `fv-z3`, which reports `unknown` as `ERROR` and never as `PASS` or `FAIL`. Then bound the theory: a linear reformulation of the rule, a bound on the multipliers, or a bit-vector encoding usually lets Z3 decide it.

## The check that catches it

`fv-z3` itself. Its `run_checks` function checks for the string `"unknown"` before comparing anything to the declared expectation, so a hand-rolled script that skips this step is the only place this anti-pattern can still reach a reader.
