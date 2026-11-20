# Anti-pattern: fairness on an action that is never continuously enabled

**Symptom:** a liveness property holds with the fairness condition in the spec, and holds identically with it removed. The fairness condition never does anything.

`Escalate`'s guard is `pc = "stuck"`, and nothing in `Watchdog.tla` ever sets `pc` to `"stuck"`: an earlier refactor removed the only transition that used to produce it. `WF_pc(Escalate)` can never find a continuously enabled window, because the action is never enabled at all, so the fairness condition is true on every behaviour for free.

```text
PASS NeverStuck.cfg: holds (2 distinct states)
PASS WithEscalateFairness.cfg: holds (2 distinct states)
PASS WithoutEscalateFairness.cfg: holds (2 distinct states)
```

`NeverStuck.cfg` confirms the cause: `pc = "stuck"` is unreachable. `WithEscalateFairness.cfg` and `WithoutEscalateFairness.cfg` check the same property, `EventuallyDone`, with `WF_pc(Escalate)` present and absent. Both report `holds`, in the same two states. Adding `WF_pc(Escalate)` to the spec changed nothing.

## Why it is wrong

`EventuallyDone` holds here entirely because of `WF_pc(Advance)`, the normal path to completion. The author likely added `WF_pc(Escalate)` believing it backs up the liveness proof for the case where a job gets stuck and needs the watchdog to intervene. It does not: TLC cannot distinguish "this fairness condition is irrelevant" from "this fairness condition is essential" from the `holds` result alone. If a later change made `Advance` itself unreliable, for example by giving `job.py` a crash path the model does not yet show, the report would still say `EventuallyDone` holds, and the one place that was meant to catch that regression was never providing any guarantee in the first place.

## The check that catches it

An invariant that states the guard is unreachable, as `NeverStuck` does, catches a vacuous guard directly: `fv-tlc` reports `holds`, confirming the state the fairness condition depends on never occurs. For an action that is sometimes enabled but never continuously, as opposed to never enabled at all, the same question is answered by removing the fairness condition and comparing the result: an unchanged outcome, as the two `EventuallyDone` runs show here, means the condition was vacuous. Removing a fairness condition and expecting the property to then fail is the mutation `bite.md` calls for on every fairness condition, and this is what happens when that mutation finds nothing to detect.
