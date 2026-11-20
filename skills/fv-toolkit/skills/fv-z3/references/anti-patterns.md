# Z3 anti-patterns

Each row is a way a check passes while it proves nothing, with the symptom and the fix.

| Anti-pattern | Symptom | Fix / check |
|---|---|---|
| Checking the claim instead of its negation | `expect: sat` passes on almost any non-degenerate rule, because some input satisfies it; a real gap or overlap stays hidden | Assert the negation and `expect: unsat`. See `examples/bad/existence-not-universality/` |
| Nonlinear arithmetic or a heavy quantifier | Z3 returns `unknown`; a naive script treats "not sat" or "not unsat" as a pass | `fv-z3` reports `unknown` as `ERROR`. Bound the theory: linear arithmetic, bit-vectors, or a smaller domain. See `examples/bad/unknown-read-as-pass/` |
| Contradictory domain constraints | Every `check` is `unsat`, including one that states something false, because no input satisfies the setup at all | Add a `check_<Name>` with `expect: sat` that only asserts the domain constraints, and confirm it finds a model |
| Expecting Z3 to prove an inductive fact | A check over an unbounded recursive structure times out or returns `unknown` on every run | Supply the induction yourself, or move the claim to Dafny or Lean |
| `expect:` left behind after the rule changed | The check still declares the old expectation, so a real regression shows as `FAIL` and gets explained away instead of fixed | Treat `FAIL` on a check whose rule did not change as a sign the `expect:` line is the wrong one, not the code |
