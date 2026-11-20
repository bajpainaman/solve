"""A toy refund service in the two designs that ../good/refund-race/RefundRace.tla models."""


class CheckThenRefund:
    """Read the refundable amount in one step, and issue the refund in a later step."""

    def __init__(self, paid):
        self.paid = paid
        self.refunded = 0
        self.snapshot = {}

    def check(self, job):
        # The model's Check action: the SELECT that reads the refundable amount.
        self.snapshot[job] = self.paid - self.refunded

    def refund(self, job):
        # The model's Refund action: the INSERT that issues what the job read earlier.
        self.refunded += self.snapshot.pop(job)


class AtomicRefund:
    """Check and refund in one step."""

    def __init__(self, paid):
        self.paid = paid
        self.refunded = 0

    def check(self, job):
        # This design has no separate read.
        pass

    def refund(self, job):
        self.refunded += self.paid - self.refunded
