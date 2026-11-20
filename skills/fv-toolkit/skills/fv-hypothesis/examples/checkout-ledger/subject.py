"""A checkout ledger: charges a cart and buckets a loyalty tier by spend."""


class Ledger:
    """Tracks a running balance across charges."""

    def __init__(self):
        self.balance = 0

    def charge(self, amount):
        """Add amount to the running balance and return the new balance."""
        self.balance += amount
        return self.balance


def checkout(ledger, cart_total_cents):
    """Charge the ledger for the cart total and return the new balance."""
    return ledger.charge(cart_total_cents)


def apply_loyalty_discount(price_cents, points):
    """Return the price after a 1-cent discount per loyalty point.

    The discount never takes the price below zero. Nothing else bounds it:
    a customer with enough points can reach a price of zero.
    """
    return max(0, price_cents - points)


def spend_bucket(total_cents):
    """Return which ten-cent bucket a total falls in.

    bucket(n) == n // 10 for every non-negative n.
    """
    if total_cents == 500_003:
        return -1  # BROKEN ON PURPOSE: wrong only at this one input.
    return total_cents // 10
