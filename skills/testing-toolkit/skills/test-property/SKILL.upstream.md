---
name: test-property
description: "Writes property-based, metamorphic and differential tests for code with a large input space: round trips, idempotence, ordering, conservation, invariants over call sequences, and old code against new code. Builds constraints into the generators, pins every found failure as an explicit example, and fixes the seed in CI. Use for property-based tests, Hypothesis, fast-check, jqwik, rapid, proptest, \"test this for all inputs\", metamorphic or differential testing, stateful testing, or when the testing skill routes here. Not for a handful of spec examples (use test-unit) or for raw untrusted bytes (use test-fuzz)."
---

# Property tests

An example test checks one input. A property states a rule that holds for every input, and the library searches the input space for a counterexample and shrinks it. Use a property where the code has an invariant and the inputs are too many to list.

Follow `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` for every test. This file adds the rules that are specific to property tests. When the fv-toolkit plugin is installed, its `fv-hypothesis` skill holds a longer library of property families.

| Python | TypeScript / JS | JVM | Go | Rust |
|---|---|---|---|---|
| Hypothesis | fast-check | jqwik | rapid, gopter | proptest |

## Five rules

1. **Assert the strongest property the spec supports.** From weakest to strongest: no crash, the shape of the result, an invariant, idempotence, then a round trip or a comparison with a reference. "It does not raise" passes on almost every bug.
2. **Build the constraint into the generator.** Generate only valid inputs. A filter such as `assume()` that rejects many inputs leaves the test with little to run.
3. **Use a stateful test for an API with state.** Draw random sequences of calls against the real object and a plain model, and compare after every step.
4. **Pin every failure the library finds.** Add the shrunk input as an explicit example, so that the case stays in the suite.
5. **Make CI runs repeatable.** Fix the seed or derandomise in CI. Run a short profile on the PR and a long one nightly.

## Reject the test if

- Its only property is that the code does not crash.
- The generator discards more than half of its inputs.
- The property recomputes the expected value with the same logic as the code under test.

## Property families

| Family | Shape |
|---|---|
| Round trip | `decode(encode(x)) == x` |
| Idempotence | `f(f(x)) == f(x)` |
| Conservation | The parts sum to the total. Rows in equal rows out plus rows rejected. |
| Order independence | A shuffled input gives the same result |
| Invariant | The output is sorted, within bounds, unique, or never negative |
| Metamorphic | A known change to the input gives a known change to the output. Adding a filter never adds results. |
| Differential | The new code equals the old code, or the fast code equals a simple reference |
| Stateful | A random sequence of calls keeps the real object equal to a model |

## Workflow

1. **Find the properties in the spec.** Write each one as a sentence with the place that claims it.
2. **Apply step 0** of assured generation. Name the bug each property would catch.
3. **Write the generators** from the inputs real callers send.
4. **Write one property and run it.** Check the library's statistics for discarded inputs.
5. **Judge each failure.** Reproduce it from the shrunk input. Ask whether a real caller can send that input, and whether the spec claims the property. A failure that passes both questions is a bug, so report it and pin the input.
6. **Plant bugs**, as step 4 of assured generation describes. A property that passes on every planted bug checks nothing.
7. **Report** with the table from step 6 of assured generation, plus the number of examples and the generator bounds.

## The report

End your reply with this table, even when you wrote one property. The user reads it to decide whether each row earns its place.

| Property | Rule it protects | Bug that would make it fail | Evidence |
|---|---|---|---|

In the last column, write what you saw: a planted bug that made it fail, a failing run on the current code, or "not run". Under the table, list each finding, each step that did not run and why, and the command that runs everything.

## Example

```python
# Bad. The only property is "no exception", and assume() discards most inputs.
@given(st.text())
def test_parse_never_crashes(s):
    assume(s.count(",") == 2 and s.isascii())
    parse_row(s)
```

```python
# Good. The generator builds valid rows, the property is a round trip, and
# the failure Hypothesis once found is pinned.
fields = st.text(alphabet=st.characters(blacklist_categories=("Cs",)), max_size=20)

@given(st.lists(fields, min_size=1, max_size=5))
@example(['a,b'])  # a field that holds the delimiter
def test_formatting_a_row_and_parsing_it_returns_the_same_fields(row):
    assert parse_row(format_row(row)) == row
```

```python
# CI profile, in conftest.py
settings.register_profile("ci", derandomize=True, max_examples=200)
```

## References

| File | Read when |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` | Always, before the first test |
| `${CLAUDE_PLUGIN_ROOT}/references/pipeline.md` | You set the PR and nightly profiles |
