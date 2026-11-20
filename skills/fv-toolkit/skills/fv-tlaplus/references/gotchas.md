# TLC gotchas

## Measured on TLC 1.7.4

Each fact below was reproduced with this plugin's examples or its test fixtures.

| Fact | Consequence |
|---|---|
| TLC exits 0 for no error, 12 for a violated invariant, 13 for a violated temporal property, 11 for a deadlock and 150 for a parse error | `fv-tlc` reads the exit code. A parse error prints `ERROR`, so a broken spec never satisfies a config that expects a violation |
| A liveness property on a spec with no fairness fails with a trace that ends in "Stuttering" | The failure says nothing about the design. Add the fairness that the code provides. See `../examples/bad/liveness-without-fairness/` |
| Deadlock checking is on by default, and a correct end state counts as a deadlock | Give the end state a `Done` action. Use `CHECK_DEADLOCK FALSE` only for a model that is meant to stop anywhere |
| The `-deadlock` command-line flag switches deadlock checking off | `fv-tlc` never passes it. Put the choice in the config, where a reader sees it |
| TLC does not say which temporal property failed | `fv-tlc` lists every property of the config. Put one temporal property in a config when you must know |
| TLC stops at the first violated invariant | A config for a rejected design checks only the invariant that design threatens |
| A property holds when the state it talks about is unreachable | Add a witness config. See `../examples/bad/unreachable-state/` |
| A trace of a spec with one variable has no leading `/\` | `fv-tlc --trace` handles both forms |
| TLC unpacks its standard modules into the Java temp directory, and two runs that start together can fail with "File does not exist: .../Naturals.tla" | `fv-tlc` gives each run its own temp directory. Do the same when you call TLC directly: `-Djava.io.tmpdir=<private dir>` |
| `x \in Nat` stops TLC with an error when `x` is not a number, and so does `=` between an integer and a string | Keep one type per variable. `../examples/good/cache-invalidation/` uses a flag and a number for an entry that may be absent |
| `SYMMETRY` in a config takes the name of an operator, and `SYMMETRY Permutations(Procs)` is a parse error | Define `Symm == Permutations(Procs)` in the module and write `SYMMETRY Symm` |
| TLC accepts `SYMMETRY` together with a liveness `PROPERTY` and prints no warning | The result can be wrong. Use symmetry for safety only. See `../examples/bad/symmetry-with-liveness/` |
| A violated action property such as `[][x' >= x]_x` exits 13, as a liveness violation does | `fv-tlc` reports it as `liveness`, so the config declares `expect: liveness`. See `../examples/bad/invariants-only/` |
| An unbounded counter makes TLC run without end and print no verdict | Bound it with a constant or a `CONSTRAINT`, and name the bound in the report. See `../examples/bad/unbounded-state/` |
| A config comment starts with `\*` | The `\* expect:` header is a comment to TLC |
| In a config, a set of model values is `Jobs = {a, b}` and a string needs quotes, as in `Order = "one_txn"` | An unquoted word is a model value, and it never equals a string in the spec |

## From the TLC documentation, not reproduced here

- Simulation mode, `-simulate`, samples behaviours and does not detect deadlocks. Use the default breadth-first mode for a verdict.
- A `CONSTRAINT` removes behaviours from the search. List each one in the report with the behaviour it excludes.

## A symptom and where to look first

| Symptom | Look at |
|---|---|
| A config passes and you expected a violation | The atomicity of the actions, then a missing witness |
| A witness config fails | A guard that is never true, a constant that is too small, a `CONSTRAINT` |
| Liveness fails on a stuttering trace | The spec has no fairness on the step that should progress |
| Liveness holds and you doubt it | Fairness that is stronger than the code provides. Remove the progress step with a mutation and confirm that the property fails |
| TLC reports a deadlock in a correct end state | The end state has no `Done` action |
| TLC does not finish | An unbounded variable, or constants that are too large |
| Two values that look equal compare unequal | A model value in the config against a string in the spec |
