"""BROKEN ON PURPOSE. See README.md, under "A fresh random seed with no pinned failure"."""
from hypothesis import example, given, settings, strategies as st

from subject import spend_bucket

totals = st.integers(min_value=0, max_value=999_999)


# BROKEN ON PURPOSE: no derandomize and no fixed seed. Each run draws its
# own 20 examples from a million-wide range, so whether the search happens
# to reach 500003 this run decides whether it fails. See README.md for runs
# that passed and runs that failed on this same, unmodified subject.py.
@settings(max_examples=20, deadline=None)
@given(totals)
def test_bucket_matches_integer_division(total):
    assert spend_bucket(total) == total // 10


# The fix: pin the known failing input with @example, so it runs on every
# invocation no matter what the random search draws or how big its budget is.
@example(500_003)
@settings(deadline=None)
@given(totals)
def test_bucket_matches_integer_division_pinned(total):
    assert spend_bucket(total) == total // 10
