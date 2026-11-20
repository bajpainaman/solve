# Anti-pattern: an action generator that cannot reach the bad state

**Symptom:** the check passes.

`src/lib.rs` has `Unilateral`'s unchecked commit from `../../good/two-phase-commit/`:
`next_state` lets an RM commit once it has prepared, with no check of the
other RM's vote. `actions()` is the bug: its loop pushes `Prepare` and
`Finish` for each RM but never pushes `AbortUnilaterally`.

```text
running 1 test
.
test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

## Why it is wrong

`next_state` still handles the `AbortUnilaterally` action and would set an
RM to `Aborted` if it ever received one, but `actions()` never offers that
action to the checker. No reachable state has an `Aborted` RM, so
`rms_agree`, which only fires when one RM is `Committed` and another is
`Aborted`, can never see a violation. The checker explores every state
`actions()` lets it reach, exhaustively, and that is a smaller state space
than the real code's.

## The fix

`../../good/two-phase-commit/`'s `Centralized.properties()` adds
`Property::sometimes("both_commit", ...)` as a non-vacuity witness. Adding
the matching witness here, `Property::sometimes("some_rm_aborts", |_, s|
s.rms.iter().any(|r| *r == RmState::Aborted))`, makes `assert_properties()`
panic with the real message `Discovery for "some_rm_aborts" not found.`,
which is how this mistake was actually found: a witness that is never
satisfied means the model cannot reach a state the real system can.

## The check that catches it

A `Property::sometimes` witness for every state the model is supposed to
be able to reach, as `${CLAUDE_PLUGIN_ROOT}/references/bite.md`'s
non-vacuity rule describes.
