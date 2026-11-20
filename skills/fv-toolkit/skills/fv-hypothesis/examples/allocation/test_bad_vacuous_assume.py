"""BROKEN ON PURPOSE. See README.md, under "Vacuous filter"."""
from hypothesis import HealthCheck, assume, given, settings, strategies as st

from allocate import allocate

totals = st.integers(min_value=0, max_value=10_000)
weights = st.lists(st.integers(min_value=1, max_value=20), min_size=1, max_size=6)


# Hypothesis warned that the filter rejects most inputs, and the author silenced the warning.
@settings(max_examples=300, derandomize=True, deadline=None, suppress_health_check=list(HealthCheck))
@given(totals, weights)
def test_parts_sum_to_total(total, ws):
    # The filter keeps only amounts that divide evenly, so no cent is ever left over.
    assume(all(total * w % sum(ws) == 0 for w in ws))
    assert sum(allocate(total, ws)) == total
