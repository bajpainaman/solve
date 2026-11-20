# Anti-pattern: a plain test with real threads

**Symptom:** the check passes.

`src/lib.rs` has the same lost-update bug as `../../good/counter/`:
`increment()` reads the total and writes it back one higher, as two separate
steps, so another thread's increment can land between the read and the
write. `tests::total_equals_thread_count` spawns two threads and asserts
that the total reaches 2.

```text
running 1 test
.
test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

300 runs of the compiled test binary in a row produced 0 failures.

## Why it is wrong

The OS scheduler decides when each thread runs, and spawning a thread costs
far more than one atomic load or store. By the time the second thread starts,
the first has almost always already read, incremented and written back. The
test never puts a thread to sleep between the read and the write, so the
interleaving that loses an update almost never happens on real hardware,
even though the code allows it.

## The fix

`../../good/counter/` keeps the same structure under Shuttle and Loom, which
control when each thread's steps run instead of leaving it to the OS. Loom's
search tries the interleaving where the second thread's read lands between
the first thread's read and write, every time, because it is exhaustive
within the model. Shuttle finds the same interleaving by trying 200 random
schedules.

## The check that catches it

Running the same code under `cargo test --cfg shuttle` or `--cfg loom`, as
`good/counter/` does, instead of a plain `cargo test`.
