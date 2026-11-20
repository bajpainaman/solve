---
name: test-unit
description: "Writes unit tests for pure logic from the spec: calculations, parsing, validation, business rules and state machines. Each test states one behaviour, takes its expected value from the docstring, ticket or README, and is kept only after it fails on a planted bug. Use for unit tests, pytest, Vitest, Jest, JUnit, go test or cargo test on a function or class, for a regression test of a logic bug, or when the testing skill routes here. Not for code whose bugs are at a database, queue or HTTP boundary (use test-integration), and not for rules over a large input space (use test-property)."
---

# Unit tests

A unit test checks one behaviour of pure logic and runs in milliseconds. It is worth its place only when the expected value came from the spec and the test can fail.

Follow `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` for every test. This file adds the rules that are specific to unit tests.

| Python | TypeScript / JS | JVM | Go | Rust |
|---|---|---|---|---|
| pytest | Vitest, Jest | JUnit 5 | `testing` + testify | `cargo test`, nextest |

Use the runner, the layout and the naming that the repo already has.

## Five rules

1. **Assert behaviour from the spec.** Write each expected value from the docstring, the ticket or the README before you read the function body. Never copy a value from the code's output.
2. **One behaviour per test, named after it.** `test_discount_applies_at_ten_items` tells the reader what broke. `test_calculate_2` does not.
3. **Test each rule at its boundary.** For a rule such as "10 or more", test 9, 10 and 11. Most logic bugs are a wrong comparison or an off-by-one error at the value where the outcome changes.
4. **Mock only true boundaries.** The clock, the network and randomness are boundaries. A collaborator in the same module is not one, so use the real object.
5. **Extend a table before you add a test.** When a new case checks the same contract with different inputs, add a row to the parametrized test.

## Reject the test if

- It asserts that a mock was called with whatever the code passes.
- Its expected value is computed by the code under test or restates the implementation.
- It still passes after you plant the bug it claims to catch.

## Workflow

1. **List the behaviours.** Read the spec and write one line per behaviour, with the sentence that claims it. Add the boundaries of each rule.
2. **Apply step 0** of assured generation to each line. Drop the lines that an existing test already owns.
3. **Write the tests**, then read the implementation for names and signatures.
4. **Run them.** A test that fails because the code disagrees with the spec is a finding. Keep its assertion and report it.
5. **Check for flakiness and value**, as steps 3 and 4 of assured generation describe. Plant each bug, see the test fail, and restore the code.
6. **Report** with the table from step 6 of assured generation.

## The report

End your reply with this table, even when you wrote one test. The user reads it to decide whether each row earns its place.

| Test | Contract it protects | Bug that would make it fail | Evidence |
|---|---|---|---|

In the last column, write what you saw: a planted bug that made it fail, a failing run on the current code, or "not run". Under the table, list each finding, each step that did not run and why, and the command that runs everything.

## Example

The spec says: "Orders of 10 or more items get 10% off."

```python
# Bad. The expected value comes from the function under test, and the mock
# assertion repeats the call. Neither line can fail on a wrong discount rule.
def test_total(mocker):
    rates = mocker.patch("shop.pricing.load_rates", return_value={"bulk": 0.1})
    assert total(items(10)) == total(items(10))
    rates.assert_called_once_with()
```

```python
# Good. The values come from the spec, and the rows sit on the boundary.
@pytest.mark.parametrize(
    ("quantity", "expected_cents"),
    [(9, 900), (10, 900), (11, 990)],  # 9 pay full price; 10 and 11 get 10% off
)
def test_bulk_discount_starts_at_ten_items(quantity, expected_cents):
    assert total(items(quantity, unit_cents=100)) == expected_cents
```

Planting `quantity > 10` in the code makes the second row fail, which is the evidence for the report.

## References

| File | Read when |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` | Always, before the first test |
| `${CLAUDE_PLUGIN_ROOT}/references/anti-patterns.md` | Before you show the tests |
