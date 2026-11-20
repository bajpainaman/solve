---
name: fv-hypothesis
description: "Writes, reviews and debugs property-based and stateful tests with Hypothesis on real Python code: conservation, idempotence, order independence, round trips, comparison with a reference or an old implementation, and random call sequences against a simple model. Every property must fail on a planted bug in the code before it counts. Use for property-based testing, Hypothesis, @given, RuleBasedStateMachine, model-based or differential testing, \"is this right for every input\", or when the formal-verification skill routes here. Not for orderings between concurrent actors (use fv-tlaplus) or for the shape of data and permissions (use fv-alloy)."
---

# Property tests with Hypothesis

An example test asserts one point. A property asserts a rule over the whole input domain, and Hypothesis searches that domain for a counterexample and shrinks it. This is the cheapest rung of the escalation ladder, because it runs on the real code.

If you came here directly, run steps 1 to 3 of the `formal-verification` skill first. They produce the claims table and the confirmed property ledger.

Use the project's own test runner and its existing Hypothesis setup. When the project has no Hypothesis, adding it is a dependency decision that belongs to the user. Offer it once, with the property you would write, and accept either answer.

## Five rules

1. **Test only what the code claims.** A property comes from a docstring, a comment, a type, the way callers use the result, or the confirmed ledger. A property that you only believe to be true produces false alarms.
2. **Assert the strongest property that the code supports.** From weakest to strongest: no crash, the shape of the result, an invariant, idempotence, then a round trip or a comparison with a reference. A test that checks only the length of a result passes on almost every bug.
3. **Build the constraint into the strategy.** Read the callers to learn which inputs the code really receives, and generate exactly those. Prefer a strategy that is sound and misses a few valid inputs over one that produces inputs the code never sees. An `assume` that rejects most inputs leaves the test with nothing interesting.
4. **Every property must fail on a planted bug.** Write a `.mutations` file that edits the code under test, and run `fv-mutate`. A property that stays green on every planted bug checks nothing.
5. **Make failures repeatable.** Use `derandomize=True` in CI, and pin each failure that Hypothesis finds with `@example(...)`, so that the case stays in the suite.

## From a property family to a test

| Family | Shape of the test |
|---|---|
| Conservation | `sum(parts) == total`, or rows in equal rows out plus rows rejected |
| Idempotence | `f(f(x)) == f(x)`; running a job twice equals running it once |
| Order independence | The result for a shuffled input equals the result for the input, compared as a multiset |
| Round trip | `decode(encode(x)) == x`; `reload(save(x)) == x` |
| Oracle equivalence | `fast(x) == simple(x)`; streaming equals batch; incremental equals full recompute; new code equals old code on shared fields |
| Invariant over a sequence | A `RuleBasedStateMachine` with one `@invariant` per rule that must hold after every call |
| Model equivalence | A `RuleBasedStateMachine` whose rules call the real object and a plain model, and compare after every step |
| Metamorphic | Adding a filter never adds results; scaling the input scales the output |
| Monotonicity | A later version, offset or watermark is never smaller than an earlier one |

For a finite decision function, enumerate every input through the real entry point with `pytest.mark.parametrize` over `itertools.product`. That check is exhaustive, and it needs no strategy.

## A reference implementation

When no simpler implementation exists, write the reference from the rule: the contract, the law or the specification that the code implements.

- Take every choice in the reference from the text of the rule. Never take one from the code under review, its comments or its tests. A reference that copies the code's logic is the code again.
- When the rule has two readings, write two references and say which finding needs which reading.
- Pin each boundary by hand with `@example`: the date or the value where the outcome flips, a value equal to a limit, an empty input.
- Run the comparison on a version that you know is right. Each difference that remains is an error in the reference or a second defect.

## Stateful tests

A `RuleBasedStateMachine` draws random sequences of calls. Each `@rule` calls one operation on the real object and the same operation on a model. The model is a dict or a list that is slow and plainly right. Compare inside the rule, and put what must always hold in `@invariant` methods. Use a small key space, so that collisions, overwrites and evictions happen often. `examples/lru-cache/` is the pattern to copy.

## Workflow

1. **Find the properties.** Read the function, its docstring and its callers. Write each property as one sentence, with the place that claims it.
2. **Write the strategies** from the input domain that the callers use.
3. **Write one property, then run it.** Use the project's runner. Read a failure as step 5 describes before you change anything.
4. **Plant bugs.** Put a `.mutations` file beside the tests. Its `run` line calls the test runner, and its `file` line names the code under test. Set `root` when the code and the tests are in different directories.

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-mutate <name>.mutations
   ```

5. **Judge each failure.** Ask three questions in order.
   - Does the shrunk input reproduce the failure in a standalone script?
   - Does a real caller produce this input? If every caller validates first, the strategy is too wide.
   - Does the code claim the property? If not, the property is wrong.

   A failure that passes all three is a bug. Report the shrunk input, the standalone script and the claim it breaks, and add the input as an `@example`.
6. **Record the sync point.** Put `Source read at:` and `Covers:` in the docstring of the test module, so that `fv-drift` can report when the code has moved.

## What a pass means

A pass means that the stated number of generated inputs satisfied the property. It is a search and not an exhaustive check. Say the number of examples, the strategy bounds, and whether the mutations were detected.

## Examples

`examples/INDEX.md` lists every example. `examples/allocation/` puts one test file that detects every planted bug beside three test files that detect none. Read it before you write your first property. `examples/checkout-ledger/` reproduces three more ways a property test misleads: a mocked collaborator, a property that the code never claims, and a seed that is not pinned.

## References

| File | Read when |
|---|---|
| `references/anti-patterns.md` | You review property tests, yours or someone else's |
| `${CLAUDE_PLUGIN_ROOT}/references/bite.md` | You write the mutations file |
| `${CLAUDE_PLUGIN_ROOT}/references/setup.md` | Hypothesis is missing, or you need the CI profile |
