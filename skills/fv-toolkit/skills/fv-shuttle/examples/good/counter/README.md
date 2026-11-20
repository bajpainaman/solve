# Counter

**Pattern:** mutex / RW lock, lock-free structures (catalog A4).
**Teaches:** the same code checked under Shuttle's randomized scheduler and
Loom's exhaustive one, a mutations file that plants a bug in the checked
function and a second one in its caller.

## The system

`Counter::increment()` adds one to a running total with a single atomic
`fetch_add`. `run(threads)` spawns that many threads, each calling
`increment()` once, joins every handle, and returns the total. The claim is
that the total always equals the thread count, because `fetch_add` is one
atomic step and no increment can be lost between two threads.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| The total equals the thread count under a randomized schedule | safety, search | `total_equals_thread_count_shuttle` |
| The total equals the thread count under every schedule Loom explores | safety, exhaustive within the model | `total_equals_thread_count_loom` |

## Checks

| Check | Scheduler | Declared outcome |
|---|---|---|
| `RUSTFLAGS="--cfg shuttle" cargo test` | 200 random interleavings | passes |
| `RUSTFLAGS="--cfg loom" cargo test` | every interleaving Loom's model admits | passes |
| `cargo test` (no cfg) | one run with real OS threads | passes, and proves nothing; see `../../bad/plain-threads/` |

## Run

```bash
export CARGO_TARGET_DIR="${FV_HOME:-$HOME/.cache/fv}/shuttle/target/counter"
RUSTFLAGS="--cfg shuttle" cargo test --quiet --lib
RUSTFLAGS="--cfg loom" cargo test --quiet --lib
${CLAUDE_PLUGIN_ROOT}/scripts/fv-mutate counter.mutations
```

## Telling a counterexample

Loom and Shuttle both report the interleaving as a panic, because the check
is a plain `assert_eq!` and not a search for a trace. This is the real
output from running the mutated `fetch_add` under `--cfg shuttle` (the task
id and the seed vary from run to run):

```text
tests::total_equals_thread_count_shuttle --- FAILED

failures:

---- tests::total_equals_thread_count_shuttle stdout ----
thread 'tests::total_equals_thread_count_shuttle' (2559523) panicked at src/lib.rs:76:34:
assertion `left == right` failed
  left: 1
 right: 2
```

Read as steps: thread a reads total 0; thread b reads total 0; thread a
writes 1; thread b writes 1. Both threads added one, and the total is 1,
not 2.

## Bounds and limits

The model checks two threads and one increment each. Loom's search is
exhaustive for this program as written, within the atomic operations and
thread events it models; it does not model memory reordering outside those
events. A regression test on the real counted structure is still needed if
the production code differs from this one.
