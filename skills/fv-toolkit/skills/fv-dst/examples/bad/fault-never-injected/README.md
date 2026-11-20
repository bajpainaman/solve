# A sweep that never injects the fault it claims to cover

**Symptom:** the sweep passes on the rejected design, the one that `examples/good/primary-backup` shows failing at its first seed.

## The bug

`sim_no_fault.py` runs the ack-then-replicate design, the one that acks the client before the backup applies the write, and declares a loss probability `P_LOSS = 0.3`. The line that is meant to use it does not:

```python
lost = rng.random() < 0  # BUG: should read `< P_LOSS`; this can never be true
```

`rng.random()` never returns a value less than `0`, so `lost` is always `False`. No replicate message is ever lost, so the only way `NeverAckedWriteLost` could fail in this file, a write acked before the backup has it, never gets the chance that message loss or a late delivery would create.

## The real output

```text
$ python3 sim_no_fault.py --sweep 500
PASS sweep NeverAckedWriteLost: holds for 500 seeds
```

The same design, with the same comparison written correctly, is `examples/good/primary-backup`'s `ack-then-replicate` check, which fails at seed 0.

## The fix

Compare against the declared constant: `lost = rng.random() < P_LOSS`.

## The check that catches it

None of this project's checks catch it mechanically. A `FAIL` line and a `PASS` line are both well-formed output; nothing here compares the fault rate a sweep declares against the rate it actually exercises. Catching this needs a check on the harness itself: instrument how often each fault fires across a sweep, and fail the sweep if a declared fault's rate is zero.
