"""Shipping-fee tiers by package weight, as a Z3 decision table.

Source read at: 0000000 (placeholder; this example describes no real repository)
Covers: no real repository
"""
from z3 import And, Int, Not, Or, Solver

MAX_WEIGHT = 30_000  # grams; the carrier refuses anything heavier


def tier_a(w):
    """Tier A: 0 g up to 500 g."""
    return And(w >= 0, w < 500)


def tier_b(w):
    """Tier B: 500 g up to 2,000 g."""
    return And(w >= 500, w < 2_000)


def tier_c(w):
    """Tier C: 2,000 g up to the carrier's limit."""
    return And(w >= 2_000, w <= MAX_WEIGHT)


def check_TiersAreComplete():
    """Every weight the carrier accepts matches a tier.

    expect: unsat
    """
    w = Int("w")
    s = Solver()
    s.add(w >= 0, w <= MAX_WEIGHT)
    s.add(Not(Or(tier_a(w), tier_b(w), tier_c(w))))
    return s


def check_TiersAreUnique():
    """No weight matches two tiers at once.

    expect: unsat
    """
    w = Int("w")
    s = Solver()
    s.add(Or(And(tier_a(w), tier_b(w)), And(tier_a(w), tier_c(w)), And(tier_b(w), tier_c(w))))
    return s


def tier_b_rejected(w):
    """The rejected design: tier B's upper bound is inclusive, the same weight tier C's lower bound names."""
    return And(w >= 500, w <= 2_000)


def check_RejectedDesignOverlapsAtTheBoundary():
    """The rejected design double-counts 2,000 g, so a run beside the checks must find it.

    expect: sat
    """
    w = Int("w")
    s = Solver()
    s.add(And(tier_b_rejected(w), tier_c(w)))
    return s
