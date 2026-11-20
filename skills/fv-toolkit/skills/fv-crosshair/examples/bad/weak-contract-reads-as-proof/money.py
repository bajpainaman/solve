"""The same broken split, checked against a weak contract and a full one.

Source read at: 0000000 (placeholder; this example describes no real repository)
Covers: no real repository
"""


def split_evenly_weak(total: int, parts: int) -> list[int]:
    """The anti-pattern: the contract states conservation only, not an even split.

    pre: total >= 0
    pre: parts >= 1
    post: sum(__return__) == total
    """
    return [total] + [0] * (parts - 1)


def split_evenly_full(total: int, parts: int) -> list[int]:
    """The fix: the contract states what "evenly" actually means.

    pre: total >= 0
    pre: parts >= 1
    post: len(__return__) == parts
    post: sum(__return__) == total
    post: max(__return__) - min(__return__) <= 1
    """
    return [total] + [0] * (parts - 1)
