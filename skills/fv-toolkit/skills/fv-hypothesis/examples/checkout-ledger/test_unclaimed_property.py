"""BROKEN ON PURPOSE. See README.md, under "A property the code never claims"."""
from hypothesis import given, settings, strategies as st

from subject import apply_loyalty_discount

prices = st.integers(min_value=0, max_value=10_000)
points = st.integers(min_value=0, max_value=10_000)


@settings(max_examples=200, derandomize=True, deadline=None)
@given(prices, points)
def test_discount_never_exceeds_ten_percent(price_cents, pts):
    # Nothing in apply_loyalty_discount's docstring bounds the discount to
    # 10% of the price. A customer with enough points reaches a price of
    # zero, and the docstring says that is correct, not a bug.
    result = apply_loyalty_discount(price_cents, pts)
    assert result >= price_cents * 0.9
