# Checkout ledger: three ways a property test passes while it checks nothing

**Pattern:** money and rounding, pricing and fee calculation (catalog F3).
**Teaches:** three more ways a Hypothesis property can pass without finding a real bug, beyond the three `examples/allocation/` already shows.

## The code

`subject.py` holds a small checkout ledger: a `Ledger` class that charges a running balance, `apply_loyalty_discount`, and `spend_bucket`. `spend_bucket` carries a real planted bug: it is wrong only when its input is exactly `500_003`.

## A mock in place of the real collaborator

`test_mocked_ledger.py` calls `checkout(ledger, total)` with a `MagicMock` standing in for `Ledger`, then asserts that the mock recorded a call with the right argument. `checkout` never touches the real `Ledger.charge`, so nothing that method does is exercised.

`mocked_ledger.mutations` plants a bug in the real `Ledger.charge` (it charges double). Because the test never runs the real class, the bug is missed:

```text
MISSED the real ledger charges double the amount
```

**Fix:** pass a real `Ledger()` and assert on its resulting `balance`, or run the same property against both the real class and a fake, and compare.

## A property the code never claims

`test_unclaimed_property.py` asserts that `apply_loyalty_discount` never discounts by more than 10%. Nothing in the function's docstring says that: a customer with enough loyalty points can reach a price of zero, and the docstring says that is correct. The invented bound fails on the correct, unmodified code:

```text
E       assert 0 >= (1 * 0.9)
E       Failing test case: test_discount_never_exceeds_ten_percent(
E           price_cents=1,
E           pts=1,
E       )
FAILED .../test_unclaimed_property.py::test_discount_never_exceeds_ten_percent
```

**Fix:** write the property from the docstring's own claim, `max(0, price_cents - points)`, not from an assumption about the business that the code never made.

## A fresh random seed with no pinned failure

`test_flaky_seed.py`'s first test, `test_bucket_matches_integer_division`, checks `spend_bucket(n) == n // 10` over `st.integers(0, 999_999)`, with `max_examples=20` and no `derandomize`. `spend_bucket` is wrong only at `500_003`, one point out of a million, so whether 20 random examples happen to reach it varies run to run. Six runs on the same, unmodified `subject.py`:

```text
run 1:  1 failed, 1 passed
run 2:  2 failed
run 3:  2 failed
run 4:  2 failed
run 5:  2 failed
run 6:  1 failed, 1 passed
```

Runs 1 and 6 show `test_bucket_matches_integer_division` passing; every other run shows it failing. The same suite, the same code, run to run, with no seed pinned.

**Fix:** `@example(500_003)` on `test_bucket_matches_integer_division_pinned` forces that input on every run, regardless of what the random search draws or how small its budget is. All six runs above show it failing every time, in the `2 failed` and `1 failed, 1 passed` lines alike. `derandomize=True` on the first test would have the same effect for the general case: a fixed seed means the examples drawn, and so whether they reach `500_003`, are the same on every run, not that the search is guaranteed to reach a given input. Pinning the exact input with `@example` is the stronger fix once a failing input is known. A `max_examples` large enough that this specific search always reaches `500_003` anyway would hide this lesson, not teach it: a wider net catching a planted bug is not the same as a seed making the catch reproducible.

## Run

```bash
uv run --with hypothesis --with pytest fv-mutate mocked_ledger.mutations
uv run --with hypothesis --with pytest python -m pytest -q test_unclaimed_property.py
uv run --with hypothesis --with pytest python -m pytest -q test_flaky_seed.py
```

## Bounds and limits

`tests/examples.d/hypothesis.sh` checks the mocked-ledger mutation and the unclaimed property directly, and checks only the pinned test from `test_flaky_seed.py`, because `test_bucket_matches_integer_division`'s own result is not reproducible by design. Its variation across runs is the lesson, not a result to assert on.
