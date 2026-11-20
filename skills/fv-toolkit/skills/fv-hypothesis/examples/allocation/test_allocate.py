"""Properties of allocate(). Each one states a rule from the function's docstring.

Source read at: 0000000
Covers: allocate.py
"""
from hypothesis import given, settings, strategies as st

from allocate import allocate

# The strategies produce exactly the inputs the function accepts: an amount
# that is not negative and at least one positive weight. Small weights make
# equal remainders common, which is where the tie rule matters.
totals = st.integers(min_value=0, max_value=10_000)
weights = st.lists(st.integers(min_value=1, max_value=20), min_size=1, max_size=6)
checked = settings(max_examples=300, derandomize=True, deadline=None)


@checked
@given(totals, weights)
def test_parts_sum_to_total(total, ws):
    """Conservation: no cent is created or lost."""
    assert sum(allocate(total, ws)) == total


@checked
@given(totals, weights)
def test_each_part_is_within_one_cent_of_its_share(total, ws):
    """Each part differs from its exact share by less than one cent."""
    whole = sum(ws)
    for weight, part in zip(ws, allocate(total, ws)):
        assert -whole < part * whole - total * weight < whole


@checked
@given(totals, weights, st.data())
def test_result_does_not_depend_on_line_order(total, ws, data):
    """Order independence: shuffling the lines moves the parts with them."""
    shuffled = data.draw(st.permutations(ws))
    assert sorted(zip(shuffled, allocate(total, shuffled))) == sorted(zip(ws, allocate(total, ws)))
