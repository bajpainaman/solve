"""Differential test: Allocate.dfy, compiled to Python, against reference.py.

Source read at: 0000000
Covers: billing/split.py

Allocate-py/ is the output of:
  dafny build --solver-path=<z3> --allow-warnings --target:py Allocate.dfy
Regenerate it after any change to Allocate.dfy.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "Allocate-py"))

from hypothesis import given, settings, strategies as st

import Allocate
from reference import split_reference

totals = st.integers(min_value=0, max_value=10_000)
ns = st.integers(min_value=1, max_value=20)
checked = settings(max_examples=300, derandomize=True, deadline=None)


@checked
@given(totals, ns)
def test_dafny_matches_reference(total, n):
    """Oracle equivalence: the verified core and the hand-written one agree."""
    assert list(Allocate.default__.Split(total, n)) == split_reference(total, n)
