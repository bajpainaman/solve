"""Split an amount of cents into equal shares, with a contract CrossHair checks.

Source read at: 0000000 (placeholder; this example describes no real repository)
Covers: no real repository
"""


def split_evenly(total: int, parts: int) -> list[int]:
    """
    Split `total` non-negative cents into `parts` shares that sum back to it.

    No share differs from another by more than one cent, and the extra cents
    go to the first few shares.

    pre: total >= 0
    pre: parts >= 1
    post: len(__return__) == parts
    post: sum(__return__) == total
    post: max(__return__) - min(__return__) <= 1
    """
    base, extra = divmod(total, parts)
    return [base + 1 if i < extra else base for i in range(parts)]


def split_evenly_refactored(total: int, parts: int) -> list[int]:
    """The same split, written as an explicit loop instead of a comprehension."""
    base, extra = divmod(total, parts)
    shares = []
    for i in range(parts):
        shares.append(base + 1 if i < extra else base)
    return shares


def split_evenly_rejected(total: int, parts: int) -> list[int]:
    """The rejected design: the extra cents go to the last few shares, not the first."""
    base, extra = divmod(total, parts)
    return [base + 1 if i >= parts - extra else base for i in range(parts)]
