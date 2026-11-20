"""A jitter function whose bug CrossHair cannot reliably reach.

Source read at: 0000000 (placeholder; this example describes no real repository)
Covers: no real repository

`os.urandom` is a real source of entropy, not a value CrossHair can turn
into a symbolic variable the way it does `random.random()`. CrossHair
executes the call for real on each attempt, so the branch it exercises
depends on whatever bytes the system actually returns that run.
"""
import os


def apply_jitter(cents: int) -> int:
    """
    Return the amount unchanged.

    pre: cents >= 0
    post: __return__ == cents
    """
    if os.urandom(1)[0] < 1:  # the bug: about 1 run in 256 adds a stray cent
        return cents + 1
    return cents
