---
name: fv-kani
description: "Bounded model checking of sequential Rust code with Kani: a harness that generates symbolic inputs with kani::any() and checks a property, an overflow, a panic or a bounds violation. Exhaustive within the unwind bound given to every loop. Use for a pure Rust function's arithmetic, indexing or panics over every input in its type, not only the ones a test picks. Not for concurrency (use fv-shuttle), for an actor protocol (use fv-stateright), or for a property searched rather than proved (use fv-hypothesis's Python equivalent, or write the harness anyway if the code is Rust)."
---

# Bounded model checking with Kani

A Kani harness is a `#[kani::proof]` function that draws symbolic inputs
with `kani::any()`, narrows them to the domain the real callers use with
`kani::assume()`, and asserts a property. Kani checks the property against
every value the symbolic inputs can take, within the unwind bound given to
every loop, using CBMC as its backend.

If you came here directly, run steps 1 to 3 of the `formal-verification`
skill first. They produce the claims table and the confirmed property
ledger that this skill encodes.

## Five rules

1. **Bound every loop with `#[kani::unwind(N)]`.** A loop whose bound
   depends on a symbolic value has no fixed number of iterations to
   unroll to, and Kani either runs for a very long time or cannot finish;
   see `examples/bad/unbounded-loop/`.
2. **Build `kani::assume` from how real callers use the function.** An
   assume that is not derived from the input domain the code actually
   receives can narrow the proof until it covers almost nothing; see
   `examples/bad/narrow-assume/`.
3. **Add a `kani::cover!` witness for the state the harness is meant to
   reach.** A harness that never prints `COVER ... SATISFIED` for the
   interesting case may be proving something true for the wrong reason,
   the same way a TLA+ witness config must be violated.
4. **State the unwind bound and the assumptions in the report.** A pass
   under `#[kani::unwind(4)]` says nothing about an input that needs a
   5th iteration, and `kani::assume` removes inputs from the proof
   silently unless the report says which ones.
5. **Every property must fail on a planted bug.** Write a `.mutations`
   file and run `fv-mutate`. A harness that stays green on every planted
   bug checks nothing.

## Files to write

Put the harness in the crate it checks, behind `#[cfg(kani)]` so it never
ships in a normal build.

| File | Holds |
|---|---|
| `src/lib.rs` (or the module under test) | The function, and a `#[cfg(kani)] mod verification` with one `#[kani::proof]` harness per property. Its header comment carries `Source read at:` and `Covers:` |
| `<Name>.mutations` | The planted bugs, as `${CLAUDE_PLUGIN_ROOT}/references/bite.md` describes |
| `README.md` | The property ledger, the harnesses table, the run commands, a counterexample, the bounds and limits |

Copy `examples/good/allocate-bonus/` to start.

## Workflow

1. **Write the function**, with every input the real callers can produce
   kept in its natural type (a `u8` percent, not a `u32` pre-validated to
   0 to 100).
2. **Write the harness**: `kani::any()` for every input, `kani::assume`
   for the constraint real callers already enforce, then the assertion.
3. **Bound every loop** with `#[kani::unwind(N)]`, starting from the
   smallest `N` the loop can take and raising it until Kani stops
   reporting an unwinding assertion failure.
4. **Run it.**

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-kani check_<property>
   ```

5. **Add a `kani::cover!`** for the state that makes the property
   non-vacuous, and confirm it is `SATISFIED`.
6. **Plant bugs.**

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-mutate <Name>.mutations
   ```

## Reading the output

`cargo kani`'s own output names checks, not harnesses, on each line, so
`${CLAUDE_PLUGIN_ROOT}/scripts/fv-kani` reprints its per-harness verdict in
the shape `fv-mutate` needs.

| Line | Meaning |
|---|---|
| `PASS kani <harness>: SUCCESSFUL` | Every check in the harness held for every input the unwind bound and the assumes allow |
| `FAIL kani <harness>: <failed check>` | A check failed; the description names the panic, the overflow or the assertion |
| `COVER <label>: SATISFIED` / `UNSATISFIED` | Whether the state a `kani::cover!` names is reachable at all |
| `ERROR kani <harness>: <reason>` | The harness did not compile, or Kani could not finish; never a violation |
| `UNAVAILABLE kani: ...`, exit 3 | rustup or the pinned Kani setup is missing; nothing was checked |

## Telling a counterexample

Rewrite Kani's trace as numbered steps in the system's own words, using
the concrete values it found for each `kani::any()`:

```text
1. total and percents[0] are symbolic u16 and u8 values Kani searches.
2. `total * percents[0] as u16` multiplies in u16 before dividing by 100,
   which overflows once total exceeds about 650 at a percent of 100.
3. Kani finds a concrete total and percent where this happens and
   reports it as the failed check.
```

## What a pass means

A pass means the harness's assertions held for every input its symbolic
variables and `kani::assume` calls allow, with every loop unrolled to its
`#[kani::unwind]` bound. It is exhaustive within that bound and that
input domain, not a proof over an unbounded loop or an input the harness
assumed away.

## Examples

`examples/INDEX.md` lists every example. `examples/good/allocate-bonus/`
is the smallest complete one: a bounded loop, a `kani::cover!` witness,
and a mutations file that plants a bug in the checked line and a second
one in its input.

## References

| File | Read when |
|---|---|
| `references/anti-patterns.md` | You review a Kani harness, yours or someone else's, or need a fact measured on the pinned version |
| `${CLAUDE_PLUGIN_ROOT}/references/bite.md` | You write the mutations file |
