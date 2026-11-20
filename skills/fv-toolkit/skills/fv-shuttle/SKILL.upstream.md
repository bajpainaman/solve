---
name: fv-shuttle
description: "Checks real Rust concurrency with Shuttle (randomized scheduling) and Loom (exhaustive scheduling): mutexes, RW locks, atomics, lock-free structures, bounded queues and anything else where two threads touch shared state. Both run the actual code under a controlled scheduler instead of the OS, so a check can try the interleaving that loses an update or deadlocks. Use for Rust concurrency bugs, lost updates, ABA, deadlocks, or when the formal-verification skill routes here. Not for a design before the code exists (use fv-tlaplus), for Rust code with no concurrency (use fv-kani), or for an actor protocol that should also run as a model (use fv-stateright)."
---

# Rust concurrency with Shuttle and Loom

Shuttle runs a concurrent Rust test many times under randomized schedules.
Loom runs the same kind of test under every schedule its model admits. Both
replace the OS scheduler with their own, so a check can make two threads
interleave in the one order that breaks the structure, instead of waiting
for the OS to do it by chance.

If you came here directly, run steps 1 to 3 of the `formal-verification`
skill first. They produce the claims table and the confirmed property
ledger that this skill encodes.

## Five rules

1. **Gate every sync and atomic type the structure uses.** `#[cfg(loom)]
   use loom::sync::...`, `#[cfg(shuttle)] use shuttle::sync::...`, and
   `std::sync::...` behind neither. A single `std::sync` type left in the
   checked path is invisible to the scheduler, and the check passes because
   it never ran under one.
2. **Spawn every thread before joining any of them.** Joining one thread
   before spawning the next removes the overlap the check exists to
   search; see `examples/bad/narrow-loom/`.
3. **A plain `#[test]` with real OS threads is a smoke test, not a check.**
   Thread creation costs far more than one atomic op, so the OS almost
   never produces the interleaving that breaks the structure; see
   `examples/bad/plain-threads/`.
4. **Give Shuttle enough iterations to sample the schedule space.** A
   handful of random runs on a structure with several threads searches
   almost nothing; `examples/good/counter/` uses 200 for two threads.
5. **Every property must fail on a planted bug.** Write a `.mutations`
   file and run `fv-mutate`. A check that stays green on every planted bug
   checks nothing.

## Files to write

Put the files in one crate beside the code they describe, or in the crate
itself when the structure under test is the crate.

| File | Holds |
|---|---|
| `Cargo.toml` | `shuttle` and `loom` as exact-pinned dev-dependencies, and `[lints.rust] unexpected_cfgs = "allow"` |
| `src/lib.rs` (or the module under test) | The structure, with its sync and atomic types gated per rule 1. Its header comment carries `Source read at:` and `Covers:` |
| Tests, inline or under `tests/` | One test per scheduler, named for the property it checks, gated the same way as the types it exercises |
| `<Name>.mutations` | The planted bugs, as `${CLAUDE_PLUGIN_ROOT}/references/bite.md` describes |
| `Cargo.lock` | Committed, so the pinned crate versions never drift between runs |
| `README.md` | The property ledger, the checks table, the run commands, a counterexample, the bounds and limits |

Copy `examples/good/counter/` to start.

## Workflow

1. **Write the structure with `std` types and get a plain `#[test]`
   passing.** This is the smoke test from rule 3, kept as the fallback for
   `cargo test` with no scheduler flag.
2. **Gate the sync and atomic types** per rule 1, and write one test per
   scheduler.
3. **Run each scheduler**, with the build output outside the crate so a
   later copy of it stays small:

   ```bash
   export CARGO_TARGET_DIR="${FV_HOME:-$HOME/.cache/fv}/shuttle/target/<name>"
   RUSTFLAGS="--cfg shuttle" cargo test --quiet --lib
   RUSTFLAGS="--cfg loom" cargo test --quiet --lib
   ```

4. **Plant bugs.**

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-mutate <Name>.mutations
   ```

5. **Read each failure.** The panic line names the file and the line of
   the assertion that failed; the values either side of it are the
   interleaving's result. A Shuttle failure also prints a seed that
   replays the exact schedule.

## Reading the output

`cargo test`'s own output already has the shape `fv-mutate` and this
skill's tests need, with no wrapper script.

| Line | Meaning |
|---|---|
| `test result: ok. N passed; 0 failed...` | Every scheduled run (Shuttle) or the whole model (Loom) asserted correctly |
| `<module>::<test> --- FAILED` | The scheduler found an interleaving that breaks the assertion; the panic above it is the counterexample |
| a Shuttle failing seed or schedule | Pass it to `shuttle::replay` or set `SHUTTLE_RANDOM_SEED` to replay the exact interleaving |
| a compile error, no `FAILED` line | The structure or a cfg gate is wrong; fix it before trusting any run |
| `UNAVAILABLE shuttle: ...`, exit 3 | cargo is missing; nothing was checked |

## Telling a counterexample

Rewrite the panic as numbered steps in the system's own words:

```text
1. Thread a reads total 0.
2. Thread b reads total 0.
3. Thread a writes 1.
4. Thread b writes 1. The total is 1, not 2: thread b's increment was lost.
```

## What a pass means

Loom's pass is exhaustive within the schedule points its model sees:
thread spawns, joins, and operations on its own sync and atomic types.
Shuttle's pass is a search over the number of random schedules given to
`check_random`. Neither models memory reordering outside those points, and
neither replaces a check on the real production structure if this one only
describes it.

## Examples

`examples/INDEX.md` lists every example. `examples/good/counter/` is the
smallest complete one: a single atomic step, checked under both
schedulers, with a mutations file that plants a bug in the step and a
second one in its caller.

## References

| File | Read when |
|---|---|
| `references/anti-patterns.md` | You review a Shuttle or Loom test, yours or someone else's, or need a fact measured on the pinned versions |
| `${CLAUDE_PLUGIN_ROOT}/references/bite.md` | You write the mutations file |
