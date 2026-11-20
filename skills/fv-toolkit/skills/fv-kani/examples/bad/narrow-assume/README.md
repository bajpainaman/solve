# Anti-pattern: an assume that narrows past the bug

**Symptom:** the check passes.

`src/lib.rs` has `allocate()` with a real bug: `(total * percents[i] as
u16) / 100` multiplies in `u16` before dividing, so it overflows for a
large `total` even though the mathematical result fits. The harness adds
`kani::assume(total < 600)`, which keeps every checked `total` below
where `total * 100` can overflow `u16`.

This is the real output, run in Docker because this development
machine's cargo has no rustup:

```text
SUMMARY:
 ** 0 of 51 failed (1 unreachable)

VERIFICATION:- SUCCESSFUL
Verification Time: 0.30307376s

Manual Harness Summary:
Complete - 1 successfully verified harnesses, 0 failures, 1 total.
```

## Why it is wrong

`kani::assume` tells Kani which inputs to skip, not which inputs are
impossible in production. `total < 600` is not a constraint the real
callers of `allocate` enforce; it is a constraint that happens to avoid
the overflow. The harness still reports success, because within the
inputs it actually explores, the bug never fires.

## The fix

Drop the `total < 600` assume and keep only the constraint the real
callers enforce (every percent is at most 100), as
`../../good/allocate-bonus/src/lib.rs` does. Fix the overflow itself by
promoting to `u32` before multiplying, as the good example's `allocate`
does.

## The check that catches it

Removing the narrowing assume and rerunning the same harness, which is
exactly `../../good/allocate-bonus/`'s first mutation.
`${CLAUDE_PLUGIN_ROOT}/references/bite.md`'s rule is the general one:
state every assumption in the report, and treat an assume that was not
derived from how the function is actually called as a reason to
re-check it, the same way `fv-hypothesis`'s `references/anti-patterns.md`
treats an `assume()` that rejects most inputs.
