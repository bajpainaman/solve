# Anti-pattern: facts that contradict each other

**Symptom:** every `check` passes, including one that is plainly false.

The four facts cannot hold together. Two users each hold a role, the roles are not shared, and there is one role. No instance satisfies the model, so no counterexample to any assertion exists. `NobodyHoldsARole` passes although the first fact says that every user holds a role.

```text
FAIL run SomeUsers: expected SAT, got UNSAT
PASS check NobodyHoldsARole: UNSAT
```

## The fix

Remove or weaken the fact that does not describe the system. Here, `RolesAreNotShared` is wrong, because users share roles.

## The check that catches it

The `run`. A satisfiable `run` beside the checks proves that the model has an instance. `fv-alloy` fails a model that has a `check` and no `run`, and it fails a `run` that finds no instance. Run each predicate you rely on before you trust a check.
