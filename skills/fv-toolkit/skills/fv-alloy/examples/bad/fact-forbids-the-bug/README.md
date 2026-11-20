# Anti-pattern: a fact that forbids the state you need to examine

**Symptom:** the check passes, and the model cannot show how the system reaches the bad state.

`AdminsHoldTheRole` is the rule that the code is supposed to enforce. As a fact, it removes every structure that breaks the rule. `NoEscalation` then holds by assumption. If the code has no such guard, or has it on one path and not on another, the model cannot show it.

```text
PASS run SomeoneCanGrant: SAT
PASS check NoEscalation: UNSAT
```

Every command meets its expectation, and the `run` is satisfiable, so neither the expectation nor the witness catches this error.

## The fix

Keep a fact for what is true by construction, such as a foreign key that the database enforces. Write a rule that the code must enforce as a predicate, and state the claim under each design. `../../good/rbac/` does this, and its check of the design without the rule finds the escalation.

## The check that catches it

Fidelity rule 1 in the shared `fidelity.md`: each fact names the mechanism that makes it true. A fact with no enforcing mechanism in the code is a design rule, and it belongs in a predicate.
