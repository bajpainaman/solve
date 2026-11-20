"""Split an amount of cents across weighted lines so that the parts sum to the amount."""


def allocate(total: int, weights: list[int]) -> list[int]:
    """Return one part per weight. The parts sum to `total`.

    Each part is its exact share rounded down. The cents left over go to the
    lines with the largest remainders, one cent each. A tie goes to the heavier
    line, so the result does not depend on the order of the lines.
    """
    if total < 0 or not weights or any(w <= 0 for w in weights):
        raise ValueError("total must be >= 0 and every weight must be > 0")
    whole = sum(weights)
    parts = [total * w // whole for w in weights]
    remainders = [total * w % whole for w in weights]
    order = sorted(range(len(weights)), key=lambda i: (-remainders[i], -weights[i], i))
    for i in order[: total - sum(parts)]:
        parts[i] += 1
    return parts
