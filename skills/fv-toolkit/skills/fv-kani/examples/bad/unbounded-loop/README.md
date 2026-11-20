# Anti-pattern: a loop with no unwind bound

**Symptom:** the check never reaches a verdict.

`count_up_to` loops while `i < target`, and `target` is a `kani::any()`
`u16` with no upper bound. The harness has no `#[kani::unwind(N)]`.

This is the real output of running it in Docker (because this
development machine's cargo has no rustup) under a 45-second timeout:

```text
Unwinding loop ...count_up_to.0 iteration 4092 ... function count_up_to thread 0
Unwinding loop ...count_up_to.0 iteration 4093 ... function count_up_to thread 0
Unwinding loop ...count_up_to.0 iteration 4094 ... function count_up_to thread 0
```

45 seconds unwound 4,094 of the up to 65,535 iterations `target: u16`
allows, and never reached a check, a solve, or a verdict.

## Why it is wrong

Kani's backend unrolls every loop into a bounded program before checking
it. With no `#[kani::unwind(N)]`, it keeps unrolling one further
iteration at a time, bounded only by the type of `target`. The harness
either runs for a very long time or is killed first; either way, nothing
was proved for any input.

## The fix

Bound the loop with `#[kani::unwind(N)]` for a small `N`, and add
`kani::assume(target <= N)` so the harness only claims what it checked,
or rewrite the property around a function whose loop bound is a fixed
constant, the way `../../good/allocate-bonus/`'s loop runs a fixed three
times and needs only `#[kani::unwind(4)]`.

## The check that catches it

No mechanical check inside this harness catches it; the harness simply
never finishes. A reviewer checking that every `#[kani::proof]` has an
`#[kani::unwind]` whenever its target iterates a symbolic number of
times would catch this before running it at all.
