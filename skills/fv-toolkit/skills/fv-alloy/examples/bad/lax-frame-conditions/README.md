# Anti-pattern: missing or lax frame conditions in a temporal model

**Symptom:** a property the author expected to hold fails, and the counterexample shows a field the event never mentions changing anyway.

`Lock` constrains `locked` and says nothing about `alarmArmed`. Alloy 6 gives no event an implicit frame: a `var` field that an event's predicate does not mention is free to take any value in the next state, so long as the sig's own multiplicity still holds. `LockPreservesAlarm` says that locking the door never changes whether the alarm is armed, which is true of `door.py`, but the model lets `Lock` also flip `alarmArmed`.

```text
PASS run DoorLocksAtSomePoint: SAT
FAIL check LockPreservesAlarm: expected UNSAT, got SAT
  this/System<:locked={}
  this/System<:alarmArmed={System$0->System$0}
  this/System<:locked={System$0->System$0}
  this/System<:alarmArmed={}
```

The trace has two states. In the first, the door is unlocked and the alarm is armed. `Lock` fires: `locked` becomes `System` as the predicate requires, and `alarmArmed` becomes empty, which nothing in `Lock` forbids.

## The fix

Add a line to `Lock` that carries `alarmArmed` forward unchanged, the way `Unlock` and `Stutter` already do:

```alloy
pred Lock {
  no System.locked
  System.locked' = System
  System.alarmArmed' = System.alarmArmed
}
```

With that line added, `check LockPreservesAlarm for 3 but 5 steps expect 0` passes as `UNSAT`, confirmed by running the fixed predicate through `fv-alloy`.

Frame every `var` field per event, one line per field, never as a union across events. A single `UNCHANGED`-style line for several fields at once hides the moment a later edit adds a field and forgets to add it there too.

## The check that catches it

None of this model's own commands catch a missing frame condition by construction, because the missing line does not break syntax or satisfiability, only the behavior. The catch is a property that mentions the unrelated field directly, as `LockPreservesAlarm` does, checked with `expect 0`. Writing one such property per `var` field, for every event that should leave it alone, is the only way `fv-alloy` can tell a true design bug from a frame condition the author forgot.
