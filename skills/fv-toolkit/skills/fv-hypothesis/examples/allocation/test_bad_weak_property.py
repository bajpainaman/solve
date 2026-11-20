"""BROKEN ON PURPOSE. See README.md, under "Weak property"."""
from hypothesis import given, settings, strategies as st

from allocate import allocate

totals = st.integers(min_value=0, max_value=10_000)
weights = st.lists(st.integers(min_value=1, max_value=20), min_size=1, max_size=6)


@settings(max_examples=300, derandomize=True, deadline=None)
@given(totals, weights)
def test_allocate_returns_one_part_per_line(total, ws):
    # The property checks the shape of the result and nothing about its values.
    assert len(allocate(total, ws)) == len(ws)
