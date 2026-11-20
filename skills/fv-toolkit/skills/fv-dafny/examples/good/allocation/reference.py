"""A hand-written reference for Allocate.Split, written independently of the Dafny model.

Source read at: 0000000
Covers: billing/split.py
"""


def split_reference(total: int, n: int) -> list[int]:
    """Split total evenly across n recipients. The first `total % n` recipients get one extra."""
    share, leftover = divmod(total, n)
    return [share + 1 if i < leftover else share for i in range(n)]
