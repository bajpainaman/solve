# Allocation: one test file that bites and three that do not

**Pattern:** money and rounding, pricing and fee calculation (catalog F3).
**Teaches:** conservation, a bound on each part, order independence, and three ways a property test passes while it checks nothing.

## The code

`allocate(total, weights)` splits an amount of cents across weighted lines. Its docstring makes three claims: the parts sum to the total, each part is its exact share rounded to a neighbouring cent, and the result does not depend on the order of the lines.

## The good test file

`test_allocate.py` has one property per claim.

| Property | Family | Claim |
|---|---|---|
| `test_parts_sum_to_total` | conservation | No cent is created or lost |
| `test_each_part_is_within_one_cent_of_its_share` | invariant | Each part differs from its exact share by less than one cent |
| `test_result_does_not_depend_on_line_order` | order independence | Shuffling the lines moves the parts with them |

`allocate.mutations` plants three bugs in `allocate.py`, and each property catches the bug aimed at it:

```text
DETECTED the leftover cents are dropped: FAILED test_allocate.py::test_parts_sum_to_total - assert 0 == 1
DETECTED every leftover cent goes to the first line: FAILED test_allocate.py::test_each_part_is_within_one_cent_of_its_share
DETECTED a tie goes to the earlier line: FAILED test_allocate.py::test_result_does_not_depend_on_line_order
GREEN the error message is reworded
SUMMARY detected=3 missed=0 error=0 green=1 brittle=0 uncovered=0
```

The third bug changes who gets a cent when two lines have equal remainders. The totals still match, so only the order property sees it.

## The three bad test files

Each file passes on the correct code. Each one also passes on the planted bugs, and `fv-mutate` reports that.

### Tautology

`test_bad_tautology.py` asserts `sum(parts) == sum(allocate(total, ws))`. Both sides come from the function under test, so no bug in the function can make them differ.

```text
MISSED the leftover cents are dropped
```

**Fix:** compare the result with something the function did not compute, such as the input `total`.

### Vacuous filter

`test_bad_vacuous_assume.py` has the right assertion behind an `assume` that keeps only amounts that divide evenly. No cent is ever left over in those cases, so the code that distributes leftover cents never runs. Hypothesis warned that the filter rejects most inputs, and the test silences the warning.

```text
300 passing, 0 failing, and 1138 invalid test cases
MISSED the leftover cents are dropped
```

**Fix:** remove the filter. When a constraint is real, build it into the strategy, and never silence the `filter_too_much` health check.

### Weak property

`test_bad_weak_property.py` asserts only that the result has one part per line.

```text
MISSED the leftover cents are dropped
MISSED every leftover cent goes to the first line
MISSED a tie goes to the earlier line
```

**Fix:** assert the strongest property that the docstring claims.

## Run

```bash
python -m pytest -q test_allocate.py
fv-mutate allocate.mutations
fv-mutate bad_tautology.mutations        # exits 1 and prints MISSED
```

## Bounds and limits

Each property runs 300 generated inputs, with totals up to 10,000 cents, up to six lines and weights from 1 to 20. The run is a search. It is not an exhaustive check.
