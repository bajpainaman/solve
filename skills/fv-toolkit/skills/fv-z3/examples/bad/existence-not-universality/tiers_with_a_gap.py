"""The same shipping tiers as examples/good/shipping-tiers, with a real gap between B and C.

Source read at: 0000000 (placeholder; this example describes no real repository)
Covers: no real repository
"""
from z3 import And, Int, Not, Or, Solver

MAX_WEIGHT = 30_000

# Tier B stops at 1,900 g, and tier C starts at 2,000 g, so [1900, 2000) g matches nothing.


def tier_a(w):
    return And(w >= 0, w < 500)


def tier_b(w):
    return And(w >= 500, w < 1_900)


def tier_c(w):
    return And(w >= 2_000, w <= MAX_WEIGHT)


def check_SomeWeightMatchesATier():
    """The anti-pattern: checks that the claim can be true, not that it always is.

    expect: sat
    """
    w = Int("w")
    s = Solver()
    s.add(w >= 0, w <= MAX_WEIGHT)
    s.add(Or(tier_a(w), tier_b(w), tier_c(w)))
    return s


def check_EveryWeightMatchesATier():
    """The fix: checks that no weight matches none of the tiers.

    expect: unsat
    """
    w = Int("w")
    s = Solver()
    s.add(w >= 0, w <= MAX_WEIGHT)
    s.add(Not(Or(tier_a(w), tier_b(w), tier_c(w))))
    return s
