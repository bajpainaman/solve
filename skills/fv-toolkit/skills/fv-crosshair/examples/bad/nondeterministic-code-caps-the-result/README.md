# Anti-pattern: real entropy runs once, so `holds` can be luck

**Symptom:** `check JitterNeverChangesTheAmount` reports `holds` on a function that is wrong about one run in 256.

`apply_jitter` is supposed to return its input unchanged. `os.urandom(1)[0] < 1` adds a stray cent on roughly one call in 256. CrossHair patches `random.random()` into a symbolic value it can search over, but it does not patch `os.urandom`; the call runs for real, once, on whatever path CrossHair happens to try.

Real output, from the pinned crosshair-tool 0.0.113, across three separate runs:

```text
PASS check JitterNeverChangesTheAmount: holds
PASS check JitterNeverChangesTheAmount: holds
PASS check JitterNeverChangesTheAmount: holds
```

`--verbose` on the same run shows why: `explore_loop() Iteration 1`, immediately followed by `Postcondition confirmed` and `Stopping due to path exhaustion`. CrossHair found only one path, because `cents` is the only symbolic variable in the function; the branch on `os.urandom` was decided once, for real, by whatever bytes the system returned that run.

## The fix

Pass the nondeterministic value in as a parameter instead of reading it inside the function. CrossHair can only make a symbolic variable out of something in its control; an argument qualifies, a system call does not.

## The check that catches it

None, mechanically. A `holds` from code that calls a real source of entropy is never evidence either way; treat the function as unchecked until its nondeterminism is pulled out to an argument.
