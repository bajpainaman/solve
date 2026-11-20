"""BROKEN ON PURPOSE. See README.md, under "Tautology"."""
from hypothesis import given, settings, strategies as st

from allocate import allocate

totals = st.integers(min_value=0, max_value=10_000)
weights = st.lists(st.integers(min_value=1, max_value=20), min_size=1, max_size=6)


@settings(max_examples=300, derandomize=True, deadline=None)
@given(totals, weights)
def test_parts_sum(total, ws):
    parts = allocate(total, ws)
    # Both sides come from the function under test, so no bug in it can fail this.
    assert sum(parts) == sum(allocate(total, ws))
