# Anti-pattern: an invariant only, with no action property

**Symptom:** the invariant holds on every state, and a step the design forbids still happens.

The design says a view count only ever climbs. `Next` also includes `Decrement`, a step the design forbids in production but a buggy rollback can still reach. `NonNegative` says nothing about which direction `x` moves, so `Decrement` never breaks it.

```text
PASS InvariantOnly.cfg: holds (4 distinct states)
```

`InvariantOnly.cfg` passes with `Decrement` in the model. The invariant checks a property of one state at a time, and every state this model reaches has `x >= 0`, whether `x` went up or down to get there.

## Why it is wrong

"The count only climbs" is a relation between two consecutive states, `x' >= x`, not a property of one state, so an `INVARIANT` cannot state it. An `INVARIANT` can only rule out shapes of a single state, such as a negative count. It cannot rule out the step that produced that state.

## The fix

State the rule as an action property and check it as a temporal `PROPERTY`:

```tla
Monotonic == [][x' >= x]_x
```

```text
PASS ActionProperty.cfg: liveness (properties: Monotonic) (3 distinct states)
  1. Initial: x = 0
  2. Increment: x: 0 -> 1
  3. Decrement: x: 1 -> 0
```

TLC 1.7.4 checks an action property through the same path as a temporal property, so `fv-tlc` reports the violation as `liveness (properties: Monotonic)`, even though `Monotonic` makes a safety claim about one pair of states, not a claim about what eventually happens. `ActionProperty.cfg`'s header says `expect: liveness` for that reason, not because `Decrement` is a progress bug.

## The check that catches it

An action property that states the rule the invariant cannot, checked once per rule the design forbids. `references/anti-patterns.md`'s Datadog citation makes the same point about production telemetry: an implementation can violate a spec while every invariant in the spec still holds, and only an action or refinement property sees the violating step.
