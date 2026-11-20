"""BROKEN ON PURPOSE. See README.md, under "A mock in place of the real collaborator"."""
from unittest.mock import MagicMock

from hypothesis import given, settings, strategies as st

from subject import checkout

totals = st.integers(min_value=0, max_value=10_000)


@settings(max_examples=200, derandomize=True, deadline=None)
@given(totals)
def test_checkout_charges_the_cart_total(total):
    ledger = MagicMock()
    checkout(ledger, total)
    # The property checks that the mock recorded a call with this argument.
    # It never runs the real Ledger.charge, so nothing Ledger.charge does
    # with that argument is exercised.
    ledger.charge.assert_called_once_with(total)
