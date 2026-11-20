# A sweep that shares one RNG across every run

**Symptom:** a seed that the sweep reports as failing does not fail when it is replayed on its own.

## The bug

`sweep()` in `sim_unseeded.py` creates one `random.Random(seed_start)` before its loop and passes that same object into every run of the sweep:

```python
def sweep(steps, seed_start, count):
    rng = random.Random(seed_start)  # BUG: one Random object, shared by every run in the sweep
    for i in range(count):
        if run(rng, steps):
```

Each run consumes some draws from that one stream, so run number `i` sees whatever draws are left after runs `0` through `i - 1` already took theirs. The number the sweep prints as the failing "seed" is really just a loop index into a shared stream, not a seed that reconstructs that run on its own.

## The real output

```text
$ python3 sim_unseeded.py --sweep 500 --seed-start 4
FAIL sweep NeverAckedWriteLost: expected holds, got violated at seed 5
```

```text
$ python3 sim_unseeded.py --replay 5
PASS replay NeverAckedWriteLost: holds
```

Replaying seed 5 on its own creates `random.Random(5)` fresh and gets a different draw sequence than the fifth run of the sweep got, so the violation does not come back.

## The fix

Create a fresh `random.Random(seed)` inside each run, as `examples/good/primary-backup/simulate.py` does: `rng = random.Random(seed)` at the top of `run()`, one per seed, never shared across iterations.

## The check that catches it

None of this project's checks catch it mechanically. `fv-mutate` confirms that a property detects a planted bug in the code under test; it cannot tell that the harness itself fails to replay, because nothing here asserts that `--replay N` after a sweep reproduces that sweep's run at index `N`. Catching this needs a check written for the harness: run a sweep, take its first failing seed, replay it, and assert the two outcomes match.
