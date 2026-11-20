# Anti-pattern: liveness checked with no fairness

**Symptom:** the liveness property fails on a trace that ends in "Stuttering", and the trace shows no bug in the design.

`Spec == Init /\ [][Next]_state` allows the system to stop at any state for ever. A behaviour that takes the job and then never finishes it is legal, so `queued ~> finished` is false.

```text
PASS NoFairness.cfg: liveness (properties: QueuedLeadsToFinished) (3 distinct states)
  1. Initial: state = "queued"
  2. Take: state: "queued" -> "running"
  3. Stuttering: no variable changed
```

A leads-to property without fairness does not pass trivially. TLC 1.7.4 reports the violation and exits 13.

## The fix

State the fairness that the code provides. `FairSpec` adds weak fairness on `Take` and `Finish`: a step that stays possible is eventually taken. `WeakFairness.cfg` then holds.

Give fairness only to steps that the system keeps trying. An optional user action and a fault such as a crash get none, because fairness on a step forces that step to happen. Use strong fairness only when the code guarantees a turn to a step that is possible again and again. Polling does not give that guarantee.

## The check that catches the opposite error

Fairness that is too strong makes liveness hold under an assumption that no implementation provides. For each fairness condition, name the code that provides it in a comment. Then add a mutation that removes the progress step, and confirm that the liveness property fails.
