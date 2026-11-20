# Anti-pattern: a Loom test with no concurrency to search

**Symptom:** the check passes.

`src/lib.rs` has the same read-then-write race as `good/counter`'s planted
bug. `run()` spawns a thread and joins it before spawning the next one, so
by the time the second thread starts, the first has already run every step.

```text
running 1 test
.
test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

## Why it is wrong

Loom is exhaustive within the schedule it is given, not within every
schedule the real code allows. `run()`'s own driver removes the overlap
before Loom ever sees it: with one thread finished before the next begins,
there is only one order for Loom to try, and that order never puts one
thread's read between another thread's read and write. The check is
non-vacuous in the sense that it runs and asserts something, but the state
that would break the invariant is unreachable from how the test drives the
code.

## The fix

`../../good/counter/` spawns every thread first and joins every handle only
after all of them are running, which is what lets Loom's scheduler choose
to run one thread's read before another thread's write.

## The check that catches it

No mechanical check inside this test catches it, because the test asserts
correctly on the only schedule it can reach. `${CLAUDE_PLUGIN_ROOT}/references/bite.md`'s
witness rule is the general check: a model (here, a test driver) needs a run
that is expected to reach the interesting state, and this driver has none. A
reviewer comparing the driver against the production code it claims to
cover would see that the production code spawns a batch of workers at once,
while this driver spawns and joins one at a time.
