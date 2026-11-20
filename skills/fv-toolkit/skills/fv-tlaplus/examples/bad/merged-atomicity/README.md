# Anti-pattern: one action per function

**Symptom:** the check passes.

`MergedRefund.tla` models `refund_job()` as one action. The real function runs a SELECT and a later INSERT, and another job can run between the two statements. The model cannot reach that interleaving, so `NeverOverRefund` holds on a design that refunds twice in production.

```text
PASS Merged.cfg: holds (4 distinct states)
```

## Why it is wrong

A TLA+ action is indivisible. One action per function claims that the whole function runs with nothing in between. That claim is true only when the function is one SQL statement, or runs under one lock that every other writer takes.

## The fix

Write one action per atomic step in the code. `../../good/refund-race/` splits the job into `Check` and `Refund`, and its `CheckThenRefund.cfg` then finds the double refund in five steps. `../../../references/refactors.md` gives the procedure for splitting an action.

## The check that catches it

Fidelity rule 3 in the shared `fidelity.md`: put the statement that each action transcribes in a comment, and compare the action's boundaries with the statement boundaries. A mutations file does not catch this error, because the model is wrong in the same way before and after each mutation.
