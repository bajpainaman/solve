# Anti-pattern: a contract too weak to find the bug it should

**Symptom:** `check WeakContractHolds` reports `holds` on a function that puts every cent into the first share.

Both functions in `money.py` share the same body, `[total] + [0] * (parts - 1)`, which is not an even split by any reasonable reading. `split_evenly_weak`'s contract only checks `sum(__return__) == total`. `split_evenly_full`'s contract checks the length, the sum and the 1-cent bound between the highest and lowest share.

Real output, from the pinned crosshair-tool 0.0.113:

```text
PASS check WeakContractHolds: holds
PASS check FullContractRefutesTheSameBug: refuted
```

`FullContractRefutesTheSameBug` finds the same bug the first command never could see, because its contract asks a question the weak one did not:

```text
money.py:25: error: false when calling split_evenly_full(2, 2) (which returns [2, 0])
```

## The fix

Write the contract for everything the function promises its callers, not just the one property that happens to be easy to state. `holds` only ever answers the question the contract asked.

## The check that catches it

None, mechanically, for the weak contract; it does exactly what it was asked to check. Review every `post:` line and ask what a function could still get wrong and satisfy it.
