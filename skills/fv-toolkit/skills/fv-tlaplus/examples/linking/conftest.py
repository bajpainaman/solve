"""The driver that maps each action of RefundRace.tla to a call on the service."""
import os

import pytest

from refunds import AtomicRefund, CheckThenRefund

PAID = 10  # The constant Paid in the configs of the model.


class Driver:
    def reset(self, state):
        design = AtomicRefund if os.environ.get("REFUND_DESIGN") == "atomic" else CheckThenRefund
        self.service = design(PAID)

    def step(self, action, changed, state):
        # The job whose program counter moved is the job that took the step.
        (job,) = changed["pc"]
        {"Check": self.service.check, "Refund": self.service.refund}[action](job)

    def check(self):
        assert self.service.refunded <= self.service.paid, (
            f"refunded {self.service.refunded} on a payment of {self.service.paid}")


@pytest.fixture
def driver():
    return Driver()
