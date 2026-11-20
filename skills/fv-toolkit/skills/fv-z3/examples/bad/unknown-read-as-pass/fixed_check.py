"""The same rule, run through fv-z3 instead of a hand-rolled script.

Source read at: 0000000 (placeholder; this example describes no real repository)
Covers: no real repository
"""
from z3 import Int, Solver


def check_NoChargebackCombination():
    """No three discount multipliers cube-sum to the chargeback threshold.

    expect: unsat
    """
    x, y, z = Int("x"), Int("y"), Int("z")
    s = Solver()
    s.set("timeout", 3000)
    s.add(x ** 3 + y ** 3 + z ** 3 == 114)
    return s
