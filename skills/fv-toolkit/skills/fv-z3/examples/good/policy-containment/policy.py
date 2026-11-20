"""IAM-style policy containment: the new policy must allow nothing the old one denied.

Source read at: 0000000 (placeholder; this example describes no real repository)
Covers: no real repository

region: 0 = us, 1 = eu, 2 = global (a region the old policy never named)
action: 0 = read, 1 = write, 2 = delete
"""
from z3 import And, Int, Not, Or, Solver


def old_allows(region, action):
    """The policy in force today: us or eu, read or write."""
    return And(Or(region == 0, region == 1), Or(action == 0, action == 1))


def new_allows_tightened(region, action):
    """The rule change under review: us only, read only."""
    return And(region == 0, action == 0)


def check_TightenedPolicyAllowsNothingTheOldOneDenied():
    """No request the new policy allows was denied by the old one.

    expect: unsat
    """
    region, action = Int("region"), Int("action")
    s = Solver()
    s.add(new_allows_tightened(region, action))
    s.add(Not(old_allows(region, action)))
    return s


def new_allows_widened(region, action):
    """The rejected design: a later change adds the 'global' region by mistake."""
    return And(Or(region == 0, region == 2), action == 0)


def check_RejectedDesignWidensAccessToGlobal():
    """The widened policy allows a region the old policy never covered, so a check beside it must find it.

    expect: sat
    """
    region, action = Int("region"), Int("action")
    s = Solver()
    s.add(new_allows_widened(region, action))
    s.add(Not(old_allows(region, action)))
    return s
